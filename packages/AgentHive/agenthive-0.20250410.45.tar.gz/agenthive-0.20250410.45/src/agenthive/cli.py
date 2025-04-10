import os
import shutil
import click
from pathlib import Path

@click.group()
def cli():
    """AgentHive CLI tool for managing projects."""
    pass

from agenthive.version import __version__

@cli.command()
def version():
    """Display the AgentHive version."""
    click.echo(f"AgentHive: v{__version__}")

@cli.command()
@click.argument("path")
@click.option("--agenthive-project-path", type=click.Path(exists=True, file_okay=False, dir_okay=True),
              help="Path to the agenthive project root directory containing src/, setup.py, and optionally requirements/ "
                   "(e.g., /path/to/agenthive). Enables developer mode if specified.")
def init(path, agenthive_project_path):
    """Initialize a new AgentHive project at the specified path."""
    project_path = Path(path).resolve()
    if project_path.exists():
        click.echo(f"Error: Directory {project_path} already exists.")
        return
    
    # 創建目錄結構
    project_path.mkdir(parents=True)
    docker_path = project_path / "docker"
    docker_path.mkdir()
    workers_path = project_path / "src" / "workers"
    workers_path.mkdir(parents=True)
    (workers_path / "requirements").mkdir()
    
    # 從 templates/docker/ 複製 Docker 文件
    template_dir = Path(__file__).parent / "templates" / "docker"
    shutil.copytree(template_dir, docker_path, dirs_exist_ok=True)
    
    if agenthive_project_path:
        project_root = Path(agenthive_project_path).resolve()
        required_items = ["src/agenthive/core", "src/agenthive/service", "setup.py", "README.md"]
        missing_items = [item for item in required_items if not (project_root / item).exists()]
        if missing_items:
            click.echo(f"Error: {project_root} does not contain a valid agenthive structure. "
                       f"Missing: {', '.join(missing_items)}")
            return
        
        shutil.copytree(project_root / "src", project_path / "src", dirs_exist_ok=True)
        shutil.copy(project_root / "setup.py", project_path / "setup.py")
        shutil.copy(project_root / "README.md", project_path / "README.md")
        # 選擇性複製 requirements/
        if (project_root / "requirements").exists():
            shutil.copytree(project_root / "requirements", project_path / "requirements", dirs_exist_ok=True)
        
        # 修改 Dockerfile 使用本地 /app/
        for component in ["coordinator", "monitor", "worker"]:
            dockerfile_path = docker_path / component / "Dockerfile"
            with open(dockerfile_path, "r") as f:
                content = f.read()
            content = content.replace(
                "RUN pip install --no-cache-dir agenthive",
                "COPY src/ /app/src/\n"
                "COPY setup.py /app/setup.py\n"
                "COPY requirements/ /app/requirements/\n"
                "RUN pip install --no-cache-dir -r /app/requirements/base_requirements.txt\n"
                "RUN pip install -e /app/"
            )
            with open(dockerfile_path, "w") as f:
                f.write(content)
        click.echo(f"Developer mode enabled: Using local project from {project_root}")
    else:
        click.echo("No --agenthive-project-path specified, Dockerfiles will use PyPI installation (agenthive).")
    
    # 生成範例 worker
    with open(workers_path / "example_worker.py", "w") as f:
        f.write(
            """from agenthive.core.worker import Worker
from typing import Dict, Any

class ExampleWorker(Worker):
    TASK_TYPES = ["example_task"]

    async def setup(self) -> None:
        print("ExampleWorker setting up...")

    async def process_task(self, task) -> Dict[str, Any]:
        print(f"Processing task: {task.data}")
        return {"result": "Task completed", "data": task.data}
"""
        )
    
    # 生成範例 worker 依賴
    with open(workers_path / "requirements" / "example_worker.txt", "w") as f:
        f.write("# Dependencies for ExampleWorker\n")
        f.write("requests==2.32.3\n")
    
    click.echo(f"AgentHive project initialized at {project_path}")
    click.echo("Next steps:")
    click.echo(f"1. cd {project_path}")
    click.echo("2. docker-compose -f docker/docker-compose.yml up --build")

if __name__ == "__main__":
    cli()
