from datetime import date, datetime, timezone

import pytest

from app.services.datetime_service import format_jalali, gregorian_to_jalali, jalali_to_gregorian, parse_jalali


def test_known_new_year_conversion():
    assert gregorian_to_jalali(date(2026, 3, 21)) == (1405, 1, 1)
    assert format_jalali(date(2026, 3, 21)) == "1405/01/01"


def test_round_trip():
    value = date(2026, 10, 5)
    assert jalali_to_gregorian(*gregorian_to_jalali(value)) == value


def test_datetime_uses_calendar_date_only():
    value = datetime(2026, 10, 5, 14, 30, tzinfo=timezone.utc)
    assert format_jalali(value) == "1405/07/13"


def test_invalid_input_is_rejected():
    with pytest.raises(ValueError):
        jalali_to_gregorian(1405, 13, 1)
    with pytest.raises(ValueError):
        parse_jalali("bad-date")
