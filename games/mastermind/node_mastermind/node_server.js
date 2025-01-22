const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Configuration
const colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple'];
const codeLength = 4;
const maxAttempts = 20;
const gameData = {};

// Generate a secret code
function generateSecretCode() {
  return Array.from({ length: codeLength }, () =>
    colors[Math.floor(Math.random() * colors.length)]
  );
}

// Start a new game
app.post("/start", (req, res) => {
  const gameId = Object.keys(gameData).length + 1;
  const secretCode = generateSecretCode();
  gameData[gameId] = {
    secret_code: secretCode,
    attempts: 0,
    max_attempts: maxAttempts,
    finished: false,
  };
  console.log(`Game ${gameId} started:`, secretCode); // Debug
  res.status(201).json({ game_id: gameId, message: "Game started!" });
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
    console.log(`Game ${game_id} won in ${game.attempts} attempts.`); // Debug
    return res.json({
      result: "win",
      black_pegs: blackPegs,
      white_pegs: whitePegs,
      attempts: game.attempts,
    });
  }

  if (game.attempts >= maxAttempts) {
    game.finished = true;
    console.log(`Game ${game_id} lost. Secret code:`, secretCode); // Debug
    return res.json({
      result: "lose",
      secret_code: secretCode,
      black_pegs: blackPegs,
      white_pegs: whitePegs,
    });
  }

  console.log(`Game ${game_id} ongoing. Attempts: ${game.attempts}.`); // Debug
  res.json({
    result: "ongoing",
    black_pegs: blackPegs,
    white_pegs: whitePegs,
    attempts: game.attempts,
  });
});

const PORT = 5002;
app.listen(PORT, () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});
