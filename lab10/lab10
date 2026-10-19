import tkinter as tk
from tkinter import messagebox
import random


class TicTacToe:
    HUMAN = "X"
    COMPUTER = "O"
    EMPTY = ""

    def __init__(self):
        self.board = [self.EMPTY] * 9
        self.current_player = self.HUMAN
        self.game_over = False
        self.winner = None

    def reset(self):
        self.board = [self.EMPTY] * 9
        self.current_player = self.HUMAN
        self.game_over = False
        self.winner = None

    def available_moves(self):
        return [i for i, v in enumerate(self.board) if v == self.EMPTY]

    def make_move(self, index, player):
        if 0 <= index <= 8 and self.board[index] == self.EMPTY:
            self.board[index] = player
            return True
        return False

    def check_winner(self):
        lines = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a, b, c in lines:
            if self.board[a] != self.EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return "ничья" if self.EMPTY not in self.board else None

    def find_winning_move(self, player):
        for i in self.available_moves():
            self.board[i] = player
            if self.check_winner() == player:
                self.board[i] = self.EMPTY
                return i
            self.board[i] = self.EMPTY
        return None

    def best_move(self):
        for player in (self.COMPUTER, self.HUMAN):
            move = self.find_winning_move(player)
            if move is not None:
                return move
        if self.board[4] == self.EMPTY:
            return 4
        corners = [c for c in [0, 2, 6, 8] if self.board[c] == self.EMPTY]
        free = corners if corners else self.available_moves()
        return random.choice(free) if free else None


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.resizable(False, False)
        self.game = TicTacToe()
        self.buttons = []
        self.setup_ui()
        self.update_status()
        self.root.update_idletasks()
        self.center_window()

    def center_window(self):
        w, h = self.root.winfo_width(), self.root.winfo_height()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14, "bold"), fg="navy")
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)
        for i in range(9):
            btn = tk.Button(self.root, text="", font=("Arial", 24, "bold"),
                            width=4, height=2, command=lambda idx=i: self.on_cell_click(idx))
            btn.grid(row=1 + i // 3, column=i % 3)
            self.buttons.append(btn)
        control = tk.Frame(self.root)
        control.grid(row=4, column=0, columnspan=3, pady=10)
        tk.Button(control, text="Новая игра", width=12, command=self.new_game).pack(side=tk.LEFT, padx=5)
        tk.Button(control, text="Выход", width=12, command=self.root.destroy).pack(side=tk.LEFT, padx=5)

    def update_status(self):
        if self.game.game_over:
            if self.game.winner == "ничья":
                self.status_label.config(text="Ничья!", fg="orange")
            elif self.game.winner == TicTacToe.HUMAN:
                self.status_label.config(text="Вы победили!", fg="green")
            else:
                self.status_label.config(text="Компьютер победил!", fg="red")
        else:
            if self.game.current_player == TicTacToe.HUMAN:
                self.status_label.config(text="Ваш ход (X)", fg="navy")
            else:
                self.status_label.config(text="Ход компьютера (O)", fg="purple")

    def refresh_board(self):
        for i, btn in enumerate(self.buttons):
            val = self.game.board[i]
            btn.config(text=val, fg="blue" if val == "X" else "red" if val == "O" else "black")

    def on_cell_click(self, index):
        if self.game.game_over:
            messagebox.showinfo("Игра окончена", "Начните новую игру.")
            return
        if self.game.current_player != TicTacToe.HUMAN:
            return
        if not self.game.make_move(index, TicTacToe.HUMAN):
            messagebox.showwarning("Недопустимый ход", "Эта клетка уже занята.")
            return
        self.refresh_board()
        self.after_move()

    def after_move(self):
        result = self.game.check_winner()
        if result is not None:
            self.game.game_over = True
            self.game.winner = result
            self.update_status()
            self.show_result()
            return
        self.game.current_player = TicTacToe.COMPUTER
        self.update_status()
        self.root.after(300, self.computer_move)

    def computer_move(self):
        if self.game.game_over:
            return
        self.game.make_move(self.game.best_move(), TicTacToe.COMPUTER)
        self.refresh_board()
        result = self.game.check_winner()
        if result is not None:
            self.game.game_over = True
            self.game.winner = result
            self.update_status()
            self.show_result()
            return
        self.game.current_player = TicTacToe.HUMAN
        self.update_status()

    def show_result(self):
        if self.game.winner == "ничья":
            text = "Ничья! Отличная игра."
        elif self.game.winner == TicTacToe.HUMAN:
            text = "Поздравляем, вы выиграли!"
        else:
            text = "Компьютер выиграл. Попробуйте ещё раз!"
        messagebox.showinfo("Результат", text)

    def new_game(self):
        self.game.reset()
        for btn in self.buttons:
            btn.config(text="", state=tk.NORMAL)
        self.refresh_board()
        self.update_status()


if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()
