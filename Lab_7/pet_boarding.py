import math


def _to_finite_float(value):
    """Convert text to a finite float, or return None if that is not possible."""
    try:
        number = float(value)
    except (ValueError, TypeError, OverflowError):
        return None
    if not math.isfinite(number):  # rejects nan, inf, -inf
        return None
    return number


def parse_booking(text):
    """Parse 'pet:days' -> (Pet, days). Returns None for invalid input."""
    if not isinstance(text, str):
        return None

    parts = text.split(':')
    if len(parts) != 2:  # no ':' or more than one ':'
        return None

    pet = parts[0].strip()
    days = _to_finite_float(parts[1])

    if not pet:  # empty pet name
        return None
    if days is None or days < 0:  # non-numeric, nan, inf or negative
        return None

    return pet.title(), days


def stay_average(days_csv):
    """Average of comma-separated whole-day stays. Returns None for invalid input."""
    if not isinstance(days_csv, str):
        return None

    values = []
    for part in days_csv.split(','):
        part = part.strip()
        try:
            value = int(part)
        except (ValueError, TypeError):  # '', 'abc', '1.5', huge digit strings
            return None
        if value < 0:
            return None
        values.append(value)

    if not values:  # defensive: never divide by zero
        return None

    return sum(values) / len(values)  # true division (was floor division //)


def payable_fee(text):
    """Parse 'fee|discount' -> fee * 1.18 - discount, floored at 0. None if invalid."""
    if not isinstance(text, str):
        return None

    parts = text.split('|')
    if len(parts) != 2:  # no '|' or more than one '|'
        return None

    fee = _to_finite_float(parts[0])
    discount = _to_finite_float(parts[1])

    if fee is None or discount is None:
        return None
    if fee < 0 or discount < 0:
        return None

    total = fee * 1.18 - discount
    if not math.isfinite(total):  # e.g. fee so large that it overflows to inf
        return None

    return max(total, 0)


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter pet:days (e.g. dog:5): ")
    result = parse_booking(user_input)
    print("Pet and Days:", result if result is not None else "Invalid input")

    print("\n==== Running stay_average ====")
    user_input = input("Enter stay lengths in days as CSV (e.g. 2,5,7): ")
    result = stay_average(user_input)
    print("Average Stay:", result if result is not None else "Invalid input")

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 1500|100): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()