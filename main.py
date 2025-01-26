import tkinter as tk
from tkinter import ttk, messagebox
from games_buttons import GameButtons
from high_scores import HighScores

class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("550x750")
        self.root.configure(bg="#2c3e50")

        # Title label
        title = tk.Label(root, text="Game Launcher", font=("Helvetica", 26, "bold"), bg="#2c3e50", fg="#f39c12")
        title.pack(pady=20)

        # Input for name
        tk.Label(root, text="Enter your name:", font=("Helvetica", 16), bg="#2c3e50", fg="#ecf0f1").pack(pady=10)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(root, textvariable=self.name_var, font=("Helvetica", 16), width=25)
        self.name_entry.pack(pady=5)

        # Label for selecting a game
        tk.Label(root, text="Select a Game to Play", font=("Helvetica", 18), bg="#2c3e50", fg="#f39c12").pack(pady=20)

        # Game buttons
        self.game_buttons = GameButtons(root, self.name_var)
        self.game_buttons.pack()

        # High Scores button
        high_scores_btn = ttk.Button(
            root, text="View High Scores", style="Rounded.TButton",
            command=self.open_high_scores
        )
        high_scores_btn.pack(pady=20, ipadx=20, ipady=5, fill=tk.X)

    def open_high_scores(self):
        HighScores(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    launcher = MainLauncher(root)
    root.mainloop()
