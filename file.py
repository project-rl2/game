import os
from stable_baselines3.common.evaluation import evaluate_policy

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
from my_game.environment import RPGEnv
from my_game.main import RPG

Game = RPG()
Game.game_cycle()