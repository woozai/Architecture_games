const express = require("express");
const bodyParser = require("body-parser");

// Initialize the app
const app = express();
app.use(bodyParser.json());

// Word list and game state
const wordList = [
  "python", "wizard", "dragon", "quest", "magic",
  "castle", "grimoire", "phantom", "sorcery", "charm",
  "oracle", "alchemy", "rune", "spell", "wand"
];

let gameState = {
  targetWord: wordList[Math.floor(Math.random() * wordList.length)].toUpperCase(),
  guesses: [],
  attempts: 0,
  score: 0,
};

// Start a new game
app.get("/start", (req, res) => {
  gameState.targetWord = wordList[Math.floor(Math.random() * wordList.length)].toUpperCase();
  gameState.guesses = [];
  gameState.attempts = 0;
  gameState.score = 0;

  res.json({
    message: "Game started",
    wordLength: gameState.targetWord.length
  });
});

// Handle a letter guess
app.post("/guess", (req, res) => {
  const { letter } = req.body;

  if (!letter || typeof letter !== "string" || letter.length !== 1 || !/^[a-zA-Z]$/.test(letter)) {
    return res.status(400).json({ error: "Invalid input. Please send a single letter." });
  }

  const upperLetter = letter.toUpperCase();

  if (gameState.guesses.includes(upperLetter)) {
    return res.status(400).json({ error: `You already guessed '${upperLetter}'.` });
  }

  gameState.guesses.push(upperLetter);
  gameState.attempts += 1;

  let correct = false;
  if (gameState.targetWord.includes(upperLetter)) {
    gameState.score += 4 + gameState.targetWord.length; // Add points for correct guess
    correct = true;
  } else {
    gameState.score -= 2 + gameState.targetWord.length; // Deduct points for incorrect guess
  }

  // Prepare the displayed word
  const displayedWord = gameState.targetWord
    .split("")
    .map(letter => (gameState.guesses.includes(letter) ? letter : "_"))
    .join(" ");

  const gameOver = !displayedWord.includes("_");

  res.json({
    correct,
    displayedWord,
    attempts: gameState.attempts,
    score: gameState.score,
    gameOver,
    guessedLetters: gameState.guesses,
    message: gameOver ? "Congratulations! You won!" : ""
  });
});

// Start the server
const PORT = 5004;
app.listen(PORT, () => {
  console.log(`Server is running on http://0.0.0.0:${PORT}`);
});
