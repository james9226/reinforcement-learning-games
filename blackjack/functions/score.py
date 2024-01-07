from blackjack.data.constants import CARD_VALUE_MAP


def calculate_score(hand: list[int]) -> int:
    score = sum(CARD_VALUE_MAP.get(card, 0) for card in hand)

    num_aces = sum(1 for card in hand if card == 1)

    if score <= 21:
        return score

    while score > 21 and num_aces > 0:
        num_aces -= 1
        score -= 10
    return score
