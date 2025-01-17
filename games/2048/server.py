from flask import Flask, request, jsonify
import random

app = Flask(__name__)

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.board = [[0] * size for _ in range(size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_tiles = [(r, c) for r in range(self.size) for c in range(self.size) if self.board[r][c] == 0]
        if empty_tiles:
            r, c = random.choice(empty_tiles)
            self.board[r][c] = 2 if random.random() < 0.9 else 4

    def slide_and_merge_row(self, row):
        new_row = [value for value in row if value != 0]
        for i in range(len(new_row) - 1):
            if new_row[i] == new_row[i + 1]:
                new_row[i] *= 2
                self.score += new_row[i]
                new_row[i + 1] = 0
        new_row = [value for value in new_row if value != 0]
        while len(new_row) < self.size:
            new_row.append(0)
        return new_row

    def move_left(self):
        for r in range(self.size):
            self.board[r] = self.slide_and_merge_row(self.board[r])

    def move_right(self):
        for r in range(self.size):
            self.board[r] = list(reversed(self.slide_and_merge_row(reversed(self.board[r]))))

    def move_up(self):
        for c in range(self.size):
            column = [self.board[r][c] for r in range(self.size)]
            new_column = self.slide_and_merge_row(column)
            for r in range(self.size):
                self.board[r][c] = new_column[r]

    def move_down(self):
        for c in range(self.size):
            column = [self.board[r][c] for r in range(self.size)]
            new_column = list(reversed(self.slide_and_merge_row(reversed(column))))
            for r in range(self.size):
                self.board[r][c] = new_column[r]

    def can_move(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.board[r][c] == 0:
                    return True
                if c < self.size - 1 and self.board[r][c] == self.board[r][c + 1]:
                    return True
                if r < self.size - 1 and self.board[r][c] == self.board[r + 1][c]:
                    return True
        return False

game = Game2048()

@app.route('/new_game', methods=['POST'])
def new_game():
    global game
    game = Game2048()
    return jsonify({"board": game.board, "score": game.score})

@app.route('/move', methods=['POST'])
def move():
    direction = request.json.get('direction')
    if direction == 'left':
        game.move_left()
    elif direction == 'right':
        game.move_right()
    elif direction == 'up':
        game.move_up()
    elif direction == 'down':
        game.move_down()
    else:
        return jsonify({"error": "Invalid direction"}), 400
    game.add_new_tile()
    return jsonify({"board": game.board, "score": game.score, "can_move": game.can_move()})

@app.route('/state', methods=['GET'])
def state():
    return jsonify({"board": game.board, "score": game.score, "can_move": game.can_move()})

if __name__ == '__main__':
    app.run(debug=True)
