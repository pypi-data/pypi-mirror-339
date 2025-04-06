import time
import functools
from google.auth.transport.requests import Request


def safe_refresh(credentials) -> None:
    """Refresh credentials if they're expired or invalid."""
    if not credentials.valid or credentials.expired:
        credentials.refresh(Request())


def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """Exponential backoff retry decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            wait = delay
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        raise
                    time.sleep(wait)
                    wait *= backoff
        return wrapper
    return decorator


def log_debug(message: str):
    """Optional: Basic debug logger."""
    print(f"[DEBUG] {message}")
