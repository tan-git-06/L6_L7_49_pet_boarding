import math

from hypothesis import given, settings, strategies as st

from pet_boarding import parse_booking, stay_average, payable_fee


# ---------------------------------------------------------------------------
# Part 1: "no crash" fuzz tests (as given in the handout, bodies completed)
# Inputs: arbitrary Unicode text OR None
# ---------------------------------------------------------------------------

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):
    try:
        parse_booking(s)
    except Exception as e:
        assert False, f"parse_booking crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_stay_average_no_crash(s):
    try:
        stay_average(s)
    except Exception as e:
        assert False, f"stay_average crashed with: {type(e).__name__}: {e}"


@given(st.text() | st.none())
def test_payable_fee_no_crash(s):
    try:
        payable_fee(s)
    except Exception as e:
        assert False, f"payable_fee crashed with: {type(e).__name__}: {e}"


# ---------------------------------------------------------------------------
# Part 2: structured fuzzing - well-formed inputs built from valid pieces,
# so Hypothesis reaches the "happy path" and checks correctness properties
# ---------------------------------------------------------------------------

pet_names = st.text(
    alphabet=st.characters(whitelist_categories=("L",)), min_size=1, max_size=20
).filter(lambda p: p.strip() != "")


@given(pet_names, st.integers(min_value=0, max_value=10_000))
def test_parse_booking_valid(pet, days):
    result = parse_booking(f"{pet}:{days}")
    assert result is not None
    name, d = result
    assert name == pet.strip().title()
    assert d == float(days)


@given(st.lists(st.integers(min_value=0, max_value=10_000), min_size=1, max_size=50))
def test_stay_average_valid(values):
    csv = ",".join(str(v) for v in values)
    result = stay_average(csv)
    assert result is not None
    # An average must lie between the smallest and largest value
    assert min(values) <= result <= max(values)
    # ...and must be mathematically correct (no silent floor-division)
    assert math.isclose(result, sum(values) / len(values))


@given(
    st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=1e9, allow_nan=False, allow_infinity=False),
)
def test_payable_fee_valid(fee, discount):
    result = payable_fee(f"{fee}|{discount}")
    assert result is not None
    assert math.isfinite(result)
    assert result >= 0  # fee can never be negative


# ---------------------------------------------------------------------------
# Part 3: explicit regression tests for the edge cases fuzzing discovered
# ---------------------------------------------------------------------------

def test_regression_edge_cases():
    # parse_booking
    assert parse_booking(None) is None
    assert parse_booking("dog") is None            # missing ':'
    assert parse_booking("dog:5:6") is None        # too many ':'
    assert parse_booking(":5") is None             # empty pet name
    assert parse_booking("dog:abc") is None        # non-numeric days
    assert parse_booking("dog:nan") is None        # NaN days
    assert parse_booking("dog:inf") is None        # infinite days
    assert parse_booking("dog:-3") is None         # negative days
    assert parse_booking(" dog : 5 ") == ("Dog", 5.0)

    # stay_average
    assert stay_average(None) is None
    assert stay_average("") is None                # empty string
    assert stay_average("2,,5") is None            # empty element
    assert stay_average("a,b") is None             # non-numeric
    assert stay_average("-1,2") is None            # negative stay
    assert stay_average("2,5,6") == 13 / 3         # true average, not 4

    # payable_fee
    assert payable_fee(None) is None
    assert payable_fee("1500") is None             # missing '|'
    assert payable_fee("1|2|3") is None            # too many '|'
    assert payable_fee("abc|1") is None            # non-numeric
    assert payable_fee("nan|0") is None            # NaN
    assert payable_fee("inf|inf") is None          # inf - inf = NaN
    assert payable_fee("-100|0") is None           # negative fee
    assert payable_fee("100|-5") is None           # negative discount
    assert payable_fee("100|1000") == 0            # discount larger than fee