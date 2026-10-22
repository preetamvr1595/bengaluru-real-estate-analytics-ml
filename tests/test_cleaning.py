import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))   # so "src" can be imported

import pytest
from src.cleaning import parse_bhk, price_per_sqft, to_sqft


def test_plain_number():
    assert to_sqft("1056") == 1056.0


def test_range_is_averaged():
    assert to_sqft("2100 - 2850") == 2475.0


@pytest.mark.parametrize("text,expected", [
    ("1Acres", 43560.0), ("100Sq. Yards", 900.0), ("10Sq. Meter", 107.639),
])
def test_units_converted(text, expected):
    assert to_sqft(text) == pytest.approx(expected)


@pytest.mark.parametrize("bad", ["abc", "12 - x", "1-2-3", None, float("nan")])
def test_bad_values_become_nan(bad):
    assert math.isnan(to_sqft(bad))


def test_parse_bhk():
    assert parse_bhk("2 BHK") == 2
    assert parse_bhk("4 Bedroom") == 4
    assert parse_bhk("1 RK") == 1
    assert math.isnan(parse_bhk(None))


def test_price_per_sqft():
    assert price_per_sqft(50, 1000) == 5000
