import pygame


class Point(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = 0

    def pickup(self):
        raise NotImplemented()

    def getscore(self):
        return self.points

    def render(self, display, debug=False):
        raise NotImplemented()
