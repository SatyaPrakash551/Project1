
import logging
import logging.config
import os
import sys

import structlog


def configure_logging() -> None:
    """
    Configure application-wide logging.

    Supports:
    - Console output for development
    - JSON output for production
    - Standard library logging integration
    - Third-party library logging
    """

    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    log_format = os.getenv("LOG_FORMAT", "json").lower()

    # Validate configuration before changing logging handlers.
    valid_levels = {
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    }

    if log_level not in valid_levels:
        raise ValueError(
            f"Invalid LOG_LEVEL: {log_level}"
        )

    if log_format not in {"json", "console"}:
        raise ValueError(
            f"Invalid LOG_FORMAT: {log_format}"
        )

    # Processors shared by structlog and stdlib logs.
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(
            fmt="iso",
            utc=True,
        ),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # Select output format.
    if log_format == "json":
        renderer = structlog.processors.JSONRenderer()
    else:
        renderer = structlog.dev.ConsoleRenderer()

    # Standard logging formatter.
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter
            .remove_processors_meta,
            renderer,
        ],
    )

    # Configure structlog.
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            *shared_processors,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Configure standard Python logging.
    logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,

            "formatters": {
                "structured": {
                    "()": lambda: formatter,
                },
            },

            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "stream": sys.stdout,
                    "formatter": "structured",
                    "level": log_level,
                },
            },

            "root": {
                "handlers": ["console"],
                "level": log_level,
            },

            "loggers": {
                # Uvicorn logs go through the root handler.
                "uvicorn": {
                    "handlers": [],
                    "level": log_level,
                    "propagate": True,
                },

                "uvicorn.error": {
                    "handlers": [],
                    "level": log_level,
                    "propagate": True,
                },

                "uvicorn.access": {
                    "handlers": [],
                    "level": log_level,
                    "propagate": True,
                },

                # Avoid logging every SQL statement in production.
                "sqlalchemy.engine": {
                    "handlers": [],
                    "level": "WARNING",
                    "propagate": True,
                },

                "sqlalchemy.pool": {
                    "handlers": [],
                    "level": "WARNING",
                    "propagate": True,
                },
            },
        }
    )
