"""
Branch Coverage Test Suite for Visa Application
Lab 6: Code and Branch Coverage Analysis
Student: Suhas S Iyengar (PES1UG24AM291)
Target: >90% Branch Coverage (Achieved: 100% Line & 100% Branch Coverage)
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# ==============================================================================
# Branch Coverage Tests for visa_fee
# ==============================================================================

def test_visa_fee_branch_unknown_type():
    """Branch: visa_type not in INCLUDED_ENTRIES (True)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("transit", 2, "normal", "A")


def test_visa_fee_branch_negative_entries():
    """Branch: entries < 0 (True)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -5, "normal", "A")


def test_visa_fee_branch_nationality_a_non_student():
    """
    Branch: nationality_group == 'A' and visa_type != 'student' (Both True).
    included becomes 1 + 1 = 2.
    entries = 2 -> extra = 0 -> branch extra <= 0 (True) -> returns 0.
    """
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_visa_fee_branch_nationality_a_student():
    """
    Branch: nationality_group == 'A' (True) and visa_type != 'student' (False).
    included remains 2. entries = 2 -> extra = 0 -> returns 0.
    """
    assert visa_fee("student", 2, "normal", "A") == 0


def test_visa_fee_branch_nationality_not_a():
    """
    Branch: nationality_group != 'A' (False).
    included remains 3 for business.
    entries = 3 -> extra = 0 -> returns 0.
    """
    assert visa_fee("business", 3, "normal", "B") == 0


def test_visa_fee_branch_normal_speed_extra_under_or_equal_5():
    """
    Branch: extra > 0 (False for extra <= 0)
    Branch: speed == 'express' (False -> rate = 40)
    Branch: extra > 5 (False -> rate remains 40)
    tourist (included 1), nationality B. entries = 3 -> extra = 2.
    Fee = 2 * 40 = 80.
    """
    assert visa_fee("tourist", 3, "normal", "B") == 80


def test_visa_fee_branch_express_speed_extra_under_or_equal_5():
    """
    Branch: speed == 'express' (True -> rate = 100)
    Branch: extra > 5 (False -> rate remains 100)
    tourist (included 1), nationality B. entries = 3 -> extra = 2.
    Fee = 2 * 100 = 200.
    """
    assert visa_fee("tourist", 3, "express", "B") == 200


def test_visa_fee_branch_normal_speed_extra_over_5():
    """
    Branch: speed == 'express' (False -> rate = 40)
    Branch: extra > 5 (True -> rate = 40 + 20 = 60)
    Branch inside extra > 5: speed == 'express' (False -> skips line 22, covers 21->23!)
    tourist (included 1), nationality B. entries = 8 -> extra = 7.
    Fee = 7 * 60 = 420.
    """
    assert visa_fee("tourist", 8, "normal", "B") == 420


def test_visa_fee_branch_express_speed_extra_over_5():
    """
    Branch: speed == 'express' (True -> rate = 100)
    Branch: extra > 5 (True -> rate = 100 + 20 = 120)
    Branch inside extra > 5: speed == 'express' (True -> rate = 120 + 10 = 130)
    tourist (included 1), nationality B. entries = 8 -> extra = 7.
    Fee = 7 * 130 = 910.
    """
    assert visa_fee("tourist", 8, "express", "B") == 910


# ==============================================================================
# Branch Coverage Tests for documents_complete
# ==============================================================================

def test_documents_complete_branch_renewal_valid():
    """Branch: is_renewal (True), forms_filed >= 1 (True)."""
    assert documents_complete(1, 0, True) is True


def test_documents_complete_branch_renewal_invalid():
    """Branch: is_renewal (True), forms_filed >= 1 (False)."""
    assert documents_complete(0, 5, True) is False


def test_documents_complete_branch_not_renewal_photos_insufficient():
    """Branch: is_renewal (False), photos < 2 (True)."""
    assert documents_complete(5, 1, False) is False


def test_documents_complete_branch_not_renewal_photos_sufficient_forms_sufficient():
    """Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (True)."""
    assert documents_complete(3, 2, False) is True


def test_documents_complete_branch_not_renewal_photos_sufficient_forms_insufficient():
    """Branch: is_renewal (False), photos < 2 (False), forms_filed >= 3 (False)."""
    assert documents_complete(2, 2, False) is False


# ==============================================================================
# Branch Coverage Tests for application_status
# ==============================================================================

def test_application_status_express_non_peak_open():
    """
    Branch: is_express (True -> cutoff = 10)
    Branch: is_peak_season (False)
    Branch: days_left >= cutoff (True -> 'open')
    """
    assert application_status(10, True, False) == "open"


def test_application_status_express_non_peak_closing():
    """
    Branch: is_express (True -> cutoff = 10)
    Branch: is_peak_season (False)
    Branch: days_left >= cutoff (False)
    Branch: days_left >= cutoff - 15 (True -> 'closing')
    cutoff - 15 = -5. days_left = 5.
    """
    assert application_status(5, True, False) == "closing"


def test_application_status_express_non_peak_closed():
    """
    Branch: is_express (True -> cutoff = 10)
    Branch: is_peak_season (False)
    Branch: days_left >= cutoff - 15 (False -> 'closed')
    cutoff - 15 = -5. days_left = -6.
    """
    assert application_status(-6, True, False) == "closed"


def test_application_status_standard_peak_open():
    """
    Branch: is_express (False -> cutoff = 30)
    Branch: is_peak_season (True -> cutoff = 30 + 15 = 45)
    Branch: days_left >= cutoff (True -> 'open')
    """
    assert application_status(45, False, True) == "open"


def test_application_status_standard_peak_closing():
    """
    Branch: is_express (False -> cutoff = 30)
    Branch: is_peak_season (True -> cutoff = 45)
    Branch: days_left >= cutoff (False)
    Branch: days_left >= cutoff - 15 (True -> 'closing')
    cutoff - 15 = 30. days_left = 35.
    """
    assert application_status(35, False, True) == "closing"


def test_application_status_standard_peak_closed():
    """
    Branch: is_express (False -> cutoff = 30)
    Branch: is_peak_season (True -> cutoff = 45)
    Branch: days_left >= cutoff - 15 (False -> 'closed')
    cutoff - 15 = 30. days_left = 20.
    """
    assert application_status(20, False, True) == "closed"
