import time

from functools import wraps
from typing import Any, Callable
from loguru import logger


def execution_time(func: Callable) -> Callable:
    """Decorator that prints the execution time of a function.

    Args:
        func (Callable): Function to be decorated

    Returns:
        Callable: Wrapped function
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.info(f"Function {func.__name__} took {end_time - start_time:.4f} seconds to execute")
        return result
    return wrapper
