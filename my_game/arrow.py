import pygame
from my_game.config import *
import math
class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, direction, collision_for_arrow, damage, damage_to_player, arrow_movement_in_player):
        super().__init__()
        self.direction = direction.normalize()
        self.dist = ARROW_FLIGHT_LENGTH
        self.speed = ARROW_SPEED
        self.speed_fall = 1
        self.stop_arrow = False

        # hitting player
        self.damage = damage
        self.shot_player = False
        self.damage_to_player = damage_to_player
        self.arrow_movement_in_player = arrow_movement_in_player

        angle = math.degrees(math.atan2(-direction.y, direction.x))
        angle = (angle + 360) % 360  # Преобразование отрицательных углов к положительным

        if abs(angle - 360) <= 5.625:
            self.num = 8
        elif abs(angle - 348.75) <= 5.625:
            self.num = 9
        elif abs(angle - 337.5) <= 5.625:
            self.num = 10
        elif abs(angle - 326.25) <= 5.625:
            self.num = 11
        elif abs(angle - 315) <= 5.625:
            self.num = 12
        elif abs(angle - 303.75) <= 5.625:
            self.num = 13
        elif abs(angle - 292.5) <= 5.625:
            self.num = 14
        elif abs(angle - 281.25) <= 5.625:
            self.num = 15
        elif abs(angle - 270) <= 5.625:
            self.num = 16
        elif abs(angle - 258.75) <= 5.625:
            self.num = 17
        elif abs(angle - 247.5) <= 5.625:
            self.num = 18
        elif abs(angle - 236.25) <= 5.625:
            self.num = 19
        elif abs(angle - 225) <= 5.625:
            self.num = 20
        elif abs(angle - 213.75) <= 5.625:
            self.num = 21
        elif abs(angle - 202.5) <= 5.625:
            self.num = 22
        elif abs(angle - 191.25) <= 5.625:
            self.num = 23
        elif abs(angle - 180) <= 5.625:
            self.num = 24
        elif abs(angle - 168.75) <= 5.625:
            self.num = 25
        elif abs(angle - 157.5) <= 5.625:
            self.num = 26
        elif abs(angle - 146.25) <= 5.625:
            self.num = 27
        elif abs(angle - 135) <= 5.625:
            self.num = 28
        elif abs(angle - 123.75) <= 5.625:
            self.num = 29
        elif abs(angle - 112.5) <= 5.625:
            self.num = 30
        elif abs(angle - 101.25) <= 5.625:
            self.num = 31
        elif abs(angle - 90) <= 5.625:
            self.num = 0
        elif abs(angle - 78.75) <= 5.625:
            self.num = 1
        elif abs(angle - 67.5) <= 5.625:
            self.num = 2
        elif abs(angle - 56.25) <= 5.625:
            self.num = 3
        elif abs(angle - 45) <= 5.625:
            self.num = 4
        elif abs(angle - 33.75) <= 5.625:
            self.num = 5
        elif abs(angle - 22.5) <= 5.625:
            self.num = 6
        else:
            self.num = 7
        self.image = pygame.image.load('my_game/images/arrow/an arrow ' + str(self.num) + '.png')
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-26, -50)
        self.collision_for_arrow = collision_for_arrow
        self.shot_player = False

        # disappearance
        self.time_of_existence = 6000
        self.time_of_appearance = pygame.time.get_ticks()


    def flight_of_arrow(self):
        if not self.shot_player:
            self.hitbox.x += self.direction.x * self.speed
            self.hitbox.y += self.direction.y * self.speed
            self.hitbox.y += self.speed_fall
            self.dist -= self.speed
            self.rect.center = self.hitbox.center

            self.stop_arrow = self.collision_for_arrow(self)
        else:
            self.hitbox.center += self.arrow_movement_in_player()
            self.rect.center = self.hitbox.center



    def cooldown(self):
        cur_time = pygame.time.get_ticks()
        if cur_time - self.time_of_appearance >= self.time_of_existence:
            self.kill()


    def update(self):
       # print(self.hitbox.size)
        if not self.stop_arrow or self.shot_player:
            self.flight_of_arrow()
        if self.damage_to_player is not None and self.shot_player:
            self.damage_to_player(self.damage)
            self.damage_to_player = None
        self.cooldown()