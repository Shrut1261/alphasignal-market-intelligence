import sys

from loguru import logger


def configure_logging(level: str = "INFO") -> None:
    """Configure structured console logging once at service startup."""

    logger.remove()
    logger.add(
        sys.stderr,
        level=level.upper(),
        serialize=True,
        backtrace=False,
        diagnose=False,
    )
