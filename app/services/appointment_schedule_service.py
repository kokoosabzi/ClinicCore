from datetime import date, datetime, time, timedelta


DEFAULT_WORKING_DAYS = "1,2,3,4,6,7"


def parse_working_days(value: str) -> set[int]:
    try:
        days = {int(part) for part in value.split(",") if part}
    except (AttributeError, TypeError, ValueError) as error:
        raise ValueError("روزهای کاری معتبر نیستند.") from error
    if not days or not days.issubset(set(range(1, 8))):
        raise ValueError("حداقل یک روز کاری معتبر انتخاب کنید.")
    return days


def build_daily_slots(
    selected_day: date,
    occupied: set[datetime],
    now: datetime,
    *,
    workday_start: str,
    workday_end: str,
    slot_minutes: int,
    working_days: str,
) -> list[dict[str, str]]:
    days = parse_working_days(working_days)
    if selected_day.isoweekday() not in days:
        return []
    try:
        start = time.fromisoformat(workday_start)
        end = time.fromisoformat(workday_end)
    except (TypeError, ValueError) as error:
        raise ValueError("ساعت شروع یا پایان معتبر نیست.") from error
    if slot_minutes not in {15, 20, 30, 45, 60} or start >= end:
        raise ValueError("تنظیمات برنامه کاری معتبر نیست.")
    duration = int((datetime.combine(selected_day, end) - datetime.combine(selected_day, start)).total_seconds() // 60)
    if duration % slot_minutes:
        raise ValueError("مدت بازه کاری باید بر مدت هر نوبت بخش‌پذیر باشد.")

    cursor = datetime.combine(selected_day, start)
    finish = datetime.combine(selected_day, end)
    slots = []
    while cursor + timedelta(minutes=slot_minutes) <= finish:
        if cursor in occupied:
            state = "booked"
        elif cursor < now:
            state = "past"
        else:
            state = "available"
        slots.append({"time": cursor.strftime("%H:%M"), "status": state})
        cursor += timedelta(minutes=slot_minutes)
    return slots
