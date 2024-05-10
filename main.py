from typing import Optional
import pandas as pd


class FinanceManager:
    def __init__(self, filename: str):
        self.filename = filename
        self.df = self.load_data()

    def load_data(self) -> pd.DataFrame:
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
                        data.append([date, category, amount, description])

                if data:
                    df = pd.DataFrame(data, columns=['Date', 'Category', 'Amount', 'Description'])
                else:
                    df = pd.DataFrame(columns=['Date', 'Category', 'Amount', 'Description'])

                self.df = df  # Update self.df with the loaded DataFrame
                return df
        except FileNotFoundError:
            columns = ['Date', 'Category', 'Amount', 'Description']
            self.df = pd.DataFrame(columns=columns)  # Update self.df with an empty DataFrame
            return self.df

    def save_data(self) -> None:
        self.df.to_csv(self.filename, index=False)

    def add_entry(self, date: str, category: str, amount: float, description: str) -> None:
        try:
            new_id = len(self.df) + 1
            new_record = {'Date': date, 'Category': category, 'Amount': amount, 'Description': description}
            self.df = pd.concat([self.df, pd.DataFrame([new_record])], ignore_index=True)
            self.save_data()
            print("Запись добавлена успешно.")
        except Exception as e:
            print("Ошибка при добавлении записи:", e)

    def edit_record(self, record_id: int, new_date: str, new_category: str, new_amount: float,
                    new_description: str) -> None:
        if record_id in self.df.index:
            self.df.at[record_id, 'Date'] = new_date
            self.df.at[record_id, 'Category'] = new_category
            self.df.at[record_id, 'Amount'] = new_amount
            self.df.at[record_id, 'Description'] = new_description
            self.save_data()
            print("Запись успешно отредактирована.")
        else:
            print("Запись с таким ID не найдена.")

    def show_wallet_balance(self) -> tuple:
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
        filtered_df = self.df.copy()

        if category is not None:
            filtered_df = filtered_df[filtered_df['Category'].str.lower() == category.lower()]

        if date is not None:
            date = pd.to_datetime(date).date()  # Convert to date object
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
