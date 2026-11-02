# CodeCoverageTest_pet_boarding.py
import pytest
from pet_boarding import boarding_fee, admission_ok, checkout_status

def test_boarding_fee_basic():
    assert boarding_fee("dog", 1, False) == 0
    assert boarding_fee("cat", 5, False) == 40

def test_admission_basic():
    assert admission_ok(4, 2, False) is True
    assert admission_ok(0.5, 2, False) is False

def test_checkout_basic():
    assert checkout_status(20, False, False) == "open"
    assert checkout_status(5, False, False) == "closed"