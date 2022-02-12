from random import randint

import pygame


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, o_type):
        super().__init__()

        if o_type == 'fly':
            frame_1 = pygame.image.load('../graphics/Fly/Fly1.png').convert_alpha()
            frame_2 = pygame.image.load('../graphics/Fly/Fly2.png').convert_alpha()
            y_pos = 210
            self.speed = 0.3
        else:
            frame_1 = pygame.image.load('../graphics/snail/snail1.png').convert_alpha()
            frame_2 = pygame.image.load('../graphics/snail/snail2.png').convert_alpha()
            y_pos = 300
            self.speed = 0.2

        self.frames = [frame_1, frame_2]
        self._type = o_type
        self._index = 0
        self.image = self.frames[self._index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    @property
    def type(self):
        return self._type

    def animation(self):
        self._index += self.speed
        if self._index > len(self.frames):
            self._index = 0
        self.image = self.frames[int(self._index)]

    def update(self):
        self.animation()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x < -100:
            self.kill()