from flask import Flask, jsonify, request
import random
import time

app = Flask(__name__)

ROWS, COLS = 4, 7
CARD_IMAGES = [
                  "\U0001F600", "\U0001F601", "\U0001F602", "\U0001F923",
                  "\U0001F604", "\U0001F605", "\U0001F606", "\U0001F607",
                  "\U0001F609", "\U0001F60A", "\U0001F60B", "\U0001F60C",
                  "\U0001F60D", "\U0001F60E"
              ] * 2
random.shuffle(CARD_IMAGES)
CARD_IMAGES = CARD_IMAGES[:ROWS * COLS]

HIGH_SCORE_FILE = "high_score.txt"

game_state = {
    "matched": [],
    "start_time": time.time(),
    "first_selection": None,
    "second_selection": None
}


def read_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    except Exception:
        return None


def write_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


@app.route("/high_score", methods=["GET"])
def get_high_score():
    return jsonify({"high_score": read_high_score()})


@app.route("/reveal_card", methods=["POST"])
def reveal_card():
    x = request.json.get("x")
    y = request.json.get("y")

    if (x, y) in game_state["matched"]:
        return jsonify({"error": "Card already matched"}), 400

    if game_state["first_selection"] is None:
        game_state["first_selection"] = (x, y)
    elif game_state["second_selection"] is None:
        game_state["second_selection"] = (x, y)
        check_match()

    return jsonify({"card": CARD_IMAGES[x * COLS + y]})


def check_match():
    x1, y1 = game_state["first_selection"]
    x2, y2 = game_state["second_selection"]
    if CARD_IMAGES[x1 * COLS + y1] == CARD_IMAGES[x2 * COLS + y2]:
        game_state["matched"].extend([(x1, y1), (x2, y2)])
    game_state["first_selection"] = None
    game_state["second_selection"] = None


@app.route("/reset_game", methods=["POST"])
def reset_game():
    global CARD_IMAGES
    random.shuffle(CARD_IMAGES)
    CARD_IMAGES = CARD_IMAGES[:ROWS * COLS]
    game_state.update({
        "matched": [],
        "start_time": time.time(),
        "first_selection": None,
        "second_selection": None
    })
    return jsonify({"message": "Game reset"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
