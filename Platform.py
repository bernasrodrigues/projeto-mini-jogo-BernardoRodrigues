import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, xloc, yloc, platformModel):
        pygame.sprite.Sprite.__init__(self)
        self.platformModel = platformModel
        self.rect = self.platformModel.image.get_rect()
        self.rect.y = yloc
        self.rect.x = xloc

    def render(self, display, debug=False):
        display.blit(self.platformModel.image, self.rect)
        if debug:
            pygame.draw.rect(display, (255, 0, 0), self.rect)
