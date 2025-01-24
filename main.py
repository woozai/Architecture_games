import tkinter as tk
from tkinter import ttk
import threading
from client_gui.card_matching_client import launch_game as launch_memory_game
from client_gui.simon_client import launch_game as launch_simon_game
from client_gui.mastermind_client import launch_game as launch_mastermind_game
from client_gui.hit_2048_client import launch_game as launch_2048_game
from client_gui.hangman_client import launch_game as launch_hangman_game

GAMES = [
    {"name": "2048 Game", "server_url": "http://localhost:5000", "launcher": launch_2048_game},
    {"name": "Memory Game", "server_url": "http://localhost:5001", "launcher": launch_memory_game},
    {"name": "Mastermind Game", "server_url": "http://localhost:5002", "launcher": launch_mastermind_game},
    {"name": "Simon Game", "server_url": "http://localhost:5003", "launcher": launch_simon_game},
    {"name": "Hangman Game", "server_url": "http://localhost:5004", "launcher": launch_hangman_game},
]


class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")
        self.root.geometry("550x700")
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

        self.buttons = {}
        self.running_games = {}

        # Style for buttons
        self.style = ttk.Style()
        self.style.configure("Rounded.TButton", font=("Helvetica", 14), padding=10, relief="flat", background="#1abc9c",
                             foreground="#2c3e50", borderwidth=1)
        self.style.map("Rounded.TButton",
                       background=[("active", "#16a085")],
                       foreground=[("active", "#ffffff")],
                       relief=[("pressed", "groove")])

        # Game buttons
        button_frame = tk.Frame(root, bg="#2c3e50")
        button_frame.pack(pady=10)
        for game in GAMES:
            btn = ttk.Button(button_frame, text=game["name"], style="Rounded.TButton",
                             command=lambda g=game: self.start_game(g))
            btn.pack(pady=10, ipadx=20, ipady=5, fill=tk.X)
            self.buttons[game["name"]] = btn

    def start_game(self, game):
        player_name = self.name_var.get().strip()
        if not player_name:
            tk.messagebox.showwarning("Name Required", "Please enter your name before selecting a game.")
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


if __name__ == "__main__":
    root = tk.Tk()
    launcher = MainLauncher(root)
    root.mainloop()
