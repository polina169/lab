import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import math
import csv

class Circle:
    """Класс, представляющий круг (3 атрибута: x, y, radius)"""

    def __init__(self, x, y, radius, color="blue"):
        self.x = x          # координата центра X 
        self.y = y          # координата центра Y 
        self.radius = radius # радиус 
        self.color = color   # цвет 

    def move(self, dx, dy):
        """Перемещение круга на плоскости (метод 1)"""
        self.x += dx
        self.y += dy

    def recolor(self, new_color):
        """Раскраска круга (метод 2)"""
        self.color = new_color

    def get_bbox(self):
        """Возвращает координаты прямоугольника для отрисовки (метод 3)"""
        return (self.x - self.radius, self.y - self.radius,
                self.x + self.radius, self.y + self.radius)

    def __str__(self):
        return f"{self.x},{self.y},{self.radius},{self.color}"


class CircleApp:
    """Главный класс приложения"""

    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор - Круги")
        self.root.geometry("800x600")
        self.center_window(self.root, 800, 600)

        self.circles = []       # список кругов
        self.selected_index = None

        self.setup_ui()
        self.setup_canvas()

    def center_window(self, window, width, height):
        """Центрирует окно на экране"""
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ui(self):
        """Создание элементов управления"""
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        tk.Button(control_frame, text="1. Загрузить из файла",
                  command=self.load_from_file, width=22).pack(pady=5)

        tk.Button(control_frame, text="2. Сохранить в файл",
                  command=self.save_to_file, width=22).pack(pady=5)

        tk.Button(control_frame, text="3. Визуализация",
                  command=self.visualize, width=22).pack(pady=5)

        tk.Button(control_frame, text="4. Раскраска",
                  command=self.change_color, width=22).pack(pady=5)

        tk.Button(control_frame, text="5. Перемещение",
                  command=self.move_circle, width=22).pack(pady=5)

        tk.Button(control_frame, text="6. Равномерная сегментация",
                  command=self.uniform_segmentation, width=22).pack(pady=5)

        tk.Button(control_frame, text="7. Очистить холст",
                  command=self.visualize, width=22).pack(pady=20)

        # Информационная метка
        self.info_label = tk.Label(control_frame, text="Готов", wraplength=180, fg="blue")
        self.info_label.pack(pady=20)

    def setup_canvas(self):
        """Создание холста для рисования"""
        canvas_frame = tk.Frame(self.root)
        canvas_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)

        self.canvas = tk.Canvas(canvas_frame, bg="white", width=550, height=550)
        self.canvas.pack(expand=True, fill=tk.BOTH)

    # ========== ВВОД ИЗ ФАЙЛА ==========
    def load_from_file(self):
        """Загрузка кругов из CSV файла с проверкой данных"""
        file_path = filedialog.askopenfilename(
            title="Выберите файл с кругами",
            parent=self.root,
            filetypes=[("CSV файлы", "*.csv"), ("Текстовые файлы", "*.txt")]
        )

        if not file_path:
            return

        new_circles = []
        errors = []

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row_num, row in enumerate(reader, 1):
                    # Пропускаем пустые строки
                    if not row or all(not cell.strip() for cell in row):
                        continue

                    # Проверка количества полей 
                    if len(row) < 3:
                        errors.append(f"Строка {row_num}: недостаточно данных (нужно x, y, radius)")
                        continue

                    try:
                        x = float(row[0].strip())
                        y = float(row[1].strip())
                        radius = float(row[2].strip())
                        color = row[3].strip() if len(row) > 3 else "blue"

                        # Проверка корректности
                        if radius <= 0:
                            errors.append(f"Строка {row_num}: радиус должен быть > 0")
                            continue

                        if x < 0 or x > 550 or y < 0 or y > 550:
                            errors.append(f"Строка {row_num}: координаты за пределами холста (0-550)")

                        new_circles.append(Circle(x, y, radius, color))

                    except ValueError:
                        errors.append(f"Строка {row_num}: ошибка преобразования чисел")

            if new_circles:
                self.circles = new_circles
                self.visualize()
                self.info_label.config(text=f"Загружено {len(new_circles)} кругов")
                messagebox.showinfo("Успех", f"Загружено {len(new_circles)} кругов", parent=self.root)
            else:
                messagebox.showwarning("Предупреждение", "Нет корректных данных для загрузки", parent=self.root)

            if errors:
                err_msg = "\n".join(errors[:5])
                if len(errors) > 5:
                    err_msg += f"\n... и еще {len(errors)-5} ошибок"
                messagebox.showwarning("Ошибки в файле", err_msg, parent=self.root)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{e}", parent=self.root)

    def save_to_file(self):
        """Сохранение кругов в CSV файл"""
        if not self.circles:
            messagebox.showwarning("Предупреждение", "Нет данных для сохранения", parent=self.root)
            return

        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            parent=self.root,
            defaultextension=".csv",
            filetypes=[("CSV файлы", "*.csv")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8', newline='') as file:
                    writer = csv.writer(file)
                    for circle in self.circles:
                        writer.writerow([circle.x, circle.y, circle.radius, circle.color])

                messagebox.showinfo("Успех", "Данные сохранены", parent=self.root)
                self.info_label.config(text="Данные сохранены")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить:\n{e}", parent=self.root)

    # ========== ВИЗУАЛИЗАЦИЯ ==========
    def visualize(self):
        """Отрисовка всех кругов на холсте"""
        self.canvas.delete("all")

        if not self.circles:
            self.canvas.create_text(275, 275, text="Нет кругов для отображения",
                                     font=("Arial", 14), fill="gray")
            return

        for i, circle in enumerate(self.circles):
            x1, y1, x2, y2 = circle.get_bbox()
            if i == self.selected_index:
                # Выделяем выбранный круг жирной красной границей
                self.canvas.create_oval(x1, y1, x2, y2, fill=circle.color,
                                        outline="red", width=3)
            else:
                self.canvas.create_oval(x1, y1, x2, y2, fill=circle.color,
                                        outline="black", width=1)

        self.info_label.config(text=f"Кругов: {len(self.circles)}")

    # ========== РАВНОМЕРНАЯ СЕГМЕНТАЦИЯ ==========
    def uniform_segmentation(self):
        """Разбиение плоскости на области, относящиеся к ближайшему центру круга"""
        if not self.circles:
            messagebox.showwarning("Предупреждение", "Нет кругов для сегментации", parent=self.root)
            return

        self.canvas.update()
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        if width <= 1 or height <= 1:
            width, height = 550, 550

        # Создаём изображение для сегментации
        img = tk.PhotoImage(width=width, height=height)

        for x in range(width):
            for y in range(height):
                min_dist = float('inf')
                nearest_color = "white"

                for circle in self.circles:
                    dist = math.sqrt((x - circle.x) ** 2 + (y - circle.y) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_color = circle.color

                img.put(nearest_color, (x, y))

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

        # Поверх рисуем границы кругов
        for circle in self.circles:
            x1, y1, x2, y2 = circle.get_bbox()
            self.canvas.create_oval(x1, y1, x2, y2, outline="black", width=2)

        self.info_label.config(text="Выполнена равномерная сегментация")

    # ========== РАСКРАСКА ==========
    def change_color(self):
        """Изменение цвета выбранного круга"""
        if not self.circles:
            messagebox.showwarning("Предупреждение", "Нет кругов для раскраски", parent=self.root)
            return

        # Если нет выбранного, выбираем первый
        if self.selected_index is None and self.circles:
            self.selected_index = 0
            self.visualize()

        color = colorchooser.askcolor(
            title="Выберите цвет для круга",
            parent=self.root,
            color=self.circles[self.selected_index].color
        )
        if color[1]:
            self.circles[self.selected_index].recolor(color[1])
            self.visualize()
            self.info_label.config(text=f"Цвет круга изменён")

    # ========== ПЕРЕМЕЩЕНИЕ НА ПЛОСКОСТИ ==========
    def move_circle(self):
        """Перемещение выбранного круга"""
        if not self.circles:
            messagebox.showwarning("Предупреждение", "Нет кругов для перемещения", parent=self.root)
            return

        if self.selected_index is None:
            messagebox.showwarning("Предупреждение", "Сначала выберите круг (кликните по нему)", parent=self.root)
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Перемещение круга")
        dialog.resizable(False, False)
        dialog.geometry("300x200")

        # Центрируем диалог
        self.center_window(dialog, 300, 200)

        tk.Label(dialog, text=f"Перемещение круга №{self.selected_index + 1}", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Label(dialog, text="Введите смещение:").pack(pady=5)

        tk.Label(dialog, text="dx (по горизонтали):").pack()
        dx_entry = tk.Entry(dialog)
        dx_entry.pack()
        dx_entry.insert(0, "0")

        tk.Label(dialog, text="dy (по вертикали):").pack()
        dy_entry = tk.Entry(dialog)
        dy_entry.pack()
        dy_entry.insert(0, "0")

        def move():
            try:
                dx = float(dx_entry.get())
                dy = float(dy_entry.get())
                self.circles[self.selected_index].move(dx, dy)
                self.visualize()
                self.info_label.config(text=f"Круг перемещён на ({dx}, {dy})")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Ошибка", "Введите числа", parent=dialog)

        tk.Button(dialog, text="Переместить", command=move).pack(pady=20)

    # ========== ВЫБОР КРУГА ПО КЛИКУ ==========
    def on_canvas_click(self, event):
        """Обработка клика по холсту для выбора круга"""
        min_dist = 20
        best_idx = None

        for i, circle in enumerate(self.circles):
            # Вычисляем расстояние от точки клика до центра круга
            dist = math.sqrt((event.x - circle.x) ** 2 + (event.y - circle.y) ** 2)
            if dist < min_dist:
                min_dist = dist
                best_idx = i

        if best_idx is not None:
            self.selected_index = best_idx
            self.visualize()
            c = self.circles[best_idx]
            self.info_label.config(text=f"Выбран круг: центр({c.x},{c.y}), R={c.radius}")


# ========== ЗАПУСК ==========
if __name__ == "__main__":
    root = tk.Tk()
    app = CircleApp(root)
    app.canvas.bind("<Button-1>", app.on_canvas_click)
    root.mainloop()
