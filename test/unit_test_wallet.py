import io
import unittest
import os
import pandas as pd
from unittest.mock import patch, mock_open
from main import FinanceManager


class TestFinanceManager(unittest.TestCase):
    def setUp(self):
        self.filename = "test_finance_records.csv"
        self.manager = FinanceManager(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_show_wallet_balance(self):
        # Arrange
        mock_data = (
            "Date,Category,Amount,Description\n"
            "2024-05-01,Income,1000,Salary\n"
            "2024-05-02,Expense,500,Rent"
        )
        with patch("builtins.open", mock_open(read_data=mock_data)):
            # Act
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                self.manager.show_wallet_balance()
                output = mock_stdout.getvalue()

            # Assert
            expected_output = (
                "Баланс: 500.0\n"
                "Доходы: 1000.0\n"
                "Расходы: 500.0\n"
            )
            self.assertEqual(output, expected_output)

    def test_add_record(self):
        # Arrange
        date = "2024-05-03"
        category = "Income"
        amount = 2000
        description = "Freelance work"

        # Act
        self.manager.add_record(date, category, amount, description)

        # Assert
        df = pd.read_csv(self.filename)
        self.assertEqual(len(df), 3)  # Adjusted to expect 3 records
        self.assertTrue((df["Date"] == pd.Timestamp(date)).any())  # Check if the added record exists

    def test_edit_record(self):
        # Arrange
        mock_data = (
            "Date,Category,Amount,Description\n"
            "2024-05-01,Income,1000,Salary"
        )
        with patch("builtins.open", mock_open(read_data=mock_data)):
            new_date = pd.Timestamp("2024-05-02")  # Convert to Pandas Timestamp object
            new_category = "Expense"
            new_amount = 500
            new_description = "Rent"

            # Act
            self.manager.edit_record(0, new_date, new_category, new_amount, new_description)

            # Assert
            df = pd.read_csv(self.filename)
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]["Date"], new_date)  # Compare with Timestamp object
            self.assertEqual(df.iloc[0]["Category"], new_category)
            self.assertEqual(df.iloc[0]["Amount"], new_amount)
            self.assertEqual(df.iloc[0]["Description"], new_description)

    def test_search_records(self):
        # Arrange
        mock_data = (
            "Date,Category,Amount,Description\n"
            "2024-05-01,Income,1000,Salary\n"
            "2024-05-02,Expense,500,Rent\n"
            "2024-05-03,Income,2000,Freelance work"
        )
        with patch("builtins.open", mock_open(read_data=mock_data)):
            # Act
            income_records = self.manager.search_records(category="Income")
            date_records = self.manager.search_records(date="2024-05-02")
            amount_records = self.manager.search_records(amount=2000)

            # Assert
            self.assertEqual(len(income_records), 2)
            self.assertEqual(len(date_records), 1)
            self.assertEqual(len(amount_records), 1)
            self.assertEqual(amount_records.iloc[0]["Description"], "Freelance work")


if __name__ == "__main__":
    unittest.main()
