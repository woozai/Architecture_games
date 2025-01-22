from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Word list and game state
word_list = ["python", "wizard", "dragon", "quest", "magic",
             "castle", "grimoire", "phantom", "sorcery", "charm",
             "oracle", "alchemy", "rune", "spell", "wand"]

game_state = {
    "target_word": random.choice(word_list).upper(),
    "guesses": [],
    "attempts": 0,
    "score": 0,
}

@app.route("/start", methods=["GET"])
def start_game():
    """Reset the game and return initial state."""
    game_state["target_word"] = random.choice(word_list).upper()
    game_state["guesses"] = []
    game_state["attempts"] = 0
    game_state["score"] = 0
    return jsonify({"message": "Game started", "word_length": len(game_state["target_word"])})

@app.route("/guess", methods=["POST"])
def guess_letter():
    """Handle a letter guess."""
    data = request.json
    letter = data.get("letter", "").upper()

    if not letter.isalpha() or len(letter) != 1:
        return jsonify({"error": "Invalid input. Please send a single letter."}), 400

    if letter in game_state["guesses"]:
        return jsonify({"error": f"You already guessed '{letter}'."}), 400

    game_state["guesses"].append(letter)
    game_state["attempts"] += 1

    if letter in game_state["target_word"]:
        game_state["score"] += 4 + len(game_state["target_word"])  # Add points for correct guess
        correct = True
    else:
        game_state["score"] -= 2 + len(game_state["target_word"])  # Deduct points for incorrect guess
        correct = False

    # Prepare response data
    displayed_word = " ".join([l if l in game_state["guesses"] else "_" for l in game_state["target_word"]])
    game_over = "_" not in displayed_word

    return jsonify({
        "correct": correct,
        "displayed_word": displayed_word,
        "attempts": game_state["attempts"],
        "score": game_state["score"],
        "game_over": game_over,
        "guessed_letters": game_state["guesses"],  # Include guessed letters in the response
        "message": "Congratulations! You won!" if game_over else "",
    })


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5004)
