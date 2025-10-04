"""LangSmith tracing and observability configuration.

This module provides configuration and utilities for LangSmith tracing,
enabling observability for AI operations throughout the application.
"""

import os
from typing import Optional
from functools import wraps

from .logging import get_logger

logger = get_logger(__name__)


class TracingConfig:
    """LangSmith tracing configuration."""

    def __init__(self):
        """Initialize tracing configuration from environment variables."""
        self.enabled = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        self.project = os.getenv("LANGCHAIN_PROJECT", "componentforge-dev")
        self.endpoint = os.getenv(
            "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
        )

    def is_configured(self) -> bool:
        """Check if tracing is properly configured.

        Returns:
            bool: True if tracing is enabled and API key is set
        """
        return self.enabled and bool(self.api_key)

    def get_config(self) -> dict:
        """Get tracing configuration as dictionary.

        Returns:
            dict: Configuration dictionary with tracing settings
        """
        return {
            "enabled": self.enabled,
            "project": self.project,
            "endpoint": self.endpoint,
            "api_key_set": bool(self.api_key),
        }


# Global tracing configuration instance
_tracing_config: Optional[TracingConfig] = None


def get_tracing_config() -> TracingConfig:
    """Get or create the global tracing configuration instance.

    Returns:
        TracingConfig: The global tracing configuration instance
    """
    global _tracing_config
    if _tracing_config is None:
        _tracing_config = TracingConfig()
    return _tracing_config


def init_tracing() -> bool:
    """Initialize LangSmith tracing.

    Returns:
        bool: True if tracing was successfully initialized, False otherwise
    """
    config = get_tracing_config()

    if not config.is_configured():
        logger.warning(
            "LangSmith tracing not configured. Set LANGCHAIN_TRACING_V2=true "
            "and LANGCHAIN_API_KEY to enable tracing."
        )
        return False

    # Set environment variables for LangChain
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = config.api_key
    os.environ["LANGCHAIN_PROJECT"] = config.project
    os.environ["LANGCHAIN_ENDPOINT"] = config.endpoint

    logger.info(
        f"LangSmith tracing initialized",
        extra={
            "extra": {
                "project": config.project,
                "endpoint": config.endpoint,
            }
        },
    )
    return True


def traced(run_name: Optional[str] = None, **kwargs):
    """Decorator to add tracing to a function.

    This is a convenience decorator that can be used with LangChain's
    @traceable decorator when it's available.

    Args:
        run_name: Optional name for the trace run
        **kwargs: Additional arguments to pass to the tracer

    Returns:
        Decorated function with tracing enabled
    """

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            config = get_tracing_config()
            if not config.is_configured():
                # If tracing not configured, just run the function normally
                return await func(*args, **kwargs)

            # Try to use LangChain's traceable decorator if available
            try:
                from langchain_core.tracers.langchain import LangChainTracer

                # Run with tracing
                return await func(*args, **kwargs)
            except ImportError:
                logger.debug("LangChain tracer not available, running without trace")
                return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            config = get_tracing_config()
            if not config.is_configured():
                return func(*args, **kwargs)

            try:
                from langchain_core.tracers.langchain import LangChainTracer

                return func(*args, **kwargs)
            except ImportError:
                logger.debug("LangChain tracer not available, running without trace")
                return func(*args, **kwargs)

        # Return appropriate wrapper based on function type
        import asyncio

        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def get_trace_url(run_id: str) -> str:
    """Get the LangSmith URL for a specific trace run.

    Args:
        run_id: The run ID from LangSmith

    Returns:
        str: Full URL to view the trace in LangSmith UI
    """
    config = get_tracing_config()
    base_url = "https://smith.langchain.com"
    return f"{base_url}/o/default/projects/p/{config.project}/r/{run_id}"


# Initialize tracing on module import if configured
init_tracing()
