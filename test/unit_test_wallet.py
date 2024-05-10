import unittest
import os
import tempfile
from unittest.mock import patch, mock_open
import pandas as pd
from main import FinanceManager


class TestFinanceManager(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.filename = self.temp_file.name
        self.manager = FinanceManager(self.filename)

    def tearDown(self):
        os.remove(self.temp_file.name)

    def test_load_data(self):
        self.assertEqual(len(self.manager.df), 0)

        mock_data = (
            "Дата:2023-05-01\n"
            "Категория:Доход\n"
            "Сумма:1000\n"
            "Описание:Зарплата\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_data)):
            self.manager.load_data()
            self.assertEqual(len(self.manager.df), 1)

    def test_add_entry(self):
        date = "2023-06-01"
        category = "Доход"
        amount = 2000
        description = "Фриланс"

        self.manager.add_entry(date, category, amount, description)
        self.assertEqual(len(self.manager.df), 1)
        self.assertEqual(self.manager.df.iloc[0]["Date"].date(), pd.to_datetime(date).date())
        self.assertEqual(self.manager.df.iloc[0]["Category"], category)
        self.assertEqual(self.manager.df.iloc[0]["Amount"], amount)
        self.assertEqual(self.manager.df.iloc[0]["Description"], description)

    def test_edit_record(self):
        mock_data = (
            "Дата:2023-05-01\n"
            "Категория:Доход\n"
            "Сумма:1000\n"
            "Описание:Зарплата\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_data)):
            self.manager.load_data()

        new_date = "2023-05-03"
        new_category = "Расход"
        new_amount = 1500
        new_description = "Аренда"
        index = 0

        self.manager.edit_record(index, new_date, new_category, new_amount, new_description)
        self.assertEqual(self.manager.df.iloc[index]["Date"].date(), pd.to_datetime(new_date).date())
        self.assertEqual(self.manager.df.iloc[index]["Category"], new_category)
        self.assertEqual(self.manager.df.iloc[index]["Amount"], new_amount)
        self.assertEqual(self.manager.df.iloc[index]["Description"], new_description)

    def test_show_wallet_balance(self):
        mock_data = (
            "Дата:2023-05-01\n"
            "Категория:Доход\n"
            "Сумма:1000\n"
            "Описание:Зарплата\n"

            "Дата:2023-05-02\n"
            "Категория:Расход\n"
            "Сумма:500\n"
            "Описание:Покупки\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_data)):
            self.manager.load_data()

        expected_balance, expected_income, expected_expenses = 500, 1000, 500
        balance, income, expenses = self.manager.show_wallet_balance()

        self.assertEqual(balance, expected_balance)
        self.assertEqual(income, expected_income)
        self.assertEqual(expenses, expected_expenses)

    def test_search_records(self):
        mock_data = (
            "Дата:2023-05-01\n"
            "Категория:Доход\n"
            "Сумма:1000\n"
            "Описание:Зарплата\n"

            "Дата:2023-05-02\n"
            "Категория:Расход\n"
            "Сумма:500\n"
            "Описание:Покупки\n"

            "Дата:2023-05-03\n"
            "Категория:Доход\n"
            "Сумма:1500\n"
            "Описание:Фриланс\n"
        )

        with patch("builtins.open", mock_open(read_data=mock_data)):
            self.manager.load_data()

        category = "Доход"
        expected_df = pd.DataFrame({"Date": [pd.to_datetime("2023-05-01"), pd.to_datetime("2023-05-03")],
                                    "Category": ["Доход", "Доход"],
                                    "Amount": [1000, 1500],
                                    "Description": ["Зарплата", "Фриланс"]})
        result_df = self.manager.search_records(category=category)
        self.assertTrue(result_df.equals(expected_df))


if __name__ == "__main__":
    unittest.main()
