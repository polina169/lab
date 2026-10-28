import tkinter as tk
from tkinter import ttk


# ==========================================
# BACKEND (Логика конечного автомата)
# ==========================================
class TrafficLightFSM:
    def __init__(self, root):
        self.root = root  # Сохраняем ссылку на окно для таймера
        self.state = "RED"
        self.timer_id = None
        self.is_running = False

        self.durations = {
            "RED": 4000,
            "YELLOW_R": 1000,
            "GREEN": 3000,
            "YELLOW_G": 1000
        }

        # Граф переходов
        self.transitions = {
            "RED": "YELLOW_R",
            "YELLOW_R": "GREEN",
            "GREEN": "YELLOW_G",
            "YELLOW_G": "RED"
        }

    def start(self, update_callback):
        if not self.is_running:
            self.is_running = True
            self.callback = update_callback
            self._next_state()

    def stop(self):
        self.is_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)  # Отменяем таймер
            self.timer_id = None
            self.callback("", "")

    def _next_state(self):
        if not self.is_running:
            return

        # Вызываем фронтенд для обновления цвета
        self.callback(self.state, self.durations[self.state])

        # Запускаем таймер через root.after
        self.timer_id = self.root.after(self.durations[self.state], self._step)

    def _step(self):
        self.state = self.transitions[self.state]
        self._next_state()


# ==========================================
# FRONTEND (Интерфейс) 
# ==========================================
class TrafficLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конечный автомат: Светофор")
        self.root.geometry("400x550")
        self.root.resizable(False, False)

        # Передаем root в бэкенд
        self.fsm = TrafficLightFSM(self.root)

        self.setup_ui()
        self.center_window()

    def center_window(self):
        self.root.update_idletasks()
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="black", padx=20, pady=20)
        self.frame.pack(pady=20)

        self.lbl_red = tk.Label(self.frame, bg="#4a0000", width=10, height=4, relief="sunken", borderwidth=5)
        self.lbl_red.pack(pady=10)

        self.lbl_yellow = tk.Label(self.frame, bg="#4a3e00", width=10, height=4, relief="sunken", borderwidth=5)
        self.lbl_yellow.pack(pady=10)

        self.lbl_green = tk.Label(self.frame, bg="#003a00", width=10, height=4, relief="sunken", borderwidth=5)
        self.lbl_green.pack(pady=10)

        self.status_label = tk.Label(self.root, text="Светофор выключен", font=("Arial", 14, "bold"))
        self.status_label.pack(pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Запустить", font=("Arial", 12), bg="#2ecc71", fg="white", width=12,
                  command=self.start_fsm).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Остановить", font=("Arial", 12), bg="#e74c3c", fg="white", width=12,
                  command=self.stop_fsm).pack(side=tk.LEFT, padx=10)

    def start_fsm(self):
        self.fsm.start(self.update_ui)

    def stop_fsm(self):
        self.fsm.stop()
        self.lbl_red.config(bg="#4a0000", relief="sunken")
        self.lbl_yellow.config(bg="#4a3e00", relief="sunken")
        self.lbl_green.config(bg="#003a00", relief="sunken")
        self.status_label.config(text="Светофор выключен", fg="black")

    def update_ui(self, state, duration_ms):
        if not state:
            return

        # Гасим все
        self.lbl_red.config(bg="#4a0000", relief="sunken")
        self.lbl_yellow.config(bg="#4a3e00", relief="sunken")
        self.lbl_green.config(bg="#003a00", relief="sunken")

        # Включаем нужный
        if state == "RED":
            self.lbl_red.config(bg="red", relief="raised")
            self.status_label.config(text=f"Красный (осталось {duration_ms / 1000} сек)", fg="red")
        elif state in ["YELLOW_R", "YELLOW_G"]:
            self.lbl_yellow.config(bg="yellow", relief="raised")
            self.status_label.config(text=f"Желтый (осталось {duration_ms / 1000} сек)", fg="#b8860b")
        elif state == "GREEN":
            self.lbl_green.config(bg="#00ff00", relief="raised")
            self.status_label.config(text=f"Зеленый (осталось {duration_ms / 1000} сек)", fg="green")


if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficLightApp(root)
    root.mainloop()
