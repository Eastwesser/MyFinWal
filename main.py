import csv
import os
from typing import Optional
import pandas as pd


class FinanceManager:
    """Класс, представляющий финансовый менеджер для обработки финансовых записей."""

    def __init__(self, filename: str):
        """
        Инициализация FinanceManager.

        Args:
            filename (str): Имя файла для хранения финансовых записей.
        """
        self.filename = filename

    def show_wallet_balance(self) -> None:
        """
        Показываем текущий баланс кошелька.

        Выводим общий баланс, общий доход и общие расходы.
        """
        try:
            df = pd.read_csv(self.filename, parse_dates=['Date'])
            total_income = df[df['Category'] == 'Доход']['Amount'].sum()
            total_expense = df[df['Category'] == 'Расход']['Amount'].sum()
            balance = total_income - total_expense
            print("Баланс:", balance)
            print("Доходы:", total_income)
            print("Расходы:", total_expense)
        except Exception as e:
            print("Ошибка при чтении данных:", e)

    def add_record(self, date: str, category: str, amount: float, description: str) -> None:
        """
        Добавляем новую финансовую запись.

        Args:
            date (str): Дата записи.
            category (str): Категория записи (Доход или Расход).
            amount (float): Сумма записи.
            description (str): Описание записи.
        """
        try:
            with open(self.filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([date, category, amount, description])
            print("Запись добавлена успешно.")
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def edit_record(self, record_id: int, new_date: str, new_category: str, new_amount: float,
                    new_description: str) -> None:
        """Редактируем существующую финансовую запись.

        Args:
            record_id (int): Индекс записи для редактирования.
            new_date (str): Новая дата записи.
            new_category (str): Новая категория записи.
            new_amount (float): Новая сумма записи.
            new_description (str): Новое описание записи.
        """
        try:
            df = pd.read_csv(self.filename, parse_dates=['Date'])
            df['Date'] = pd.to_datetime(df['Date'])  # Convert "Date" column to datetime

            if record_id < len(df):
                df.at[record_id, 'Date'] = pd.to_datetime(new_date)
                df.at[record_id, 'Category'] = new_category
                df.at[record_id, 'Amount'] = new_amount
                df.at[record_id, 'Description'] = new_description

                df.to_csv(self.filename, index=False)
                print("Запись успешно отредактирована.")
            else:
                print("Запись с таким индексом не найдена.")
        except Exception as e:
            print("Ошибка при редактировании записи:", e)

    def search_records(self, category: Optional[str] = None, date: Optional[str] = None,
                       amount: Optional[float] = None) -> pd.DataFrame:
        """
        Поиск финансовых записей по заданным критериям.

        Args:
            category (str, optional): Категория для поиска.
            date (str, optional): Дата для поиска.
            amount (float, optional): Сумма для поиска.

        Returns:
            pd.DataFrame: DataFrame с результатами поиска.
        """
        try:
            df = pd.read_csv(self.filename, parse_dates=['Date'])

            if category is not None:
                df = df[df['Category'] == category]

            if date is not None:
                df = df[df['Date'] == date]

            if amount is not None:
                df = df[df['Amount'] == amount]

            return df
        except Exception as e:
            print("Ошибка при поиске записей:", e)


def main() -> None:
    """Основная функция для запуска приложения финансового менеджера."""
    filename = "finance_records.csv"
    if not os.path.exists(filename):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Date', 'Category', 'Amount', 'Description'])

    manager = FinanceManager(filename)

    try:
        while True:
            print("Личный финансовый кошелек")
            print("1. Показать баланс")
            print("2. Добавить запись")
            print("3. Редактировать запись")
            print("4. Поиск записей")
            print("5. Выход")
            choice = input("Выберите действие: ")

            if choice == '1':
                manager.show_wallet_balance()
            elif choice == '2':
                date = input("Введите дату (ГГГГ-ММ-ДД): ")
                category = input("Введите категорию (Доход/Расход): ")
                amount = float(input("Введите сумму: "))
                description = input("Введите описание: ")
                manager.add_record(date, category, amount, description)
            elif choice == '3':
                record_id = int(input("Введите индекс записи, которую хотите отредактировать: "))
                date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
                category = input("Введите новую категорию (Доход/Расход): ")
                amount = float(input("Введите новую сумму: "))
                description = input("Введите новое описание: ")
                manager.edit_record(record_id, date, category, amount, description)
            elif choice == '4':
                category = input("Введите категорию (Доход/Расход) для поиска или нажмите Enter: ")
                date = input("Введите дату (ГГГГ-ММ-ДД) для поиска или нажмите Enter: ")
                amount = float(input("Введите сумму для поиска или нажмите Enter: "))
                records = manager.search_records(category, date, amount)
                if records is not None and not records.empty:
                    print("Результаты поиска:")
                    print(records)
                else:
                    print("Ничего не найдено.")
            elif choice == '5':
                print("До свидания!")
                break
            else:
                print("Неверный ввод. Попробуйте еще раз.")

    finally:
        pass


if __name__ == "__main__":
    main()
