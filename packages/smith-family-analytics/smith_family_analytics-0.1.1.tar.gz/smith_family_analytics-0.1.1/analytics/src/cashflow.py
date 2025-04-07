from datetime import datetime
from typing import List

import pandas as pd
from pandas import DatetimeIndex

from analytics.src.counterparty_info import CounterPartyInfo
from analytics.src.date_utils import date_range_inclusive


class CashFlow:
    def __init__(self,
                 name: str,
                 counterparties: CounterPartyInfo,
                 start_date: datetime | str,
                 end_date: datetime | str = datetime(2200, 12, 31),
                 frequency: str = 'MS',
                 day_of_month: int = None,
                 amount: float = 0.0):
        if isinstance(start_date, str):
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if isinstance(end_date, str):
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        if day_of_month is None:
            day_of_month = start_date.date().day
        if day_of_month < 1 or day_of_month > 31:
            raise ValueError('day_of_month must be between 1 and 31')
        if end_date < start_date:
            raise ValueError('end_date must be after start_date')
        self.__counterparties__ = counterparties
        self.__start_date__ = start_date
        self.__end_date__ = end_date
        self.__frequency__ = frequency
        self.__day_of_month__ = day_of_month
        self.__amount__ = amount
        self.__cashflow_name__ = name

        self.__settled__: pd.DataFrame = pd.DataFrame(columns=['Date', 'Amount'])
        self.__overridden__: pd.DataFrame = pd.DataFrame(columns=['Date', 'Amount'])
        self.__cancelled__: List[datetime] = []

    @property
    def name(self) -> str:
        return self.__cashflow_name__

    @property
    def counterparties(self) -> CounterPartyInfo:
        return self.__counterparties__

    @property
    def start_date(self) -> datetime:
        return self.__start_date__

    @property
    def end_date(self) -> datetime:
        return self.__end_date__

    @property
    def frequency(self) -> str:
        return self.__frequency__

    @property
    def amount(self) -> float:
        return self.__amount__

    @property
    def day_of_month(self) -> int:
        return self.__day_of_month__

    @property
    def cash_flow_dates(self) -> DatetimeIndex:
        return date_range_inclusive(
            start_date=self.__start_date__,
            end_date=self.__end_date__,
            day_of_month=self.__day_of_month__,
            freq=self.__frequency__)

    def add_settlement(self, date: datetime, amount: float):
        if date not in self.__settled__['Date'].values:
            self.__settled__ = pd.concat([self.__settled__, pd.DataFrame({'Date': date, 'Amount': amount}, index=[0])])
        else:
            self.__settled__.loc[self.__settled__['Date'] == date, 'Amount'] += amount

    def add_overridden(self, date: datetime, amount: float):
        if date not in self.__overridden__['Date'].values:
            self.__overridden__ = pd.concat(
                [self.__overridden__, pd.DataFrame({'Date': date, 'Amount': amount}, index=[0])])
        else:
            self.__overridden__.loc[self.__overridden__['Date'] == date, 'Amount'] += amount

    def add_cancelled(self, date: datetime):
        if date not in self.__cancelled__:
            self.__cancelled__.append(date)

    def cashflows(self, from_date: datetime | str = None) -> pd.DataFrame:

        if isinstance(from_date, str):
            from_date = datetime.strptime(from_date, '%Y-%m-%d')

        df = pd.DataFrame(self.cash_flow_dates, columns=['Date'])
        df['Amount'] = self.amount
        df['Status'] = None

        # Merge in Overrides
        df = df.merge(
            self.__overridden__,
            on="Date",
            how="left",
            suffixes=("", "_overridden"),
        )
        df["Amount"] = df["Amount_overridden"].combine_first(df["Amount"])
        df.drop(columns=["Amount_overridden"], inplace=True)

        # Merge in Settlements

        df = df.merge(
            self.__settled__,
            on="Date",
            how="outer",
            suffixes=("", "_settled"),
        )
        df["Amount"] = df["Amount_settled"].combine_first(df["Amount"])
        df.drop(columns=["Amount_settled"], inplace=True)

        df['Source'] = self.counterparties.source
        df['Target'] = self.counterparties.target
        df['Cashflow'] = self.name
        df.loc[df['Date'].isin(self.__overridden__['Date']), 'Status'] = 'Overridden'
        df.loc[df['Date'].isin(self.__settled__['Date']), 'Status'] = 'Settled'

        # Set Cancellations
        df.loc[df['Date'].isin(self.__cancelled__), 'Status'] = 'Cancelled'
        df.loc[df['Date'].isin(self.__cancelled__), 'Amount'] = 0

        if from_date is not None:
            df = df[df['Date'] >= from_date]

        return df

    def to_dict(self):
        return {
            "cashflow_name": self.__cashflow_name__,
            "counterparties": self.__counterparties__.to_dict(),
            "start_date": self.__start_date__.strftime('%Y-%m-%d'),
            "end_date": self.__end_date__.strftime('%Y-%m-%d'),
            "frequency": self.__frequency__,
            "amount": self.__amount__,
            "day_of_month": self.__day_of_month__,
            "settled": self.__settled__.map(
                lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x
            )
            .to_dict(orient='records'),
            "overridden": self.__overridden__.map(
                lambda x: x.strftime('%Y-%m-%d') if isinstance(x, pd.Timestamp) else x
            )
            .to_dict(orient='records'),
            "cancelled": [c.strftime('%Y-%m-%d') for c in self.__cancelled__]

        }

    @staticmethod
    def from_dict(data):
        """
        Create a CashFlow object from a dictionary representation.
        """
        # Parse start_date and end_date as datetime objects
        start_date = datetime.strptime(data["start_date"], '%Y-%m-%d') if "start_date" in data else None
        end_date = datetime.strptime(data["end_date"], '%Y-%m-%d') if "end_date" in data else None

        # Parse counterparties (assumes it's stored as a dictionary and the corresponding class has a from_dict method)
        counterparties = CounterPartyInfo.from_dict(data["counterparties"])

        # Parse settled and overridden (convert lists of records back into DataFrames)
        settled = pd.DataFrame(data["settled"]) if "settled" in data else None
        overridden = pd.DataFrame(data["overridden"]) if "overridden" in data else None

        # Parse cancelled dates back into datetime objects
        cancelled = [datetime.strptime(c, '%Y-%m-%d') for c in data["cancelled"]] if "cancelled" in data else []

        cflw = CashFlow(
            name=data["cashflow_name"],
            counterparties=counterparties,
            start_date=start_date,
            end_date=end_date,
            frequency=data["frequency"],
            amount=data["amount"],
            day_of_month=data["day_of_month"],
        )

        for idx, row in settled.iterrows():
            cflw.add_settlement(pd.to_datetime(row['Date']), row['Amount'])

        for idx, row in overridden.iterrows():
            cflw.add_overridden(pd.to_datetime(row['Date']), row['Amount'])

        for c in cancelled:
            cflw.add_cancelled(c)
        return cflw
