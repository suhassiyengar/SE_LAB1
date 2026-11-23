"""
Visa Application Processing Module (Hardened Version)
Lab 7: Fuzzing for Input Validation Bugs
Student: Suhas S Iyengar (PES1UG24AM291)
"""

import math

def parse_application(text):
    """
    Parses a visa application string in the format 'visa_type:entries'.
    Returns (visa_type, entries) if valid, or None if invalid or malformed.
    """
    if not isinstance(text, str):
        return None
    parts = text.split(':')
    if len(parts) != 2:
        return None
    visa, entries = parts
    visa_clean = visa.strip()
    if not visa_clean:
        return None
    try:
        entries_int = int(entries.strip())
        if entries_int < 0:
            return None
        return visa_clean.title(), entries_int
    except (ValueError, TypeError):
        return None

def processing_average(days_csv):
    """
    Computes integer average processing days from a comma-separated string of days.
    Returns 0 if input is invalid or contains no positive integer entries.
    """
    if not isinstance(days_csv, str):
        return 0
    parts = [r.strip() for r in days_csv.split(',') if r.strip()]
    if not parts:
        return 0
    values = []
    for r in parts:
        try:
            val = int(r)
            if val >= 0:
                values.append(val)
            else:
                return 0
        except (ValueError, TypeError):
            return 0
    if not values:
        return 0
    return sum(values) // len(values)

def payable_fee(text):
    """
    Calculates payable fee with 18% tax minus discount: fee * 1.18 - discount.
    Returns rounded float, or 0.0 if input is invalid or values are negative.
    """
    if not isinstance(text, str):
        return 0.0
    parts = text.split('|')
    if len(parts) != 2:
        return 0.0
    try:
        fee_str = parts[0].strip()
        discount_str = parts[1].strip()
        fee = float(fee_str)
        discount = float(discount_str)
        if math.isnan(fee) or math.isinf(fee) or math.isnan(discount) or math.isinf(discount):
            return 0.0
        if fee < 0 or discount < 0:
            return 0.0
        total = fee * 1.18 - discount
        return max(round(total, 2), 0.0)
    except (ValueError, TypeError):
        return 0.0

def main():
    print("==== Running parse_application ====")
    user_input = input("Enter visa type:entries (e.g. tourist:2): ")
    result = parse_application(user_input)
    print("Visa Type and Entries:", result)

    print("\n==== Running processing_average ====")
    user_input = input("Enter processing days as CSV (e.g. 5,10,21): ")
    result = processing_average(user_input)
    print("Average Processing Days:", result)

    print("\n==== Running payable_fee ====")
    user_input = input("Enter fee|discount (e.g. 6000|500): ")
    result = payable_fee(user_input)
    print("Payable Fee:", result)

if __name__ == "__main__":
    main()
