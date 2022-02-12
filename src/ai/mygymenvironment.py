import sys

import gym
import pygame
from gym import spaces
from game.runnergame import RunnerGame


def check_press_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


class MyGymEnvironment(gym.Env):
    def __init__(self, env_config={}):
        self._game = RunnerGame()

        # l1 - state in the space (0 - on the ground, 1...200 y position in the air)
        # l2 - player gravity [-20, 20]
        # l3 - 1-st closest obstacle type to player (0 - no obstacle, 1 - snail, 2 - fly)
        # l4 - 1-st closest obstacle to player x position [-100, 200]
        self.l1n = 201
        self.l2n = 41
        self.l3n = 3
        self.l4n = 301

        self.observation_space = spaces.Discrete(self.l1n*self.l2n*self.l3n*self.l4n)

        # 1 - press space (to jump), 0 - not press space (not to jump)
        self.action_space = gym.spaces.Discrete(2)

    @property
    def observation(self):
        l1 = self._game.player.height
        l2 = 20 + self._game.player.gravity
        l3 = 0
        l4 = 0
        if len(self._game.obstacles) > 0:
            obs = self._game.obstacles[0]
            if obs.type == 'snail':
                l3 = 1
            else:
                l3 = 2
            l4 = min(max(obs.rect.x + 100, 0), 300)
        return l1 + l2 * self.l1n + l3 * self.l2n * self.l1n + l4 * self.l3n * self.l2n * self.l1n

    def reset(self):
        """ Reset the environment to the initial state """
        self._game.reset()
        self._game.start()
        return self.observation

    def render(self, mode="human"):
        if mode == "human":
            self._game.render()
        elif mode == "fast_human":
            self._game.render(1000)
        check_press_quit()

    def step(self, action: int):
        # perform one step in the game logic
        if action == 1:
            jump = True
        else:
            jump = False
        self._game.player.action(jump)
        self._game.update()
        obs = self.observation
        reward = self._game.score
        done = self._game.is_done
        if done:
            reward = -100
        return obs, reward, done, {}

    def mute_game_on(self):
        self._game.mute_on()

    def mute_game_off(self):
        self._game.mute_off()



