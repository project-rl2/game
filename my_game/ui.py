import math

import pygame
from my_game.config import *


class UserInterface:
    def __init__(self, player):
        self.player = player
        self.screen = pygame.display.get_surface()
        self.font = pygame.font.Font(FONT, FONT_SIZE)

        # Bars
        self.health_bar_back = pygame.Rect(15, self.screen.get_height() - 30, BAR_W, BAR_H)
        self.stamina_bar_back = pygame.Rect(15, self.screen.get_height() - 50, BAR_W - 50, BAR_H - 4)
        self.exp_bar_back = pygame.Rect(15, self.screen.get_height() - 70, BAR_W - 50, BAR_H - 4)

        # Load images
        self.icon_level = pygame.image.load(UI_IMAGE_PATHS['icon_level'])

        self.images_of_weapons = {
            'axe': pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['axe']).convert_alpha(), (64, 64)),
            'sword': pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['sword']).convert_alpha(), (64, 64))
        }

        # Upgrade menu
        self.load_upgrade_menu_images()
        self.buttonsUp = pygame.sprite.Group()
        self.InitButtonsUp()

    def load_upgrade_menu_images(self):
        self.health_image1 = pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['health_image1']).convert_alpha(),
                                                    (200, 250))
        self.health_image2 = pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['health_image2']).convert_alpha(),
                                                    (100, 100))
        self.stamina_image = pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['stamina_image']).convert_alpha(),
                                                    (200, 250))
        self.cooldown_image = pygame.transform.scale(
            pygame.image.load(UI_IMAGE_PATHS['cooldown_image']).convert_alpha(),
            (200, 250))
        self.melee_attack_image = pygame.transform.scale(
            pygame.image.load(UI_IMAGE_PATHS['melee_attack_image']).convert_alpha(), (200, 250))

        self.health_image1_rect = self.health_image1.get_rect(topleft=(250, 200))
        self.health_image2_rect = self.health_image2.get_rect(topleft=(300, 250))
        self.stamina_image_rect = self.stamina_image.get_rect(topleft=(450, 200))
        self.cooldown_image_rect = self.cooldown_image.get_rect(topleft=(650, 200))
        self.melee_attack_image_rect = self.melee_attack_image.get_rect(topleft=(850, 200))

        self.update_rect()

    def update_rect(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        self.icon_level_rect = self.icon_level.get_rect(midright=(32, surf.get_height() - 65))

        # Bars
        self.health_bar_back.topleft = (15, surf.get_height() - 30)
        self.stamina_bar_back.topleft = (15, surf.get_height() - 50)
        self.exp_bar_back.topleft = (15, surf.get_height() - 70)


    def drawBarsForStatePlayer(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        self.drawBar(self.health_bar_back, 'red', self.player.health, self.player.parameters['health'], 10,
                      HEALTH_BAR_H, BAR_W, Learning_Surf)
        self.drawBar(self.stamina_bar_back, 'green', self.player.stamina, self.player.parameters['stamina'], 8,
                      BAR_H - 8, STAMINA_W, Learning_Surf)
        self.drawBar(self.exp_bar_back, 'yellow', self.player.exp, self.player.parameters['exp'], 8, BAR_H - 8,
                      STAMINA_W, Learning_Surf)

        surf.blit(self.icon_level, self.icon_level_rect)
        text_level = self.font.render(str(self.player.level), False, 'white')
        text_level_rect = text_level.get_rect(center=self.icon_level_rect.center)
        surf.blit(text_level, text_level_rect)

    def drawBar(self, back_rect, color, current_value, max_value, radius, h, W, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        self.draw_rounded_rect(surf, 'black', back_rect, radius)
        fill_rect = back_rect.copy()
        fill_rect.width = W * (current_value / max_value)
        fill_rect.height = h
        fill_rect.top += 2
        self.draw_rounded_rect(surf, color, fill_rect, radius - 2)

    def draw_rounded_rect(self, surface, color, rect, radius):
        pygame.draw.rect(surface, color, rect)
        if rect.width > 0:
            pygame.draw.circle(surface, color, (rect.left, rect.bottom - radius), radius)
            pygame.draw.circle(surface, color, (rect.right, rect.bottom - radius), radius)

    def InitButtonsUp(self):
        for i, parameter in enumerate(self.player.parameters.keys()):
            if parameter == 'exp':
                break
            button = ButtonUpgrade(
                pos=(self.health_image1_rect.x + i * 200, self.health_image1_rect.y + self.health_image1_rect.height),
                parameter_name=parameter,
                font=self.font
            )
            self.buttonsUp.add(button)

    def draw_weapon_interface(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        weapon_interface_rect = pygame.Rect(200, surf.get_height()-70, 64, 64)
        pygame.draw.rect(surf, (33, 29, 29), weapon_interface_rect)
        pygame.draw.rect(surf, 'red', weapon_interface_rect, 2)
        weapon = self.images_of_weapons[self.player.weapon]
        surf.blit(weapon, weapon_interface_rect)

    def handle_click(self, mouse_pos):
        for button in self.buttonsUp:
            if button.rect.collidepoint(mouse_pos):
                self.upgradePlayer(button.parameter_name)
                button.register_click()
                break

    def upgradePlayer(self, parameter_name):
        if self.player.UpPoints > 0:
            self.player.UpPoints -= 1
            self.player.parameters[parameter_name] *= 1.10
            current_level = getattr(self.player, 'level_'+'_'.join(parameter_name.split()), None)
            setattr(self.player, 'level_'+'_'.join(parameter_name.split()), current_level + 1)

    def drawUpgradeInterface(self):
        self.drawUpgradeButton(self.health_image1, self.health_image1_rect)
        self.screen.blit(self.health_image2, self.health_image2_rect)
        self.drawUpgradeButton(self.stamina_image, self.stamina_image_rect)
        self.drawUpgradeButton(self.cooldown_image, self.cooldown_image_rect)
        self.drawUpgradeButton(self.melee_attack_image, self.melee_attack_image_rect)

        for button in self.buttonsUp:
            button.update(getattr(self.player, 'level_'+'_'.join(button.parameter_name.split()), None))
            button.draw(self.screen)



    def draw_background(self, surface, rect, color1, color2):
        gradient_surface = pygame.Surface((rect.width, rect.height))
        for y in range(rect.height):
            color = (
                int(color1[0] * (1 - y / rect.height) + color2[0] * (y / rect.height)),
                int(color1[1] * (1 - y / rect.height) + color2[1] * (y / rect.height)),
                int(color1[2] * (1 - y / rect.height) + color2[2] * (y / rect.height))
            )
            pygame.draw.line(gradient_surface, color, (0, y), (rect.width, y))
        pygame.draw.rect(gradient_surface, color2, gradient_surface.get_rect(), 4)
        surface.blit(gradient_surface, rect)

    def drawUpgradeButton(self, image, rect):
        self.draw_background(self.screen, rect, (75, 0, 130), (139, 0, 139))
        self.screen.blit(image, rect)

    def draw_upgrade_points(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        text = f"Upgrade Points: {self.player.UpPoints}"
        upgrade_points_text = self.font.render(text, True, 'white')
        text_rect = upgrade_points_text.get_rect(center=(100, 30))
        pygame.draw.rect(surf, (0, 0, 0), text_rect.inflate(10, 10))
        surf.blit(upgrade_points_text, text_rect)

    def draw_ui(self, Learning_Surf=None):
        self.update_rect()
        self.drawBarsForStatePlayer()
        self.draw_weapon_interface()
        self.draw_upgrade_points()

        if Learning_Surf is not None:
            self.update_rect(Learning_Surf)
            self.drawBarsForStatePlayer(Learning_Surf)
            self.draw_weapon_interface(Learning_Surf)
            self.draw_upgrade_points(Learning_Surf)


class ButtonUpgrade(pygame.sprite.Sprite):
    def __init__(self, pos, parameter_name, font):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(UI_IMAGE_PATHS['button_for_upgrade']).convert_alpha(),
                                            (200, 150))
        self.rect = self.image.get_rect(topleft=pos)

        self.parameter_name = parameter_name
        self.font = font

        self.level = 0

        self.text_bg_rect = pygame.Rect(self.rect.left, self.rect.y - 300, self.rect.width, 50)
        self.name_text = self.font.render(self.parameter_name, False, (255, 0, 0))
        self.text_rect = self.name_text.get_rect(center=(self.rect.centerx, self.rect.y - 280))
        self.level_text = self.font.render(f"Level: {self.level}", False, (255, 215, 0))
        self.text_rect = self.name_text.get_rect(center=(self.rect.centerx, self.rect.y - 280))
        self.level_rect = self.level_text.get_rect(center=(self.rect.centerx, self.rect.y - 225))

        # shading
        self.shadow_offset = 2
        self.shadow_text_rect = self.text_rect.copy()
        self.shadow_text_rect.move_ip(self.shadow_offset, self.shadow_offset)
        self.shadow_text = self.font.render(self.parameter_name, True, (0, 0, 0))

        self.click = False
        self.click_time = None

    def register_click(self):
        self.click_time = pygame.time.get_ticks()
        self.click = True
        self.rect.inflate_ip(-10, -10)

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def cooldown(self):
        cur_time = pygame.time.get_ticks()
        if self.click and cur_time - self.click_time >= 100:
            self.click = not self.click
            self.rect.inflate_ip(10, 10)

    def update_level(self, cur_level):
        self.level = cur_level
        self.level_text = self.font.render(f"Level: {self.level}", False, (255, 215, 0))

    def update(self, cur_level):
        self.update_level(cur_level)
        self.cooldown()


    def draw(self, screen):
        pygame.draw.rect(screen, 'red', self.rect)

        screen.blit(self.image, self.rect)

        pygame.draw.rect(screen, (255, 255, 255), self.text_bg_rect)
        pygame.draw.rect(screen, '#45322E', self.text_bg_rect, 4)
        screen.blit(self.name_text, self.text_rect)
        screen.blit(self.level_text, self.level_rect)

        if self.is_hovered(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, (255, 215, 0), self.rect, 8)
        else:
            pygame.draw.rect(screen, 'gold' if self.click else '#45322E', self.rect, 4)

        screen.blit(self.shadow_text, self.shadow_text_rect)
