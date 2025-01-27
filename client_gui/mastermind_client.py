import tkinter as tk
import requests

class MastermindGame:
    # server_url = "http://127.0.0.1:5000"

    def __init__(self, root, server, username):
        self.root = root
        self.server_url = server
        self.username = username
        self.root.title("Mastermind Game")
        self.root.geometry("500x700")
        self.root.resizable(False, False)
        self.colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
        self.code_length = 4
        self.current_guess = []
        self.game_id = None
        self.setup_gui()



    def setup_gui(self):
        self.message_label = tk.Label(self.root, text="Press Start to begin the game.", font=("Arial", 12))
        self.message_label.pack(pady=5)

        self.current_guess_display = []
        guess_frame = tk.Frame(self.root)
        guess_frame.pack(pady=5)

        for _ in range(self.code_length):
            btn = tk.Label(guess_frame, bg="white", width=4, height=2, relief="solid")
            btn.pack(side="left", padx=5)
            self.current_guess_display.append(btn)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        self.color_buttons = []
        for color in self.colors:
            btn = tk.Button(button_frame, bg=color, width=8, height=2, command=lambda c=color: self.add_color_to_guess(c))
            btn.pack(side="left", padx=5)
            self.color_buttons.append(btn)

        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=10)

        self.submit_button = tk.Button(action_frame, text="Submit Guess", font=("Arial", 10), command=self.submit_guess)
        self.submit_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(action_frame, text="Clear", font=("Arial", 10), command=self.clear_guess)
        self.clear_button.pack(side="left", padx=5)

        self.start_button = tk.Button(action_frame, text="Start Game", font=("Arial", 10), command=self.start_game)
        self.start_button.pack(side="left", padx=5)

        self.history_container = tk.Frame(self.root)
        self.history_container.pack(pady=10, fill="both", expand=True)

    def start_game(self):
        payload = {"username": self.username}
        response = requests.post(f"{self.server_url}/start", json=payload)
        if response.status_code == 201:
            self.enable_buttons()
            data = response.json()
            print(data)
            self.game_id = data['game_id']
            self.message_label.config(text=data['message'])
            self.clear_guess()
            for widget in self.history_container.winfo_children():
                widget.destroy()
        else:
            self.message_label.config(text="Error starting the game. Try again.")

    def submit_guess(self):
        # Validate if the game is initialized and the guess is of the correct length
        if not self.game_id or len(self.current_guess) != self.code_length:
            self.message_label.config(text=f"Please complete your guess with {self.code_length} colors.")
            return

        # Check for repeated colors in the guess
        if len(set(self.current_guess)) != len(self.current_guess):
            self.message_label.config(text="Your guess must not contain repeated colors.")
            return

        try:
            # Submit the guess to the server
            response = requests.post(
                f"{self.server_url}/guess",
                json={'game_id': self.game_id, 'guess': self.current_guess}
            )

            if response.status_code == 200:
                data = response.json()
                if data['result'] == 'win':
                    self.message_label.config(text=f"Congratulations! You won in {data['attempts']} attempts!")
                    self.disable_buttons()
                elif data['result'] == 'lose':
                    self.message_label.config(text=f"Game Over! The correct code was: {', '.join(data['secret_code'])}")
                    self.disable_buttons()
                else:
                    self.add_guess_to_history(self.current_guess, data['black_pegs'], data['white_pegs'])
                    self.message_label.config(text=f"Black: {data['black_pegs']}, White: {data['white_pegs']}")
                    self.clear_guess()
            else:
                self.message_label.config(text=f"Error submitting the guess: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.message_label.config(text=f"Network error: {e}")

    def add_guess_to_history(self, guess, black_pegs, white_pegs):
        history_row = tk.Frame(self.history_container)
        history_row.pack(fill="x", pady=5)
        for color in guess:
            tk.Label(history_row, bg=color, width=4, height=2, relief="solid").pack(side="left", padx=2)
        tk.Label(history_row, text=f"Black: {black_pegs}, White: {white_pegs}", font=("Arial", 10)).pack(side="left", padx=10)

    def clear_guess(self):
        self.current_guess = []
        for btn in self.current_guess_display:
            btn.config(bg="white")

    def add_color_to_guess(self, color):
        if len(self.current_guess) < self.code_length:
            self.current_guess.append(color)
            self.current_guess_display[len(self.current_guess) - 1].config(bg=color)

    def disable_buttons(self):
        for btn in self.color_buttons:
            btn.config(state=tk.DISABLED)
        self.submit_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.DISABLED)
    def enable_buttons(self):
        for btn in self.color_buttons:
            btn.config(state=tk.NORMAL)
        self.submit_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.NORMAL)

def launch_game(server,username):
    root = tk.Tk()
    app = MastermindGame(root, server, username)
    app.disable_buttons()
    root.mainloop()
