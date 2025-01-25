from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

# Connect to the MongoDB container (mapped to localhost:5005)
client = MongoClient("mongodb://mongodb:27017/")  # Inside the Docker network, MongoDB listens on port 27017
db = client["game_scores_db"]
scores_collection = db["scores"]


@app.route("/submit_score", methods=["POST"])
def submit_score():
    """Receive score updates from games and store them in MongoDB."""
    data = request.json
    username = data.get("username")
    game_name = data.get("game_name")
    score = data.get("score")

    if not username or not game_name or score is None:
        return jsonify({"error": "Invalid data"}), 400

    # Retrieve the existing game or initialize a new structure
    game = scores_collection.find_one({"name": game_name})

    if not game:
        # Initialize new game entry
        game = {
            "name": game_name,
            "score_description": "Highest sequence",
            "scores": []
        }

    # Check if the user already has a score for this game
    user_exists = False
    for player_score in game["scores"]:
        if player_score["player"] == username:
            player_score["score"] = max(player_score["score"], score)
            user_exists = True
            break

    if not user_exists:
        # Add new user score if not already present
        game["scores"].append({"player": username, "score": score})

    # Sort scores in descending order and keep top 10
    game["scores"] = sorted(game["scores"], key=lambda x: x["score"], reverse=True)[:10]

    # Update or insert the game document
    scores_collection.replace_one({"name": game_name}, game, upsert=True)

    return jsonify({"message": "Score submitted successfully!"}), 201


@app.route("/get_scores", methods=["GET"])
def get_all_scores():
    """
    Retrieve all scores from the database.
    """
    # Retrieve all scores from the collection
    scores = list(scores_collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal `_id` field
    print(scores, flush=True)
    return jsonify(scores), 200

@app.route("/clear_data", methods=["DELETE"])
def clear_data():
    """Clear all data in the scores collection."""
    result = scores_collection.delete_many({})
    print(f"Deleted {result.deleted_count} records.", flush=True)
    return jsonify({"message": f"Cleared {result.deleted_count} records."}), 200

@app.route("/get_scores_by_game", methods=["GET"])
def get_scores_by_game():
    """Retrieve scores filtered by game name."""
    game_name = request.args.get("game_name")
    if not game_name:
        return jsonify({"error": "Game name parameter is required."}), 400

    scores = list(scores_collection.find({"game_name": game_name}, {"_id": 0}))  # Filter by game_name
    print(scores, flush=True)
    return jsonify(scores), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5010)
