import sys
from random import choice

import pygame

from game.obstacle import Obstacle
from game.player import Player

OBSTACLE_TIMER = 80


class RunnerGame:
    _game_active: bool
    _start_time: int
    _score: int
    _obstacle_c: int

    def __init__(self):
        pygame.init()
        self._screen = pygame.display.set_mode((800, 400))
        pygame.display.set_caption('pygame-init')
        self._clock = pygame.time.Clock()
        self._font = pygame.font.Font('../font/Pixeltype.ttf', 50)

        self._sky_surface = pygame.image.load('../graphics/Sky.png').convert()
        self._ground_surface = pygame.image.load('../graphics/ground.png').convert()

        self._player_stand_surf = pygame.image.load('../graphics/Player/player_stand.png').convert_alpha()
        self._player_stand_surf = pygame.transform.scale2x(self._player_stand_surf)
        self._player_stand_rect = self._player_stand_surf.get_rect(center=(400, 200))
        self._name_surf = self._font.render('The runner game', False, (111, 196, 169))
        self._name_rect = self._name_surf.get_rect(midbottom=(400, 100))
        self._start_surf = self._font.render('Press return to start...', False, (111, 196, 169))
        self._start_surf = pygame.transform.rotozoom(self._start_surf, 0, 0.5)
        self._start_rect = self._start_surf.get_rect(midtop=(400, 300))

        self._bg_music = pygame.mixer.Sound('../audio/music.wav')
        self._bg_music.set_volume(0.05)

        self._mute_on = False

        # Groups
        self._player = pygame.sprite.GroupSingle()
        self._player.add(Player())
        self._obstacles = pygame.sprite.Group()

        self.reset()

    def reset(self):
        """ Reset game to the initial state and stop it """
        self._game_active = False
        self._start_time = 0
        self._score = 0
        self.player.reset()
        self._obstacles.empty()
        self._obstacle_c = 0
        self._bg_music.stop()

    def start(self):
        self._game_active = True
        self._start_time = int(pygame.time.get_ticks() / 1000)
        if not self._mute_on:
            self._bg_music.play(loops=-1)

    def mute_on(self):
        self._bg_music.stop()
        self._mute_on = True
        self.player.mute_on = True

    def mute_off(self):
        if not self._mute_on:
            return
        self._mute_on = False
        self.player.mute_on = False
        if self._game_active:
            self._bg_music.play(loops=-1)

    @property
    def player(self) -> Player:
        # noinspection PyTypeChecker
        return self._player.sprite

    @property
    def obstacles(self):
        # noinspection PyTypeChecker
        return self._obstacles.sprites()

    @property
    def score(self):
        return self._score

    @property
    def is_done(self):
        return not self._game_active

    def _display_score(self):
        surf = self._font.render(f'Score: {self._score}', False, (64, 64, 64))
        rect = surf.get_rect(center=(400, 50))
        self._screen.blit(surf, rect)

    def stop(self):
        self._game_active = False

    def run_game(self):
        while True:
            self._check_events()
            self.update()
            self.render()

    def render(self, frame_rate=60):
        self._update_screen()
        self._clock.tick(frame_rate)

    def _update_screen(self):
        if self._game_active:
            self._update_screen_active()
        else:
            self._update_screen_non_active()
        pygame.display.update()

    def _add_obstacle(self):
        self._obstacle_c += 1
        if self._obstacle_c >= OBSTACLE_TIMER:
            self._obstacle_c = 0
            self._obstacles.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))

    def update(self):
        self._score = int(pygame.time.get_ticks() / 1000) - self._start_time
        self._add_obstacle()
        self._player.update()
        self._obstacles.update()
        self._check_collisions()

    def _update_screen_non_active(self):
        self.reset()
        self._screen.fill((94, 129, 162))
        self._screen.blit(self._player_stand_surf, self._player_stand_rect)
        score_surf = self._font.render(f'Your score: {self._score}', False, (111, 196, 169))
        score_rect = score_surf.get_rect(center=(400, 330))
        self._screen.blit(self._name_surf, self._name_rect)
        if self._score > 0:
            self._screen.blit(score_surf, score_rect)
        else:
            self._screen.blit(self._start_surf, self._start_rect)

    def _update_screen_active(self):
        self._screen.blit(self._sky_surface, (0, 0))
        self._screen.blit(self._ground_surface, (0, 300))
        self._display_score()
        self._player.draw(self._screen)
        self._obstacles.draw(self._screen)

    def _check_collisions(self):
        if pygame.sprite.spritecollide(self._player.sprite, self._obstacles, False):
            self.stop()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if self._game_active:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    self.player.action(True)
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.start()
