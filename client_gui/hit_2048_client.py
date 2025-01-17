import tkinter as tk
import requests


class Game2048GUI:
    def __init__(self, server):
        # self.api_url = "http://127.0.0.1:5000"
        self.api_url = server
        self.window = tk.Tk()
        self.game_over = False  # Initialize game_over flag
        self.window.title("2048 Game")
        self.score_label = tk.Label(self.window, text="Score: 0", font=("Helvetica", 16))
        self.score_label.pack()
        self.grid_frame = tk.Frame(self.window)
        self.grid_frame.pack()
        self.tiles = []
        self.create_grid()
        self.window.bind("<Key>", self.handle_keypress)
        self.start_new_game()

    def create_grid(self):
        for r in range(4):
            row = []
            for c in range(4):
                label = tk.Label(self.grid_frame, text="", width=6, height=3, font=("Helvetica", 20),
                                 bg="lightgray", relief="raised", borderwidth=2, anchor="center")
                label.grid(row=r, column=c, padx=5, pady=5)
                row.append(label)
            self.tiles.append(row)

    def start_new_game(self):
        response = requests.post(f"{self.api_url}/new_game")
        self.update_grid(response.json())

    def handle_keypress(self, event):
        if self.game_over:  # Check if the game is already over
            return  # Do nothing if the game is over

        direction_map = {"w": "up", "a": "left", "s": "down", "d": "right"}
        direction = direction_map.get(event.keysym.lower())
        if direction:
            response = requests.post(f"{self.api_url}/move", json={"direction": direction})
            data = response.json()
            self.update_grid(data)
            if not data.get("can_move"):  # If no more moves are possible
                self.show_game_over()

    def update_grid(self, data):
        self.score_label.config(text=f"Score: {data['score']}")
        for r in range(4):
            for c in range(4):
                value = data['board'][r][c]
                self.tiles[r][c].config(text=str(value) if value != 0 else "",
                                        bg=self.get_tile_color(value))

    def get_tile_color(self, value):
        colors = {
            0: "lightgray",
            2: "#eee4da",
            4: "#ede0c8",
            8: "#f2b179",
            16: "#f59563",
            32: "#f67c5f",
            64: "#f65e3b",
            128: "#edcf72",
            256: "#edcc61",
            512: "#edc850",
            1024: "#edc53f",
            2048: "#edc22e",
        }
        return colors.get(value, "#3c3a32")

    def show_game_over(self):
        if not self.game_over:  # Only allow the popup to appear once
            self.game_over = True  # Set the flag to indicate the game is over
            game_over_window = tk.Toplevel(self.window)
            game_over_window.title("Game Over")
            tk.Label(game_over_window, text="Game Over!", font=("Helvetica", 24)).pack(pady=20)
            tk.Label(game_over_window, text=f"Final Score: {self.score_label.cget('text')}",
                     font=("Helvetica", 16)).pack(pady=10)
            tk.Button(game_over_window, text="Close", command=self.window.quit).pack(pady=10)

    def play(self):
        self.window.mainloop()


def launch_game(server_url):
    game_gui = Game2048GUI(server_url)
    game_gui.play()
