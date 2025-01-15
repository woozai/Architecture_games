import tkinter as tk
from requests_games.card_matching_client import launch_game

GAMES = [
    {"name": "Memory Game", "server_url": "http://127.0.0.1:5000"}
]


class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Launcher")

        tk.Label(root, text="Select a Game to Play", font=("Helvetica", 16)).pack(pady=10)

        for game in GAMES:
            btn = tk.Button(root, text=game["name"], font=("Helvetica", 14),
                            command=lambda g=game: self.start_game(g))
            btn.pack(pady=5)

    def start_game(self, game):
        self.root.destroy()  # Close the launcher before starting the game
        launch_game(game["server_url"])


if __name__ == "__main__":
    root = tk.Tk()
    launcher = MainLauncher(root)
    root.mainloop()
