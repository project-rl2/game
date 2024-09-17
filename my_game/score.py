import pygame.font
from my_game.config import FONT, FONT_SIZE, SCREEN_WIDTH


class Score:
    def __init__(self, screen, stats):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.stats = stats
        self.text_color = (139, 195, 74)
        self.font = pygame.font.Font(FONT, FONT_SIZE + 10)

        self.score_image = None
        self.score_rect = None
        self.max_score_image = None
        self.max_score_rect = None

        self.create_images()

    def create_images(self):
        self.render_current_score()
        self.render_max_score()

    def render_current_score(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        self.score_image = self.font.render(str(self.stats.DefeatedEnemies), True, self.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = surf.get_rect().right - 40
        self.score_rect.top = 20

    def render_max_score(self, Learning_Surf=None):
        surf = Learning_Surf if Learning_Surf is not None else self.screen

        self.max_score_image = self.font.render(str(self.stats.maxDefeatedEnemies), True, self.text_color)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.top = 20
        self.max_score_rect.right = surf.get_rect().left + surf.get_width() / 2

    def draw(self, Learning_Surf=None):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)

        if Learning_Surf is not None:
            self.render_max_score(Learning_Surf)
            self.render_current_score(Learning_Surf)
            Learning_Surf.blit(self.score_image, self.score_rect)
            Learning_Surf.blit(self.max_score_image, self.max_score_rect)


    def update(self, stats):
        self.stats = stats

        if self.stats.DefeatedEnemies > self.stats.maxDefeatedEnemies:
            self.stats.maxDefeatedEnemies = self.stats.DefeatedEnemies
            self._save_new_record(self.stats.maxDefeatedEnemies)
        self.render_max_score()
        self.render_current_score()

    def _save_new_record(self, max_score):
        with open('my_game/record.txt', 'w') as file:
            file.write(str(max_score))