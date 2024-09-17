import pygame
from my_game.config import *
from my_game.databases.managerDb import *


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.status = "menu"

        self.buttons = {"menu": [Meny_Button(self.screen.get_width() / 2 - 550, 250, 252, 74, "Continue"),
                                 Meny_Button(self.screen.get_width() / 2 - 550, 350, 252, 74, "Player Ratings"),
                                 Meny_Button(self.screen.get_width() - 350, 550, 252, 74, "AUTOPILOT"),
                                 Meny_Button(self.screen.get_width() / 2 - 550, 450, 252, 74, "Settings"),
                                 Meny_Button(self.screen.get_width() / 2 - 550, 550, 252, 74, "Exit")],
                        "settings": [Meny_Button(self.screen.get_width() / 2 - 550, 250, 252, 74, "up volume"),
                                     Meny_Button(self.screen.get_width() / 2 - 550, 350, 252, 74, "down volume"),
                                     Meny_Button(self.screen.get_width() / 2 - 550, 450, 252, 74, "video"),
                                     Meny_Button(self.screen.get_width() / 2 - 550, 550, 252, 74, "back")],
                        "ratings": [Meny_Button(self.screen.get_width() / 2 - 550, 50, 252, 74, "back"),
                                    Meny_Button(self.screen.get_width() - 90 - 252, 50, 252, 74, "reset rating")]}

        self.font = pygame.font.Font(FONT, FONT_SIZE + 25)
        self.text_surface = self.font.render(self.status, True, (255, 10, 10))
        self.text_rect = self.text_surface.get_rect(
            center=(self.screen.get_width() / 6, self.screen.get_height() * 0.27))

    def settings_menu(self):
        pass

    def upgrade(self, mouse_pos, event, cur_volume):
        for button in self.buttons[self.status]:
            button.upgrade(event, mouse_pos, cur_volume)

    def draw(self):
        for button in self.buttons[self.status]:
            button.draw(self.screen)

        if self.status == 'ratings':
            self.draw_player_ratings()
            return

        self.screen.blit(self.text_surface, self.text_rect)

    def draw_player_ratings(self):
        player_ratings = get_player_ratings()
        column_names = ["Nickname", "Enem.", "Lvl", "HP", "Stam.", "CD", "Atk", "DMG"]

        font = pygame.font.Font(None, 36)
        title_font = pygame.font.Font(None, 48)

        title_surface = title_font.render("Player Ratings", True, (255, 255, 255))
        self.screen.blit(title_surface, (self.screen.get_width() // 2 - title_surface.get_width() // 2, 50))

        nickname_col_width = int(self.screen.get_width() * 0.2)
        other_col_width = (self.screen.get_width() - nickname_col_width) // (len(column_names) - 1)

        for i, col_name in enumerate(column_names):
            if i == 0:
                x_pos = 20
            else:
                x_pos = nickname_col_width + (i - 1) * other_col_width + 20

            header_surface = font.render(col_name, True, (255, 255, 255))
            self.screen.blit(header_surface, (x_pos, 150))

        row_height = 40
        start_y = 200

        for index, player_data in enumerate(player_ratings):
            y_pos = start_y + index * row_height

            for col_index, value in enumerate(player_data):
                if col_index == 0:
                    value_surface = font.render(str(value), True, (255, 255, 255))
                    x_pos = 20
                else:
                    value_surface = font.render(str(value), True, (255, 255, 255))
                    x_pos = nickname_col_width + (col_index - 1) * other_col_width + 20

                self.screen.blit(value_surface, (x_pos, y_pos))


class Meny_Button:
    def __init__(self, x, y, width, height, text):

        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(ButtonMenuImage)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hover_image = pygame.image.load(HoverButtonMenuImage)
        self.hover_image = pygame.transform.scale(self.hover_image, (width, height))

        self.sound = pygame.mixer.Sound(click_sound)
        self.is_hovered = False

        # label of button for render
        self.font = pygame.font.Font(FONT, FONT_SIZE + 10)
        self.text_surface = self.font.render(self.text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        if self.is_hovered:
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

        screen.blit(self.text_surface, self.text_rect)

    def update_mouse_over_state(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def get_event(self, event, cur_volume):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            self.sound.set_volume(cur_volume)
            self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def upgrade(self, event, mouse_pos, cur_volume):
        self.update_mouse_over_state(mouse_pos)
        self.get_event(event, cur_volume)
