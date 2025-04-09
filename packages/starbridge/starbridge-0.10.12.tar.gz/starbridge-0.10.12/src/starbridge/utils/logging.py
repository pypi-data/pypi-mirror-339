"""Logging configuration and utilities for the starbridge package."""

import logging as python_logging
from typing import Annotated, Literal

import click
import logfire
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from rich.console import Console
from rich.logging import RichHandler

from starbridge import __project_name__
from starbridge.instrumentation import logfire_initialize
from starbridge.utils.settings import load_settings


def get_logger(name: str | None) -> python_logging.Logger:
    """
    Get a logger instance with the given name or project name as default.

    Args:
        name: The name for the logger. If None, uses project name.

    Returns:
        Logger: Configured logger instance.

    """
    if (name is None) or (name == __project_name__):
        return python_logging.getLogger(__project_name__)
    return python_logging.getLogger(f"{__project_name__}.{name}")


class LoggingSettings(BaseSettings):
    """Settings for configuring logging behavior."""

    model_config = SettingsConfigDict(
        env_prefix=f"{__project_name__.upper()}_LOGGING_",
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )

    loglevel: Annotated[
        Literal["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        Field(description="Logging level", default="INFO"),
    ]
    log_file_enabled: Annotated[
        bool,
        Field(description="Enable logging to file", default=False),
    ]
    log_file_name: Annotated[
        str,
        Field(description="Name of the log file", default="starbridge.log"),
    ]
    log_console_enabled: Annotated[
        bool,
        Field(description="Enable logging to console", default=False),
    ]


settings = load_settings(LoggingSettings)


class CustomFilter(python_logging.Filter):
    """Custom filter for log records."""

    @staticmethod
    def filter(_record: python_logging.LogRecord) -> bool:
        """
        Filter log records based on custom criteria.

        Args:
            record: The log record to filter.

        Returns:
            bool: True if record should be logged, False otherwise.

        """
        return True


log_filter = CustomFilter()

handlers = []

if settings.log_file_enabled:
    file_handler = python_logging.FileHandler(settings.log_file_name)
    file_formatter = python_logging.Formatter(
        fmt="%(asctime)s %(process)d %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(log_filter)
    handlers.append(file_handler)

if settings.log_console_enabled:
    rich_handler = RichHandler(
        console=Console(stderr=True),
        markup=True,
        rich_tracebacks=True,
        tracebacks_suppress=[click],
        show_time=True,
        omit_repeated_times=True,
        show_path=True,
        show_level=True,
        enable_link_path=True,
    )
    rich_handler.addFilter(log_filter)
    handlers.append(rich_handler)

logfire_initialized = logfire_initialize()
if logfire_initialized:
    logfire_handler = logfire.LogfireLoggingHandler()
    logfire_handler.addFilter(log_filter)
    handlers.append(logfire_handler)


python_logging.basicConfig(
    level=settings.loglevel,
    format="%(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=handlers,
)
