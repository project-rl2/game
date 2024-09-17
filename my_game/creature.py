import pygame


class Creature(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.time_existence_corpse = 5000

    def check_collision(self, x, y, direction):

        temp_rect = self.hitbox.copy()
        if direction == 'x':
            temp_rect.x = x
        elif direction == 'y':
            temp_rect.y = y

        for sprite in self.sprites_collision:
            if sprite.hitbox.colliderect(temp_rect):
                if direction == 'x':
                    self.direction.x = 0
                else:
                    self.direction.y = 0
                return False  # collision
        if self.type == "robber":
            for sprite in self.mobs_sprites:
                if sprite != self:
                    if sprite.hitbox.colliderect(temp_rect):
                        return False  # collision

        return True  # not collision

    def load_spritesheet(self, types_of_sprite, type_of_creature, spritesheet):
        for type_of_sprite in types_of_sprite:
            path = 'my_game/images/' + type_of_creature + '_' + type_of_sprite
            for state in spritesheet[type_of_sprite].keys():
                for direction in spritesheet[type_of_sprite]['running'].keys():
                    sprites_path = path + '/' + state + '_' + direction
                    if state in ['attack', 'looking', 'tipping over', 'shooting']:
                        for i in range(12):
                            png_path = sprites_path + '/' + state + ' ' + direction
                            if type_of_creature == 'robber' and i == 8 and state not in ['tipping over', 'shooting',
                                                                                         'attack']:
                                break
                            if i == 9 and type_of_sprite == 'swordsman' and  state == 'tipping over':
                                break

                            if i > 9:
                                png_path = png_path + '00' + str(i)
                            else:
                                png_path = png_path + '000' + str(i)
                            spritesheet[type_of_sprite][state][direction].append(
                                pygame.image.load(png_path + '.png').convert_alpha())
                    else:
                        for i in range(8):
                            png_path = sprites_path + '/' + state + ' ' + direction + '000' + str(i)
                            spritesheet[type_of_sprite][state][direction].append(
                                pygame.image.load(png_path + '.png').convert_alpha())

    def update_state(self):
        if self.state not in ['been hit', 'tipping over']:
            if self.direction.x > 0 and self.direction.y > 0:
                self.orientation = 'se'
            elif self.direction.x > 0 > self.direction.y:
                self.orientation = 'ne'
            elif self.direction.x > 0 and self.direction.y == 0:
                self.orientation = 'e'
            elif self.direction.x == 0 and self.direction.y > 0:
                self.orientation = 's'
            elif self.direction.x == 0 and self.direction.y < 0:
                self.orientation = 'n'
            elif self.direction.x < 0 < self.direction.y:
                self.orientation = 'sw'
            elif self.direction.x < 0 and self.direction.y == 0:
                self.orientation = 'w'
            elif self.direction.x < 0 and self.direction.y < 0:
                self.orientation = 'nw'
            else:
                self.state = 'looking'
        else:
            self.direction = pygame.math.Vector2()

    def update_position(self):
        # Updating the horizontal position
        new_x = self.hitbox.x + self.speed * self.direction.x
        if self.check_collision(new_x, self.hitbox.y, 'x'):
            self.hitbox.x = new_x

        # Updating the vertical position
        new_y = self.hitbox.y + self.speed * self.direction.y
        if self.check_collision(self.hitbox.x, new_y, 'y'):
            self.hitbox.y = new_y

        self.rect.center = self.hitbox.center



