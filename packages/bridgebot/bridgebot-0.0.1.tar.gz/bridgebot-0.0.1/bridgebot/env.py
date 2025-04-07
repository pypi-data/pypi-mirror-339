from bridgepy.exception import BizException
from bridgepy.game import Game
from bridgepy.player import PlayerId, PlayerScore
from dataclasses import asdict
import gymnasium as gym
from typing_extensions import override

from bridgebot.action import Action
from bridgebot.exception import BridgeEnvGameAlreadyTerminalState, BridgeEnvGameNotReadyToStart
from bridgebot.observation import Observation


class BridgeEnv(gym.Env):
    """
    Floating bridge environment

    Parameters
    :param game: bridgepy ``Game`` object, must have 4 players

    Attributes
    - :attr:`action_space`: 141 discrete actions labeled 0, 1, 2, ..., 140
        - bid: labeled 0-pass, 1-1C, 2-1D, 3-1H, 4-1S, 5-1NT, 6-2C, 7-2D, 8-2H, 9-2S, 10-2NT, ..., 35-7NT
        - choose partner: labeled 36-2C, 37-2D, 38-2H, 39-2S, 40-3C, 41-3D, 42-3H, 43-3S, ..., 87-AS
        - trick: labeled 88-2C, 89-2D, 90-2H, 91-2S, 92-3C, 93-3D, 94-3H, 95-3S,..., 139-AS
        - update reward: 140-update reward
    - :attr:`observation_space`: a dictionary of 7 spaces
        - player turn: 5 discrete observations labeled 0-na, 1-player 1, 2-player 2, 3-player 3, 4-player 4
        - player hand: 52 multi-discrete observations labeled 0-card not on hand, 1-card on hand
        - bid history: 210 multi-discrete observations consisting of 105 (player, bid) pairs where
        player is 0-na, 1-player 1, 2-player 2, 3- player 3, 4-player 4 and
        bid is 0-na, 1-pass, 2-1C, 3-1D, 4-1H, 5-1S, 6-1NT, 7-2C, 8-2D, 9-2H, 10-2S, 11-2NT, ..., 36-7NT
        - game bid ready: 2 discrete observations labeled 0-game bid not ready, 1-game bid ready
        - partner card: 53 discrete observations labeled 0-partner not chosen,
        1-2C, 2-2D, 3-2H, 4-2S, 5-3C, 6-3D, 7-3H, 8-3S, ..., 52-AS
        - partner: 5 discrete observations labeled 0-partner not revealed, 1-player 1, 2-player 2, 3-player 3, 4-player 4
        - trick history: 104 multi discrete observations consisting of 52 (player, trick) pairs where
        player is 0-na, 1-player 1, 2-player 2, 3-player 3, 4-player 4 and
        trick is 0-na, 1-2C, 2-2D, 3-2H, 4-2S, 5-3C, 6-3D, 7-3H, 8-3S, ..., 52-AS
    """

    def __init__(self, game: Game):
        super(BridgeEnv, self).__init__()
        if not game.dealt():
            raise BridgeEnvGameNotReadyToStart()
        self.game = game

        self.action_space = gym.spaces.Discrete(140 + 1)

        self.observation_space = gym.spaces.Dict({
            "player_turn": gym.spaces.Discrete(4 + 1),
            "player_hand": gym.spaces.MultiBinary(52),
            "bid_history": gym.spaces.MultiDiscrete([4 + 1, 36 + 1] * 105),
            "game_bid_ready": gym.spaces.Discrete(1 + 1),
            "partner_card": gym.spaces.Discrete(52 + 1),
            "partner": gym.spaces.Discrete(4 + 1),
            "trick_history": gym.spaces.MultiDiscrete([4 + 1, 52 + 1] * 52),
        })

    def _get_observation(self) -> dict:
        player_id: PlayerId | None = self._get_player_turn()
        observation = Observation.build(self.game, player_id)
        return asdict(observation)
    
    def _get_player_turn(self) -> PlayerId | None:
        dealt: bool = self.game.dealt()
        game_bid_ready: bool = self.game.game_bid_ready()
        game_finished: bool = self.game.game_finished()
        bid_winner = self.game.bid_winner() if dealt and game_bid_ready else None

        player_id = None
        if dealt and not game_bid_ready:
            player_id = self.game.next_bid_player_id()
        if bid_winner is not None and self.game.partner is None:
            player_id = bid_winner.player_id
        if dealt and game_bid_ready and self.game.partner is not None and not game_finished:
            player_id = self.game.next_trick_player_id()
        if game_finished:
            for id, reward_updated in self.updated_reward.items():
                if not reward_updated:
                    player_id = id
                    break
        return player_id
    
    @override
    def reset(self, *, seed = None, options = None) -> tuple[dict, dict]:
        super().reset(seed = seed)

        self.game.reset_game()
        self.updated_reward = {player_id: False for player_id in self.game.player_ids}

        return self._get_observation(), {}

    @override
    def step(self, action: int) -> tuple[dict, float, bool, bool, dict]:
        reward: float = 0
        done: bool = False

        player_id: PlayerId | None = self._get_player_turn()
        if player_id is None:
            raise BridgeEnvGameAlreadyTerminalState()

        try:
            Action(action).apply(self.game, player_id)
        except BizException as e:
            print(e)
            reward -= 100

        player_scores: list[PlayerScore] = self.game.scores()
        for player_score in player_scores:
            if player_score.player_id == player_id:
                reward = player_score.score
                if player_score.won:
                    reward += 10
                break

        if self.game.game_finished():
            self.updated_reward[player_id] = True
            print(self.updated_reward)
            if all(self.updated_reward.values()):
                done = True

        truncated: bool = False
        return self._get_observation(), reward, done, truncated, {}
