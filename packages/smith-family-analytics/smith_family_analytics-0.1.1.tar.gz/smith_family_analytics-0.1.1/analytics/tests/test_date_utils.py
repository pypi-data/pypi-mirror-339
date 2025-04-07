import pytest
from datetime import datetime
import pandas as pd

from analytics.src.date_utils import date_range_inclusive


def test_valid_date_range():
    # Valid case: Start and end dates within the same year at the 1st of each month
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 6, 1)
    result = date_range_inclusive(start_date, end_date)
    expected = pd.concat(
        [pd.Series([start_date]), pd.Series(result)]).drop_duplicates().sort_values().reset_index(
        drop=True)
    assert all(expected == result)


def test_day_of_month_adjustment():
    # Ensure the `day_of_month` parameter is correctly applied
    start_date = datetime(2023, 1, 15)
    end_date = datetime(2023, 6, 15)
    day_of_month = 15

    result = date_range_inclusive(start_date, end_date, day_of_month=day_of_month)
    expected = pd.concat(
        [pd.Series([start_date]), pd.Series(result)]).drop_duplicates().sort_values().reset_index(
        drop=True)
    assert all(expected == result)


def test_include_start_date():
    # Test that the start_date is always included
    start_date = datetime(2023, 1, 10)
    end_date = datetime(2023, 6, 10)
    day_of_month = 10
    result = date_range_inclusive(start_date, end_date, day_of_month)
    assert start_date in [pd.to_datetime(r) for r in result]


def test_invalid_day_of_month_below_range():
    # Check that ValueError is raised for day_of_month < 1
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 6, 1)
    with pytest.raises(ValueError, match='day_of_month must be between 1 and 31'):
        date_range_inclusive(start_date, end_date, day_of_month=0)


def test_invalid_day_of_month_above_range():
    # Check that ValueError is raised for day_of_month > 31
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 6, 1)
    with pytest.raises(ValueError, match='day_of_month must be between 1 and 31'):
        date_range_inclusive(start_date, end_date, day_of_month=32)


def test_end_date_before_start_date():
    # Check that ValueError is raised if end_date < start_date
    start_date = datetime(2023, 6, 1)
    end_date = datetime(2023, 1, 1)
    with pytest.raises(ValueError, match='end_date must be after start_date'):
        date_range_inclusive(start_date, end_date)


def test_single_date_range():
    # Test the edge case where start_date == end_date
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 1, 1)
    expected = pd.date_range(start=start_date, end=end_date, freq='MS') + pd.offsets.Day(0)
    result = date_range_inclusive(start_date, end_date)
    pd.testing.assert_index_equal(result, expected)
