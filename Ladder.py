import os

import pygame


class Ladder(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc , ladderModel):
        pygame.sprite.Sprite.__init__(self)
        self.ladderModel = ladderModel
        self.rect = self.ladderModel.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

    def render(self, display, debug=False):
        display.blit(self.ladderModel.image, self.rect)
        if debug:
            pygame.draw.rect(display, (255, 0, 0), self.rect)
