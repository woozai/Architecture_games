import tkinter as tk
import time
import requests
import winsound

class SimonGame:
    def __init__(self, root, server,username ):
        self.root = root
        # self.API_URL = "http://127.0.0.1:5000"
        self.API_URL = server
        self.sequence = []
        self.colors = ['red', 'blue', 'green', 'yellow']
        self.score = 0
        self.username = username
        # Initialize GUI
        self.root.title("Simon Game")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.instructions = tk.Label(self.root, text="Simon Game\nFollow the sequence of colors!", font=("Arial", 16, "bold"))
        self.instructions.pack(pady=10)

        self.message_label = tk.Label(self.root, text="Press Start to begin.", font=("Arial", 14))
        self.message_label.pack(pady=10)

        self.buttons = {}
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        for color in self.colors:
            self.buttons[color] = tk.Button(
                self.button_frame,
                bg=color,
                width=10,
                height=5,
                command=lambda c=color: self.check_input(c)
            )
            if color in ['red', 'blue']:
                self.buttons[color].grid(row=0, column=self.colors.index(color), padx=10, pady=10)
            else:
                self.buttons[color].grid(row=1, column=self.colors.index(color) - 2, padx=10, pady=10)

        self.start_button = tk.Button(self.root, text="Start Game", font=("Arial", 14), command=self.start_game)
        self.start_button.pack(pady=20)

    def start_game(self):
        # Include the username in the request body
        payload = {"username": self.username}
        response = requests.post(f"{self.API_URL}/start", json=payload)

        if response.status_code == 200:
            print(response.json())
            self.message_label.config(text="Game started! Watch closely.")
            self.score = 0
            self.next_round()
        else:
            self.message_label.config(text="Failed to start the game.")
            print(f"Error: {response.status_code}, {response.text}")

    def next_round(self):
        response = requests.get(f"{self.API_URL}/sequence")
        if response.status_code == 200:
            data = response.json()
            self.sequence = data["sequence"]
            self.display_sequence()

    def display_sequence(self):
        self.disable_buttons()
        for index, color in enumerate(self.sequence):
            self.root.after(index * 1000, lambda c=color: self.light_up(c))
        self.root.after(len(self.sequence) * 1000, self.enable_buttons)

    def play_tone(self, color):
        frequencies = {
            "red": 440,    # A4
            "blue": 494,   # B4
            "green": 523,  # C5
            "yellow": 587  # D5
        }
        winsound.Beep(frequencies[color], 500)  # 500 ms tone

    def light_up(self, color):
        self.play_tone(color)  # Play the tone
        self.buttons[color].config(bg='white')
        self.root.update()
        time.sleep(0.5)
        self.buttons[color].config(bg=color)
        self.root.update()

    def check_input(self, color):
        response = requests.post(f"{self.API_URL}/check", json={"color": color})
        self.play_tone(color)  # Play tone when player clicks
        if response.status_code == 200:
            data = response.json()
            if data["result"] == "correct":
                self.score = data["score"]
                self.message_label.config(text=f"Correct! Score: {self.score}")
                self.root.after(1000, self.next_round)
            elif data["result"] == "progress":
                self.message_label.config(text="Good! Keep going!")
            elif data["result"] == "wrong":
                self.message_label.config(text=f"Game Over! Final Score: {self.score}")
                self.disable_buttons()
        else:
            self.message_label.config(text="Error checking input!")

    def enable_buttons(self):
        for btn in self.buttons.values():
            btn.config(state=tk.NORMAL)

    def disable_buttons(self):
        for btn in self.buttons.values():
            btn.config(state=tk.DISABLED)

def launch_game(server, username):
    root = tk.Tk()
    game = SimonGame(root, server, username)
    root.mainloop()
