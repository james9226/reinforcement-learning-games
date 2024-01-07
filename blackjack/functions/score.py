from blackjack.data.constants import CARD_VALUE_MAP


def calculate_score(hand: list[int]) -> int:
    score = sum(CARD_VALUE_MAP.get(card, 0) for card in hand)

    num_aces = hand.count(1)

    while num_aces > 0 and score > 21:
        score -= 10
        num_aces -= 1

    return score
