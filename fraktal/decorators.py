"""Decorators for logging execution time and memory usage.

Provides `time_and_memory` decorator which logs time and memory usage of function calls.
"""
from __future__ import annotations

import functools
import logging
import time
from typing import Callable, Optional, Any

try:
    import psutil
except Exception:  # psutil might not be installed yet
    psutil = None  # type: ignore

logger = logging.getLogger("fraktal")
if not logger.handlers:
    # Basic default handler; users can configure logging in their app
    handler = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s] %(levelname)s - %(module)s - %(filename)s - %(funcName)s - %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def time_and_memory(log: Optional[Callable[[str], None]] = None):
    """Decorator factory that returns a decorator which logs execution time and memory usage.

    Args:
        log: Optional callable that accepts a string. If not provided, uses `fraktal` logger.
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            proc = psutil.Process() if psutil is not None else None
            mem_before = proc.memory_info().rss if proc is not None else None
            result = func(*args, **kwargs)
            end = time.perf_counter()
            mem_after = proc.memory_info().rss if proc is not None else None
            elapsed = end - start
            msg = f"{func.__name__} took {elapsed:.6f}s"
            if mem_before is not None and mem_after is not None:
                delta = mem_after - mem_before
                msg += f", mem: {mem_before} -> {mem_after} bytes (Δ {delta} bytes)"
            if log:
                try:
                    log(msg)
                except Exception:
                    logger.info(msg)
            else:
                logger.info(msg)
            return result

        return wrapper

    return decorator
