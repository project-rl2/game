from gymnasium import Env
from gymnasium import spaces
import numpy as np
from my_game.config import *
import pygame
import cv2
from matplotlib import pyplot as plt
import random


class RPGEnv(Env):
    def __init__(self, render_mode='human', game=None):
        super(RPGEnv, self).__init__()

        if game is None:
            raise ValueError("The game can't be None. Pass the object of the game.")

        # init game
        self.game = game
        self.game.open_menu = False
        self.screen = self.game.screen
        self.current_step = 0
        self.render_mode = render_mode

        """space actions:
        0: attack
        1: change weapon
        2: upgrade health
        3: upgrade cooldown
        4: upgrade stamina
        5: upgrade melee attack
        6: move W
        7: move S
        8: move A
        9: move D
        10: move WD
        11: move SD
        12: move SA
        13: move WA
        """

        self.action_space = spaces.Discrete(14)
        self.numeric_data_dim = 6
        self.mobs_data_dim = (self.game.number_enemies + 1) * 2
        self.observation_space = spaces.Dict({
            "image": spaces.Box(low=0, high=255, shape=(3, LEARNING_SCREEN_HEIGHT // 2 - 90, LEARNING_SCREEN_WIDTH // 2 - 120),

                                            dtype=np.uint8),
            "numeric_data": spaces.Box(low=-np.inf, high=np.inf, shape=(self.numeric_data_dim,), dtype=np.float32)
        })
        # counter of killed mobs
        
        self.counter_killed_mobs = 0

        self.previous_health = self.game.player.health
        self.damage_done = 0
        self.prevUpPoints = 0
        self.prev_pos = self.game.player.rect.center
        self.inactive_steps = 0

        self.steps_without_damage_done = 0
        self.steps_without_damage_received = 0

        self.visited_sectors = set()
        self.sector_size = 200
        self.initial_positions = [(2600, 1950), (1200, 1200), (3000, 3000), (3000, 3800), (3346, 2078)]


    def get_mobs_data(self):
        data = np.zeros(self.mobs_data_dim,  dtype=np.float32)

        data[0] = self.game.player.rect.centerx
        data[1] = self.game.player.rect.centery
        for mob in self.game.mobs_sprites.sprites():
            data[mob.index * 2] = mob.rect.centerx
            data[mob.index * 2 + 1] = mob.rect.centery
        return data    

    def get_numeric_data(self):
        health = self.game.player.health
        damage = self.game.player.damage_done - self.damage_done
        swdd = self.steps_without_damage_done
        iS = self.inactive_steps
        cs = self.current_step
        gpce = self.game.player.countEnemies
         

        return np.array([health, damage, swdd, iS, cs, gpce], dtype=np.float32) 

    def reset(self, seed=None):
        pos = random.choice(self.initial_positions)

        random_number = random.choice([1, 2])

        spawn_swordsmans = True if random_number == 1 else False

        
        self.game.creating_environment(pos_player=pos, learning=True, spawn_swordsmans=spawn_swordsmans )
        self.game.open_menu = False

        self.current_step = 0
        self.screen = self.game.screen
        self.counter_killed_mobs = 0
        self.previous_health = self.game.player.health
        self.damage_done = 0
        self.prevUpPoints = 0
        self.inactive_steps = 0
        self.steps_without_damage_done = 0
        self.steps_without_damage_received = 0
        self.game.update(action=None)
        self.prev_pos = self.game.player.rect.center
        self.visited_sectors = set()

        observation = self.get_observation()
        return observation, {}

    def step(self, action, dt=0.1):
        self.game.update(action, dt=dt, render_mode=self.render_mode)

        state = self.get_observation()
        reward = self.get_reward(action)
        done = self.get_done()
        self.current_step += 1

        return state, reward, done, False, {}

    def render(self, mode='human'):

        pygame.display.flip()

    def close(self):
        pygame.quit()

    def get_observation(self):

        image = pygame.surfarray.array3d(self.game.Learning_Surf)
        image = np.transpose(image, (1, 0, 2))

        resized_image = cv2.resize(image, (LEARNING_SCREEN_WIDTH // 2 - 120, LEARNING_SCREEN_HEIGHT // 2 - 90))
        observation = np.reshape(resized_image, (3, LEARNING_SCREEN_HEIGHT // 2 - 90, LEARNING_SCREEN_WIDTH // 2 - 120))

        numeric_data = self.get_numeric_data()

        normalized_numeric_data = numeric_data / np.array(
        [self.game.player.parameters['health'], 55, 550, 250, 5000, self.game.number_enemies], dtype=np.float32
    )
        
         



        combined_observation = {
            "image": observation,
            "numeric_data": normalized_numeric_data
        }


        return combined_observation

    def get_reward(self, action):
        reward = 0.0

        # Reward for defeating mobs
        reward += 1.05 ** (self.game.player.countEnemies) * 25.0 * (
                    self.game.player.countEnemies - self.counter_killed_mobs)

        self.counter_killed_mobs = self.game.player.countEnemies

        # reward for dealing damage

        damage = (self.game.player.damage_done - self.damage_done) * 0.5

        if damage > 0:
            self.steps_without_damage_done = 0
        else:
            self.steps_without_damage_done += 1
            reward -= 2 if action == 0 else 0

        reward += damage
        self.damage_done = self.game.player.damage_done

        # Positive reward for survival
        if self.game.number_enemies == self.counter_killed_mobs:
            reward += 300

        # penalty for committing useless actions
        if action in [2, 3, 4, 5] and self.prevUpPoints <= 0:
            reward -= 5.0

        # reward for leveling up
        if action in [2, 3, 4, 5] and self.prevUpPoints > 0:
            reward += 50.0

        # penalty for inactive steps
        if self.prev_pos == self.game.player.rect.center:
            self.inactive_steps += 1
        else:
            self.inactive_steps = 0
            self.prev_pos = self.game.player.rect.center

        if self.inactive_steps > 60:
            reward -= 3.0

        # Rewards for exploring the map
        cur_sector = (self.game.player.rect.x // self.sector_size, self.game.player.rect.y // self.sector_size)

        if cur_sector not in self.visited_sectors:
            reward += 1.0
            self.visited_sectors.add(cur_sector)

        self.prevUpPoints = self.game.player.UpPoints

        self.previous_health = self.game.player.health

        x = self.game.player.rect.centerx
        y = self.game.player.rect.centery
        minim = 100000000
        for mob in self.game.mobs_sprites.sprites():
            if mob.type_of_robber == 'archer':
                dif = (x-mob.rect.centerx)*(x-mob.rect.centerx) + (y-mob.rect.centery)*(y-mob.rect.centery)
                if dif < minim:
                    minim = dif

        if minim < 900:
            reward += 3

        if minim < 15 * 15:
            reward += 6     

        return reward

    def get_done(self):
        return (self.game.number_enemies == self.game.player.countEnemies or
                self.game.player.health <= 0 or
                self.inactive_steps > 250 or
                self.current_step >= 5000 or
                self.steps_without_damage_done > 2500)