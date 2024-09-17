from my_game.environment import RPGEnv
import os
from stable_baselines3.common.evaluation import evaluate_policy

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack

class AutoPilot:
    def __init__(self, game):
        self.model = PPO.load('my_game/new_model.zip')
        self.game = game

    def initEnv(self):
        self.env = RPGEnv(render_mode='human', game=self.game)
        self.env = DummyVecEnv([lambda: self.env])
        self.env = VecFrameStack(self.env, 4, channels_order='first')

    def exit_Autopilot(self):
        self.game.open_menu = True
        self.game.creating_environment()
        self.game.game_cycle()

    def run(self):
        self.initEnv()

        obs = self.env.reset()

        done = False

        while not done:
            action, _ = self.model.predict(obs)
            obs, rewards, done, info = self.env.step(action)

        self.exit_Autopilot()
