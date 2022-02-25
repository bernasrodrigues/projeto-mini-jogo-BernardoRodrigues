import os

import pygame

from Point import Point


class EggPoint(Point):
    def __init__(self, xloc, yloc):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join('Sprites/Points', "egg.png"))
        self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

        self.points = 100

    def pickup(self):
        # TODO do some animation when picked up
        return

    def render(self, display, debug=False):
        display.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(display, (255, 0, 0), self.rect)
