

from blackjack.functions.score import calculate_score


class BlackJackHand:

    def __init__(self, initial_hand : list[int]):
        self.hand = initial_hand

    def get_score(self) -> int:
        return calculate_score(self.hand) 

    def get_first_card(self) -> int:
        return self.hand[0] 

    def has_ace(self) -> int:
        return int(1 in self.hand) 

    def is_charlie(self) -> bool:
        return len(self.hand) >= 7

    def is_bust(self) -> bool:
        return self.get_score() > 21

    def add_card(self, card : int) -> None:
        self.hand.append(card)