"""
Code Coverage Test Suite for Visa Application
Lab 6: Code and Branch Coverage Analysis
Student: Suhas S Iyengar (PES1UG24AM291)
Target: >90% Line/Statement Coverage (Achieved: 100%)
"""

import pytest
from visa_application import visa_fee, documents_complete, application_status


# ==============================================================================
# Tests for visa_fee (Aiming for full line coverage)
# ==============================================================================

def test_visa_fee_unknown_type():
    """Test ValueError raised on unrecognized visa type (Line 6)."""
    with pytest.raises(ValueError, match="unknown visa type"):
        visa_fee("diplomatic", 1, "normal", "B")


def test_visa_fee_invalid_negative_entries():
    """Test ValueError raised on negative entries (Line 8)."""
    with pytest.raises(ValueError, match="invalid entries"):
        visa_fee("tourist", -1, "normal", "B")


def test_visa_fee_included_entries_nationality_a():
    """Test nationality group A bonus and extra <= 0 return 0 (Lines 11, 14)."""
    # tourist has 1 included; group A gets +1 = 2 included. entries=2 -> extra=0 -> returns 0
    assert visa_fee("tourist", 2, "normal", "A") == 0


def test_visa_fee_normal_speed_extra_under_five():
    """Test normal speed and extra <= 5 (Lines 18, 23)."""
    # business has 3 included; nationality B. entries=5 -> extra=2. rate=40 -> 2 * 40 = 80
    assert visa_fee("business", 5, "normal", "B") == 80


def test_visa_fee_express_speed_extra_over_five():
    """Test express speed and extra > 5 with surcharge (Lines 16, 20, 22, 23)."""
    # student has 2 included; nationality B. entries=9 -> extra=7 (> 5).
    # express rate = 100 + 20 + 10 = 130. Total = 7 * 130 = 910
    assert visa_fee("student", 9, "express", "B") == 910


# ==============================================================================
# Tests for documents_complete (Aiming for full line coverage)
# ==============================================================================

def test_documents_complete_renewal_true():
    """Test renewal branch with forms >= 1 (Line 28)."""
    assert documents_complete(1, 0, True) is True


def test_documents_complete_insufficient_photos():
    """Test non-renewal with photos < 2 (Line 30)."""
    assert documents_complete(5, 1, False) is False


def test_documents_complete_standard_success():
    """Test non-renewal with sufficient photos and forms >= 3 (Line 31)."""
    assert documents_complete(3, 2, False) is True


# ==============================================================================
# Tests for application_status (Aiming for full line coverage)
# ==============================================================================

def test_application_status_express_open():
    """Test express application status returning 'open' (Lines 36, 42)."""
    # express cutoff = 10; days_left = 15 >= 10 -> 'open'
    assert application_status(15, True, False) == "open"


def test_application_status_peak_closing():
    """Test standard application status with peak season returning 'closing' (Lines 38, 40, 44)."""
    # standard cutoff = 30 + 15 = 45; days_left = 32 >= 30 -> 'closing'
    assert application_status(32, False, True) == "closing"


def test_application_status_closed():
    """Test application status returning 'closed' (Line 45)."""
    # standard cutoff = 30; days_left = 10 < 15 -> 'closed'
    assert application_status(10, False, False) == "closed"
