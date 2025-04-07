import pytest
import pandas as pd
from datetime import datetime

from analytics.src.cashflow import CashFlow
from analytics.src.counterparty_info import CounterPartyInfo
from analytics.src.date_utils import date_range_inclusive


@pytest.fixture
def sample_cashflow():
    # A sample `CashFlow` object to use across tests
    return CashFlow(
        name="Test CashFlow",
        counterparties=CounterPartyInfo("source","target"),
        start_date=datetime(2023, 1, 1),
        end_date=datetime(2023, 6, 30),
        amount=1000
    )



class TestCashFlow:
    def setup_method(self):
        self.counterparties = CounterPartyInfo("source","target")

    def test_default_arguments(self):
        """Test to verify default arguments are handled correctly."""
        start_date = datetime(2023, 1, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date)

        assert cash_flow.start_date == start_date
        assert cash_flow.end_date == datetime(2200, 12, 31)
        assert cash_flow.frequency == 'MS'

        # Verify that correct cash flow dates are generated.
        expected_dates = pd.date_range(start=start_date, end=datetime(2200, 12, 31), freq='MS') \
                         + pd.offsets.Day(0)
        assert all(cash_flow.cash_flow_dates == expected_dates)

    def test_custom_end_date(self):
        """Test when a custom end date is provided."""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 6, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date)

        assert cash_flow.start_date == start_date
        assert cash_flow.end_date == end_date

        expected_dates = date_range_inclusive(start_date=cash_flow.start_date,
                                              end_date=cash_flow.end_date,
                                              day_of_month=1,
                                              freq=cash_flow.frequency)
        assert all(cash_flow.cash_flow_dates == expected_dates)

    def test_default_arguments_as_str(self):
        """Test to verify default arguments are handled correctly."""
        start_date = '2023-01-01'
        end_date = '2200-12-31'

        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date)

        assert cash_flow.start_date == datetime(2023, 1, 1)
        assert cash_flow.end_date == datetime(2200, 12, 31)
        assert cash_flow.frequency == 'MS'

        # Verify that correct cash flow dates are generated.
        expected_dates = date_range_inclusive(start_date=cash_flow.start_date,
                                              end_date=cash_flow.end_date,day_of_month=1,
                                              freq=cash_flow.frequency)
        assert all(cash_flow.cash_flow_dates == expected_dates)

    def test_custom_day_of_month(self):
        """Test the handling of custom day_of_month."""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 4, 1)
        day_of_month = 15
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date, day_of_month=day_of_month)

        assert cash_flow.start_date == start_date
        assert cash_flow.end_date == end_date

        # Verify that cash flow generates dates with the correct day_of_month.
        expected_dates = date_range_inclusive(start_date, end_date, day_of_month=day_of_month)
        assert all(cash_flow.cash_flow_dates == expected_dates)

    def test_invalid_day_of_month(self):
        """Test for ValueError when day_of_month is invalid (e.g., <1 or >31)."""
        start_date = datetime(2023, 1, 1)

        with pytest.raises(ValueError):
            CashFlow("test",self.counterparties, start_date=start_date, day_of_month=0)  # Invalid day_of_month

        with pytest.raises(ValueError):
            CashFlow("test",self.counterparties, start_date=start_date, day_of_month=32)  # Invalid day_of_month

    def test_invalid_end_date_less_than_start_date(self):
        """Test for ValueError when day_of_month is invalid (e.g., <1 or >31)."""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2022, 12, 31)

        with pytest.raises(ValueError):
            CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date)  # Invalid day_of_month

    def test_large_date_range(self):
        """Test the generation of cash flow dates over a very large range."""
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2025, 12, 31)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date)

        assert cash_flow.start_date == start_date
        assert cash_flow.end_date == end_date

        expected_dates = pd.date_range(start=start_date, end=end_date, freq='MS') + pd.offsets.Day(0)
        assert all(cash_flow.cash_flow_dates == expected_dates)
        assert len(cash_flow.cash_flow_dates) == len(expected_dates)

    def test_edge_case_end_of_month(self):
        """Test for cash flows generating dates at the end of each month."""
        start_date = datetime(2023, 2, 28)
        end_date = datetime(2023, 6, 28)
        day_of_month = 28
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date, day_of_month=day_of_month)

        assert cash_flow.start_date == start_date
        assert cash_flow.end_date == end_date

        # Since setting day_of_month=28 in February might go beyond the range, verify edge handling
        expected_dates = date_range_inclusive(cash_flow.start_date, cash_flow.end_date, day_of_month=cash_flow.day_of_month)
        assert all(cash_flow.cash_flow_dates == expected_dates)

    def test_amount(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 6, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date,amount=1000)

        assert cash_flow.amount == 1000

    def test_name(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 6, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date,amount=1000)

        assert cash_flow.name == 'test'

    def test_day_of_month(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 6, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date,amount=1000, day_of_month=15)

        assert cash_flow.day_of_month == 15

    def test_counterparties(self):
        start_date = datetime(2023, 1, 1)
        end_date = datetime(2023, 6, 1)
        cash_flow = CashFlow("test",self.counterparties, start_date=start_date, end_date=end_date,amount=1000)

        assert cash_flow.counterparties.source == 'source'
        assert cash_flow.counterparties.target == 'target'

    def test_cashflows_valid_dates(self):
        """
        Test the cashflows method generates the correct cash flow schedule for valid input.
        """
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 3, 15)
        cashflow = CashFlow(
            "Test",
            self.counterparties,
            start_date=start_date,
            end_date=end_date,
            frequency="MS",
            amount=100,
            day_of_month=15
        )
        result = cashflow.cashflows()
        assert len(result) == 3, "Expected 3 cash flow entries for a monthly frequency"
        assert pd.to_datetime(result["Date"].values[0]) == datetime(2023, 1, 15), "First entry date should match 15th Jan 2023"
        assert pd.to_datetime(result["Date"].values[-1]) == datetime(2023, 3, 15), "Last entry date should match 15th Mar 2023"
        assert all([entry == 100 for entry in result['Amount']]), "Every entry should have the correct amount"

    def test_cashflows_edge_case_end_of_month(self):
        """
        Test the cashflows method when the start date is at the end of the month.
        """
        start_date = datetime(2023, 1, 15)
        end_date = datetime(2023, 3, 15)
        cashflow = CashFlow(
            "End of Month Test",
            self.counterparties,
            start_date=start_date,
            end_date=end_date,
            frequency="MS",
            amount=200,
            day_of_month=15
        )
        result = cashflow.cashflows()
        assert len(result) == 3, "Expected 3 cash flow entries for a monthly frequency"
        assert all(pd.to_datetime(entry).day == 15 for entry in result['Date']), "All cash flow dates should fall on the 31st"


