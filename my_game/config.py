from my_game.working_with_csv_fles import read_csv



trees = "my_game/images/my_objects/tree-variations.png"

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

LEARNING_SCREEN_WIDTH = 640
LEARNING_SCREEN_HEIGHT = 480

PLAYER_SPEED = 5
FPS = 60
TILE_SIZE = 64
SPEED_ANIMATION = 0.20
FONT = 'my_game/fonts/Oswald-Medium.ttf'
FONT_SIZE = 30

# information about the game map

layers_of_map = {"creatures": read_csv("my_game/level_0/new_map_creatures.csv"),
                 "obstacles": read_csv("my_game/level_0/new_map_obstacles.csv")}

grass_images_path = ['my_game/images/grass_my/details_93.gif',
                     'my_game/images/grass_my/details_94.gif',
                     'my_game/images/grass_my/details_100.gif',
                     'my_game/images/grass_my/details_101.gif',
                     'my_game/images/grass_my/details_108.gif']

objects_obstacles_path = ['my_game/images/my_objects/details_104.gif',
                          'my_game/images/my_objects/details_114.gif']

WEAPONS = {'sword': {'damage': 40, 'speed': 50, 'stamina': 20}, 'axe': {'damage': 55, 'speed': 70, 'stamina': 23}}

# UI

BAR_W = 150
BAR_H = 20

HEALTH_BAR_H = 16

STAMINA_W = BAR_W - 50
STAMINA_H = BAR_H - 4

# enemy data
# TYPES_OF_ROBBERS = ['archer']
NAME_OF_ATTACK_STATE = {"archer": "shooting", "swordsman": "attack"}
PARAMETERS_ROBBER = {
    "archer": {'cooldown': 1000, 'health': 80, 'damage': 30, 'exp': 50, 'speed': 3, 'visibility radius': 400,
               'attack radius': 250,
               'sprites': 'my_game/images/robber_archer'},
    "swordsman": {'cooldown': 1000, 'health': 130, 'damage': 30, 'exp': 60, 'speed': 2,
                  'attack radius': 50, 'visibility radius': 320,
                  'sprites': 'my_game/images/robber_swordsman'}}

SPRITESHEET_ROBBER = {'archer': {'shooting': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                              'sw': [], 'w': []},
                                 'been hit': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                              'sw': [], 'w': []},
                                 'looking': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                             'sw': [], 'w': []},
                                 'running': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                             'sw': [], 'w': []},
                                 'tipping over': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [],
                                                  'se': [],
                                                  'sw': [], 'w': []}},
                      'swordsman': {'attack': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                               'sw': [], 'w': []},
                                    'been hit': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                 'sw': [], 'w': []},
                                    'looking': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                'sw': [], 'w': []},
                                    'running': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [], 'se': [],
                                                'sw': [], 'w': []},
                                    'tipping over': {'e': [], 'n': [], 'ne': [], 'nw': [], 's': [],
                                                     'se': [],
                                                     'sw': [], 'w': []}}}

# shooting
ARROW_SPEED = 8
ARROW_FLIGHT_LENGTH = 200

# images and buttons for the menu
menu_image = 'my_game/images/for_menu/menu_image.jpg'
ButtonMenuImage = 'my_game/images/for_menu/green_button2.jpg'
HoverButtonMenuImage = 'my_game/images/for_menu/green_button2_hover.jpg'

# the mouse cursor
mouse_image = 'my_game/images/mouse_image/pngwing.com.png'

# clicking sound
click_sound = 'my_game/audio/pressed/jeleznaya-knopka-vyiklyucheniya1.mp3'

background_music = 'my_game/audio/background music.mp3'

# for UI

UI_IMAGE_PATHS = {
    'icon_level': 'my_game/images/for_level.png',
    'axe': 'my_game/images/axe.png',
    'sword': 'my_game/images/sword.png',
    'health_image1': 'my_game/images/player_sword/been hit_e/been hit e0004.png',
    'health_image2': 'my_game/images/arrow/an arrow 22.png',
    'stamina_image': 'my_game/images/player_sword/running_e/running e0005.png',
    'cooldown_image': 'my_game/images/player_sword/attack_e/attack e0007.png',
    'melee_attack_image': 'my_game/images/attack e0005.png',
    'button_for_upgrade': 'my_game/images/button_for_upgrade.png'
}
