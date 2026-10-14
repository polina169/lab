import time
import itertools
import math
import random
import tkinter as tk
from tkinter import scrolledtext, messagebox

def dist(p1, p2):
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5

def is_square(p):
    d = []
    for i in range(4):
        for j in range(i+1,4):
            d.append(dist(p[i],p[j]))
    d.sort()
    if d[0]>0 and d[0]==d[1]==d[2]==d[3] and d[4]==d[5]:
        return True
    return False

def generate_points(K):
    """Генерация K точек с чётными координатами"""
    points = []
    for i in range(K):
        x = random.randint(-5, 5) * 2
        y = random.randint(-5, 5) * 2
        points.append((x, y))
    return list(set(points))

def find_squares_cycles(points):
    """1 способ: 4 вложенных цикла"""
    s1 = []
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                for m in range(k+1, n):
                    if is_square([points[i], points[j], points[k], points[m]]):
                        s1.append([points[i], points[j], points[k], points[m]])
    return s1

def find_squares_combinations(points):
    """2 способ: itertools.combinations"""
    s2 = []
    for combo in itertools.combinations(points, 4):
        if is_square(list(combo)):
            s2.append(list(combo))
    return s2

def find_max_area_square(squares):
    """Находит квадрат с максимальной площадью """
    if not squares:
        return None, 0
    
    max_square = squares[0]
    max_area = 0
    
    for sq in squares:
        dists = []
        for i in range(4):
            for j in range(i+1, 4):
                dists.append(dist(sq[i], sq[j]))
        dists.sort()
        side = dists[0]
        area = side * side
        if area > max_area:
            max_area = area
            max_square = sq
    
    return max_square, max_area

# ======================== ГРАФИЧЕСКИЙ ИНТЕРФЕЙС ========================

class SquareFinderApp:
    def __init__(self, master):
        self.master = master
        master.title("Поиск квадратов среди точек")
        master.geometry("900x750")
        master.resizable(True, True)
        
        # Центрирование окна
        self.center_window(900, 750)

        # Окно ввода
        tk.Label(master, text="Количество точек (K):", font=("Arial", 12)).pack(pady=(15,0))
        self.k_entry = tk.Entry(master, width=15, font=("Arial", 12))
        self.k_entry.pack(pady=5)
        self.k_entry.insert(0, "100")
        
        tk.Label(master, text="(точки генерируются с чётными координатами от -10 до 10)", font=("Arial", 8), fg="gray").pack()

        # Кнопка
        self.run_button = tk.Button(master, text="Сгенерировать и найти квадраты", command=self.run_analysis, bg="lightblue", font=("Arial", 12))
        self.run_button.pack(pady=15)

        # Окно вывода со скроллингом
        tk.Label(master, text="Результаты:", font=("Arial", 12)).pack(anchor="w", padx=10)
        self.output_text = scrolledtext.ScrolledText(master, height=28, width=100, wrap=tk.WORD, font=("Courier New", 9))
        self.output_text.pack(padx=10, pady=5)

        # Строка статуса
        self.status_label = tk.Label(master, text="Готов.", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(fill="x", padx=10, pady=2)

    def center_window(self, width, height):
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def log(self, message):
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.master.update_idletasks()

    def update_status(self, message):
        self.status_label.config(text=message)
        self.master.update_idletasks()

    def run_analysis(self):
        self.output_text.delete(1.0, tk.END)

        k_value = self.k_entry.get()
        if not k_value.isdigit():
            messagebox.showerror("Ошибка", "Введите целое число")
            return
        
        K = int(k_value)
        if K < 4:
            messagebox.showerror("Ошибка", "K должно быть >= 4")
            return

        self.update_status("Генерация точек...")
        self.log("=" * 80)
        self.log(f"--- ПОИСК КВАДРАТОВ ДЛЯ K = {K} ---")
        self.log("=" * 80)

        points = generate_points(K)
        self.log(f"\nСгенерировано {len(points)} уникальных точек:")
        self.log(f"Ограничение: только чётные координаты (x и y кратны 2)")
        points_str = ", ".join([str(p) for p in points[:15]])
        if len(points) > 15:
            points_str += f" ... и еще {len(points)-15}"
        self.log(f"Точки: {points_str}")

        # 1 способ
        self.update_status("Поиск квадратов (циклы)...")
        self.log("\n--- 1 способ (циклы) ---")
        start = time.time()
        s1 = find_squares_cycles(points)
        t1 = (time.time() - start) * 1000
        self.log(f"Найдено квадратов: {len(s1)}")
        self.log(f"Время: {t1:.2f} мс")

        # 2 способ
        self.update_status("Поиск квадратов (combinations)...")
        self.log("\n--- 2 способ (combinations) ---")
        start = time.time()
        s2 = find_squares_combinations(points)
        t2 = (time.time() - start) * 1000
        self.log(f"Найдено квадратов: {len(s2)}")
        self.log(f"Время: {t2:.2f} мс")

        # Сравнение
        self.log("\n--- Сравнение ---")
        self.log(f"1 способ (циклы): {t1:.2f} мс")
        self.log(f"2 способ (combinations): {t2:.2f} мс")
        if t1 < t2:
            self.log(f"Циклы быстрее в {t2/t1:.2f} раз")
        else:
            self.log(f"Combinations быстрее в {t1/t2:.2f} раз")

        # Квадрат с максимальной площадью
        self.log("\n--- Квадрат с максимальной площадью ---")
        max_square, max_area = find_max_area_square(s1)
        
        if max_square:
            self.log(f"\nОПТИМАЛЬНЫЙ КВАДРАТ (с максимальной площадью):")
            self.log(f"Вершины: {max_square}")
            self.log(f"Площадь: {max_area:.6f}")
            if len(s1) > 1:
                self.log(f"\nВсе найденные квадраты ({len(s1)} шт.):")
                for i, sq in enumerate(s1):
                    self.log(f"  {i+1}: {sq}")
            messagebox.showinfo("Результат", f"Найдено квадратов: {len(s1)}\nПлощадь наибольшего: {max_area:.4f}")
        else:
            self.log("Квадратов не найдено")
            messagebox.showinfo("Результат", "Квадратов не найдено")

        self.log("\n" + "=" * 80)
        self.update_status("Готов.")


if __name__ == "__main__":
    root = tk.Tk()
    app = SquareFinderApp(root)
    root.mainloop()
