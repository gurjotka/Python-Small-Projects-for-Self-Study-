import time
from datetime import datetime


def log_request(method: str, path: str, status_code: int, duration: float):
    log = (
        f"{datetime.now()} | "
        f"{method} {path} | "
        f"STATUS={status_code} | "
        f"TIME={round(duration * 1000, 2)}ms"
    )

    print(log)
