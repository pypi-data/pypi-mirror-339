"""Example job functions for the Llama Scheduler.

This module provides examples of common job patterns:
1. Simple job functions
2. Jobs with logging/error handling
3. Jobs interacting with other system components
4. async job functions

Job functions can be referenced in scheduler configurations using the
format: "llama_scheduler.job_functions:job_name"
"""

import asyncio
import subprocess
import time
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests
from loguru import logger


def simple_job(name: str = "simple_job") -> None:
    """A simple job that logs its execution time."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{name}] Simple job executed at {current_time}")


def parameterized_job(message: str, count: int = 1) -> None:
    """A job that accepts parameters."""
    for i in range(count):
        logger.info(f"Parameterized job message ({i+1}/{count}): {message}")


def long_running_job(duration: int = 10) -> None:
    """A job that simulates long-running work."""
    logger.info(f"Starting long running job for {duration} seconds")
    start_time = time.time()

    # Simulate work with progress updates
    for i in range(duration):
        # In a real job, this would be doing actual work
        time.sleep(1)
        if i % 5 == 0 or i == duration - 1:
            progress = (i + 1) / duration * 100
            elapsed = time.time() - start_time
            logger.info(f"Long job progress: {progress:.1f}% ({elapsed:.1f}s elapsed)")

    logger.info(f"Long running job completed after {time.time() - start_time:.2f} seconds")


def error_handling_job(fail_probability: float = 0.3) -> bool:
    """A job demonstrating error handling patterns.

    Returns:
        bool: True if job completed successfully, False otherwise
    """
    import random

    try:
        logger.info("Starting job with error handling")

        # Simulate potential failure
        if random.random() < fail_probability:
            raise ValueError("Simulated random failure in job")

        # Simulate actual work
        logger.info("Job processing completed successfully")
        return True

    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        # Depending on the error, you might want to:
        # 1. Return a failure status: return False
        # 2. Re-raise the exception: raise
        # 3. Take remedial action
        return False


def shell_command_job(command: str) -> int:
    """Execute a shell command as a job.

    Args:
        command: Shell command to execute

    Returns:
        int: Return code from the command
    """
    logger.info(f"Executing shell command: {command}")
    try:
        # For security, avoid shell=True when possible
        result = subprocess.run(command.split(), capture_output=True, text=True, check=False)

        if result.returncode == 0:
            logger.info(f"Command succeeded with output: {result.stdout}")
        else:
            logger.error(f"Command failed with code {result.returncode}: {result.stderr}")

        return result.returncode
    except Exception as e:
        logger.error(f"Failed to execute command: {e}")
        return -1


def http_request_job(
    url: str,
    method: str = "GET",
    data: Optional[Dict[str, Any]] = None,
    timeout: int = 30,
) -> Dict[str, Any]:
    """Make an HTTP request as a job.

    Args:
        url: Target URL
        method: HTTP method (GET, POST, etc.)
        data: Request data/payload for POST/PUT
        timeout: Request timeout in seconds

    Returns:
        dict: Response information including status and content
    """
    logger.info(f"Making {method} request to {url}")
    result = {
        "success": False,
        "status_code": None,
        "elapsed_ms": None,
        "error": None,
        "content": None,
    }

    try:
        start_time = time.time()
        response = requests.request(method=method.upper(), url=url, json=data, timeout=timeout)
        elapsed = (time.time() - start_time) * 1000  # ms

        result.update(
            {
                "success": 200 <= response.status_code < 300,
                "status_code": response.status_code,
                "elapsed_ms": elapsed,
                "content": response.text[:500],  # Truncate large responses
            }
        )

        if result["success"]:
            logger.info(f"Request succeeded: {response.status_code} in {elapsed:.1f}ms")
        else:
            logger.warning(f"Request failed: {response.status_code} in {elapsed:.1f}ms")

    except requests.RequestException as e:
        result["error"] = str(e)
        logger.error(f"Request error: {e}")

    return result


async def async_job(sleep_time: float = 1.0) -> None:
    """An example of an async job function.

    For async jobs to work properly, the scheduler needs to be configured
    to use the asyncio executor.
    """
    logger.info(f"Starting async job, will sleep for {sleep_time}s")
    await asyncio.sleep(sleep_time)
    logger.info("Async job completed")


async def parallel_async_job(urls: List[str], timeout: float = 5.0) -> List[Dict[str, Any]]:
    """An example of a job making parallel async requests.

    Args:
        urls: List of URLs to request
        timeout: Request timeout in seconds

    Returns:
        list: Results for each URL
    """
    import aiohttp

    logger.info(f"Starting parallel async job for {len(urls)} URLs")
    results = []

    async with aiohttp.ClientSession() as session:

        async def fetch_url(url):
            try:
                start_time = time.time()
                async with session.get(url, timeout=timeout) as response:
                    content = await response.text()
                    elapsed = time.time() - start_time
                    return {
                        "url": url,
                        "status": response.status,
                        "success": 200 <= response.status < 300,
                        "elapsed_seconds": elapsed,
                        "content_length": len(content),
                    }
            except Exception as e:
                return {"url": url, "success": False, "error": str(e)}

        # Create tasks for all URLs
        tasks = [fetch_url(url) for url in urls]
        results = await asyncio.gather(*tasks)

    logger.info(f"Parallel async job completed for {len(urls)} URLs")
    return results


def data_processing_job(input_path: str, output_path: str) -> Dict[str, Any]:
    """Example job for processing data files.

    Args:
        input_path: Path to input data file
        output_path: Path to write output

    Returns:
        dict: Processing statistics
    """
    import json
    import os

    stats = {
        "start_time": datetime.now().isoformat(),
        "input_size_bytes": 0,
        "output_size_bytes": 0,
        "records_processed": 0,
        "success": False,
    }

    logger.info(f"Starting data processing: {input_path} -> {output_path}")

    try:
        # Ensure input exists
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"Input file not found: {input_path}")

        stats["input_size_bytes"] = os.path.getsize(input_path)

        # Simulate data processing
        # In a real job, this would parse/process the actual file content
        with open(input_path, "r") as f:
            # Count lines as "records"
            for i, _ in enumerate(f):
                stats["records_processed"] = i + 1

        # Write dummy output for demo
        with open(output_path, "w") as f:
            json.dump(
                {
                    "processed_at": stats["start_time"],
                    "record_count": stats["records_processed"],
                    "source": input_path,
                },
                f,
            )

        stats["output_size_bytes"] = os.path.getsize(output_path)
        stats["success"] = True
        logger.info(f"Data processing complete: {stats['records_processed']} records")

    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        stats["error"] = str(e)

    stats["end_time"] = datetime.now().isoformat()
    return stats
