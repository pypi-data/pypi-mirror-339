# AgentHive

![PyPI](https://img.shields.io/pypi/v/AgentHive.svg)

AgentHive is a Python-based framework for managing distributed task execution with a focus on scalability and ease of use. It coordinates **producers (tasks)** and **consumers (workers)** in a high-availability setup, using Redis for messaging and PostgreSQL for persistent storage. With a powerful CLI, Docker Compose integration, and a web-based monitor, AgentHive is ideal for developers building extensible task-processing systems.

## Key Features

- **Task Coordination**: Producers submit tasks; workers process them dynamically.
- **High Availability**: Coordinators manage workers and tasks with failover support.
- **Dynamic Workers**: Workers declare task-handling capabilities, loaded at runtime.
- **Real-Time Monitoring**: Web interface displays worker and task statuses via coordinator APIs.
- **Dockerized**: Pre-configured services for easy deployment with Docker Compose.
- **CLI-Driven**: Initialize projects and manage workers with simple `agenthive` commands.

## Installation

Install AgentHive from PyPI to use the CLI:

```bash
pip install agenthive
```

## Quick Start

1. **Initialize a Project**
   Create a new project with the `agenthive init` command:

   ```bash
   agenthive init my-project
   cd my-project
   ```

2. **Run the System**
   Start all services (Redis, PostgreSQL, coordinators, workers, monitor) using Docker Compose:

   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

3. **Customize Workers**
   Add custom workers to `src/workers/` and rebuild the services:

   ```bash
   # Example: Add a new worker manually or extend CLI in the future
   echo "print('Custom worker loaded')" > src/workers/custom_worker.py
   docker-compose -f docker/docker-compose.yml up --build
   ```

## Project Structure

After initialization, your project looks like this:

```
my-project/
├── docker/
│   ├── coordinator/
│   │   └── Dockerfile
│   ├── monitor/
│   │   └── Dockerfile
│   ├── workers/
│   │   └── Dockerfile
│   ├── docker-compose.yml
│   ├── postgres/
│   │   └── init.sql
│   └── redis/
│       └── redis.conf
└── src/
    └── workers/
        ├── example_worker.py
        └── requirements/
            └── example_worker.txt
```

- **`docker/`**: Contains Dockerfiles and Compose configuration.
- **`src/workers/`**: Directory for custom worker implementations.

## Architecture

- **Coordinators**: Assign tasks via Redis, track states in PostgreSQL.
- **Workers**: Fetch tasks from Redis, report heartbeats, execute custom logic.
- **Redis**: Message broker for tasks and status updates.
- **PostgreSQL**: Persistent storage for task and worker data.
- **Monitor**: Web UI querying coordinator APIs for system insights.

## Usage

### For End Users
- Initialize with `agenthive init <project-name>` and run with Docker Compose.
- Dockerfiles use `pip install agenthive` by default, requiring a PyPI-published version.

### For Developers
- Use `--agenthive-project-path` to test local code:
  ```bash
  agenthive init my-project --agenthive-project-path /path/to/agenthive
  cd my-project
  docker-compose -f docker/docker-compose.yml up --build
  ```
- This copies `/path/to/agenthive/src/`, `setup.py`, and `requirements/` into the project, configuring Dockerfiles to use local code instead of PyPI.

## Development Setup

1. **Clone and Install Locally**
   ```bash
   git clone https://github.com/changyy/py-AgentHive.git
   cd py-AgentHive
   python3 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

2. **Test CLI**
   ```bash
   agenthive init test-project --agenthive-project-path .
   cd test-project
   docker-compose -f docker/docker-compose.yml up --build
   ```

3. **Run Original Development Environment**
   Use the local `docker/` for core development:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```

## Worker Customization

Workers are Python modules in `src/workers/`. The worker service scans this directory dynamically at runtime. Example worker:

```python
# src/workers/example_worker.py
from agenthive.core.worker import Worker
from typing import Dict, Any

class ExampleWorker(Worker):
    TASK_TYPES = ["example_task"]

    async def setup(self) -> None:
        print("ExampleWorker setting up...")

    async def process_task(self, task) -> Dict[str, Any]:
        print(f"Processing task: {task.data}")
        return {"result": "Task completed", "data": task.data}
```

Add dependencies in `src/workers/requirements/<worker_name>.txt` (e.g., `requests==2.32.3`).

## Contributing

Fork the repo, create a feature branch, and submit a pull request to `github.com/changyy/py-AgentHive`.

## License

MIT License. See the `LICENSE` file for details.
