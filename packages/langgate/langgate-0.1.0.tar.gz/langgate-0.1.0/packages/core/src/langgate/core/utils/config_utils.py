"""Configuration utilities for LangGate."""

import os
from pathlib import Path

from langgate.core.logging import StructLogger


def resolve_path(
    env_var: str,
    arg_path: Path | None = None,
    default_path: Path | None = None,
    path_desc: str = "path",
    logger: StructLogger | None = None,
) -> Path:
    """Resolve a file path based on priority: args > env > default.

    Args:
        env_var: Environment variable name to check
        arg_path: Path provided in constructor args
        default_path: Default path to use if others not provided
        path_desc: Description for logging
        logger: Optional logger instance for recording path resolution

    Returns:
        Resolved Path object
    """
    # Priority: args > env > default
    resolved_path = arg_path or Path(os.getenv(env_var, str(default_path)))

    # Log the resolved path and its existence
    if logger:
        exists = resolved_path.exists()
        logger.debug(
            f"resolved_{path_desc}",
            path=str(resolved_path),
            exists=exists,
            source="args" if arg_path else ("env" if os.getenv(env_var) else "default"),
        )

    return resolved_path
