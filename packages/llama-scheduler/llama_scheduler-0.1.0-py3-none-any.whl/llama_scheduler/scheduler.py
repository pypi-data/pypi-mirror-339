# src/llama_scheduler/scheduler.py

import asyncio
import signal
from typing import Any, Dict

import yaml
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from loguru import logger

# Placeholder for actual job functions module
# from . import job_functions


class LlamaSchedulerService:
    """Manages the APScheduler instance and loads jobs from config."""

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.scheduler = AsyncIOScheduler(self.config.get("apscheduler", {}))
        self._shutdown_event = asyncio.Event()

    def load_jobs_from_config(self):
        """Loads job definitions from the 'jobs' section of the config."""
        jobs = self.config.get("jobs", [])
        if not jobs:
            logger.warning("No jobs found in configuration.")
            return

        logger.info(f"Loading {len(jobs)} job(s) from configuration...")
        for job_def in jobs:
            try:
                job_id = job_def.get("id")
                func_path = job_def.get("func")
                trigger_type = job_def.get("trigger")
                args = job_def.get("args", [])
                kwargs = job_def.get("kwargs", {})
                trigger_args = {
                    k: v
                    for k, v in job_def.items()
                    if k not in ["id", "func", "trigger", "args", "kwargs"]
                }

                if not all([job_id, func_path, trigger_type]):
                    logger.error(f"Skipping job due to missing id, func, or trigger: {job_def}")
                    continue

                # --- Resolve job function ---
                # This needs a robust way to import the function from string path
                # Example: Use importlib or resolve relative to a known module
                # func = self._resolve_function(func_path)
                # if func is None:
                #     logger.error(f"Could not resolve function '{func_path}' for job '{job_id}'. Skipping.")
                #     continue
                # Using placeholder function for now
                func = self._placeholder_job_func
                logger.warning(
                    f"Using placeholder function for job '{job_id}'. Implement function resolution."
                )
                # ---------------------------

                logger.info(
                    f"Adding job '{job_id}': func='{func_path}', trigger='{trigger_type}', args={trigger_args}"
                )
                self.scheduler.add_job(
                    func,
                    trigger=trigger_type,
                    args=args,
                    kwargs=kwargs,
                    id=job_id,
                    name=job_id,
                    replace_existing=True,
                    **trigger_args,
                )
            except Exception as e:
                logger.error(f"Failed to load job definition {job_def}: {e}", exc_info=True)

    def _placeholder_job_func(self, *args, **kwargs):
        """Placeholder for actual job functions until resolution is implemented."""
        logger.info(f"Placeholder job executed with args: {args}, kwargs: {kwargs}")

    # --- Function Resolution (Example using importlib) ---
    # import importlib
    # def _resolve_function(self, func_path: str):
    #     try:
    #         module_path, func_name = func_path.rsplit(':', 1)
    #         module = importlib.import_module(module_path)
    #         return getattr(module, func_name)
    #     except (ImportError, AttributeError, ValueError) as e:
    #         logger.error(f"Error resolving function path '{func_path}': {e}")
    #         return None
    # -----------------------------------------------------

    async def start(self):
        """Loads jobs and starts the scheduler."""
        logger.info("Starting Llama Scheduler Service...")
        self.load_jobs_from_config()
        self.scheduler.start()
        logger.info("Scheduler started. Waiting for shutdown signal...")
        # Keep running until shutdown event is set
        await self._shutdown_event.wait()
        logger.info("Shutdown signal received.")
        self.shutdown()

    def shutdown(self):
        """Shuts down the scheduler gracefully."""
        logger.info("Shutting down scheduler...")
        try:
            self.scheduler.shutdown(wait=True)
            logger.info("Scheduler shut down successfully.")
        except Exception as e:
            logger.error(f"Error during scheduler shutdown: {e}", exc_info=True)
        self._shutdown_event.set()  # Ensure the start loop exits

    def set_shutdown_event(self):
        """Signals the service to shut down."""
        self._shutdown_event.set()


def load_config(config_path: str) -> Dict[str, Any]:
    """Loads scheduler configuration from a YAML file."""
    logger.info(f"Loading configuration from: {config_path}")
    try:
        with open(config_path, "r") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file {config_path}: {e}")
        raise


async def run_service(config_path: str):
    """Loads config, creates service, and runs it."""
    config = load_config(config_path)
    service = LlamaSchedulerService(config)

    # Set up signal handlers for graceful shutdown
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, service.set_shutdown_event)

    await service.start()


# --- Example main entry point (could be called via `python -m llama_scheduler run ...`) ---
if __name__ == "__main__":
    # Example: run with a default config path if run directly
    # In practice, use a proper CLI (like Typer) or entry script
    default_config = "scheduler_config.yaml"
    logger.info(f"Running scheduler directly with config: {default_config}")
    # Create a dummy config if it doesn't exist for direct run
    import os

    if not os.path.exists(default_config):
        logger.warning(f"Config file '{default_config}' not found, creating dummy config.")
        dummy_config_content = {
            "apscheduler": {"jobstores": {"default": {"type": "memory"}}},
            "jobs": [],
        }
        with open(default_config, "w") as f:
            yaml.dump(dummy_config_content, f)

    try:
        asyncio.run(run_service(default_config))
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received, stopping...")
    except Exception as e:
        logger.exception(f"Scheduler service failed: {e}")
