from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# Game state
sequence = []
player_sequence = []
colors = ['red', 'blue', 'green', 'yellow']
score = 0
current_step = 0


@app.route('/start', methods=['POST'])
def start_game():
    global sequence, player_sequence, score, current_step
    sequence = []
    player_sequence = []
    score = 0
    current_step = 0
    return jsonify({"message": "Game started", "score": score})


@app.route('/sequence', methods=['GET'])
def get_sequence():
    global sequence, current_step
    color = random.choice(colors)
    sequence.append(color)
    current_step = 0
    return jsonify({"sequence": sequence})


@app.route('/check', methods=['POST'])
def check_input():
    global sequence, player_sequence, score, current_step
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
        return jsonify({"result": "wrong", "score": score})


@app.route('/score', methods=['GET'])
def get_score():
    global score
    return jsonify({"score": score})


if __name__ == '__main__':
    app.run(debug=True, port=5003)
