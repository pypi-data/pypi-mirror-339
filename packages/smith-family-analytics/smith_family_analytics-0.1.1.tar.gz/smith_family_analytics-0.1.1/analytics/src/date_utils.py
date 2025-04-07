from datetime import datetime

import pandas as pd


def date_range_inclusive(start_date: datetime, end_date: datetime, day_of_month: int = 1, freq: str = 'MS'):
    if day_of_month < 1 or day_of_month > 31:
        raise ValueError('day_of_month must be between 1 and 31')
    if end_date < start_date:
        raise ValueError('end_date must be after start_date')

    date_range = pd.date_range(
        start=start_date,
        end=end_date,
        freq=freq
    ) + pd.offsets.Day(day_of_month - 1)

    # Ensure the start_date is included
    if start_date not in date_range:
        date_range = pd.concat(
            [pd.Series([start_date]), pd.Series(date_range)]).drop_duplicates().sort_values().reset_index(
            drop=True)
    return date_range