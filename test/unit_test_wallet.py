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
        mock_data = "Date,Category,Amount,Description\n"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            # Act
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                self.manager.show_wallet_balance()
                output = mock_stdout.getvalue()

            # Assert
            expected_output = "Баланс: 0\nДоходы: 0\nРасходы: 0\n"
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
        df = pd.read_csv(self.filename, names=["Date", "Category", "Amount", "Description"])
        df["Date"] = pd.to_datetime(df["Date"])  # Convert "Date" column to datetime
        self.assertEqual(len(df), 1)
        self.assertTrue((df["Date"].dt.date == pd.Timestamp(date).date()).any())

    def test_edit_record(self):
        # Arrange
        mock_data = "Date,Category,Amount,Description\n2024-05-01,Income,1000,Salary"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            new_date = "2024-05-02"
            new_category = "Expense"
            new_amount = 500
            new_description = "Rent"

            # Act
            self.manager.edit_record(0, new_date, new_category, new_amount, new_description)

            # Assert
            df = pd.read_csv(self.filename)
            df["Date"] = pd.to_datetime(df["Date"])  # Convert "Date" column to datetime
            self.assertEqual(len(df), 1)
            expected_date = pd.Timestamp(2024, 5, 2)  # Update the expected date
            self.assertEqual(df.iloc[0]["Date"], expected_date)
            self.assertEqual(df.iloc[0]["Category"], new_category)
            self.assertEqual(df.iloc[0]["Amount"], new_amount)
            self.assertEqual(df.iloc[0]["Description"], new_description)

    def test_search_records(self):
        # Arrange
        mock_data = "Date,Category,Amount,Description\n2024-05-01,Income,1000,Salary\n2024-05-02,Expense,500,Rent\n2024-05-03,Income,2000,Freelance work"
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
