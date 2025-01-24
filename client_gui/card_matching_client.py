import tkinter as tk
import requests
import threading

class MemoryGameClient:
    def __init__(self, root, server_url, username):
        self.root = root
        self.username = username
        self.attempts = 0
        self.server_url = server_url
        self.root.title("Memory Card Game")
        self.buttons = []
        self.first_selection = None
        self.create_ui()

    def create_ui(self):
        # High Score Label
        self.high_score_label = tk.Label(self.root, text=f"Score:{self.attempts}", font=("Helvetica", 16))
        self.high_score_label.grid(row=0, column=0, columnspan=7, pady=10)

        # Reset Button
        self.reset_button = tk.Button(self.root, text="Reset Game", font=("Helvetica", 16), command=self.reset_game)
        self.reset_button.grid(row=0, column=7, padx=10, pady=10)

        # Game Grid
        self.create_grid()

    def create_grid(self):
        for i in range(4):
            row = []
            for j in range(7):
                button = tk.Button(self.root, text="", font=("Helvetica", 20), width=10, height=5,
                                   command=lambda x=i, y=j: self.reveal_card(x, y))
                button.grid(row=i + 1, column=j, padx=5, pady=5)
                row.append(button)
            self.buttons.append(row)

    def reveal_card(self, x, y):
        # Prevent clicking the same square twice
        if self.first_selection is not None and self.first_selection[0] == (x, y):
            return

        # Prevent multiple selections during animations
        if self.first_selection is not None and self.first_selection[1] is None:
            return

        # Request to reveal the card
        response = requests.post(f"{self.server_url}/reveal_card", json={"x": x, "y": y})
        if response.status_code == 200:
            print(response.json())
            card = response.json()["card"]
            self.attempts = response.json()["attempts"]
            self.high_score_label.config(text=f"High Score: {self.attempts}")
            self.buttons[x][y].config(text=card)
            if self.first_selection is None:
                self.first_selection = ((x, y), card)
            else:
                self.handle_second_selection(x, y, card)
        else:
            print("Failed to reveal card:", response.json().get("error"))

    def handle_second_selection(self, x, y, card):
        first_coords, first_card = self.first_selection
        self.first_selection = ((first_coords[0], first_coords[1]), None)

        # Check if cards match
        if first_card == card:
            self.buttons[first_coords[0]][first_coords[1]].config(bg="green", fg="white")
            self.buttons[x][y].config(bg="green", fg="white")
            self.first_selection = None
        else:
            # Hide cards after 1 second if they don't match
            def hide_cards():
                self.buttons[first_coords[0]][first_coords[1]].config(text="", bg="SystemButtonFace")
                self.buttons[x][y].config(text="", bg="SystemButtonFace")
                self.first_selection = None

            threading.Timer(1, hide_cards).start()

    def reset_game(self):
        response = requests.post(f"{self.server_url}/reset_game")
        if response.status_code == 200:
            self.first_selection = None
            self.update_high_score()
            # Reset the grid
            for i in range(4):
                for j in range(7):
                    self.buttons[i][j].config(text="", bg="SystemButtonFace", fg="black")
        else:
            print("Failed to reset game:", response.json().get("error"))




def launch_game(server_url, username):
    root = tk.Tk()
    MemoryGameClient(root, server_url, username)
    root.mainloop()
