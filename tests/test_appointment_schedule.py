from datetime import date, datetime

import pytest

from app.services.appointment_schedule_service import build_daily_slots, parse_working_days


def test_default_schedule_generates_thirty_minute_slots():
    slots = build_daily_slots(
        date(2030, 1, 15), set(), datetime(2029, 1, 1),
        workday_start="09:00",
        workday_end="17:00",
        slot_minutes=30,
        working_days="1,2,3,4,6,7",
    )
    assert len(slots) == 16
    assert slots[0] == {"time": "09:00", "status": "available"}
    assert slots[-1] == {"time": "16:30", "status": "available"}


def test_custom_schedule_generates_fifteen_minute_slots_and_marks_occupied():
    occupied = {datetime(2030, 1, 15, 8, 15)}
    slots = build_daily_slots(
        date(2030, 1, 15), occupied, datetime(2029, 1, 1),
        workday_start="08:00",
        workday_end="16:00",
        slot_minutes=15,
        working_days="1,2,3,4,6,7",
    )
    assert len(slots) == 32
    assert slots[1] == {"time": "08:15", "status": "booked"}


def test_non_working_day_has_no_slots():
    slots = build_daily_slots(
        date(2030, 1, 18), set(), datetime(2029, 1, 1),
        workday_start="09:00",
        workday_end="17:00",
        slot_minutes=30,
        working_days="1,2,3,4,6,7",
    )
    assert slots == []


@pytest.mark.parametrize("value", ["", "0,1", "1,8", "abc", "1,,2"])
def test_invalid_working_days_are_rejected(value):
    with pytest.raises(ValueError):
        parse_working_days(value)


def test_slot_generation_rejects_non_divisible_workday():
    with pytest.raises(ValueError):
        build_daily_slots(
            date(2030, 1, 15), set(), datetime(2029, 1, 1),
            workday_start="09:00",
            workday_end="17:00",
            slot_minutes=45,
            working_days="1,2,3,4,6,7",
        )
