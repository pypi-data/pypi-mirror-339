import unittest

from analytics.src.counterparty_info import CounterPartyInfo


class TestCounterPartyInfo(unittest.TestCase):
    def test_initialization(self):
        """Test that the source and target are properly initialized."""
        source = "Bank A"
        target = "Bank B"

        counterparty_info = CounterPartyInfo(source, target)

        self.assertEqual(counterparty_info.source, source)
        self.assertEqual(counterparty_info.target, target)

    def test_empty_initialization(self):
        """Test initialization with empty strings."""
        source = ""
        target = ""

        counterparty_info = CounterPartyInfo(source, target)

        self.assertEqual(counterparty_info.source, source)
        self.assertEqual(counterparty_info.target, target)

    def test_none_initialization(self):
        """Test initialization with None as parameters."""
        source = None
        target = None

        counterparty_info = CounterPartyInfo(source, target)

        self.assertIsNone(counterparty_info.source)
        self.assertIsNone(counterparty_info.target)

    def test_mutability(self):
        """Test that the attributes can be changed after initialization."""
        counterparty_info = CounterPartyInfo(source="Bank A", target="Bank B")

        # Change values
        counterparty_info.source = "Bank X"
        counterparty_info.target = "Bank Y"

        self.assertEqual(counterparty_info.source, "Bank X")
        self.assertEqual(counterparty_info.target, "Bank Y")
