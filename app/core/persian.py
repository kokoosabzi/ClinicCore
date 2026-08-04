PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")

IRANIAN_HOLIDAYS = {
    "01-01": "نوروز",
    "01-02": "نوروز",
    "01-03": "نوروز",
    "01-04": "نوروز",
    "01-12": "روز جمهوری اسلامی",
    "01-13": "روز طبیعت",
}


def to_persian_digits(value: object) -> str:
    return str(value).translate(PERSIAN_DIGITS)


def format_jalali_placeholder(value: object) -> str:
    return to_persian_digits(value)
