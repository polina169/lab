import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import statistics


class TitanicAnalyzer:
    def __init__(self):
        self.data = []
        self.headers = []

    def load_csv(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.headers = next(reader)
            self.data = list(reader)
        return len(self.data)

    def get_ages(self):
        ages = []
        for row in self.data:
            age_str = row[0]
            if age_str and age_str.strip():
                ages.append(float(age_str))
        return ages

    def analyze(self):
        # === 1. Мода возраста ===
        ages = self.get_ages()

        uniq = []
        counts = []
        for a in ages:
            age = int(a)
            if age in uniq:
                i = uniq.index(age)
                counts[i] = counts[i] + 1
            else:
                uniq.append(age)
                counts.append(1)

        mode_age = uniq[0]
        best = counts[0]
        for i in range(len(counts)):
            if counts[i] > best:
                best = counts[i]
                mode_age = uniq[i]

        # === 2. Диапазон моды ±10 ===
        age_min = mode_age - 10
        age_max = mode_age + 10
        age_range = str(age_min) + "–" + str(age_max)

        # === 3. Дети из Квинстауна ===
        children = []
        for row in self.data:
            age_str = row[0]
            port = row[1].strip().upper()
            if age_str and age_str.strip():
                age = float(age_str)
                if age < 18 and port == 'Q' and age_min <= age <= age_max:
                    children.append(row)

        # === 4. Выжило детей ===
        survived = 0
        for row in children:
            if int(row[2]) == 1:
                survived += 1

        # === 5. Медиана ===
        median_age = statistics.median(ages)
        med_min = median_age - 7
        med_max = median_age + 7
        median_range = str(round(med_min, 1)) + "–" + str(round(med_max, 1))

        # === 6. Билеты выживших и погибших ===
        survived_fares = []
        died_fares = []
        for row in self.data:
            age_str = row[0]
            if age_str and age_str.strip():
                age = float(age_str)
                if med_min <= age <= med_max:
                    fare = float(row[3]) if row[3] else 0
                    if int(row[2]) == 1:
                        survived_fares.append(fare)
                    else:
                        died_fares.append(fare)

        if survived_fares:
            avg_survived = sum(survived_fares) / len(survived_fares)
        else:
            avg_survived = 0

        if died_fares:
            avg_died = sum(died_fares) / len(died_fares)
        else:
            avg_died = 0

        return [
            mode_age,                  # 0 — мода
            age_range,                 # 1 — диапазон моды
            len(children),             # 2 — детей всего
            survived,                  # 3 — выжило детей
            len(children) - survived,  # 4 — погибло детей
            median_age,                # 5 — медиана 
            median_range,              # 6 — диапазон медианы
            len(survived_fares),       # 7 — выживших в диапазоне
            avg_survived,              # 8 — средняя цена выживших
            len(died_fares),           # 9 — погибших в диапазоне
            avg_died                   # 10 — средняя цена погибших
        ]


class TitanicGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ Titanic")
        self.root.geometry("900x600")
        self.analyzer = TitanicAnalyzer()
        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def setup_ui(self):
        top = tk.Frame(self.root, bg="#34495e", pady=10)
        top.pack(fill=tk.X)

        tk.Button(top, text="Открыть CSV", width=15, command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Анализ", width=15, command=self.run_analysis).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Выход", width=15, command=self.root.destroy).pack(side=tk.LEFT, padx=5)

        self.status = tk.Label(self.root, text="Файл не загружен", fg="gray")
        self.status.pack(pady=5)

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="Данные")
        self.tree = ttk.Treeview(tab1, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)

        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="Результаты")
        self.result_text = tk.Text(tab2, font=("Arial", 12), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not filename:
            return
        count = self.analyzer.load_csv(filename)
        self.status.config(text="Загружено: " + str(count), fg="green")
        self.show_data()

    def show_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        if not self.analyzer.data:
            return
        self.tree['columns'] = self.analyzer.headers
        for col in self.analyzer.headers:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        for row in self.analyzer.data[:50]:
            self.tree.insert('', tk.END, values=row)

    def run_analysis(self):
        if not self.analyzer.data:
            messagebox.showwarning("Внимание", "Загрузите CSV!")
            return
        result = self.analyzer.analyze()
        self.show_results(result)

    def show_results(self, r):
        text = "=" * 50 + "\n"
        text += "АНАЛИЗ TITANIC (Вариант 16)\n"
        text += "=" * 50 + "\n\n"
        text += "1. Мода возраста: " + str(r[0]) + " лет\n"
        text += "   Диапазон: " + r[1] + "\n\n"
        text += "2. Дети из Квинстауна: " + str(r[2]) + "\n"
        text += "   Выжило: " + str(r[3]) + "\n"
        text += "   Погибло: " + str(r[4]) + "\n\n"
        text += "3. Медиана возраста: " + str(round(r[5], 1)) + " лет\n"
        text += "   Диапазон: " + r[6] + "\n\n"
        text += "4. Стоимость билетов:\n"
        text += "   Выжившие: " + str(r[7]) + " чел., средняя " + str(round(r[8], 2)) + " £\n"
        text += "   Погибшие: " + str(r[9]) + " чел., средняя " + str(round(r[10], 2)) + " £\n"

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.status.config(text="Анализ выполнен", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = TitanicGUI(root)
    root.mainloop()
