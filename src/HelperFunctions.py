from datetime import datetime


def time_to_minutes(time_str: str) -> int:
    hour, minute = time_str.strip().split(":")
    return int(hour) * 60 + int(minute)


def minutes_to_time(minutes: int) -> str:
    hour = minutes // 60
    minute = minutes % 60
    return f"{hour:02d}:{minute:02d}"


def parse_location(location_text: str) -> tuple:
    x, y = location_text.split(";")
    return float(x), float(y)


def validate_date(date_text: str) -> bool:
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def format_route(route) -> str:
    total = route.total_weight

    if total == int(total):
        total = int(total)

    return f"{' -> '.join(route.path)} | Total Time= {total} Minutes"