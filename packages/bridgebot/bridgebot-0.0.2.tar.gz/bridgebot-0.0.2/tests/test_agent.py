from unittest import TestCase, main
from bridgepy.game import Game, GameId
from bridgepy.player import PlayerId

from bridgebot.agent import BridgeRandomAgent
from bridgebot.env import BridgeEnv


class TestAgent(TestCase):

    def test_RandomAgent(self):
        # create game with 4 players
        game_id = GameId("1")
        player_id1 = PlayerId("1")
        player_id2 = PlayerId("2")
        player_id3 = PlayerId("3")
        player_id4 = PlayerId("4")
        game = Game(id = game_id, player_ids = [player_id1])
        game.add_player(player_id2)
        game.add_player(player_id3)
        game.add_player(player_id4)

        # create bridge environment
        env = BridgeEnv(game)

        # create bridge random agent
        agent = BridgeRandomAgent()

        # play game until done
        observation, _ = env.reset()
        done = False
        while not done:
            action = agent.predict(observation)
            observation, reward, done, _, _ = env.step(action)
            # all actions should be valid, no negative rewards expected
            self.assertTrue(reward >= 0)

if __name__ == '__main__':
    main()
