import tkinter as tk
from tkinter import ttk, messagebox
from games_buttons import GameButtons
from high_scores import HighScores

class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("550x900")  # Increased height
        self.root.configure(bg="#2c3e50")
        self.root.resizable(False, False)  # Fixed size

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

        # Frame for game buttons with a scrollbar
        self.button_frame = tk.Frame(root, bg="#2c3e50")
        self.button_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.button_frame, bg="#2c3e50", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.button_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#2c3e50")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Add game buttons
        self.game_buttons = GameButtons(self.scrollable_frame, self.name_var)
        self.game_buttons.pack()

        # High Scores button
        high_scores_btn = tk.Button(
            root, text="View High Scores", font=("Helvetica", 16, "bold"), bg="#f39c12", fg="#ffffff",
            activebackground="#d35400", activeforeground="#ffffff", relief="raised", bd=3,
            command=self.open_high_scores
        )
        high_scores_btn.pack(pady=20, ipadx=20, ipady=10)

        # Add fade effect for scrollable area
        self.add_fade_overlay()

    def add_fade_overlay(self):
        # Overlay at the top and bottom
        top_overlay = tk.Label(self.button_frame, bg="#2c3e50", height=1)
        bottom_overlay = tk.Label(self.button_frame, bg="#2c3e50", height=1)

        # Adding a gradient-like fade effect
        gradient_color = "#2c3e50"
        top_overlay.place(relx=0, rely=0, relwidth=1, y=0, height=20)
        bottom_overlay.place(relx=0, rely=1, relwidth=1, anchor="sw", height=20)

        for widget in (top_overlay, bottom_overlay):
            widget.lower()

    def open_high_scores(self):
        HighScores(self.root)


if __name__ == "__main__":
    root = tk.Tk()
    launcher = MainLauncher(root)
    root.mainloop()
