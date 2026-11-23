"""
Test Suite for Visa Application
Lab 6: Code and Branch Coverage Analysis
Student: Suhas S Iyengar (PES1UG24AM291)
Combines initial starter test cases with complete 100% code and branch coverage verification.
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# ==============================================================================
# Starter Example Test Cases
# ==============================================================================

def test_within_included_entries():
    """Starter test: within included entries for tourist visa."""
    assert visa_fee("tourist", 1, "normal", "B") == 0


def test_documents_complete_starter():
    """Starter test: valid documents for non-renewal."""
    assert documents_complete(3, 2, False) is True


# ==============================================================================
# Additional Comprehensive Test Cases (100% Statement & Branch Coverage)
# ==============================================================================

def test_visa_fee_unknown_type():
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "A")


def test_visa_fee_negative_entries():
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -5, "normal", "A")


def test_visa_fee_nationality_a_non_student():
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_visa_fee_nationality_a_student():
    assert visa_fee("student", 2, "normal", "A") == 0


def test_visa_fee_nationality_not_a():
    assert visa_fee("business", 3, "normal", "B") == 0


def test_visa_fee_normal_speed_extra_under_5():
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_visa_fee_express_speed_extra_under_5():
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_visa_fee_normal_speed_extra_over_5():
    assert visa_fee("tourist", 8, "normal", "B") == 420


def test_visa_fee_express_speed_extra_over_5():
    assert visa_fee("tourist", 8, "express", "B") == 910


def test_documents_complete_renewal_true():
    assert documents_complete(1, 0, True) is True


def test_documents_complete_renewal_false():
    assert documents_complete(0, 5, True) is False


def test_documents_complete_not_renewal_photos_insufficient():
    assert documents_complete(5, 1, False) is False


def test_documents_complete_not_renewal_photos_sufficient_forms_insufficient():
    assert documents_complete(2, 2, False) is False


def test_application_status_express_non_peak_open():
    assert application_status(10, True, False) == "open"


def test_application_status_express_non_peak_closing():
    assert application_status(5, True, False) == "closing"


def test_application_status_express_non_peak_closed():
    assert application_status(-6, True, False) == "closed"


def test_application_status_standard_peak_open():
    assert application_status(45, False, True) == "open"


def test_application_status_standard_peak_closing():
    assert application_status(35, False, True) == "closing"


def test_application_status_standard_peak_closed():
    assert application_status(20, False, True) == "closed"
