import random
import time

class MemoryCardGame:
    def __init__(self, rows=4, cols=7):
        self.rows = rows
        self.cols = cols
        self.cards = []
        self.revealed = set()
        self.matched = set()
        self.start_time = None
        self.score = 0

        self.reset_game()

    def reset_game(self):
        emojis = [
            "\U0001F600", "\U0001F601", "\U0001F602", "\U0001F923",
            "\U0001F604", "\U0001F605", "\U0001F606", "\U0001F607",
            "\U0001F609", "\U0001F60A", "\U0001F60B", "\U0001F60C",
            "\U0001F60D", "\U0001F60E"
        ] * 2
        random.shuffle(emojis)
        self.cards = emojis[:self.rows * self.cols]
        self.revealed = set()
        self.matched = set()
        self.start_time = time.time()
        self.score = 0

    def reveal_card(self, index1, index2):
        if index1 in self.matched or index2 in self.matched:
            return {"error": "Card already matched"}

        if index1 == index2:
            return {"error": "Cannot match the same card"}

        if self.cards[index1] == self.cards[index2]:
            self.matched.update({index1, index2})
            self.score += 10
            return {"match": True, "score": self.score}
        else:
            return {"match": False, "score": self.score}

    def get_game_state(self):
        elapsed_time = int(time.time() - self.start_time)
        return {
            "board": [self.cards[i] if i in self.matched else "?" for i in range(len(self.cards))],
            "revealed": list(self.revealed),
            "matched": list(self.matched),
            "score": self.score,
            "time": elapsed_time
        }
