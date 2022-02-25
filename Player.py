import os
from enum import Enum

import pygame


class State(Enum):
    IDLE = 0
    MOVING = 1
    JUMPING = 2
    FALLING = 3
    LADDER = 4


class Player(pygame.sprite.Sprite):
    def __init__(self, startx=0, starty=0):
        pygame.sprite.Sprite.__init__(self)
        # Player Stats
        self.steps = 3
        #self.steps = 10

        # Get sprites
        self.images = []

        # add spites to image list
        for i in range(1, 12):
            img = pygame.image.load(os.path.join('Sprites/Player', 'Walk_cycle_-_Emu' + str(i) + '.png'))
            img.convert_alpha()  # optimise alpha
            #img.set_colorkey((0, 0, 0))  # remove background
            self.images.append(img)
        self.image = self.images[0]

        # create rect for player
        self.rect = self.image.get_rect()
        self.rect.x = startx
        self.rect.y = starty

        # movement options
        self.movex = 0  # move along X
        self.movey = 0  # move along Y
        self.frame = 0  # count frames

        # Jumping and falling
        # self.in_jumping = True
        self.fall = True
        self.state = State.IDLE
        self.near_ladder = False
        self.death = False

    def jump(self):
        self.movey = -5.2
        return

    # IDLE STATE
    def idle(self, command):
        self.movex = 0
        if self.fall:
            self.state = State.FALLING
            self.falling(command)

        elif command == "left" or command == "right":
            self.state = State.MOVING
            self.moving(command)

        elif command == "jump":
            self.state = State.JUMPING
            self.jump()

        elif self.near_ladder and (command == "up" or command == "down"):
            self.state = State.LADDER
            self.ladder(command)


        return

    # MOVING STATE
    def moving(self, command):
        if self.fall:
            self.state = State.FALLING
            self.falling(command)

        elif command == "":
            self.movex = 0
            self.state = State.IDLE
        elif command == "right":
            self.movex = self.steps
        elif command == "left":
            self.movex = -self.steps
        elif command == "jump":
            self.state = State.JUMPING
            self.jump()

        elif self.near_ladder and (command == "up" or command == "down"):
            self.state = State.LADDER
            self.ladder(command)

        return

    # JUMPING STATE
    def jumping(self, command):
        if command == "right":
            self.movex = self.steps
        elif command == "left":
            self.movex = -self.steps

    # FALLING STATE
    def falling(self, command):
        self.movex = 0
        if not self.fall:
            self.state = State.IDLE
            self.control(command)
        return

    # LADDER STATE
    def ladder(self, command):
        self.movex = 0
        if command == "up":
            self.movey = -self.steps
        elif command == "down":
            self.movey = self.steps
        #elif command == "":
        #    self.movey = 0
        return

    # handles commands from the player
    def control(self, command):
        if self.state == State.IDLE:
            self.idle(command)

        elif self.state == State.MOVING:
            self.moving(command)

        elif self.state == State.JUMPING:
            self.jumping(command)

        elif self.state == State.LADDER:
            self.ladder(command)

        elif self.state == State.FALLING:
            self.falling(command)
        return

    def gravity(self):

        if self.state == State.LADDER:  # no gravity when in ladder
            return

        self.movey += 0.3
        if self.movey > 5:
            self.movey = 5


    def update(self):
        if self.death:
            return


        if self.state != State.JUMPING and self.fall:   # just in case to prevent errors
            self.state = State.FALLING
            self.falling("")

        # Update sprite position
        self.rect.x += self.movex
        self.rect.y += self.movey

        # moving left
        if self.movex < 0:
            self.frame += 1
            if self.frame >= 11:
                self.frame = 0
            self.image = self.images[self.frame]
        # moving right
        if self.movex > 0:
            self.frame += 1
            if self.frame >= 11:
                self.frame = 0
            self.image = pygame.transform.flip(self.images[self.frame], True, False)


    def die(self):
        self.death = True


    def render(self, display, debug=False):
        display.blit(self.image, self.rect)
        if debug:
            pygame.draw.rect(display, (255, 255, 0), self.rect)
