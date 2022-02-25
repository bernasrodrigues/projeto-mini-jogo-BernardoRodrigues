import os

import pygame


class LadderModel:
    def __init__(self) -> None:
        self.image = pygame.image.load(os.path.join('Sprites/Platforms', "ladder.png"))
        self.image.convert_alpha()
