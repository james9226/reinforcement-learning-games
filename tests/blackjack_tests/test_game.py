import pytest

from blackjack.game import BlackJackEnv


@pytest.fixture
def blackjack_env():
    env = BlackJackEnv()
    env.reset()
    return env


def test_initialization(blackjack_env):
    assert blackjack_env.action_space.n == 2, "Action space should be 2 (hit or stick)"
    assert len(blackjack_env.player.hand) == 2, "Player should start with 2 cards"
    assert len(blackjack_env.dealer.hand) == 1, "Dealer should start with 1 card"


def test_reset(blackjack_env):
    blackjack_env.step(1)  # Change the state of the environment
    obs, _ = blackjack_env.reset()
    assert len(blackjack_env.player.hand) == 2, "Player should have 2 cards after reset"
    assert len(blackjack_env.dealer.hand) == 1, "Dealer should have 1 card after reset"
    assert (
        blackjack_env.player.get_score() <= 21
    ), "Player score should be 21 or less after reset"
    assert (
        blackjack_env.dealer.get_score() <= 21
    ), "Dealer score should be 21 or less after reset"


# Additional tests can be added to cover more scenarios and edge cases.
