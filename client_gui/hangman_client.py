import tkinter as tk
from tkinter import messagebox
import requests


class WordGuessGameGUI:
    def __init__(self, root,server_url):
        self.root = root
        self.root.title("Word Guess Game")
        self.api_url = server_url
        self.word_length = 0
        self.score = 0

        self.create_widgets()
        self.start_game()

    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(self.root, text="Word Guess Game", font=("Arial", 20, "bold"))
        self.title_label.pack(pady=10)

        # Display word with dashes
        self.word_label = tk.Label(self.root, text="", font=("Arial", 18))
        self.word_label.pack(pady=10)

        # Input for guessing a letter
        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=5)

        self.letter_label = tk.Label(self.input_frame, text="Enter a letter:", font=("Arial", 14))
        self.letter_label.grid(row=0, column=0, padx=5)

        self.letter_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=5)
        self.letter_entry.grid(row=0, column=1, padx=5)

        self.submit_button = tk.Button(self.input_frame, text="Submit", font=("Arial", 14), command=self.guess_letter)
        self.submit_button.grid(row=0, column=2, padx=5)

        # Feedback label
        self.feedback_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.feedback_label.pack(pady=5)

        # Stats frame
        self.stats_frame = tk.Frame(self.root)
        self.stats_frame.pack(pady=10)

        self.score_label = tk.Label(self.stats_frame, text=f"Score: {self.score}", font=("Arial", 14))
        self.score_label.grid(row=0, column=0, padx=10)

        self.guessed_label = tk.Label(self.stats_frame, text="Guessed: None", font=("Arial", 14))
        self.guessed_label.grid(row=0, column=1, padx=10)

    def log_debug(self, message):
        """Log debugging information to the console."""
        print(f"[DEBUG] {message}")

    def start_game(self):
        """Start a new game by calling the API."""
        self.log_debug("Starting a new game...")
        response = requests.get(f"{self.api_url}/start")
        if response.status_code == 200:
            data = response.json()
            self.word_length = data["word_length"]
            self.score = 0
            self.word_label.config(text="_ " * self.word_length)
            self.feedback_label.config(text="")
            self.score_label.config(text=f"Score: {self.score}")
            self.guessed_label.config(text="Guessed: None")
            self.log_debug(f"Game started successfully: Word length = {self.word_length}")
        else:
            messagebox.showerror("Error", "Failed to start the game.")
            self.log_debug(f"Error starting game: {response.status_code}, {response.text}")

    def guess_letter(self):
        """Send the guessed letter to the API and update the GUI."""
        letter = self.letter_entry.get().upper()
        self.letter_entry.delete(0, tk.END)

        self.log_debug(f"Sending guess to API: Letter = {letter}")
        response = requests.post(f"{self.api_url}/guess", json={"letter": letter})
        if response.status_code == 200:
            data = response.json()
            self.log_debug(f"API Response: {data}")

            if "error" in data:
                self.feedback_label.config(text=data["error"])
                self.log_debug(f"Error from API: {data['error']}")
                return

            self.word_label.config(text=data["displayed_word"])
            self.score = data["score"]
            self.feedback_label.config(
                text="Correct!" if data["correct"] else "Incorrect!"
            )
            self.score_label.config(text=f"Score: {self.score}")
            self.guessed_label.config(text=f"Guessed: {', '.join(letter.upper() for letter in data.get('guessed_letters', []))}")

            if data["game_over"]:
                messagebox.showinfo("Game Over", data["message"])
                self.start_game()
        else:
            messagebox.showerror("Error", "Failed to process the guess.")
            self.log_debug(f"Error processing guess: {response.status_code}, {response.text}")


def launch_game(server_url):
    root = tk.Tk()
    WordGuessGameGUI(root, server_url)
    root.mainloop()
