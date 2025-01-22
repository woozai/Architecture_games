const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.json());

// Word list and game state
const wordList = [
  "python", "wizard", "dragon", "quest", "magic",
  "castle", "grimoire", "phantom", "sorcery", "charm",
  "oracle", "alchemy", "rune", "spell", "wand"
];

const gameState = {
  target_word: wordList[Math.floor(Math.random() * wordList.length)].toUpperCase(),
  guesses: [],
  attempts: 0,
  score: 0,
};

// Endpoint to start/restart the game
app.get("/start", (req, res) => {
  gameState.target_word = wordList[Math.floor(Math.random() * wordList.length)].toUpperCase();
  gameState.guesses = [];
  gameState.attempts = 0;
  gameState.score = 0;
  console.log("Game started: ", gameState.target_word); // Debug
  res.json({ message: "Game started", word_length: gameState.target_word.length });
});

// Endpoint to handle a letter guess
app.post("/guess", (req, res) => {
  const { letter } = req.body;
  console.log("Received guess: ", letter); // Debug

  if (!letter || typeof letter !== "string" || letter.length !== 1 || !/^[a-zA-Z]$/.test(letter)) {
    console.log("Invalid input."); // Debug
    return res.status(400).json({ error: "Invalid input. Please send a single letter." });
  }

  const upperLetter = letter.toUpperCase();

  if (gameState.guesses.includes(upperLetter)) {
    console.log(`Letter '${upperLetter}' already guessed.`); // Debug
    return res.status(400).json({ error: `You already guessed '${upperLetter}'.` });
  }

  gameState.guesses.push(upperLetter);
  gameState.attempts += 1;

  let correct = false;
  if (gameState.target_word.includes(upperLetter)) {
    gameState.score += 4 + gameState.target_word.length; // Add points for correct guess
    correct = true;
    console.log(`Correct guess: '${upperLetter}'.`); // Debug
  } else {
    gameState.score -= 2 + gameState.target_word.length; // Deduct points for incorrect guess
    console.log(`Incorrect guess: '${upperLetter}'.`); // Debug
  }

  // Prepare the displayed word with guessed letters
  const displayed_word = gameState.target_word
    .split("")
    .map((char) => (gameState.guesses.includes(char) ? char : "_"))
    .join(" ");

  const game_over = !displayed_word.includes("_");

  console.log("Current game state:", { displayed_word, attempts: gameState.attempts, score: gameState.score, game_over }); // Debug

  res.json({
    correct,
    displayed_word: displayed_word,
    attempts: gameState.attempts,
    score: gameState.score,
    game_over: game_over,
    guessed_letters: gameState.guesses, // Include guessed letters in the response
    message: game_over ? "Congratulations! You won!" : "",
  });
});

const PORT = 5004;
app.listen(PORT, () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});
