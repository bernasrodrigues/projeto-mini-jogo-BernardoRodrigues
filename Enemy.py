import os

import pygame


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Get sprites
        self.images = []

        # add spites to image list
        for i in range(1, 12):
            img = pygame.image.load(os.path.join('Sprites/Player', 'Walk_cycle_-_Emu' + str(i) + '.png'))
            img.convert_alpha()  # optimise alpha
            #img.set_colorkey((0, 0, 0))  # remove background
            self.images.append(img)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.movey = 0
        self.counter = 0

    def update(self):
        distance = 80
        speed = 1

        if self.movey != 0:
            self.rect.y += self.movey
            return

        if 0 <= self.counter <= distance:
            self.rect.x += speed
        elif distance <= self.counter <= distance * 2:
            self.rect.x -= speed
        else:
            self.counter = 0

        self.counter += 1

    def gravity(self):
        self.movey = 1

    def render(self, display, debug=False):
        display.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(display, (255, 0, 0), self.rect)
