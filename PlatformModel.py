import os

import pygame


class PlatformModel:
    def __init__(self) -> None:
        self.image = pygame.image.load(os.path.join('Sprites/Platforms', "ground2.png")).convert()
        self.image.convert_alpha()
        self.image.set_colorkey((0, 255, 0))
