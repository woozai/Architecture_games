import requests
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Configuration
colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple']
code_length = 4
max_attempts = 100
game_data = {}


def generate_secret_code():
    return random.sample(colors, code_length)


@app.route('/start', methods=['POST'])
def start_game():
    # Get the username from the request body
    data = request.json
    username = data.get("username")
    print(username)
    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Generate a new game ID
    game_id = len(game_data) + 1
    secret_code = generate_secret_code()
    print(secret_code, flush=True)

    # Store the game data with the username
    game_data[game_id] = {
        'username': username,           # Store the username
        'secret_code': secret_code,
        'attempts': 0,
        'max_attempts': max_attempts,
        'finished': False,
    }

    # Return the game ID and success message
    return jsonify({'game_id': game_id, 'username': username, 'message': 'Game started!'}), 201


@app.route('/guess', methods=['POST'])
def make_guess():
    data = request.json
    game_id = data.get('game_id')
    guess = data.get('guess')

    # Validate input
    if not game_id or not guess or len(guess) != code_length:
        return jsonify({'error': 'Invalid game ID or guess'}), 400

    # Ensure no repeated colors in the guess
    if len(set(guess)) != len(guess):
        return jsonify({'error': 'Guess must not contain repeated colors'}), 400

    game = game_data.get(game_id)
    if not game or game['finished']:
        return jsonify({'error': 'Invalid or finished game'}), 400

    game['attempts'] += 1
    secret_code = game['secret_code']
    black_pegs = sum([1 for i in range(code_length) if guess[i] == secret_code[i]])
    white_pegs = sum([min(guess.count(c), secret_code.count(c)) for c in set(colors)]) - black_pegs

    if black_pegs == code_length:
        game['finished'] = True
        payload = {
            "username": game['username'],
            "score": game['attempts'],
            "game_name": "mastermind"
        }
        print(payload, flush=True)
        response = requests.post("http://host.docker.internal:31010/submit_score", json=payload)

        if response.status_code == 201:
            print("Score submitted successfully!")
        else:
            print(f"Failed to submit score: {response.status_code}, {response.json()}")
        return jsonify(
            {'result': 'win', 'black_pegs': black_pegs, 'white_pegs': white_pegs, 'attempts': game['attempts']}
        )

    if game['attempts'] >= max_attempts:
        game['finished'] = True
        return jsonify(
            {'result': 'lose', 'secret_code': secret_code, 'black_pegs': black_pegs, 'white_pegs': white_pegs})

    return jsonify(
        {'result': 'ongoing', 'black_pegs': black_pegs, 'white_pegs': white_pegs, 'attempts': game['attempts']})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)

