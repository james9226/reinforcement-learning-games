from typing import Any, Optional
import gymnasium as gym

from blackjack.models.deck import BlackJackDeck
from blackjack.models.hand import BlackJackHand


class BlackJackEnv(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(2)  # 0 -> stick, 1 -> hit

        self.observation_space = gym.spaces.Dict(
            {
                "Dealer": gym.spaces.Discrete(14),
                "PlayerCount": gym.spaces.Discrete(32),
                "PlayerAce": gym.spaces.Discrete(2),
            }
        )

    def get_obs(self) -> dict[str, int]:
        return {
            "Dealer": self.dealer.get_first_card(),
            "PlayerCount": self.player.get_score(),
            "PlayerAce": self.player.has_ace(),
        }

    def reset(
        self, seed: Optional[int] = 0, options: Optional[Any] = None
    ) -> tuple[Any, dict[str, int]]:
        super().reset(seed=seed)
        self.deck = BlackJackDeck(num_decks=1, seed=seed)
        self.dealer = BlackJackHand(self.deck.deal())
        self.player = BlackJackHand(self.deck.deal(2))

        return (None, self.get_obs())
