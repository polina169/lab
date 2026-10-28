import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import sqlite3
import csv


class TitanicApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная 12 - БД Titanic")
        self.root.geometry("1000x650")

        self.conn = sqlite3.connect('titanic.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS passengers 
                               (id INTEGER PRIMARY KEY AUTOINCREMENT, Age REAL, Embarked TEXT, Survived INTEGER, Fare REAL)''')
        self.conn.commit()

        self.current_records = []
        self.setup_ui()
        self.refresh_table()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")

    def setup_ui(self):
        # Верхняя панель
        top = tk.Frame(self.root, bg="#2c3e50", pady=10)
        top.pack(fill=tk.X)
        tk.Button(top, text="Импорт CSV", command=self.import_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Очистить БД", command=self.clear_db, bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Вычисления", command=self.run_calc, bg="#f1c40f").pack(side=tk.LEFT, padx=5)

        # Вкладки
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Вкладка 1: База Данных
        tab1 = tk.Frame(self.notebook)
        self.notebook.add(tab1, text="База Данных")

        # Таблица
        self.tree = ttk.Treeview(tab1, columns=("id", "Age", "Embarked", "Survived", "Fare"), show='headings')
        for col in ("id", "Age", "Embarked", "Survived", "Fare"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center")
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Кнопки управления
        ctrl = tk.Frame(tab1, pady=10)
        ctrl.pack(fill=tk.X)
        tk.Button(ctrl, text="Ввести", command=self.add_record).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Редактировать", command=self.edit_record).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="Удалить", command=self.delete_record).pack(side=tk.LEFT, padx=5)
        tk.Button(ctrl, text="<< Назад", command=self.prev_record).pack(side=tk.RIGHT, padx=5)
        tk.Button(ctrl, text="Вперед >>", command=self.next_record).pack(side=tk.RIGHT, padx=5)

        # Поиск
        search_frame = tk.LabelFrame(tab1, text="Поиск по возрасту")
        search_frame.pack(fill=tk.X, pady=5)
        self.search_age = tk.Entry(search_frame, width=10)
        self.search_age.pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Найти", command=self.search_records).pack(side=tk.LEFT, padx=5)
        tk.Button(search_frame, text="Сброс", command=self.refresh_table).pack(side=tk.LEFT, padx=5)

        # Вкладка 2: Вычисления
        tab2 = tk.Frame(self.notebook)
        self.notebook.add(tab2, text="Вычисления")
        self.result_text = tk.Text(tab2, font=("Arial", 14), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    # Логика
    def refresh_table(self, records=None):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if records is None:
            self.cursor.execute("SELECT * FROM passengers")
            self.current_records = self.cursor.fetchall()
        else:
            self.current_records = records
        for row in self.current_records:
            self.tree.insert('', tk.END, values=row)

    def import_csv(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not filename: return

        self.cursor.execute("DELETE FROM passengers")
        count = 0
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row:
                    age = float(row[0]) if row[0].strip() else 0.0
                    self.cursor.execute("INSERT INTO passengers (Age, Embarked, Survived, Fare) VALUES (?, ?, ?, ?)",
                                        (age, row[1].strip().upper(), int(row[2]), float(row[3])))
                    count += 1

        self.conn.commit()
        self.refresh_table()
        messagebox.showinfo("Успех", f"Загружено {count} записей в базу данных!")

    def clear_db(self):
        if messagebox.askyesno("Очистка", "Удалить все данные?"):
            self.cursor.execute("DELETE FROM passengers")
            self.conn.commit()
            self.refresh_table()
            messagebox.showinfo("Успех", "База данных очищена.")

    def add_record(self):
        age = simpledialog.askfloat("Ввод", "Возраст:")
        if age is None: return
        port = simpledialog.askstring("Ввод", "Порт (S, C, Q):").upper()
        survived = simpledialog.askinteger("Ввод", "Выжил (1/0):")
        fare = simpledialog.askfloat("Ввод", "Цена:")
        self.cursor.execute("INSERT INTO passengers (Age, Embarked, Survived, Fare) VALUES (?, ?, ?, ?)",
                            (age, port, survived, fare))
        self.conn.commit()
        self.refresh_table()

    def edit_record(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Ошибка", "Выберите запись")
            return
        item = self.tree.item(selected[0])['values']
        age = simpledialog.askfloat("Ред.", "Возраст:", initialvalue=item[1])
        port = simpledialog.askstring("Ред.", "Порт:", initialvalue=item[2]).upper()
        survived = simpledialog.askinteger("Ред.", "Выжил:", initialvalue=item[3])
        fare = simpledialog.askfloat("Ред.", "Цена:", initialvalue=item[4])
        self.cursor.execute("UPDATE passengers SET Age=?, Embarked=?, Survived=?, Fare=? WHERE id=?",
                            (age, port, survived, fare, item[0]))
        self.conn.commit()
        self.refresh_table()

    def delete_record(self):
        selected = self.tree.selection()
        if not selected: return
        rec_id = self.tree.item(selected[0])['values'][0]
        self.cursor.execute("DELETE FROM passengers WHERE id=?", (rec_id,))
        self.conn.commit()
        self.refresh_table()

    def search_records(self):
        age = self.search_age.get().strip()
        if not age: return
        self.cursor.execute("SELECT * FROM passengers WHERE Age = ?", (float(age),))
        self.refresh_table(self.cursor.fetchall())

    def next_record(self):
        if not self.current_records: return
        idx = self.tree.index(self.tree.selection()[0]) if self.tree.selection() else -1
        children = self.tree.get_children()
        if idx + 1 < len(children):
            self.tree.selection_set(children[idx + 1])
            self.tree.see(children[idx + 1])

    def prev_record(self):
        if not self.current_records: return
        idx = self.tree.index(self.tree.selection()[0]) if self.tree.selection() else 0
        children = self.tree.get_children()
        if idx - 1 >= 0:
            self.tree.selection_set(children[idx - 1])
            self.tree.see(children[idx - 1])

    def run_calc(self):
        self.result_text.delete(1.0, tk.END)

        # ЗАЩИТА ОТ ПУСТОЙ БАЗЫ
        self.cursor.execute("SELECT COUNT(*) FROM passengers")
        if self.cursor.fetchone()[0] == 0:
            messagebox.showwarning("Внимание", "Сначала импортируйте CSV-файл!")
            return

        # 1. Мода
        self.cursor.execute(
            "SELECT CAST(Age AS INT) as a, COUNT(*) as c FROM passengers GROUP BY a ORDER BY c DESC LIMIT 1")
        mode = self.cursor.fetchone()[0]

        # 2. Медиана
        self.cursor.execute(
            "SELECT AVG(Age) FROM (SELECT Age FROM passengers ORDER BY Age LIMIT 2 - (SELECT COUNT(*) FROM passengers) % 2 OFFSET (SELECT (COUNT(*) - 1) / 2 FROM passengers))")
        median = round(self.cursor.fetchone()[0], 1)

        # 3. Дети
        self.cursor.execute("SELECT COUNT(*) FROM passengers WHERE Age < 18 AND Embarked = 'Q'")
        children = self.cursor.fetchone()[0]

        # 4. Средняя стоимость билетов
        self.cursor.execute("SELECT AVG(Fare), COUNT(*) FROM passengers WHERE Survived = 1")
        avg_surv, count_surv = self.cursor.fetchone()
        avg_surv = round(avg_surv, 2) if avg_surv else 0

        self.cursor.execute("SELECT AVG(Fare), COUNT(*) FROM passengers WHERE Survived = 0")
        avg_died, count_died = self.cursor.fetchone()
        avg_died = round(avg_died, 2) if avg_died else 0

        text = "АНАЛИЗ (SQLite)\n" + "=" * 30 + "\n\n"
        text += f"1. Мода возраста: {mode} лет\n"
        text += f"2. Медиана возраста: {median} лет\n"
        text += f"3. Дети из Квинстауна: {children} чел.\n\n"
        text += "4. Средняя стоимость билетов:\n"
        text += f"   Выжившие: {count_surv} чел., средняя {avg_surv} £\n"
        text += f"   Погибшие: {count_died} чел., средняя {avg_died} £\n"

        self.result_text.insert(tk.END, text)
        self.notebook.select(1)


if __name__ == "__main__":
    root = tk.Tk()
    app = TitanicApp(root)
    root.mainloop()
