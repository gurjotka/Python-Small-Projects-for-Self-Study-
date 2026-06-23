from datetime import datetime

def log_error(error: str, path: str):
    print(f"[ERROR] {datetime.now()} | {path} | {error}")