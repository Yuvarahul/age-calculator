"""Age Calculator (CLI)

Calculates exact age in years, months and days from a date of birth.
Handles leap years and variable month lengths, and validates input.
Usage: python age_calculator.py
"""
from calendar import monthrange
from datetime import date


def days_in_month(year: int, month: int) -> int:
    return monthrange(year, month)[1]


def add_months(birth: date, n: int) -> date:
    """Add n whole months to birth, clamping the day to the month's length
    (e.g. 31 Jan + 1 month -> 28/29 Feb)."""
    total = birth.month - 1 + n
    year = birth.year + total // 12
    month = total % 12 + 1
    return date(year, month, min(birth.day, days_in_month(year, month)))


def calculate_age(birth: date, today: date):
    """Return (years, months, days) between birth and today."""
    months = (today.year - birth.year) * 12 + (today.month - birth.month)
    if add_months(birth, months) > today:
        months -= 1
    anchor = add_months(birth, months)
    days = (today - anchor).days
    return months // 12, months % 12, days


def next_birthday(birth: date, today: date) -> date:
    year = today.year
    while True:
        # 29 Feb birthdays fall on 28 Feb in non-leap years
        day = min(birth.day, days_in_month(year, birth.month))
        candidate = date(year, birth.month, day)
        if candidate >= today:
            return candidate
        year += 1


def parse_dob(text: str, today: date) -> date:
    """Parse DD/MM/YYYY. Raises ValueError with a helpful message."""
    parts = text.strip().replace("-", "/").replace(".", "/").split("/")
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        raise ValueError("Use the format DD/MM/YYYY, for example 15/08/2001.")
    day, month, year = map(int, parts)
    if year < 1900:
        raise ValueError("Enter a year from 1900 onwards.")
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")
    if not 1 <= day <= days_in_month(year, month):
        raise ValueError(
            f"That date does not exist: month {month} of {year} "
            f"has {days_in_month(year, month)} days."
        )
    dob = date(year, month, day)
    if dob > today:
        raise ValueError("Date of birth cannot be in the future.")
    return dob


def plural(n: int, word: str) -> str:
    return f"{n:,} {word}{'' if n == 1 else 's'}"


def main() -> None:
    print("=== Age Calculator ===  (type 'q' to quit)")
    while True:
        text = input("\nEnter date of birth (DD/MM/YYYY): ")
        if text.strip().lower() in ("q", "quit", "exit"):
            print("Goodbye!")
            break
        today = date.today()
        try:
            dob = parse_dob(text, today)
        except ValueError as err:
            print(f"Invalid input: {err}")
            continue

        years, months, days = calculate_age(dob, today)
        nb = next_birthday(dob, today)
        left = (nb - today).days

        print(f"\nAge          : {plural(years, 'year')}, "
              f"{plural(months, 'month')}, {plural(days, 'day')}")
        print(f"Total days   : {plural((today - dob).days, 'day')}")
        print(f"Born on a    : {dob.strftime('%A')}")
        if left == 0:
            print("Next birthday: Today, happy birthday!")
        else:
            print(f"Next birthday: {nb.strftime('%d %B %Y')} (in {plural(left, 'day')})")


if __name__ == "__main__":
    main()