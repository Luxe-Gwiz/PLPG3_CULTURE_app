
MAX_SHORT_TEXT = 120
MAX_LONG_TEXT = 1000
DATE_MESSAGE = "Date must use the format YYYY-MM-DD (for example 2026-12-05)."
DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def clean_text(value, field, max_length=MAX_SHORT_TEXT):
    if value is None:
        raise ValueError(f"{field} is required.")
    text = " ".join(str(value).split())
    if not text:
        raise ValueError(f"{field} cannot be empty.")
    if len(text) > max_length:
        raise ValueError(f"{field} must be {max_length} characters or fewer.")
    return text


def is_leap_year(year):
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    return year % 4 == 0


def clean_date(value):
    text = (value or "").strip()
    if not text:
        raise ValueError("Event date is required.")
    parts = text.split("-")
    if len(parts) != 3:
        raise ValueError(DATE_MESSAGE)
    year_text = parts[0]
    month_text = parts[1]
    day_text = parts[2]
    if not (year_text.isdigit() and month_text.isdigit() and day_text.isdigit()):
        raise ValueError(DATE_MESSAGE)
    if len(year_text) != 4 or int(year_text) < 1:
        raise ValueError(DATE_MESSAGE)
    year = int(year_text)
    month = int(month_text)
    day = int(day_text)
    if month < 1 or month > 12:
        raise ValueError(DATE_MESSAGE)
    limit = DAYS_IN_MONTH[month - 1]
    if month == 2 and is_leap_year(year):
        limit = 29
    if day < 1 or day > limit:
        raise ValueError(DATE_MESSAGE)
    return f"{year:04d}-{month:02d}-{day:02d}"


def clean_record_id(value):
    text = str(value).strip()
    try:
        number = int(text)
    except ValueError:
        raise ValueError("Record ID must be a whole number.")
    if number <= 0:
        raise ValueError("Record ID must be greater than zero.")
    return number
