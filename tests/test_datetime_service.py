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
        jalali_to_gregorian(1404, 12, 30)
    with pytest.raises(ValueError):
        parse_jalali("bad-date")


def test_format_current_datetime_uses_timezone_and_calendar():
    from app.services.datetime_service import format_current_datetime

    now = datetime(2026, 3, 21, 20, 30, 5, tzinfo=timezone.utc)
    assert format_current_datetime("Asia/Tehran", "jalali", "YYYY/MM/DD", "24", True, now) == "۱۴۰۵/۰۱/۰۲ ۰۰:۰۰:۰۵"
    assert format_current_datetime("Asia/Tehran", "gregorian", "YYYY-MM-DD", "12", False, now) == "۲۰۲۶-۰۳-۲۲ ۱۲:۰۰ ق.ظ"
    assert format_current_datetime("Asia/Tehran", "gregorian", "YYYY-MM-DD", "24", True, now) == "۲۰۲۶-۰۳-۲۲ ۰۰:۰۰:۰۵"


def test_parse_configured_jalali_datetime():
    from app.services.datetime_service import parse_configured_datetime

    assert parse_configured_datetime("1405/01/01 12:30", "jalali").isoformat() == "2026-03-21T12:30:00"


def test_parse_configured_gregorian_datetime():
    from app.services.datetime_service import parse_configured_datetime

    assert parse_configured_datetime("2026/03/21 12:30", "gregorian").isoformat() == "2026-03-21T12:30:00"


def test_format_configured_datetime_12_hour_seconds_order():
    from app.services.datetime_service import format_configured_datetime

    value = datetime(2026, 3, 21, 13, 5, 9)
    assert format_configured_datetime(value, "gregorian", "YYYY/MM/DD", "12", True) == "۲۰۲۶/۰۳/۲۱ ۰۱:۰۵:۰۹ ب.ظ"
