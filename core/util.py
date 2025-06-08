from datetime import datetime, timedelta


def get_remaining_seconds(start_time_str: str, duration: str):
    start = datetime.fromisoformat(start_time_str)
    end = start + timedelta(seconds=duration)
    now = datetime.now()
    remaining = (end - now).total_seconds()
    return max(0, int(remaining))
