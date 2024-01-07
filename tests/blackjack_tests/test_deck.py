import pytest

from blackjack.models.deck import BlackJackDeck


def test_deck_initialization():
    single_deck = BlackJackDeck()
    assert len(single_deck.deck) == 52, "A single deck should contain 52 cards"

    multiple_decks = BlackJackDeck(num_decks=2)
    assert len(multiple_decks.deck) == 104, "Two decks should contain 104 cards"


def test_deck_shuffle():
    deck1 = BlackJackDeck(seed=42)
    deck2 = BlackJackDeck(seed=42)
    assert (
        deck1.deck != list(range(1, 13)) * 4
    ), "Deck should not be in order after shuffling"
    assert (
        deck1.deck == deck2.deck
    ), "Decks initialized with the same seed should be shuffled identically"


def test_deal_cards():
    deck = BlackJackDeck()
    initial_deck_size = len(deck.deck)
    dealt_cards = deck.deal(5)
    assert len(dealt_cards) == 5, "Deal should return the requested number of cards"
    assert (
        len(deck.deck) == initial_deck_size - 5
    ), "Deck size should decrease by the number of dealt cards"
    assert all(
        card in range(1, 13) for card in dealt_cards
    ), "All dealt cards should be valid"


def test_deal_from_empty_deck():
    deck = BlackJackDeck()
    deck.deal(len(deck.deck))  # Deal all cards
    with pytest.raises(IndexError):
        deck.deal(1)  # Attempt to deal from an empty deck
