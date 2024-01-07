import pytest

from blackjack.models.hand import BlackJackHand


def test_initialization():
    hand = BlackJackHand([10, 5])
    assert hand.hand == [10, 5]


@pytest.mark.parametrize(
    "hand, expected_score",
    [
        ([10, 5], 15),
        ([1, 10], 21),  # Testing an Ace with a face card
        ([1, 9], 20),  # Testing an Ace with a non-face card
        ([10, 10, 2], 22),  # Testing a hand that should be bust
        ([1, 1, 1], 13),  # Testing multiple Aces
    ],
)
def test_get_score(hand: list[int], expected_score: int):
    blackjack_hand = BlackJackHand(hand)
    assert blackjack_hand.get_score() == expected_score


def test_get_first_card():
    hand = BlackJackHand([7, 3])
    assert hand.get_first_card() == 7


def test_has_ace():
    hand_with_ace = BlackJackHand([1, 5])
    hand_without_ace = BlackJackHand([10, 5])
    assert hand_with_ace.has_ace() == 1
    assert hand_without_ace.has_ace() == 0


def test_is_charlie():
    charlie_hand = BlackJackHand([2, 3, 4, 5, 6, 7, 8])
    non_charlie_hand = BlackJackHand([10, 5])
    assert charlie_hand.is_charlie()
    assert not non_charlie_hand.is_charlie()


def test_is_bust():
    bust_hand = BlackJackHand([10, 10, 5])
    safe_hand = BlackJackHand([10, 5])
    assert bust_hand.is_bust()
    assert not safe_hand.is_bust()
