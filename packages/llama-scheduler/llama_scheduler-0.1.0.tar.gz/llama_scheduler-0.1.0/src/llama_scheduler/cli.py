"""Command line interface for the llama-scheduler package.

This module provides the CLI for starting, stopping, and managing the
scheduler service and jobs.
"""

import asyncio
import os
import sys

import typer
import yaml
from loguru import logger

from llama_scheduler import load_config, run_service
from llama_scheduler.job_functions import simple_job

# Configure loguru for CLI
logger.remove()
logger.add(sys.stderr, level="INFO")

app = typer.Typer(name="llama-scheduler", help="LlamaAI Scheduler - Job scheduling service")


@app.command()
def run(
    config_path: str = typer.Argument(..., help="Path to the scheduler configuration YAML file"),
    log_level: str = typer.Option("INFO", help="Log level (DEBUG, INFO, WARNING, ERROR)"),
):
    """Run the scheduler service with the specified configuration."""
    # Configure logging based on CLI options
    logger.remove()
    logger.add(sys.stderr, level=log_level)

    logger.info(f"Starting Llama Scheduler with config: {config_path}")

    # Check if config file exists
    if not os.path.exists(config_path):
        typer.echo(f"Error: Configuration file not found: {config_path}")
        raise typer.Exit(code=1)

    try:
        # Run the scheduler service
        asyncio.run(run_service(config_path))
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.exception(f"Scheduler failed: {e}")
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def validate(
    config_path: str = typer.Argument(..., help="Path to the scheduler configuration YAML file"),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Show detailed validation information"
    ),
):
    """Validate a scheduler configuration file without running the scheduler."""
    try:
        logger.info(f"Validating config file: {config_path}")

        # Try to load and parse the configuration
        config = load_config(config_path)

        # Check for required sections
        if "jobs" not in config:
            typer.echo("Warning: No 'jobs' section found in configuration")

        # Count and validate jobs
        jobs = config.get("jobs", [])
        valid_jobs = []
        invalid_jobs = []

        for i, job in enumerate(jobs):
            job_id = job.get("id", f"job_{i}")
            valid = True
            missing = []

            # Check required fields
            for field in ["id", "func", "trigger"]:
                if field not in job:
                    valid = False
                    missing.append(field)

            # Check trigger type
            trigger = job.get("trigger")
            if trigger not in ["date", "interval", "cron"]:
                valid = False
                missing.append(f"invalid trigger type: {trigger}")

            # Record result
            if valid:
                valid_jobs.append(job_id)
            else:
                reason = f"missing: {', '.join(missing)}"
                invalid_jobs.append((job_id, reason))

        # Print results
        typer.echo(f"\nConfiguration validation results for {config_path}:")
        typer.echo(f"- Total jobs defined: {len(jobs)}")
        typer.echo(f"- Valid jobs: {len(valid_jobs)}")
        typer.echo(f"- Invalid jobs: {len(invalid_jobs)}")

        if invalid_jobs:
            typer.echo("\nInvalid jobs:")
            for job_id, reason in invalid_jobs:
                typer.echo(f"  - {job_id}: {reason}")

        if verbose and valid_jobs:
            typer.echo("\nValid jobs:")
            for job_id in valid_jobs:
                typer.echo(f"  - {job_id}")

        # Return appropriate exit code
        if invalid_jobs:
            typer.echo("\nConfiguration has errors that need to be fixed.")
            raise typer.Exit(code=1)
        else:
            typer.echo("\nConfiguration is valid.")

    except Exception as e:
        typer.echo(f"Error validating configuration: {e}")
        raise typer.Exit(code=1)


@app.command()
def init(
    output_path: str = typer.Argument(
        "scheduler_config.yaml", help="Path to save the generated configuration file"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing file if it exists"),
):
    """Generate a sample configuration file."""
    if os.path.exists(output_path) and not force:
        typer.echo(f"Error: File already exists: {output_path}")
        typer.echo("Use --force to overwrite")
        raise typer.Exit(code=1)

    # Create sample configuration
    sample_config = {
        "apscheduler": {
            "jobstores": {
                "default": {"type": "memory"},
                # Uncomment to use SQLAlchemy for persistent storage
                # "sqlite": {
                #     "type": "sqlalchemy",
                #     "url": "sqlite:///jobs.sqlite"
                # }
            },
            "executors": {
                "default": {"type": "threadpool", "max_workers": 20},
                "processpool": {"type": "processpool", "max_workers": 5},
            },
            "job_defaults": {
                "coalesce": False,
                "max_instances": 3,
                "misfire_grace_time": 3600,
            },
            "timezone": "UTC",
        },
        "jobs": [
            {
                "id": "simple_example",
                "func": "llama_scheduler.job_functions:simple_job",
                "trigger": "interval",
                "seconds": 60,
                "args": ["simple_example_job"],
                "kwargs": {},
            },
            {
                "id": "parameterized_example",
                "func": "llama_scheduler.job_functions:parameterized_job",
                "trigger": "cron",
                "minute": "*/15",
                "args": [],
                "kwargs": {"message": "Scheduled message", "count": 3},
            },
            {
                "id": "one_time_example",
                "func": "llama_scheduler.job_functions:http_request_job",
                "trigger": "date",
                "run_date": "2024-01-01 00:00:00",
                "args": [],
                "kwargs": {"url": "https://httpbin.org/get", "method": "GET"},
            },
        ],
    }

    # Write to file
    try:
        with open(output_path, "w") as f:
            yaml.dump(sample_config, f, default_flow_style=False, sort_keys=False)
        typer.echo(f"Sample configuration created at: {output_path}")
    except Exception as e:
        typer.echo(f"Error creating sample configuration: {e}")
        raise typer.Exit(code=1)


@app.command()
def test(
    job_name: str = typer.Argument(
        "simple_job", help="Job function name to test (from job_functions module)"
    ),
    params: list[str] = typer.Argument(
        None, help="Parameters to pass to the job function (format: key=value)"
    ),
):
    """Test a job function by running it directly."""
    from llama_scheduler.job_functions import (
        async_job,
        data_processing_job,
        error_handling_job,
        http_request_job,
        long_running_job,
        parameterized_job,
        shell_command_job,
    )

    # Map of available job functions
    job_map = {
        "simple_job": simple_job,
        "parameterized_job": parameterized_job,
        "long_running_job": long_running_job,
        "error_handling_job": error_handling_job,
        "shell_command_job": shell_command_job,
        "http_request_job": http_request_job,
        "async_job": async_job,
        "data_processing_job": data_processing_job,
    }

    if job_name not in job_map:
        typer.echo(f"Error: Unknown job function: {job_name}")
        typer.echo(f"Available jobs: {', '.join(job_map.keys())}")
        raise typer.Exit(code=1)

    # Parse parameters (key=value format)
    kwargs = {}
    if params:
        for param in params:
            if "=" not in param:
                typer.echo(f"Error: Invalid parameter format: {param}")
                typer.echo("Parameters must be in the format key=value")
                raise typer.Exit(code=1)

            key, value = param.split("=", 1)

            # Try to convert string to appropriate type
            try:
                # If value can be converted to int
                if value.isdigit():
                    value = int(value)
                # If value is a float
                elif value.replace(".", "", 1).isdigit():
                    value = float(value)
                # Handle boolean values
                elif value.lower() in ["true", "false"]:
                    value = value.lower() == "true"
            except (ValueError, AttributeError):
                pass  # Keep as string if conversion fails

            kwargs[key] = value

    # Execute the job
    job_func = job_map[job_name]
    typer.echo(f"Executing job function: {job_name}")
    typer.echo(f"Parameters: {kwargs}")

    try:
        # Check if it's an async function
        if asyncio.iscoroutinefunction(job_func):
            result = asyncio.run(job_func(**kwargs))
        else:
            result = job_func(**kwargs)

        typer.echo(f"Job completed with result: {result}")
    except Exception as e:
        typer.echo(f"Error executing job: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
