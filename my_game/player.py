import pygame.math
from my_game.creature import Creature
from my_game.config import *


class Player(Creature):
    def __init__(self, pos, sprites_collision, mobs_sprites, player_attack, nickname):
        super().__init__(type='player')
        self.nickname = nickname

        # player characteristics
        self.level = 0
        self.parameters = {'health': 100, 'stamina': 100, 'cooldown': 10, 'melee attack': 25, 'exp': 100}
        self.health = self.parameters['health']
        self.stamina = 1001
        self.exp = 0
        self.UpPoints = 0
        self.countEnemies = 0
        self.level_health = 0
        self.level_stamina = 0
        self.level_cooldown = 0
        self.level_melee_attack = 0
        self.last_damage_time = pygame.time.get_ticks()
        self.health_regen_delay = 2000
        self.health_regen_rate = 0.1
        self.damage_done = 0

        # bars
        self.health_bar_back = pygame.Rect(15, 690, BAR_W, BAR_H)
        self.stamina_bar_back = pygame.Rect(15, 670, BAR_W - 50, BAR_H - 4)
        self.exp_bar_back = pygame.Rect(15, 650, BAR_W - 50, BAR_H - 4)
        self.icon_level = pygame.image.load('my_game/images/for_level.png')
        self.icon_level_rect = self.icon_level.get_rect(midright=(32, 655))

        # attack
        self.can_attack = True
        self.attack_timer = None
        self.attack_cooldown = 670
        self.weapon = 'sword'
        self.player_attack = player_attack

        # movement
        self.speed = PLAYER_SPEED
        self.direction = pygame.math.Vector2()
        self.state = 'looking'
        self.orientation = 's'

        self.spritesheet = {'axe':
                                {'attack': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                            'sw': [], 'w': []},
                                 'been hit': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                              'sw': [], 'w': []},
                                 'looking': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                             'sw': [], 'w': []},
                                 'running': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                             'sw': [], 'w': []},
                                 'tipping over': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                  'sw': [], 'w': []}},
                            'sword': {'attack': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                 'sw': [], 'w': []},
                                      'been hit': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                   'sw': [], 'w': []},
                                      'looking': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                  'sw': [], 'w': []},
                                      'running': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                  'sw': [], 'w': []},
                                      'tipping over': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                       'sw': [], 'w': []}}}
        self.load_spritesheet(WEAPONS, 'player', self.spritesheet)
        self.image = self.spritesheet[self.weapon][self.state][self.orientation][0]
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = self.rect.inflate(-64, -60)
        # for learning change
        self.area_attack = self.rect.inflate(-25, -25)

        # for animation
        self.sprite_index = 0

        # obstacles
        self.sprites_collision = sprites_collision
        self.mobs_sprites = mobs_sprites

    def move(self):
        if self.state not in ['been hit', 'tipping over']:
            keys = pygame.key.get_pressed()
            # right direction
            if keys[pygame.K_d]:
                self.direction.x = 1
            # left direction
            elif keys[pygame.K_a]:
                self.direction.x = -1
            else:
                self.direction.x = 0
            # up direction
            if keys[pygame.K_w]:
                self.direction.y = -1
            elif keys[pygame.K_s]:
                self.direction.y = 1
            else:
                self.direction.y = 0
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
                self.state = 'running'
            if self.state == 'running':
                self.update_position()
            self.area_attack.center = self.hitbox.center

    def attack(self):
        self.player_attack(self)
        self.stamina -= WEAPONS[self.weapon]['stamina']
        self.attack_timer = pygame.time.get_ticks()
        self.can_attack = False
        self.sprite_index = 0

    def attack_by_hyman(self):
        # change of weapon
        clicks = pygame.key.get_pressed()
        if clicks[pygame.K_1]:
            self.weapon = list(WEAPONS.keys())[0]
        elif clicks[pygame.K_2]:
            self.weapon = list(WEAPONS.keys())[1]

        if self.state != 'been hit' and self.state != "tipping over":
            # attack
            if pygame.mouse.get_pressed()[0] and self.can_attack and self.stamina >= WEAPONS[self.weapon]['stamina']:
                self.attack()

            if not self.can_attack:
                self.direction = pygame.math.Vector2()
                self.state = 'attack'

    def cooldowns(self):
        cur_time = pygame.time.get_ticks()
        if not self.can_attack and cur_time - self.attack_timer >= self.attack_cooldown - self.parameters[
            'cooldown']:
            self.can_attack = True

    def get_damage(self, damage=None):

        if self.state == 'been hit' and self.sprite_index >= len(
                self.spritesheet[self.weapon][self.state][self.orientation]):
            self.state = 'looking'

        if self.state == "tipping over" or self.state == 'been hit':
            return

        if damage is not None:
            self.last_damage_time = pygame.time.get_ticks()
            self.health -= damage
            self.state = 'been hit'
            self.sprite_index = 0

    def health_recovery(self):
        if self.state == "tipping over":
            return
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time >= self.health_regen_delay:
            self.health = min(self.parameters['health'], self.health + self.health_regen_rate)
    def stamina_recovery(self):
        if self.stamina < self.parameters['stamina']:
            self.stamina += 0.2
        else:
            self.stamina = self.parameters['stamina']

    def animation(self):

        if self.sprite_index > len(self.spritesheet[self.weapon][self.state][self.orientation]):
            self.sprite_index = 0

        self.image = self.spritesheet[self.weapon][self.state][self.orientation][int(self.sprite_index)]

        self.rect = self.image.get_rect(center=self.hitbox.center)
        self.sprite_index += SPEED_ANIMATION
        if self.state == "tipping over":
            self.sprite_index = min(self.sprite_index,
                                    len(self.spritesheet[self.weapon][self.state][self.orientation]) - SPEED_ANIMATION)

    def level_up(self):
        if self.exp >= self.parameters['exp']:
            self.level += 1
            self.UpPoints += 1
            self.exp -= self.parameters['exp']
            self.parameters['exp'] *= 1.25

    def death(self):
        if self.health <= 0:
            # print(self.state)
            if self.state != 'tipping over':
                self.sprite_index = 0
                self.time_death = pygame.time.get_ticks()
            self.state = 'tipping over'
            if self.time_death and pygame.time.get_ticks() - self.time_death >= self.time_existence_corpse:
                DEATH_EVENT = pygame.USEREVENT + 1
                death_event = pygame.event.Event(DEATH_EVENT, string="death")
                pygame.event.post(death_event)

    def move_agent(self, action):
        if self.state not in ['been hit', 'tipping over']:
            self.direction = pygame.math.Vector2()

            if action == 6:
                self.direction.y = -1
            elif action == 7:
                self.direction.y = 1
            elif action == 8:
                self.direction.x = -1
            elif action == 9:
                self.direction.x = 1
            elif action == 10:
                self.direction.y = -1
                self.direction.x = 1
            elif action == 11:
                self.direction.y = 1
                self.direction.x = 1
            elif action == 12:
                self.direction.y = 1
                self.direction.x = -1
            elif action == 13:
                self.direction.y = -1
                self.direction.x = -1

            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()
                self.state = 'running'
            if self.state == 'running':
                self.update_position()

            self.area_attack.center = self.hitbox.center

    def agent_attack(self, action):
        # change of weapon
        if action == 1:
            if self.weapon == 'sword':
                self.weapon = 'axe'
            else:
                self.weapon = 'sword'

        if self.state != 'been hit' and self.state != "tipping over":
            # attack
            if action == 0 and self.can_attack and self.stamina >= WEAPONS[self.weapon]['stamina']:
                self.attack()

            if not self.can_attack:
                self.direction = pygame.math.Vector2()
                self.state = 'attack'

    def upgrade_agent(self, action):
        if self.UpPoints > 0:
            parameter_name = '-'
            if action == 2:
                parameter_name = 'health'
            elif action == 3:
                parameter_name = 'cooldown'
            elif action == 4:
                parameter_name = 'stamina'
            elif action == 5:
                parameter_name = 'melee attack'

            if parameter_name != '-':
                self.UpPoints -= 1
                self.parameters[parameter_name] *= 1.10
                current_level = getattr(self, 'level_' + '_'.join(parameter_name.split()), None)
                setattr(self, 'level_' + '_'.join(parameter_name.split()), current_level + 1)

    def update_agent(self, action):
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
        self.death()
        if self.can_attack:
            self.move_agent(action)
        self.upgrade_agent(action)
        self.update_state()
        self.agent_attack(action)
        self.cooldowns()
        self.get_damage()
        self.animation()
        self.health_recovery()
        self.stamina_recovery()
        self.level_up()

    def update(self):
        self.death()

        if self.can_attack:
            self.move()
        self.update_state()
        self.attack_by_hyman()
        self.cooldowns()
        self.get_damage()
        self.animation()
        self.health_recovery()
        self.stamina_recovery()
        self.level_up()
