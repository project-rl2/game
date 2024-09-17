import sys

import pygame

from my_game.config import *
from my_game.player import Player
from my_game.object import Object

from my_game.ui import UserInterface
from my_game.robber import Robber
from my_game.arrow import Arrow
from my_game.menu import Menu
from my_game.stats import Stats
from my_game.score import Score
from my_game.Camera import Camera

from my_game.databases.managerDb import *
from my_game.autopilot import AutoPilot


class RPG:
    def __init__(self, pos_player=(2600, 1950), learning=False, spawn_swordsmans=True):

        self.learning = learning

        self.WIDTH = SCREEN_WIDTH
        self.HEIGHT = SCREEN_HEIGHT

        self.cur_volume = 0.0
        pygame.init()

        self.font = pygame.font.Font(FONT, 36)

        self.player_nickname = None
        if not learning:
            self.player_nickname = self.get_nickname()
            create_table()
            add_player(self.player_nickname)

        # creating camera
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.Learning_camera = Camera(LEARNING_SCREEN_WIDTH, LEARNING_SCREEN_HEIGHT)

        # initializing the game

        self.upgrade_menu = False
        pygame.init()
        pygame.mixer.init()

        # Total number of enemies
        self.number_enemies = 0

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.Learning_Surf = pygame.Surface((LEARNING_SCREEN_WIDTH, LEARNING_SCREEN_HEIGHT))

        pygame.display.set_caption('MY_PRG')

        self.background_image = pygame.image.load(menu_image).convert_alpha()
        self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))

        pygame.mixer.music.load(background_music)
        pygame.mixer.music.play(-1)

        self.open_menu = True
        self.game_menu = Menu(self.screen)

        # creating a map
        self.floor_surface = pygame.image.load('my_game/images/new_map.png').convert_alpha()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

        self.tree_images = pygame.image.load("my_game/images/my_objects/tree-variations.png").convert_alpha()

        self.creating_environment(pos_player=pos_player, spawn_swordsmans=True)


        self.DEATH_EVENT = pygame.USEREVENT + 1
        self.stats = Stats()
        self.score = Score(self.screen, self.stats)

        self.Autopilot = AutoPilot(self)

    def creating_environment(self, spawn_swordsmans=True, pos_player=(2600, 1950), learning=False):   # creating exactly game environment
        self.learning = learning

        # sprite groups
        self.visible_sprites = pygame.sprite.Group()
        self.invisible_sprites = pygame.sprite.Group()
        self.players_sprites = pygame.sprite.Group()
        self.mobs_sprites = pygame.sprite.Group()
        self.arrows_sprites = pygame.sprite.Group()

        if self.learning:
            player_attack = self.auto_aim_attack
        else:
            player_attack = self.melee_attack

        self.player = Player(pos_player, self.invisible_sprites, self.mobs_sprites, player_attack, self.player_nickname)
        self.players_sprites.add(self.player)

        self.ui = UserInterface(self.player)

        self.number_enemies += 1

        self.mobs_sprites.add(
            Robber('swordsman', (832, 930), self.invisible_sprites, self.mobs_sprites, self.player,
                   self.melee_attack, self.number_enemies))

        for nameLayer in layers_of_map.keys():

            for row_index, row in enumerate(layers_of_map[nameLayer]):
                for col_index, col in enumerate(row):
                    pos = (col_index * TILE_SIZE, row_index * TILE_SIZE)

                    if col != '-1':
                        if nameLayer == "obstacles" and col == '24':
                            # map border
                            self.invisible_sprites.add(Object(pos))
                        elif nameLayer == "obstacles":  # trees

                            tree_image = self.tree_images.subsurface(
                                pygame.Rect(TILE_SIZE * int(col), 0, TILE_SIZE, TILE_SIZE))
                            self.visible_sprites.add(Object(pos, tree_image))
                            self.invisible_sprites.add(Object(pos, tree_image))

                            # creatures
                        elif col == '0':
                            pass
                        elif col == '2':
                            # archer
                            self.number_enemies += 1
                            self.mobs_sprites.add(
                                Robber('archer', pos, self.invisible_sprites, self.mobs_sprites, self.player,
                                       self.archery_shot, self.number_enemies))

                        else:
                            # swordsman
                            if spawn_swordsmans:
                                self.number_enemies += 1

                                self.mobs_sprites.add(
                                    Robber('swordsman', pos, self.invisible_sprites, self.mobs_sprites, self.player,
                                           self.melee_attack, self.number_enemies))


    def get_nickname(self):
        width_nick = 640
        height_nick = 480

        label_font = pygame.font.Font(FONT, 48)

        input_box = pygame.Rect(width_nick // 2 - 100, height_nick // 2 - 20, 200, 40)

        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_inactive
        active = False
        text = ''
        done = False
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((width_nick, height_nick))

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active
                    else:
                        active = False
                    color = color_active if active else color_inactive
                elif event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif len(text) < 13:
                            text += event.unicode

            screen.fill((30, 30, 30))

            label_text = "Enter your player's nickname"
            label_surface = label_font.render(label_text, True, pygame.Color('white'))
            label_rect = label_surface.get_rect(center=(width_nick // 2, height_nick // 2 - 80))
            screen.blit(label_surface, label_rect)

            txt_surface = self.font.render(text, True, color)
            text_rect = txt_surface.get_rect(center=input_box.center)

            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.centerx = width_nick // 2

            screen.blit(txt_surface, text_rect.topleft)
            pygame.draw.rect(screen, color, input_box, 2)

            pygame.display.flip()
            clock.tick(30)

        return text

    def update_camera(self):
        self.camera.update(self.player)

        if self.learning:
            self.Learning_camera.update(self.player)
            self.Learning_Surf.fill((0, 0, 0))

        floor_offset_rect = self.floor_rect.move(self.camera.camera.topleft)
        self.screen.blit(self.floor_surface, floor_offset_rect)

        visible_sprites_list = (
                self.mobs_sprites.sprites() +
                self.players_sprites.sprites() +
                self.arrows_sprites.sprites() +
                self.visible_sprites.sprites() +
                self.invisible_sprites.sprites()
        )

        sorted_sprites = sorted(visible_sprites_list, key=lambda sprite: sprite.rect.centery)

        for sprite in sorted_sprites:
            if sprite not in self.invisible_sprites:
                offset_of_sprite = self.camera.apply(sprite)
                self.screen.blit(sprite.image, offset_of_sprite)
            if self.learning:
                offset_of_sprite = self.Learning_camera.apply(sprite)
                if sprite in self.invisible_sprites:
                    pygame.draw.rect(self.Learning_Surf, (255, 0, 0), offset_of_sprite)
                else:
                    self.Learning_Surf.blit(sprite.image, offset_of_sprite)

    def auto_aim_attack(self, creature):
        orientation_conditions = {
            'n': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centery < attacking_creature.rect.centery,
            's': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centery > attacking_creature.rect.centery,
            'w': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centerx < attacking_creature.rect.centerx,
            'e': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centerx > attacking_creature.rect.centerx,
            'nw': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.right < attacking_creature.rect.right and creature_under_attack.rect.bottom < attacking_creature.rect.bottom,
            'ne': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.left > attacking_creature.rect.left and creature_under_attack.rect.bottom < attacking_creature.rect.bottom,
            'sw': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.right < attacking_creature.rect.right and creature_under_attack.rect.top > attacking_creature.rect.top,
            'se': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.left > attacking_creature.rect.left and creature_under_attack.rect.top > attacking_creature.rect.top
        }

        damage = None
        if creature.type == 'player':
            creatures_under_attack = self.mobs_sprites
        elif creature.type == 'robber':
            creatures_under_attack = self.players_sprites
            damage = creature.damage

        orientation_arr = ['nw', 'ne', 'sw', 'se', 'n', 's', 'w', 'e']
        ori_count = 0
        for creature_under_attack in creatures_under_attack:
            if creature_under_attack.hitbox.colliderect(creature.area_attack):
                if creature.type == 'player':
                    while ori_count < len(orientation_arr) and not orientation_conditions[orientation_arr[ori_count]](
                            creature_under_attack, creature):
                        ori_count += 1
                    if ori_count < len(orientation_arr):
                        creature.orientation = orientation_arr[ori_count]
                        creature_under_attack.get_damage(damage=damage)
                else:
                    if creature.orientation in orientation_conditions and orientation_conditions[creature.orientation](
                            creature_under_attack, creature):
                        creature_under_attack.get_damage(damage=damage)

    def melee_attack(self, creature):
        orientation_conditions = {
            'n': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centery < attacking_creature.rect.centery,
            's': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centery > attacking_creature.rect.centery,
            'w': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centerx < attacking_creature.rect.centerx,
            'e': lambda creature_under_attack,
                        attacking_creature: creature_under_attack.rect.centerx > attacking_creature.rect.centerx,
            'nw': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.right < attacking_creature.rect.right and creature_under_attack.rect.bottom < attacking_creature.rect.bottom,
            'ne': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.left > attacking_creature.rect.left and creature_under_attack.rect.bottom < attacking_creature.rect.bottom,
            'sw': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.right < attacking_creature.rect.right and creature_under_attack.rect.top > attacking_creature.rect.top,
            'se': lambda creature_under_attack,
                         attacking_creature: creature_under_attack.rect.left > attacking_creature.rect.left and creature_under_attack.rect.top > attacking_creature.rect.top
        }
        damage = None
        if creature.type == 'player':
            creatures_under_attack = self.mobs_sprites
        elif creature.type == 'robber':
            creatures_under_attack = self.players_sprites
            damage = creature.damage

        for creature_under_attack in creatures_under_attack:
            if creature_under_attack.hitbox.colliderect(creature.area_attack):
                if creature.orientation in orientation_conditions and orientation_conditions[creature.orientation](
                        creature_under_attack, creature):
                    creature_under_attack.get_damage(damage=damage)

    def archery_shot(self, pos, direction, damage):
        self.arrows_sprites.add(
            Arrow(pos, direction, self.collision_for_arrow, damage, self.player.get_damage,
                  self.arrow_movement_in_player))

    def arrow_movement_in_player(self):
        x = self.player.speed * self.player.direction.x
        y = self.player.speed * self.player.direction.y
        return pygame.math.Vector2(x, y)

    def collision_for_arrow(self, arrow):
        for sprite in self.visible_sprites:
            if sprite.hitbox.colliderect(arrow.hitbox):
                return True  # collision
        for sprite in self.players_sprites:
            if sprite.hitbox.colliderect(arrow.hitbox):

                if sprite.type == 'player':  # arrow hit the player
                    arrow.shot_player = True

                return True

        return False  # not collision

    def updateGame(self, action=None):  # action != None => agent
        if self.open_menu:
            return

        if not self.upgrade_menu:
            self.visible_sprites.update()
            if action is None:
                self.players_sprites.update()
            else:
                self.player.update_agent(action)
            self.mobs_sprites.update()
            self.arrows_sprites.update()
        else:
            return

    def draw_sprites(self):
        if self.open_menu:
            self.game_menu.draw()
            return

        Learning_Surf = self.Learning_Surf if self.learning else None

        if not self.upgrade_menu:
            self.update_camera()
            self.score.draw(Learning_Surf)
            self.ui.draw_ui(Learning_Surf)
        else:
            self.ui.drawUpgradeInterface()
            self.ui.draw_ui()

    def upgrade_stats(self):
        self.stats.cur_lever = self.player.level
        self.stats.DefeatedEnemies = self.player.countEnemies
        self.score.update(self.stats)

    def EventInMenu(self, mouse_pos, event):
        if event.type == pygame.USEREVENT:
            if event.button.text == "Settings":
                self.game_menu.status = "settings"
                self.fade()
            elif self.learning and event.button.text == "Continue":
                self.Autopilot.exit_Autopilot()

            elif event.button.text == "back":
                self.game_menu.status = "menu"
                self.fade()

            elif event.button.text == "Continue":
                self.open_menu = False
                self.fade()

            elif event.button.text == "Exit":
                self.exitGame()

            elif event.button.text == "up volume":
                self.cur_volume = min(1.0, self.cur_volume + 0.1)
                pygame.mixer.music.set_volume(self.cur_volume)

            elif event.button.text == "down volume":
                self.cur_volume = max(0.0, self.cur_volume - 0.1)
                pygame.mixer.music.set_volume(self.cur_volume)

            elif event.button.text == "Player Ratings":
                self.game_menu.status = "ratings"
                self.fade()

            elif event.button.text == "reset rating":
                reset_data()

            elif event.button.text == "AUTOPILOT":
                self.Autopilot.run()

        self.game_menu.upgrade(mouse_pos, event, self.cur_volume)

    """def regime_change(self, learning):
        self.learning = learning

        if not self.learning:
            self.WIDTH = SCREEN_WIDTH
            self.HEIGHT = SCREEN_HEIGHT
        else:
            self.WIDTH = LEARNING_SCREEN_WIDTH
            self.HEIGHT = LEARNING_SCREEN_HEIGHT

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), pygame.RESIZABLE | pygame.DOUBLEBUF)

        self.game_menu.screen = self.screen

        self.score.screen = self.screen
        self.score.screen_rect = self.screen.get_rect()

        self.ui.screen = self.screen
        self.ui.update_rect()

        self.camera = Camera(self.WIDTH, self.HEIGHT)
         
        self.draw_sprites()"""

    def fade(self):
        fade_alpha = 0
        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
        fade_surface.fill((0, 0, 0))
        fade_surface.set_alpha(fade_alpha)

        while fade_alpha <= 200:
            fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(fade_alpha)
            self.screen.blit(fade_surface, (0, 0))
            fade_alpha += 1
            pygame.display.flip()

    def exitGame(self):
        self.fade()
        pygame.quit()
        sys.exit()

    def update(self, action, dt=0.1, render_mode='human'):  # for environment

        len_step = 6
        step = 0

        while step < len_step:
            for event in pygame.event.get():
                self.checkQuit(event)
                self.checkGameMenu(event)

                if self.open_menu:  # menu is open
                    self.EventInMenu(pygame.mouse.get_pos(), event)

            if not self.open_menu:
                step += 1
            print(step, self.open_menu)
            self.upgrade_stats()
            self.screen.blit(self.background_image, (0, 0))
            self.draw_sprites()
            self.updateGame(action=action)
            self.clock.tick(FPS)
            if render_mode == 'human':
                pygame.display.flip()

    def checkQuit(self, event):
        if event.type == pygame.QUIT:
            if not self.learning:
                update_all_data(self.player)
            self.exitGame()

    def checkGameMenu(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.open_menu = not self.open_menu
            if not self.learning:
                update_all_data(self.player)
            self.fade()

    def check_death(self, event):
        if event.type == self.DEATH_EVENT:
            if not self.learning:
                update_all_data(self.player)
            self.exitGame()

    def checkUpgradeMenu(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_j:  # upgrade menu for player
            self.upgrade_menu = not self.upgrade_menu
            if not self.learning:
                update_all_data(self.player)

        if self.upgrade_menu and event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            self.ui.handle_click(mouse_pos)

    def game_cycle(self):
        while True:
            for event in pygame.event.get():
                self.checkQuit(event)
                self.checkGameMenu(event)
                self.check_death(event)

                if not self.open_menu:
                    self.checkUpgradeMenu(event)
                else:  # menu is open
                    self.EventInMenu(pygame.mouse.get_pos(), event)

            self.screen.blit(self.background_image, (0, 0))
            self.upgrade_stats()
            self.updateGame()
            self.draw_sprites()
            pygame.display.flip()
            self.clock.tick(FPS)
