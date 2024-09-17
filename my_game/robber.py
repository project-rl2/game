import pygame
from my_game.creature import Creature
from my_game.config import *


class Robber(Creature):
    load_flag = False
    def __init__(self, type_of_robber, pos, invisible_sprites, mobs_sprites, player, attack, number_enemies):
        super().__init__(type="robber")
        self.index = number_enemies

        # death
        self.time_death = None

        self.player = player

        self.type_of_robber = type_of_robber
        # robber characteristics
        self.health = PARAMETERS_ROBBER[self.type_of_robber]['health']
        self.damage = PARAMETERS_ROBBER[self.type_of_robber]['damage']
        self.exp = PARAMETERS_ROBBER[self.type_of_robber]['exp']
        self.speed = PARAMETERS_ROBBER[self.type_of_robber]['speed']
        self.visibility_radius = PARAMETERS_ROBBER[self.type_of_robber]['visibility radius']
        self.attack_radius = PARAMETERS_ROBBER[self.type_of_robber]['attack radius']
        self.cooldown = PARAMETERS_ROBBER[self.type_of_robber]['cooldown']

        self.image = pygame.image.load(f'my_game/images/robber_{self.type_of_robber}/looking_s/looking s0000.png').convert_alpha()

        if not Robber.load_flag:
            self.load_spritesheet(['archer', 'swordsman'], 'robber', SPRITESHEET_ROBBER)
            Robber.load_flag = True

        self.spritesheet = {self.type_of_robber: SPRITESHEET_ROBBER[self.type_of_robber]}

        # the spatial state of the robber
        self.direction = pygame.math.Vector2()
        self.name_attack_state = NAME_OF_ATTACK_STATE[self.type_of_robber]
        self.state = 'looking'
        self.orientation = 's'
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-40, -40)

        # for animation
        self.sprite_index = 0

        # obstacles
        self.sprites_collision = invisible_sprites
        self.mobs_sprites = mobs_sprites

        # attack
        self.attack = attack
        self.is_attack_shown = False  # чтобы стрела не появлялась несколько раз пока идет один кадр
        self.can_attack = True
        self.attack_timer = None
        self.area_attack = self.rect.inflate(20, 20)

    def update_state_of_enemy(self):
        if self.state != 'been hit' and self.state != 'tipping over':
            # distance between player and mob
            dist = ((self.player.rect.centerx - self.rect.centerx) ** 2 + (
                    self.player.rect.centery - self.rect.centery) ** 2) ** 0.5
            offset = 22 if self.type_of_robber == 'archer' else 0
            self.direction = pygame.math.Vector2(self.player.rect.centerx - self.rect.centerx,
                                                 self.player.rect.centery - self.rect.centery - offset)
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            if dist <= self.attack_radius and self.can_attack:
                if self.state != self.name_attack_state:
                    self.sprite_index = 0
                self.attack_timer = pygame.time.get_ticks()
                self.state = self.name_attack_state
            elif self.state == 'shooting':
                pass
            elif self.attack_radius <= dist <= self.visibility_radius:
                self.state = 'running'
            else:
                self.state = 'looking'

            if self.state == self.name_attack_state and self.sprite_index >= len(
                    self.spritesheet[self.type_of_robber][self.state][self.orientation]):
                self.can_attack = False
                self.is_attack_shown = False
                self.state = 'looking'
        elif self.sprite_index >= len(self.spritesheet[self.type_of_robber][self.state][self.orientation]):
            if self.state == 'tipping over':
                self.sprite_index = len(self.spritesheet[self.type_of_robber][self.state][self.orientation]) - 1
            else:
                self.state = 'looking'

    def move(self):
        if self.state == 'running':
            self.update_position()
            self.area_attack.center = self.hitbox.center

    def animation(self):
        if self.sprite_index > len(self.spritesheet[self.type_of_robber][self.state][self.orientation]):
            self.sprite_index = 0

        self.image = self.spritesheet[self.type_of_robber][self.state][self.orientation][int(self.sprite_index)]
        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.sprite_index += (SPEED_ANIMATION+0.04)

    def attack_player(self):
        if self.state == self.name_attack_state and self.can_attack:
            if int(self.sprite_index) == 5 and not self.is_attack_shown:
                if self.type_of_robber == 'archer':
                    self.attack(self.rect.center, self.direction, self.damage)
                else:

                    self.attack(self)
                self.is_attack_shown = True

    def get_damage(self, damage=None):
        if self.state == 'tipping over':
            return
        self.state = 'been hit'
        self.sprite_index = 0
        damage = WEAPONS[self.player.weapon]['damage'] + self.player.parameters['melee attack'] * 0.4
        self.health -= damage
        self.player.damage_done += damage

    def cooldowns(self):
        cur_time = pygame.time.get_ticks()
        if self.attack_timer != None and cur_time - self.attack_timer >= self.cooldown:
            self.can_attack = True

    def death(self):
        if self.health <= 0:
            if self.state != 'tipping over':
                self.player.countEnemies += 1
                self.sprite_index = 0
                self.player.exp += self.exp

                self.time_death = pygame.time.get_ticks()
            self.state = 'tipping over'
            if self.time_death and pygame.time.get_ticks() - self.time_death >= self.time_existence_corpse:
                self.kill()

    def update(self):
        self.death()
        self.cooldowns()
        self.update_state_of_enemy()
        self.move()
        self.update_state()
        self.animation()
        self.attack_player()

