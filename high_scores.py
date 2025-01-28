import json
import tkinter as tk
from tkinter import ttk, messagebox
import requests

class HighScores:
    def __init__(self, root):
        # High scores window
        high_scores_window = tk.Toplevel(root)
        high_scores_window.title("High Scores")
        high_scores_window.geometry("600x400")  # Increased size
        high_scores_window.configure(bg="#34495e")

        # Title label
        title = tk.Label(
            high_scores_window, text="High Scores",
            font=("Helvetica", 22, "bold"), bg="#34495e", fg="#e74c3c"
        )
        title.pack(pady=20)

        # Frame for scrollbar and list
        frame = tk.Frame(high_scores_window, bg="#34495e")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Scrollbar setup
        canvas = tk.Canvas(frame, bg="#34495e", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#34495e")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Fetch and display scores
        try:
            # Simulating a GET request to fetch scores
            score_response = requests.get("http://localhost:31010/get_scores")
            if score_response.status_code == 200:
                data = score_response.json()  # Assuming data contains the list of `games`

                # Directly iterate over the list
                for game in data:
                    # Display game name
                    tk.Label(
                        scrollable_frame,
                        text=f"{game['name']} - {game['score_description']}",
                        font=("Helvetica", 18, "bold"),
                        bg="#34495e",
                        fg="#f1c40f"
                    ).pack(pady=(15, 5), anchor="w")

                    # Create a table for scores
                    score_table = ttk.Treeview(scrollable_frame, columns=("Player", "Score"), show='headings',
                                               height=10)
                    score_table.heading("Player", text="Player", anchor="center")
                    score_table.heading("Score", text="Score", anchor="center")
                    score_table.column("Player", anchor="w", width=200)
                    score_table.column("Score", anchor="center", width=100)

                    # Add player scores to the table
                    for player_score in game['scores']:
                        score_table.insert("", "end", values=(player_score['player'], player_score['score']))

                    score_table.pack(pady=5, anchor="w")
            else:
                tk.Label(
                    scrollable_frame,
                    text="Failed to fetch scores.",
                    font=("Helvetica", 16),
                    bg="#34495e",
                    fg="#e74c3c"
                ).pack(pady=5)
        except Exception as e:
            tk.Label(
                scrollable_frame,
                text=f"Error: {e}",
                font=("Helvetica", 16),
                bg="#34495e",
                fg="#e74c3c"
            ).pack(pady=5)

        # Clear Data Button
        clear_button = tk.Button(
            high_scores_window,
            text="Clear All Data",
            font=("Helvetica", 14),
            bg="#e74c3c",
            fg="#ecf0f1",
            command=self.clear_data
        )
        clear_button.pack(pady=10)

    def clear_data(self):
        try:
            response = requests.delete("http://localhost:31010/clear_data")
            if response.status_code == 200:
                messagebox.showinfo("Success", response.json().get("message", "Data cleared."))
            else:
                messagebox.showerror("Error", f"Failed to clear data: {response.status_code}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    app = HighScores(root)
    root.mainloop()
