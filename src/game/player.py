import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        walk_1 = pygame.image.load('../graphics/Player/player_walk_1.png').convert_alpha()
        walk_2 = pygame.image.load('../graphics/Player/player_walk_2.png').convert_alpha()
        self._walks = [walk_1, walk_2]
        self._index = 0.0
        self._jump_img = pygame.image.load('../graphics/Player/jump.png').convert_alpha()
        self.image = self._walks[int(self._index)]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self._gravity = 0
        self._jump_sound = pygame.mixer.Sound('../audio/jump.mp3')
        self._jump_sound.set_volume(0.1)
        self.mute_on = False

    @property
    def gravity(self):
        return self._gravity

    @property
    def height(self):
        return 300 - self.rect.bottom

    def _jump(self):
        self._gravity = -20
        if not self.mute_on:
            self._jump_sound.play()

    def action(self, to_jump: bool = True):
        if to_jump and self.rect.bottom == 300:
            self._jump()

    def apply_gravity(self):
        self._gravity += 1
        if self._gravity >= 20:
            self._gravity = 20
        self.rect.bottom += self._gravity
        if self.rect.bottom > 300:
            self.rect.bottom = 300

    def animation(self):
        if self.rect.bottom == 300:
            self._index += 0.1
            if self._index > len(self._walks):
                self._index = 0
            self.image = self._walks[int(self._index)]
        else:
            self.image = self._jump_img

    def reset(self):
        self.rect.bottom = 300
        self._gravity = 0

    def update(self):
        self.apply_gravity()
        self.animation()
