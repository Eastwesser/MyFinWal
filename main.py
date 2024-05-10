from typing import Optional  # Импортируем тип Optional для работы с необязательными аргументами
import pandas as pd  # Импортируем библиотеку pandas для работы с DataFrame


class FinanceManager:
    def __init__(self, filename: str):
        """
        Инициализация объекта FinanceManager.

        Args:
            filename (str): Путь к файлу данных.

        Attributes:
            filename (str): Путь к файлу данных.
            df (pd.DataFrame): DataFrame для хранения финансовых данных.

        """
        self.filename = filename
        self.df = self.load_data()  # Загружаем данные при инициализации объекта

    def load_data(self) -> pd.DataFrame:
        """
        Загружает данные из файла CSV в DataFrame.

        Returns:
            pd.DataFrame: DataFrame с загруженными данными или пустой DataFrame.

        """
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                data = []
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
                        data.append({'Date': date, 'Category': category, 'Amount': amount, 'Description': description})

                if data:
                    df = pd.DataFrame(data)
                else:
                    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

                self.df = df  # Обновляем self.df загруженным DataFrame
                return df
        except FileNotFoundError:
            columns = ['Date', 'Category', 'Amount', 'Description']
            self.df = pd.DataFrame(columns=columns)  # Обновляем self.df пустым DataFrame
            return self.df

    def save_data(self) -> None:
        """
        Сохраняет DataFrame в файл CSV.
        """
        self.df.to_csv(self.filename, index=False)

    def add_entry(self, date: str, category: str, amount: float, description: str) -> None:
        """
        Добавляет новую запись о финансовой операции.

        Args:
            date (str): Дата операции в формате 'ГГГГ-ММ-ДД'.
            category (str): Категория операции ('Доход' или 'Расход').
            amount (float): Сумма операции.
            description (str): Описание операции.

        """
        try:
            new_id = len(self.df) + 1
            new_record = {'Date': pd.to_datetime(date), 'Category': category, 'Amount': amount,
                          'Description': description}
            self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
            self.save_data()  # Сохраняем изменения в файл
            print("Запись добавлена успешно.")
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def edit_record(self, record_id: int, new_date: str, new_category: str, new_amount: float,
                    new_description: str) -> None:
        """
        Редактирует существующую запись о финансовой операции.

        Args:
            record_id (int): Идентификатор записи.
            new_date (str): Новая дата операции в формате 'ГГГГ-ММ-ДД'.
            new_category (str): Новая категория операции ('Доход' или 'Расход').
            new_amount (float): Новая сумма операции.
            new_description (str): Новое описание операции.

        """
        if record_id in self.df.index:
            self.df.at[record_id, 'Date'] = new_date
            self.df.at[record_id, 'Category'] = new_category
            self.df.at[record_id, 'Amount'] = new_amount
            self.df.at[record_id, 'Description'] = new_description
            self.save_data()  # Сохраняем изменения в файл
            print("Запись успешно отредактирована.")
        else:
            print("Запись с таким ID не найдена.")

    def show_wallet_balance(self) -> tuple:
        """
        Отображает баланс кошелька и суммы доходов и расходов.

        Returns:
            tuple: Кортеж из трех элементов: баланс, сумма доходов, сумма расходов.

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
        Выполняет поиск записей по заданным критериям.

        Args:
            category (Optional[str]): Категория для поиска.
            date (Optional[str]): Дата для поиска.
            amount (Optional[float]): Сумма для поиска.
            record_id (Optional[int]): Идентификатор записи для поиска.

        Returns:
            pd.DataFrame: DataFrame с найденными записями.

        """
        filtered_df = self.df.copy()

        if category is not None:
            filtered_df = filtered_df[filtered_df['Category'].str.lower() == category.lower()]

        if date is not None:
            date = pd.to_datetime(date).date()
            filtered_df = filtered_df[filtered_df['Date'].dt.date == date]

        if amount is not None:
            filtered_df = filtered_df[filtered_df['Amount'] == amount]

        if record_id is not None:
            filtered_df = filtered_df.iloc[[record_id]] if record_id < len(filtered_df) else pd.DataFrame()

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
