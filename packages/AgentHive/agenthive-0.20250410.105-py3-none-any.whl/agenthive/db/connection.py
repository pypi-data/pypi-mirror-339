"""
Database connection utilities for py-AgentHive.
"""
import logging
import os
import pkgutil
from typing import AsyncGenerator
from pathlib import Path

from sqlalchemy import inspect, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import agenthive.db.models as db_models

logger = logging.getLogger(__name__)

# 全局引擎變數
_engine = None

# 定義 ORM 基類
Base = declarative_base()

def get_all_models():
    """從 agenthive.db.models.__init__ 獲取所有暴露的模型類"""

    model_classes = []  # 使用不同的變數名稱

    logger.debug("Scanning models from 'agenthive.db.models'")

    for attr_name in db_models.__all__:
        attr = getattr(db_models, attr_name)
        if (isinstance(attr, type) and
            hasattr(attr, '__tablename__') and
            issubclass(attr, db_models.Base)):  # 使用 db_models.Base
            model_classes.append(attr)

    logger.info(f"Found {len(model_classes)} models in 'agenthive.db.models' with tables: {', '.join([m.__tablename__ for m in model_classes])}")
    return model_classes

async def init_db(db_url: str = None) -> AsyncEngine:
    """
    Initialize the database connection and ensure all tables exist.

    Args:
        db_url: Database URL

    Returns:
        Database engine
    """
    global _engine

    if not db_url:
        db_url = os.environ.get("DATABASE_URL")

    if not db_url:
        raise ValueError("Database URL is required")

    logger.info(f"Initializing database connection to {db_url}")

    _engine = create_async_engine(
        db_url,
        echo=False,
        future=True,
        connect_args={
            "server_settings": {"application_name": "AgentHive"}
        },
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800
    )

    # 獲取所有模型
    model_classes = get_all_models()

    # 檢查並創建表格
    async with _engine.begin() as conn:
        # await conn.run_sync(db_models.Base.metadata.drop_all)
        # 創建所有表
        await conn.run_sync(db_models.Base.metadata.create_all)

        # 檢查表是否存在
        def check_tables(connection):
            inspector = inspect(connection)
            for model in model_classes:
                table_name = model.__tablename__
                if not inspector.has_table(table_name):
                    logger.warning(f"Table {table_name} was not found after creation!")
                #else:
                #    logger.info(f"Table {table_name} created successfully")
                #    record_count = connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
                #    logger.info(f"Table {table_name} exists with {record_count} records")
                columns = inspector.get_columns(table_name)
                logger.info(f"Table {table_name} columns: {[c['name'] for c in columns]}")

        await conn.run_sync(check_tables)
    
    logger.info("Database engine and tables initialized")
    return _engine

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get a database session.

    Yields:
        Database session
    """
    global _engine

    if _engine is None:
        await init_db()

    async_session = sessionmaker(
        _engine, expire_on_commit=False, class_=AsyncSession
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def close_db() -> None:
    """Close the database connection."""
    global _engine

    if _engine:
        await _engine.dispose()
        _engine = None
        logger.info("Database connection closed")

async def table_exists(table_name: str) -> bool:
    """
    Check if a table exists in the database.

    Args:
        table_name: Name of the table to check

    Returns:
        Boolean indicating if the table exists
    """
    global _engine

    if _engine is None:
        await init_db()

    async with _engine.connect() as conn:
        #inspector = await conn.run_sync(inspect)
        #return inspector.has_table(table_name)

        result = await conn.run_sync(
            lambda connection: inspect(connection).has_table(table_name)
        )
        return result

__all__ = ['init_db', 'get_session', 'close_db', 'Base', 'table_exists']
