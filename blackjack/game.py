import logging
from typing import Any, Optional
import gymnasium as gym

from blackjack.models.deck import BlackJackDeck
from blackjack.models.hand import BlackJackHand

logger = logging.getLogger("BlackJackLogger")


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

    def step(self, action: int):
        match action:
            case 0:  # Dealer play out logic
                while self.dealer.get_score() < 17:
                    self.dealer.hand += self.deck.deal()

                if self.dealer.is_bust():
                    logger.debug("Dealer bust")
                    return self.player_win()
                elif self.dealer.is_charlie():
                    logger.debug("Dealer charlie")
                    return self.dealer_win()
                elif self.player.get_score() < self.dealer.get_score():
                    logger.debug("Dealer has higher score")
                    return self.dealer_win()
                logger.debug("Player has higher score")
                return self.player_win()

            case 1:  # Adding a card logic
                self.player.hand += self.deck.deal()

                if self.player.is_bust():
                    logger.debug("Player bust")
                    return self.dealer_win()

                elif self.player.is_charlie():
                    logger.debug("Player Charlie")
                    return self.player_win()
                else:
                    return self.keep_playing()

            case _:
                raise ValueError("Invalid action passed")

    def render(self):
        logger.debug(
            f"Player Hand : {self.player.hand} with score {self.player.get_score()} \n"
        )
        logger.debug(
            f"Dealer Hand : {self.dealer.hand} with score {self.dealer.get_score()} \n"
        )

    def player_win(self) -> tuple[dict, int, bool, bool, dict]:
        return self.get_obs(), 1, True, False, {}  # Obs, # Reward, # Terminated

    def dealer_win(self) -> tuple[dict, int, bool, bool, dict]:
        return self.get_obs(), -1, True, False, {}  # Obs, # Reward, # Terminated

    def keep_playing(self) -> tuple[dict, int, bool, bool, dict]:
        return self.get_obs(), 0, False, False, {}  # Obs, # Reward, # Terminated

    def get_obs(self) -> dict[str, int]:
        return {
            "Dealer": self.dealer.get_first_card(),
            "PlayerCount": self.player.get_score(),
            "PlayerAce": self.player.has_ace(),
        }

    def reset(
        self, seed: Optional[int] = 0, options: Optional[Any] = None
    ) -> tuple[dict[str, int], Any]:
        super().reset(seed=seed)
        self.deck = BlackJackDeck(num_decks=1, seed=seed)
        self.dealer = BlackJackHand(self.deck.deal())
        self.player = BlackJackHand(self.deck.deal(2))

        return (self.get_obs(), None)  # Returns a tuple of obs and info
