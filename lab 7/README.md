# LAB 7: Fuzzing for Input Validation Bugs

- **Student Name:** Suhas S Iyengar
- **SRN:** PES1UG24AM291
- **Course:** Software Engineering Lab (SE_LAB1)
- **Assigned Topic:** Visa Application (`L6_L7_52_visa_application`)

---

## Overview

Fuzz testing (or fuzzing) is a dynamic testing methodology that supplies random, malformed, and unexpected data to software components to uncover input validation bugs, uncaught exceptions, and security vulnerabilities.

This lab uses **Hypothesis**, a property-based fuzz testing library for Python, to test and harden the functions in `visa_application.py`:
1. `parse_application(text)`: Parses `visa_type:entries` into `(visa_type, entries)`
2. `processing_average(days_csv)`: Calculates average processing days from CSV values
3. `payable_fee(text)`: Calculates fee with 18% tax minus discount (`fee * 1.18 - discount`)

---

## Lab Execution & Steps

### Step 1: Installing Dependencies
```bash
pip install hypothesis pytest
```
Dependencies `hypothesis` and `pytest` were installed and verified.

### Step 2: Running Initial Application
```bash
python visa_application.py
```
Outputs on standard input:
- `tourist:2` -> `('Tourist', 2)`
- `5,10,21` -> `12`
- `6000|500` -> `6580.0`

### Step 3: Writing Hypothesis Property-Based Tests
In `test_visa_application.py`, property-based tests were implemented using `@given(st.text() | st.none())` to ensure the functions never crash on unexpected inputs.

### Step 4: Fuzzing the Buggy Application
```bash
pytest test_visa_application.py
```
Hypothesis uncovered multiple critical failure cases:
- `parse_application`: Crashed on `None` (`AttributeError`), empty string `""` (`ValueError: not enough values to unpack`), and `":"` (`ValueError: invalid literal for int() with base 10: ''`).
- `processing_average`: Crashed on `None` (`AttributeError`), empty string `""` (`ValueError`), and `","` (`ZeroDivisionError: integer division or modulo by zero`).
- `payable_fee`: Crashed on `None` (`AttributeError`), empty string `""` (`ValueError: not enough values to unpack`), and `"|"` (`ValueError: could not convert string to float: ''`).

### Step 5: Defensive Code Hardening
The functions in `visa_application.py` were hardened with defensive programming:
- Robust type checking (`isinstance(text, str)`)
- Guarding against missing or extraneous delimiters
- Safe numeric type conversion with explicit exception catching
- Filtering out empty tokens and negative values
- Guarding against zero division
- Handling non-finite numbers (`NaN`, `Infinity`)

### Step 6: Verification with Re-Fuzzing
```bash
pytest test_visa_application.py
```
**Result:** 100% of test cases passed (`3 passed in 2.20s`), validating that the module is completely crash-resilient across hundreds of randomized fuzzing inputs.

---

## Deliverables in this Directory

| File | Description |
|---|---|
| `PES1UG24AM291_Lab7_Report.pdf` | Complete lab report with embedded terminal screenshots and analysis |
| `visa_application.py` | Hardened application code |
| `test_visa_application.py` | Completed Hypothesis property-based fuzz tests |
| `processor.py` | Generic alias for the application script |
| `test_processor.py` | Generic alias for the test suite |
| `screenshots/` | Full-resolution terminal screenshots captured for each step |

---

## Running the Tests

To run the fuzz testing suite:
```bash
pytest test_visa_application.py
```
Or:
```bash
python -m pytest test_processor.py
```
