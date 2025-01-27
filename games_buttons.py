import tkinter as tk
from tkinter import ttk, messagebox
import threading
from client_gui.card_matching_client import launch_game as launch_memory_game
from client_gui.simon_client import launch_game as launch_simon_game
from client_gui.mastermind_client import launch_game as launch_mastermind_game
from client_gui.hit_2048_client import launch_game as launch_2048_game
from client_gui.hangman_client import launch_game as launch_hangman_game

GAMES = [
    {"name": "2048 Game", "description": "Merge tiles to reach 2048.", "server_url": "http://localhost:31001", "launcher": launch_2048_game},
    {"name": "Memory Game", "description": "Match pairs of cards.", "server_url": "http://localhost:31002", "launcher": launch_memory_game},
    {"name": "Hangman Game", "description": "Guess the word before time runs out.", "server_url": "http://localhost:80", "launcher": launch_hangman_game},
    {"name": "Mastermind Game", "description": "Crack the color code.", "server_url": "http://localhost:90", "launcher": launch_mastermind_game},
    {"name": "Simon Game", "description": "Follow the color sequence.", "server_url": "http://localhost:31005", "launcher": launch_simon_game},
]


class GameButtons(tk.Frame):
    def __init__(self, parent, name_var):
        super().__init__(parent, bg="#2c3e50")
        self.name_var = name_var
        self.buttons = {}
        self.running_games = {}

        # Style for labels and buttons
        self.style = ttk.Style()
        self.style.configure(
            "Colorful.TButton",
            font=("Helvetica", 16, "bold"),  # Made text bold
            padding=15,
            background="#e74c3c",  # Red background
            foreground="#2c3e50",  # Darker text color
            borderwidth=2,
        )
        self.style.map(
            "Colorful.TButton",
            background=[("active", "#c0392b"), ("disabled", "#7f8c8d")],
            foreground=[("active", "#ecf0f1"), ("disabled", "#bdc3c7")],
        )

        for game in GAMES:
            frame = tk.Frame(self, bg="#34495e", padx=20, pady=15)  # Bigger padding for frame
            frame.pack(fill=tk.X, pady=10)

            # Sub-frame for labels
            label_frame = tk.Frame(frame, bg="#34495e")
            label_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            label_name = tk.Label(
                label_frame, text=game["name"], font=("Helvetica", 18, "bold"),  # Larger font
                bg="#34495e", fg="#ecf0f1"
            )
            label_name.pack(anchor="w", pady=5)  # Added padding between labels

            label_desc = tk.Label(
                label_frame, text=game["description"], font=("Helvetica", 14),  # Larger font
                bg="#34495e", fg="#bdc3c7"
            )
            label_desc.pack(anchor="w", pady=5)

            # More colorful button aligned to the right
            btn = ttk.Button(
                frame, text="Launch Game", style="Colorful.TButton",
                command=lambda g=game: self.start_game(g)
            )
            btn.pack(side=tk.RIGHT, padx=15, pady=10)  # More padding for buttons

            self.buttons[game["name"]] = btn

    def start_game(self, game):
        player_name = self.name_var.get().strip()
        if not player_name:
            messagebox.showwarning("Name Required", "Please enter your name before selecting a game.")
            return

        # Disable the button to prevent re-launching
        self.buttons[game["name"]].state(["disabled"])

        # Start the game in a separate thread
        threading.Thread(target=self.run_game, args=(game, player_name), daemon=True).start()

    def run_game(self, game, player_name):
        self.running_games[game["name"]] = True
        try:
            print(f"Launching {game['name']} for player: {player_name}")
            game["launcher"](game["server_url"], player_name)  # Launch the game
        except Exception as e:
            print(f"Error launching game: {e}")
        finally:
            # Re-enable the button when the game closes
            self.running_games.pop(game["name"], None)
            self.buttons[game["name"]].state(["!disabled"])
