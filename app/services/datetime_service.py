from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo


def gregorian_to_jalali(value: date | datetime) -> tuple[int, int, int]:
    gy, gm, gd = value.year, value.month, value.day
    month_days = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    g = gy - 1600
    days = 365 * g + (g + 3) // 4 - (g + 99) // 100 + (g + 399) // 400 - 80 + gd + month_days[gm - 1]
    if gm > 2 and (gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0)):
        days += 1
    jy = -979 + 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm, jd = 1 + days // 31, 1 + days % 31
    else:
        jm, jd = 7 + (days - 186) // 30, 1 + (days - 186) % 30
    return jy, jm, jd


def jalali_to_gregorian(year: int, month: int, day: int) -> date:
    if not 1 <= month <= 12 or not 1 <= day <= (31 if month <= 6 else 30):
        raise ValueError("Invalid Jalali date")
    jy = year + 979
    days = 365 * jy + (jy // 33) * 8 + ((jy % 33) + 3) // 4 + day - 1
    days += (month - 1) * 31 if month <= 7 else (month - 1) * 30 + 6
    gy = 1600 + 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        gy += 100 * ((days - 1) // 36524)
        days = (days - 1) % 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    leap = gy % 4 == 0 and (gy % 100 != 0 or gy % 400 == 0)
    lengths = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 1
    while gd > lengths[gm - 1]:
        gd -= lengths[gm - 1]
        gm += 1
    return date(gy, gm, gd)


def format_jalali(value: date | datetime, separator: str = "/") -> str:
    year, month, day = gregorian_to_jalali(value)
    return f"{year:04d}{separator}{month:02d}{separator}{day:02d}"


def current_datetime(timezone_name: str = "Asia/Tehran") -> datetime:
    """Return the current instant converted to the configured timezone."""
    return datetime.now(timezone.utc).astimezone(ZoneInfo(timezone_name))


def format_current_datetime(timezone_name: str = "Asia/Tehran", calendar: str = "jalali", date_format: str = "YYYY/MM/DD", time_format: str = "24", show_seconds: bool = False, now: datetime | None = None) -> str:
    value = (now or datetime.now(timezone.utc)).astimezone(ZoneInfo(timezone_name))
    if calendar == "jalali":
        year, month, day = gregorian_to_jalali(value)
    else:
        year, month, day = value.year, value.month, value.day
    rendered_date = date_format.replace("YYYY", f"{year:04d}").replace("MM", f"{month:02d}").replace("DD", f"{day:02d}")
    if time_format == "12":
        hour = value.hour % 12 or 12
        rendered_time = f"{hour:02d}:{value.minute:02d}"
    else:
        rendered_time = f"{value.hour:02d}:{value.minute:02d}"
    if show_seconds:
        rendered_time += f":{value.second:02d}"
    return f"{rendered_date} {rendered_time}"


def parse_jalali(value: str, separator: str = "/") -> date:
    parts = value.strip().split(separator)
    if len(parts) != 3:
        raise ValueError("Jalali date must be YYYY/MM/DD")
    try:
        year, month, day = (int(part) for part in parts)
    except ValueError as exc:
        raise ValueError("Jalali date must contain numbers") from exc
    return jalali_to_gregorian(year, month, day)


def parse_configured_datetime(value: str, calendar: str = "jalali") -> datetime:
    """Parse a local date/time entered in the configured calendar into Gregorian datetime."""
    value = value.strip()
    try:
        date_text, time_text = value.replace("T", " ").split(None, 1)
        hour, minute = (int(part) for part in time_text[:5].split(":"))
        if not 0 <= hour <= 23 or not 0 <= minute <= 59:
            raise ValueError
        parts = date_text.replace("-", "/").split("/")
        if len(parts) != 3:
            raise ValueError
        year, month, day = (int(part) for part in parts)
        if calendar == "jalali":
            converted = jalali_to_gregorian(year, month, day)
        else:
            converted = date(year, month, day)
        return datetime(converted.year, converted.month, converted.day, hour, minute)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid configured date/time") from exc


def format_configured_datetime(value: datetime, calendar: str = "jalali", date_format: str = "YYYY/MM/DD", time_format: str = "24") -> str:
    if calendar == "jalali":
        year, month, day = gregorian_to_jalali(value)
    else:
        year, month, day = value.year, value.month, value.day
    rendered_date = date_format.replace("YYYY", f"{year:04d}").replace("MM", f"{month:02d}").replace("DD", f"{day:02d}")
    if time_format == "12":
        hour = value.hour % 12 or 12
        return f"{rendered_date} {hour:02d}:{value.minute:02d}"
    return f"{rendered_date} {value.hour:02d}:{value.minute:02d}"
