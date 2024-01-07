from blackjack.data.constants import CARD_VALUE_MAP


class BlackJackHand:
    def __init__(self, initial_hand: list[int]):
        self.hand = initial_hand

    def get_score(self) -> int:
        score = sum(CARD_VALUE_MAP.get(card, 0) for card in self.hand)

        num_aces = self.hand.count(1)

        while num_aces > 0 and score > 21:
            score -= 10
            num_aces -= 1

        return score

    def get_first_card(self) -> int:
        return self.hand[0]

    def has_ace(self) -> int:
        return int(1 in self.hand)

    def is_charlie(self) -> bool:
        return len(self.hand) >= 7

    def is_bust(self) -> bool:
        return self.get_score() > 21

    def __repr__(self):
        print(self.hand)
