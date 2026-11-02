# BranchCoverageTest_pet_boarding.py
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status

def test_boarding_fee_exceptions():
    with pytest.raises(ValueError, match="unknown pet type"):
        boarding_fee("bird", 5, False)
    with pytest.raises(ValueError, match="invalid days"):
        boarding_fee("dog", -1, False)

def test_boarding_fee_included_and_premium():
    # Dog within included days
    assert boarding_fee("dog", 2, False) == 0
    # Cat premium included (included = 3 + 1 = 4, days = 3 -> extra = -1 <= 0)
    assert boarding_fee("cat", 3, True) == 0
    # Rabbit premium (rabbit ignores is_premium, included = 4, days = 4 -> extra = 0)
    assert boarding_fee("rabbit", 4, True) == 0

def test_boarding_fee_rates_and_tiers():
    # Cat normal extra <= 10 (included 3, days 5 -> extra 2, rate 20 -> 40)
    assert boarding_fee("cat", 5, False) == 40
    # Dog normal extra <= 10 (included 2, days 4 -> extra 2, rate 30 -> 60)
    assert boarding_fee("dog", 4, False) == 60
    # Cat extra > 10 (included 3, days 15 -> extra 12, rate 20+10=30 -> 360)
    assert boarding_fee("cat", 15, False) == 360
    # Dog extra > 10 (included 2, days 15 -> extra 13, rate 30+10+5=45 -> 585)
    assert boarding_fee("dog", 15, False) == 585

def test_admission_ok_branches():
    # is_senior True, vaccinations >= 3
    assert admission_ok(10, 3, True) is True
    # is_senior True, vaccinations < 3
    assert admission_ok(10, 2, True) is False
    # is_senior False, pet_age_years < 1
    assert admission_ok(0.5, 2, False) is False
    # is_senior False, pet_age_years >= 1, vaccinations < 2
    assert admission_ok(2, 1, False) is False
    # is_senior False, pet_age_years >= 1, vaccinations >= 2
    assert admission_ok(2, 2, False) is True

def test_checkout_status_branches():
    # is_long_stay True, is_weekend True, minutes_left >= cutoff (50) -> "open"
    assert checkout_status(55, True, True) == "open"
    # is_long_stay True, is_weekend False, minutes_left >= cutoff (30) -> "open"
    assert checkout_status(35, True, False) == "open"
    # is_long_stay False, is_weekend True, minutes_left >= cutoff - 15 (20 <= minutes < 35) -> "late"
    assert checkout_status(25, False, True) == "late"
    # is_long_stay False, is_weekend False, minutes_left < cutoff - 15 (0 < minutes < 15) -> "closed"
    assert checkout_status(5, False, False) == "closed"
    # Late condition boundary check for long stay
    assert checkout_status(15, True, False) == "late"