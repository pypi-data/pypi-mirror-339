# llama-scheduler

[![PyPI version](https://img.shields.io/pypi/v/llama_scheduler.svg)](https://pypi.org/project/llama_scheduler/)
[![License](https://img.shields.io/github/license/llamasearchai/llama-scheduler)](https://github.com/llamasearchai/llama-scheduler/blob/main/LICENSE)
[![Python Version](https://img.shields.io/pypi/pyversions/llama_scheduler.svg)](https://pypi.org/project/llama_scheduler/)
[![CI Status](https://github.com/llamasearchai/llama-scheduler/actions/workflows/llamasearchai_ci.yml/badge.svg)](https://github.com/llamasearchai/llama-scheduler/actions/workflows/llamasearchai_ci.yml)

**Llama Scheduler (llama-scheduler)** provides job scheduling capabilities within the LlamaSearch AI ecosystem. It allows defining, scheduling, and managing recurring or one-off tasks.

## Key Features

- **Job Scheduling:** Core engine for scheduling tasks based on time or events (`scheduler.py`).
- **Job Definitions:** Allows defining the functions or tasks to be executed (`job_functions.py`).
- **Configuration Schema:** Defines the structure for configuring jobs and schedules (`config_schema.py`).
- **Command-Line Interface:** Provides tools to manage schedules and jobs via CLI (`cli.py`).
- **Core Module:** Manages the scheduler lifecycle and job execution (`core.py`).
- **Configurable:** Allows defining schedules, job parameters, and backend settings (`config.py`).

## Installation

```bash
pip install llama-scheduler
# Or install directly from GitHub for the latest version:
# pip install git+https://github.com/llamasearchai/llama-scheduler.git
```

## Usage

### Command-Line Interface (CLI)

*(CLI usage examples for adding, removing, and listing scheduled jobs will be added here.)*

```bash
llama-scheduler add-job --name "daily-report" --schedule "0 8 * * *" --task "generate_report"
llama-scheduler list-jobs
```

### Python Client / Embedding

*(Python usage examples for programmatically scheduling jobs will be added here.)*

```python
# Placeholder for Python client usage
# from llama_scheduler import Scheduler, Job
# from my_tasks import backup_database # Assuming backup_database is in job_functions or imported

# scheduler = Scheduler(config_path="config.yaml")

# # Define a job
# backup_job = Job(
#     name="database_backup",
#     func=backup_database,
#     trigger="cron",
#     hour=2, # Run at 2 AM daily
#     args=["/path/to/backup/dir"]
# )

# # Add and start the job
# scheduler.add_job(backup_job)
# scheduler.start()
```

## Architecture Overview

```mermaid
graph TD
    A[User / CLI (cli.py)] --> B{Core Module (core.py)};
    B --> C{Scheduler Engine (scheduler.py)};
    C -- Loads Job Definitions --> D[Job Functions (job_functions.py)];
    C -- Reads Schedule --> E{Job Store / Schedule DB};
    C -- Triggers Job --> F[Job Executor];
    F -- Executes --> D;

    G[Configuration (config.py, config_schema.py)] -- Configures --> B;
    G -- Configures --> C;
    G -- Defines Schema for --> E;

    style C fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#ccf,stroke:#333,stroke-width:1px
```

1.  **Interface:** Users interact via the CLI or potentially a programmatic API managed by the Core Module.
2.  **Core Module:** Handles requests and controls the scheduler engine.
3.  **Scheduler Engine:** The heart of the system, responsible for tracking time/events and triggering jobs based on the schedule.
4.  **Job Store:** Stores the defined jobs and their schedules (could be in memory, a file, or a database).
5.  **Job Functions:** Contains the actual Python code that gets executed for each job.
6.  **Executor:** The component responsible for running the job function when triggered.
7.  **Configuration:** Defines the schedule, job parameters, backend storage, etc.

## Configuration

*(Details on configuring job schedules (cron syntax, intervals), job parameters, backend persistence, etc., will be added here.)*

## Development

### Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/llama-scheduler.git
cd llama-scheduler

# Install in editable mode with development dependencies
pip install -e ".[dev]"
```

### Testing

```bash
pytest tests/
```

### Contributing

Contributions are welcome! Please refer to [CONTRIBUTING.md](CONTRIBUTING.md) and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
