const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Configuration
const colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple'];
const codeLength = 4;
const maxAttempts = 100;
const gameData = {};

// Generate a secret code without duplicates
function generateSecretCode() {
  const shuffledColors = colors.sort(() => 0.5 - Math.random());
  return shuffledColors.slice(0, codeLength);
}

// Start a new game
app.post("/start", (req, res) => {
  const { username } = req.body;

  if (!username) {
    return res.status(400).json({ error: "Username is required" });
  }

  const gameId = Object.keys(gameData).length + 1;
  const secretCode = generateSecretCode();
  gameData[gameId] = {
    username: username,
    secret_code: secretCode,
    attempts: 0,
    max_attempts: maxAttempts,
    finished: false,
  };
  console.log(`Game ${gameId} started for user ${username}:`, secretCode); // Debug
  res.status(201).json({ game_id: gameId, username: username, message: "Game started!" });
});

// Make a guess
app.post("/guess", (req, res) => {
  const { game_id, guess } = req.body;

  if (!game_id || !guess || guess.length !== codeLength) {
    console.log("Invalid game ID or guess."); // Debug
    return res.status(400).json({ error: "Invalid game ID or guess" });
  }

  const game = gameData[game_id];
  if (!game || game.finished) {
    console.log("Invalid or finished game."); // Debug
    return res.status(400).json({ error: "Invalid or finished game" });
  }

  game.attempts += 1;

  const secretCode = game.secret_code;
  const blackPegs = guess.reduce(
    (count, color, index) => count + (color === secretCode[index] ? 1 : 0),
    0
  );
  const whitePegs =
    guess.reduce((count, color) => count + Math.min(
      guess.filter(g => g === color).length,
      secretCode.filter(s => s === color).length
    ), 0) - blackPegs;

  if (blackPegs === codeLength) {
    game.finished = true;
    console.log(`Game ${game_id} won by ${game.username} in ${game.attempts} attempts.`); // Debug
    const payload = {
    username: game.username,
    score: game.attempts,
    game_name: "mastermind",
  };

  // Send the score submission request
  fetch("http://host.docker.internal:31010/submit_score", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  })
    .then((response) => {
      if (response.status === 201) {
        console.log("Score submitted successfully!");
      } else {
        response.json().then((error) => {
          console.error(`Failed to submit score: ${response.status}`, error);
        });
      }
    })
    .catch((error) => {
      console.error("Error submitting score:", error);
    });
    return res.json({
      result: "win",
      username: game.username,
      black_pegs: blackPegs,
      white_pegs: whitePegs,
      attempts: game.attempts,
    });
  }

  if (game.attempts >= maxAttempts) {
    game.finished = true;
    console.log(`Game ${game_id} lost by ${game.username}. Secret code:`, secretCode); // Debug
    return res.json({
      result: "lose",
      username: game.username,
      secret_code: secretCode,
      black_pegs: blackPegs,
      white_pegs: whitePegs,
    });
  }

  console.log(`Game ${game_id} ongoing for ${game.username}. Attempts: ${game.attempts}.`); // Debug
  res.json({
    result: "ongoing",
    username: game.username,
    black_pegs: blackPegs,
    white_pegs: whitePegs,
    attempts: game.attempts,
  });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});
