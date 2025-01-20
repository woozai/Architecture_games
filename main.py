import tkinter as tk
import threading
from client_gui.card_matching_client import launch_game as launch_memory_game
from client_gui.simon_client import launch_game as launch_simon_game
from client_gui.mastermind_client import launch_game as launch_mastermind_game
from client_gui.hit_2048_client import launch_game as launch_2048_game
from client_gui.hangman_client import launch_game as launch_hangman_game

GAMES = [
    {"name": "2048 Game", "server_url": "http://127.0.0.1:5000", "launcher": launch_2048_game},
    {"name": "Memory Game", "server_url": "http://127.0.0.1:5001", "launcher": launch_memory_game},
    {"name": "Mastermind Game", "server_url": "http://127.0.0.1:5002", "launcher": launch_mastermind_game},
    {"name": "Simon Game", "server_url": "http://127.0.0.1:5003", "launcher": launch_simon_game},
    {"name": "Hangman game", "server_url": "http://127.0.0.1:5004", "launcher": launch_hangman_game},
]


class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")

        tk.Label(root, text="Select a Game to Play", font=("Helvetica", 16)).pack(pady=10)

        self.buttons = {}
        self.running_games = {}

        for game in GAMES:
            btn = tk.Button(root, text=game["name"], font=("Helvetica", 14),
                            command=lambda g=game: self.start_game(g))
            btn.pack(pady=5)
            self.buttons[game["name"]] = btn  # Store the button for each game

    def start_game(self, game):
        # Disable the button to prevent re-launching
        self.buttons[game["name"]].config(state=tk.DISABLED)

        # Start the game in a separate thread
        threading.Thread(target=self.run_game, args=(game,), daemon=True).start()

    def run_game(self, game):
        self.running_games[game["name"]] = True
        try:
            game["launcher"](game["server_url"])  # Launch the game
        except Exception as e:
            print(f"Error launching game: {e}")
        finally:
            # Re-enable the button when the game closes
            self.running_games.pop(game["name"], None)
            self.buttons[game["name"]].config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()
    launcher = MainLauncher(root)
    root.mainloop()
