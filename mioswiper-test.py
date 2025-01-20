import tkinter as tk
import random
import time

class MinesweeperApp:
    def __init__(self, master, size=8, num_mines=10):
        self.master = master
        self.size = size
        self.num_mines = num_mines
        self.board = []
        self.mine_positions = set()
        self.buttons = []
        self.flags = set()
        self.start_time = None
        self.timer_label = tk.Label(self.master, text="Time: 0", font=("Arial", 12))
        self.timer_label.grid(row=self.size, column=0, columnspan=self.size, sticky="we")
        self.timer_running = False
        self.create_board()
        self.create_widgets()

    def create_board(self):
        self.board = [["."] * self.size for _ in range(self.size)]
        while len(self.mine_positions) < self.num_mines:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            self.mine_positions.add((x, y))
        for x, y in self.mine_positions:
            self.board[x][y] = "M"

    def count_adjacent_mines(self, x, y):
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        count = 0
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size and self.board[nx][ny] == "M":
                count += 1
        return count

    def reveal_cell(self, x, y):
        if not self.timer_running:
            self.start_timer()

        if self.buttons[x][y]["state"] == "disabled" or (x, y) in self.flags:
            return

        if (x, y) in self.mine_positions:
            self.buttons[x][y].config(text="M", bg="red")
            self.game_over(False)
            return

        adjacent_mines = self.count_adjacent_mines(x, y)
        self.buttons[x][y].config(text=str(adjacent_mines) if adjacent_mines > 0 else "", state="disabled", relief=tk.SUNKEN)

        if adjacent_mines == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    self.reveal_cell(nx, ny)

        if self.check_win():
            self.game_over(True)

    def flag_cell(self, x, y, event):
        if not self.timer_running:
            self.start_timer()

        if self.buttons[x][y]["state"] == "disabled":
            return

        if (x, y) in self.flags:
            self.flags.remove((x, y))
            self.buttons[x][y].config(text="")
        else:
            self.flags.add((x, y))
            self.buttons[x][y].config(text="F", bg="yellow")

    def check_win(self):
        for x in range(self.size):
            for y in range(self.size):
                if self.board[x][y] != "M" and self.buttons[x][y]["state"] != "disabled":
                    return False
        return True

    def game_over(self, won):
        self.timer_running = False
        elapsed_time = int(time.time() - self.start_time) if self.start_time else 0
        for x in range(self.size):
            for y in range(self.size):
                self.buttons[x][y].config(state="disabled")
                if (x, y) in self.mine_positions:
                    self.buttons[x][y].config(text="M", bg="red")
        if won:
            self.show_win_screen(elapsed_time)
        else:
            self.master.title("Game Over!")

    def show_win_screen(self, elapsed_time):
        win_screen = tk.Toplevel(self.master)
        win_screen.title("You Win!")
        tk.Label(win_screen, text=f"Congratulations! You cleared the board in {elapsed_time} seconds!", font=("Arial", 14)).pack(pady=20)
        tk.Button(win_screen, text="Close", command=win_screen.destroy).pack(pady=10)

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed_time}")
            self.master.after(1000, self.update_timer)

    def create_widgets(self):
        for x in range(self.size):
            row = []
            for y in range(self.size):
                btn = tk.Button(self.master, text="", width=3, height=1)
                btn.grid(row=x, column=y)
                btn.bind("<Button-1>", lambda event, x=x, y=y: self.reveal_cell(x, y))
                btn.bind("<Button-3>", lambda event, x=x, y=y: self.flag_cell(x, y, event))
                row.append(btn)
            self.buttons.append(row)

        new_game_btn = tk.Button(self.master, text="New Game", font=("Arial", 12), command=self.new_game)
        new_game_btn.grid(row=self.size + 1, column=0, columnspan=self.size, sticky="we")

    def new_game(self):
        self.timer_running = False
        self.start_time = None
        self.timer_label.config(text="Time: 0")
        self.mine_positions.clear()
        self.flags.clear()
        for row in self.buttons:
            for btn in row:
                btn.destroy()
        self.buttons.clear()
        self.create_board()
        self.create_widgets()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")
    app = MinesweeperApp(root, size=15, num_mines=30)
    root.mainloop()


