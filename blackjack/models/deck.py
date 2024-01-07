import random
from typing import Optional


class BlackJackDeck:
    def __init__(self, num_decks: int = 1, seed: Optional[int] = None):
        self.deck = list(range(1, 13)) * 4 * num_decks

        if seed:
            random.seed(seed)
        random.shuffle(self.deck)

    def deal(self, num_cards: int = 1) -> list[int]:
        return [self.deck.pop() for i in range(num_cards)]
