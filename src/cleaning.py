"""Reusable cleaning helpers (same logic as section 3 of the notebook)."""
import numpy as np
import pandas as pd

UNIT_TO_SQFT = {
    "Sq. Meter": 10.7639, "Sq. Yards": 9.0, "Acres": 43560.0,
    "Cents": 435.56, "Guntha": 1089.0, "Perch": 272.25, "Grounds": 2400.0,
}


def to_sqft(value):
    """Turn a total_sqft text value into float square feet (NaN if impossible)."""
    if pd.isna(value):
        return np.nan
    try:
        return float(value)
    except ValueError:
        pass
    if "-" in value:
        parts = [p.strip() for p in value.split("-")]
        if len(parts) == 2:
            try:
                return (float(parts[0]) + float(parts[1])) / 2
            except ValueError:
                return np.nan
        return np.nan
    for unit, factor in UNIT_TO_SQFT.items():
        if value.endswith(unit):
            try:
                return float(value[: -len(unit)]) * factor
            except ValueError:
                return np.nan
    return np.nan


def parse_bhk(size):
    """'2 BHK' / '4 Bedroom' -> 2 / 4 (NaN if there is no number)."""
    if pd.isna(size):
        return np.nan
    digits = "".join(ch if ch.isdigit() else " " for ch in size).split()
    return int(digits[0]) if digits else np.nan


def price_per_sqft(price_lakh, sqft):
    """Rupees per square foot from a price in lakh."""
    return price_lakh * 100_000 / sqft
