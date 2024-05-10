from typing import Optional
import pandas as pd


class FinanceManager:
    def __init__(self, filename: str):
        """
        Инициализация FinanceManager.

        Args:
            filename (str): Имя файла для хранения финансовых записей.
        """
        self.filename = filename
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
        """
        Загружает данные из файла в DataFrame.

        Returns:
            pd.DataFrame: DataFrame с финансовыми записями.
        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = []
                date, category, amount, description = None, None, None, None
                for line in file:
                    line = line.strip()
                    if line.startswith('Дата:'):
                        date = pd.to_datetime(line.split(':')[1].strip())
                    elif line.startswith('Категория:'):
                        category = line.split(':')[1].strip()
                    elif line.startswith('Сумма:'):
                        amount = float(line.split(':')[1].strip())
                    elif line.startswith('Описание:'):
                        description = line.split(':')[1].strip()
                        data.append([date, category, amount, description])
                        date, category, amount, description = None, None, None, None

                df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount', 'Description'])
                return df
        except FileNotFoundError:
            columns = ['Date', 'Category', 'Amount', 'Description']
            return pd.DataFrame(columns=columns)

    def save_data(self) -> None:
        """
        Сохраняет данные из DataFrame в CSV-файл.
        """
        self.df.to_csv(self.filename, index=False)

    def add_entry(self, date: str, category: str, amount: float, description: str) -> None:
        """
        Добавляет новую финансовую запись.

        Args:
            date (str): Дата записи.
            category (str): Категория записи (Доход или Расход).
            amount (float): Сумма записи.
            description (str): Описание записи.
        """
        try:
            new_id = len(self.df) + 1
            new_record = {'ID': new_id, 'Date': date, 'Category': category, 'Amount': amount,
                          'Description': description}
            new_record_df = pd.DataFrame([new_record])  # Создание DataFrame из новой записи
            # Объединение DataFrame'ов
            self.df = pd.concat([self.df, new_record_df], ignore_index=True)
            # Переупорядочивание столбцов
            self.df = self.df[['ID', 'Date', 'Category', 'Amount', 'Description']]
            # Сохранение данных
            self.save_data()
            print("Запись добавлена успешно.")
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def edit_record(self, record_id: int, new_date: str, new_category: str, new_amount: float,
                    new_description: str) -> None:
        """
        Редактирует существующую финансовую запись.

        Args:
            record_id (int): Индекс записи для редактирования.
            new_date (str): Новая дата записи.
            new_category (str): Новая категория записи.
            new_amount (float): Новая сумма записи.
            new_description (str): Новое описание записи.
        """
        if record_id in self.df.index:
            print("Before edit:")
            print(self.df.loc[record_id])

            self.df.at[record_id, 'Date'] = new_date
            self.df.at[record_id, 'Category'] = new_category
            self.df.at[record_id, 'Amount'] = new_amount
            self.df.at[record_id, 'Description'] = new_description
            self.save_data()
            print("After edit:")
            print(self.df.loc[record_id])

            print("Запись успешно отредактирована.")
        else:
            print("Запись с таким ID не найдена.")

    def show_wallet_balance(self) -> tuple:
        """
        Показывает текущий баланс кошелька.

        Выводит общий баланс, общий доход и общие расходы.
        """
        if self.df.empty:
            print("Нет данных для отображения баланса.")
            return 0, 0, 0

        total_income = self.df[self.df['Category'] == 'Доход']['Amount'].sum()
        total_expense = self.df[self.df['Category'] == 'Расход']['Amount'].sum()
        balance = total_income - total_expense
        print(
            f"Баланс: {balance}\n"
            f"Доходы: {total_income}\n"
            f"Расходы: {total_expense}"
        )
        return balance, total_income, total_expense

    def search_records(self, category: Optional[str] = None, date: Optional[str] = None,
                       amount: Optional[float] = None, record_id: Optional[int] = None) -> pd.DataFrame:
        """
        Поиск финансовых записей по заданным критериям.

        Args:
            category (str, optional): Категория для поиска.
            date (str, optional): Дата для поиска.
            amount (float, optional): Сумма для поиска.
            record_id (int, optional): ID записи для поиска.

        Returns:
            pd.DataFrame: DataFrame с результатами поиска.
        """
        filtered_df = self.df.copy()

        if category is not None:
            filtered_df = filtered_df[filtered_df['Category'].str.lower() == category.lower()]

        if date is not None:
            filtered_df = filtered_df[filtered_df['Date'] == pd.to_datetime(date)]

        if amount is not None:
            filtered_df = filtered_df[filtered_df['Amount'] == amount]

        if record_id is not None:
            filtered_df = filtered_df.loc[[record_id]] if record_id in filtered_df.index else pd.DataFrame()

        print("Filtered DataFrame:")
        print(filtered_df)

        return filtered_df


def main() -> None:
    """
    Основная функция для запуска приложения финансового менеджера.
    """
    filename = "finance_records.csv"
    manager = FinanceManager(filename)

    while True:
        print("\nЛичный финансовый кошелек")
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
            manager.add_entry(date, category, amount, description)

        elif choice == '3':
            index = int(input("Введите индекс записи для редактирования: "))
            date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
            category = input("Введите новую категорию (Доход/Расход): ")
            amount = float(input("Введите новую сумму: "))
            description = input("Введите новое описание: ")
            manager.edit_record(index, date, category, amount, description)

        elif choice == '4':
            category = input("Введите категорию (Доход/Расход) для поиска или нажмите Enter: ").strip().lower() or None
            date = input("Введите дату (ГГГГ-ММ-ДД) для поиска или нажмите Enter: ") or None
            amount = float(input("Введите сумму для поиска или нажмите Enter: ")) if input(
                "Введите сумму для поиска или нажмите Enter: ") else None

            records = manager.search_records(category, date, amount)

            if not records.empty:
                print("Результаты поиска:")
                print(records)
            else:
                print("Ничего не найдено.")

        elif choice == '5':
            print("До свидания!")
            break

        else:
            print("Неверный ввод. Попробуйте еще раз.")


if __name__ == "__main__":
    main()
