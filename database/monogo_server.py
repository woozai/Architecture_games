from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime

# Database server using Flask and MongoDB
db_app = Flask(__name__)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")  # Adjust connection string as needed
db = client["game_scores_db"]
scores_collection = db["scores"]

@db_app.route("/upload_score", methods=["POST"])
def upload_score():
    data = request.json
    username = data.get("username")
    gamename = data.get("gamename")
    score = data.get("score")

    if not username or not gamename or score is None:
        return jsonify({"error": "Missing required fields"}), 400

    # Insert the score into the database
    scores_collection.insert_one({
        "username": username,
        "gamename": gamename,
        "score": score,
        "timestamp": datetime.utcnow()
    })

    return jsonify({"message": "Score uploaded successfully"}), 201

if __name__ == "__main__":
    db_app.run(host="0.0.0.0", port=5001)
