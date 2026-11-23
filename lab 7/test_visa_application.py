"""
Hypothesis Property-Based Fuzz Testing Suite
Lab 7: Fuzzing for Input Validation Bugs
Student: Suhas S Iyengar (PES1UG24AM291)
"""

from hypothesis import given, strategies as st
from visa_application import parse_application, processing_average, payable_fee

@given(st.text() | st.none())
def test_parse_application_no_crash(s):
    """
    Property: parse_application should never raise unhandled exceptions
    regardless of input string or None.
    """
    try:
        parse_application(s)
    except Exception as e:
        assert False, f"parse_application crashed with: {e}"

@given(st.text() | st.none())
def test_processing_average_no_crash(s):
    """
    Property: processing_average should never raise unhandled exceptions
    (e.g., ValueError, ZeroDivisionError, AttributeError).
    """
    try:
        processing_average(s)
    except Exception as e:
        assert False, f"processing_average crashed with: {e}"

@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    """
    Property: payable_fee should gracefully handle all malformed inputs
    without raising unhandled exceptions.
    """
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {e}"
