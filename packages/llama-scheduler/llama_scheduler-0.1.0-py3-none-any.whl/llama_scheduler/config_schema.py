"""Configuration schema definitions for the llama-scheduler package.

This module provides Pydantic models for validating scheduler configuration.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class TriggerType(str, Enum):
    """Valid APScheduler trigger types."""

    DATE = "date"
    INTERVAL = "interval"
    CRON = "cron"


class JobStore(BaseModel):
    """Configuration for an APScheduler jobstore."""

    type: str = Field(..., description="Jobstore type (e.g., 'memory', 'sqlalchemy')")
    url: Optional[str] = Field(None, description="Connection URL for database-based jobstores")
    tablename: Optional[str] = Field(
        "apscheduler_jobs", description="Table name for SQLAlchemy jobstore"
    )

    # Additional fields based on jobstore type can be added
    class Config:
        extra = "allow"  # Allow additional fields based on jobstore type


class Executor(BaseModel):
    """Configuration for an APScheduler executor."""

    type: str = Field(..., description="Executor type (e.g., 'threadpool', 'processpool')")
    max_workers: Optional[int] = Field(
        None, description="Maximum number of worker threads/processes"
    )

    class Config:
        extra = "allow"  # Allow additional fields based on executor type


class APSchedulerConfig(BaseModel):
    """APScheduler configuration settings."""

    jobstores: Dict[str, JobStore] = Field(
        default_factory=lambda: {"default": JobStore(type="memory")},
        description="Job stores for persisting scheduled jobs",
    )
    executors: Dict[str, Executor] = Field(
        default_factory=lambda: {
            "default": Executor(type="threadpool", max_workers=20),
        },
        description="Executors for running jobs",
    )
    job_defaults: Dict[str, Any] = Field(
        default_factory=lambda: {
            "coalesce": False,
            "max_instances": 3,
            "misfire_grace_time": 3600,
        },
        description="Default settings for jobs",
    )
    timezone: str = Field("UTC", description="Default timezone for scheduler")

    class Config:
        extra = "allow"  # Allow additional APScheduler config options


class JobDefinition(BaseModel):
    """Definition of a scheduled job."""

    id: str = Field(..., description="Unique identifier for the job")
    func: str = Field(..., description="Function to call (module:function format)")
    trigger: TriggerType = Field(..., description="Trigger type (date, interval, cron)")

    # Common fields for all jobs
    args: List[Any] = Field(
        default_factory=list, description="Positional arguments for the job function"
    )
    kwargs: Dict[str, Any] = Field(
        default_factory=dict, description="Keyword arguments for the job function"
    )
    name: Optional[str] = Field(None, description="Human-readable name for the job")
    misfire_grace_time: Optional[int] = Field(
        None, description="Grace time for misfired jobs (seconds)"
    )
    coalesce: Optional[bool] = Field(None, description="Coalesce missed executions")
    max_instances: Optional[int] = Field(None, description="Maximum concurrent instances")
    next_run_time: Optional[datetime] = Field(None, description="Next scheduled run time")
    executor: Optional[str] = Field("default", description="Executor to use for this job")
    jobstore: Optional[str] = Field("default", description="Job store to store this job")

    # Fields for DATE trigger
    run_date: Optional[Union[str, datetime]] = Field(
        None, description="Date/time to run the job (for date trigger)"
    )

    # Fields for INTERVAL trigger
    weeks: Optional[int] = Field(None, description="Number of weeks between executions")
    days: Optional[int] = Field(None, description="Number of days between executions")
    hours: Optional[int] = Field(None, description="Number of hours between executions")
    minutes: Optional[int] = Field(None, description="Number of minutes between executions")
    seconds: Optional[int] = Field(None, description="Number of seconds between executions")
    start_date: Optional[Union[str, datetime]] = Field(
        None, description="Starting date for interval trigger"
    )
    end_date: Optional[Union[str, datetime]] = Field(
        None, description="Ending date for interval trigger"
    )

    # Fields for CRON trigger
    year: Optional[Union[str, int]] = Field(None, description="Year field for cron trigger")
    month: Optional[Union[str, int]] = Field(None, description="Month field for cron trigger")
    day: Optional[Union[str, int]] = Field(None, description="Day field for cron trigger")
    week: Optional[Union[str, int]] = Field(None, description="Week field for cron trigger")
    day_of_week: Optional[Union[str, int]] = Field(
        None, description="Day of week field for cron trigger"
    )
    hour: Optional[Union[str, int]] = Field(None, description="Hour field for cron trigger")
    minute: Optional[Union[str, int]] = Field(None, description="Minute field for cron trigger")
    second: Optional[Union[str, int]] = Field(None, description="Second field for cron trigger")

    @validator("func")
    def validate_func(cls, v):
        """Validate that func is in the format 'module:function'."""
        if ":" not in v:
            raise ValueError("Function must be in the format 'module:function_name'")
        return v

    @validator("run_date", "start_date", "end_date", pre=True)
    def validate_dates(cls, v):
        """Convert string dates to datetime objects."""
        if isinstance(v, str):
            try:
                return datetime.fromisoformat(v.replace("Z", "+00:00"))
            except ValueError:
                # Try with different format
                try:
                    return datetime.strptime(v, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    raise ValueError(f"Invalid date format: {v}")
        return v

    class Config:
        extra = "allow"  # Allow additional fields for future compatibility


class SchedulerConfig(BaseModel):
    """Complete scheduler configuration."""

    apscheduler: APSchedulerConfig = Field(
        default_factory=APSchedulerConfig,
        description="APScheduler configuration settings",
    )
    jobs: List[JobDefinition] = Field(
        default_factory=list, description="Job definitions to schedule"
    )
    logging: Optional[Dict[str, Any]] = Field(None, description="Logging configuration")

    class Config:
        extra = "allow"  # Allow additional configuration options


def validate_config(config_dict: Dict[str, Any]) -> SchedulerConfig:
    """Validate a configuration dictionary against the schema.

    Args:
        config_dict: Dictionary containing scheduler configuration

    Returns:
        SchedulerConfig: Validated configuration object

    Raises:
        ValidationError: If the configuration is invalid
    """
    return SchedulerConfig.parse_obj(config_dict)
