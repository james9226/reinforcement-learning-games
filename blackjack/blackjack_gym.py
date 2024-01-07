import random
from typing import Optional
import gymnasium as gym
import logging

from blackjack.data.constants import CARD_VALUE_MAP

logger = logging.getLogger("BlackJackLogger")


def sum_hand(hand: list[int]) -> int:
    score = sum(CARD_VALUE_MAP.get(card) for card in hand)

    num_aces = sum(1 for card in hand if card == 1)

    if score <= 21:
        return score

    while score > 21 and num_aces > 0:
        num_aces -= 1
        score -= 10
    return score


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

    def has_aces(self):
        return int(1 in self.player)

    def step(self, action):
        match action:
            case 0:  # Dealer play out logic
                while sum_hand(self.dealer) < 17:
                    self.dealer.append(random.randint(1, 13))

                dealer_score = sum_hand(self.dealer)

                if dealer_score > 21:
                    logger.debug("Dealer bust")
                    return self.player_win()
                elif len(self.dealer) >= 7:
                    logger.debug("Dealer charlie")
                    return self.dealer_win()
                elif sum_hand(self.player) < dealer_score:
                    logger.debug("Dealer has higher score")
                    return self.dealer_win()
                logger.debug("Player has higher score")
                return self.player_win()

            case 1:  # Adding a card logic
                self.player[self.player_card_count] = random.randint(1, 13)
                self.player_card_count += 1

                score = sum_hand(self.player)
                if score > 21:
                    logger.debug("Player bust")
                    return self.dealer_win()

                elif self.player_card_count >= 7:
                    logger.debug("Player Charlie")
                    return self.player_win()

                else:
                    return self.keep_playing()

            case _:
                raise ValueError("Invalid action passed")

    def render(self):
        logger.debug(
            f"Player Hand : {self.player} with score {sum_hand(self.player)} \n"
        )
        logger.debug(
            f"Dealer Hand : {self.dealer} with score {sum_hand(self.dealer)} \n"
        )

    def get_obs(self) -> dict:
        self.render()
        return {
            "Dealer": self.dealer[0],
            "PlayerCount": sum_hand(self.player),
            "PlayerAce": self.has_aces(),
        }

    def player_win(self) -> dict:
        return self.get_obs(), 1, True, False, {}  # Obs, # Reward, # Terminated

    def dealer_win(self) -> dict:
        return self.get_obs(), -1, True, False, {}  # Obs, # Reward, # Terminated

    def keep_playing(self) -> dict:
        return self.get_obs(), 0, False, False, {}  # Obs, # Reward, # Terminated

    def reset(self, seed: Optional[int] = 0) -> dict:
        super().reset(seed=seed)
        self.dealer = [random.randint(1, 13)]
        self.player_card_count = 2
        self.player = [random.randint(1, 13), random.randint(1, 13)] + [0] * 5

        return self.get_obs()
