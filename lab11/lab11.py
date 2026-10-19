import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import statistics


#КЛАСС ДЛЯ АНАЛИЗА
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
        ages = self.get_ages()
        uniq = []
        age_counts = []
        for a in ages:
            age = int(a)
            if age in uniq:
                i = uniq.index(age)
                age_counts[i] += age_counts[i] + 1
            else:
                uniq.append(age)
                age_counts.append(1)
                
        mode_age = uniq[0]
        best = age_counts[0]
        for i in range(len(age_counts)):
            if age_counts[i] > best:
                best = age_counts[i]
                mode_age = uniq[i]
                
        age_min = mode_age - 10
        age_max = mode_age + 10
        age_range = str(age_min) + "-" + str(age_max)
        
        children = []
        for row in self.data:
            age_str = row[0]
            port = row[1].strip().upper()
            if age_str and age_str.strip():
                age = float(age_str)
                if age < 18 and port == 'Q' and age_min <= age <= age_max:
                    children.append(row)
        children_count = len(children)

        survived = 0
        for row in children:
            if int(row[2]) == 1:
                survived += 1
        children_survived = survived
        children_died = len(children) - survived 

        median_age = statistics.median(ages)
        
        med_min = median_age - 7
        med_max = median_age + 7
        median_range = str(round(med_min, 1)) + "-" + str(round(med_max, 1))

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
        
        count_survived = len(survived_fares)
        count_died = len(died_fares)
        
        return [
            mode_age,
            age_range,
            len(children),
            survived,
            len(children) - survived,
            median_age,
            median_range,
            len(survived_fares),
            avg_survived,
            len(died_fares),
            avg_died
            ]

#КЛАСС ДЛЯ ИНТЕРФЕЙСА
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
        
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def setup_ui(self):
        top = tk.Frame(self.root, bg="#34495e", pady=10)
        top.pack(fill=tk.X)
        
        tk.Button(top, text="Открыть CSV", width=15, 
                  command=self.open_file).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Анализ", width=15, 
                  command=self.run_analysis).pack(side=tk.LEFT, padx=5)
        tk.Button(top, text="Выход", width=15, 
                  command=self.root.destroy).pack(side=tk.LEFT, padx=5)
        
        self.status = tk.Label(self.root, text="Файл не загружен", fg="gray")
        self.status.pack(pady=5)
        
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="Данные")
        
        self.tree = ttk.Treeview(tab1, show='headings')
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        scroll = tk.Scrollbar(tab1, orient=tk.VERTICAL, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)
        
        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="Результаты")
        
        self.result_text = tk.Text(tab2, font=("Arial", 12), wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def open_file(self):
        filename = filedialog.askopenfilename(
            title="Выберите CSV-файл",
            filetypes=[("CSV", "*.csv")]
        )
        if not filename:
            return
        
        count = self.analyzer.load_csv(filename)
        self.status.config(text="Загружено: " + str(count) + " записей", fg="green")
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
            values = row
            self.tree.insert('', tk.END, values=values)
    
    def run_analysis(self):
        if not self.analyzer.data:
            messagebox.showwarning("Внимание", "Сначала загрузите CSV-файл!")
            return
        
        result = self.analyzer.analyze()
        self.show_results(result)
    
    def show_results(self, r):
        text = ""
        text += "=" * 50 + "\n"
        text += "АНАЛИЗ TITANIC \n"
        text += "=" * 50 + "\n\n"
        
        text += "1. Мода возраста: " + str(r[0]) + " лет\n"
        text += "   Диапазон мода ±10: " + r[1] + "\n\n"
        
        text += "2. Дети (<18) из Квинстауна:\n"
        text += "   Всего: " + str(r[2]) + "\n"
        text += "   Выжило: " + str(r[3]) + "\n"
        text += "   Погибло: " + str(r[4]) + "\n\n"
        
        text += "3. Медиана возраста: " + str(round(r[5], 1)) + " лет\n"
        text += "   Диапазон медиана ±7: " + r[6] + "\n\n"
        
        text += "4. Средняя стоимость билетов:\n"
        text += "   Выжившие: " + str(r[7]) + " чел.\n"
        text += "   Средняя: " + str(round(r[8], 2)) + " £\n"
        text += "   Погибшие: " + str(r[9]) + " чел.\n"
        text += "   Средняя: " + str(round(r[10], 2)) + " £\n"
        
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, text)
        self.status.config(text="Анализ выполнен", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = TitanicGUI(root)
    root.mainloop()
