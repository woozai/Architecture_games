import requests
from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Game state
sequence = []
player_sequence = []
colors = ['red', 'blue', 'green', 'yellow']
score = 0
current_step = 0
username = ""


@app.route('/start', methods=['POST'])
def start_game():
    global sequence, player_sequence, score, current_step, username
    data = request.json
    username = data.get("username")
    if not username:
        return jsonify({"error": "Username is required"}), 400
    sequence = []
    player_sequence = []
    score = 0
    current_step = 0
    return jsonify({"message": "Game started", "score": score, "username": username})


@app.route('/sequence', methods=['GET'])
def get_sequence():
    global sequence, current_step
    color = random.choice(colors)
    sequence.append(color)
    current_step = 0
    return jsonify({"sequence": sequence})


@app.route('/check', methods=['POST'])
def check_input():
    global sequence, player_sequence, score, current_step, username
    data = request.json
    color = data.get('color')

    if color is None:
        return jsonify({"error": "No color provided"}), 400

    player_sequence.append(color)
    if player_sequence[current_step] == sequence[current_step]:
        current_step += 1
        if current_step == len(sequence):
            score += 1
            player_sequence = []
            return jsonify({"result": "correct", "score": score})
        return jsonify({"result": "progress"})
    else:
        payload = {
            "username": username,  # Fallback if name isn't set
            "score": score,
            "game_name": "simon"
        }
        print(payload, flush=True)
        response = requests.post("http://proxy_server:5010/submit_score", json=payload)

        if response.status_code == 201:
            print("Score submitted successfully!")
        else:
            print(f"Failed to submit score: {response.status_code}, {response.json()}")
        return jsonify({"result": "wrong", "score": score})


@app.route('/score', methods=['GET'])
def get_score():
    global score
    return jsonify({"score": score})

@app.route('/health', methods=['GET'])
def health_check():
    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5005)
