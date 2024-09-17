import pygame
from my_game.config import *

class Object(pygame.sprite.Sprite):
    def __init__(self, pos, image=pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__()
        self.type = 'object'
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-30, -26)