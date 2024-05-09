import io
import unittest
import os
import pandas as pd
from unittest.mock import patch, mock_open
from main import FinanceManager


class TestFinanceManager(unittest.TestCase):
    """
    Класс, содержащий юнит-тесты для проверки функционала класса FinanceManager.
    """

    def setUp(self):
        """
        Подготовка тестовой среды перед запуском каждого теста.
        """
        self.filename = "test_finance_records.csv"
        self.manager = FinanceManager(self.filename)

    def tearDown(self):
        """
        Очистка тестовой среды после выполнения каждого теста.
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_show_wallet_balance(self):
        """
        Тестирование функции вывода баланса кошелька.
        """
        # Arrange
        mock_data = "Date,Category,Amount,Description\n"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            # Act
            with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
                self.manager.show_wallet_balance()
                output = mock_stdout.getvalue()

            # Assert
            expected_output = (
                "Баланс: 0\n"
                "Доходы: 0\n"
                "Расходы: 0\n"
            )
            self.assertEqual(output, expected_output)

    def test_add_record(self):
        """
        Тестирование функции добавления записи о финансовой операции.
        """
        # Arrange
        date = "2024-05-03"
        category = "Income"
        amount = 2000
        description = "Freelance work"

        # Act
        self.manager.add_record(date, category, amount, description)

        # Assert
        df = pd.read_csv(self.filename, names=["Date", "Category", "Amount", "Description"])
        df["Date"] = pd.to_datetime(df["Date"])  # Преобразование столбца "Date" в формат datetime
        self.assertEqual(len(df), 1)
        self.assertTrue((df["Date"].dt.date == pd.Timestamp(date).date()).any())

    def test_edit_record(self):
        """
        Тестирование функции редактирования записи о финансовой операции.
        """
        # Устанавливаем начальные данные для теста
        mock_data = "Date,Category,Amount,Description\n2024-05-01,Income,1000,Salary"
        with patch("builtins.open", mock_open(read_data=mock_data)):
            new_date = "2024-05-02"
            new_category = "Expense"
            new_amount = 500
            new_description = "Rent"

            # Действие: вызываем функцию редактирования записи
            self.manager.edit_record(0, new_date, new_category, new_amount, new_description)

            # Получаем данные из CSV файла после редактирования
            df = pd.read_csv(self.filename)
            df["Date"] = pd.to_datetime(df["Date"])  # Преобразуем столбец "Date" в формат datetime

            # Проверяем ожидаемый результат после редактирования записи
            self.assertEqual(len(df), 1)
            self.assertEqual(df.iloc[0]["Date"], pd.Timestamp(new_date))
            self.assertEqual(df.iloc[0]["Category"], new_category)
            self.assertEqual(df.iloc[0]["Amount"], new_amount)
            self.assertEqual(df.iloc[0]["Description"], new_description)

    def test_search_records(self):
        """
        Тестирование функции поиска записей в журнале финансовых операций.
        """
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
