import os

import pygame

from EggPoint import EggPoint
from Enemy import Enemy
from Ladder import Ladder
from LadderModel import LadderModel
from Platform import Platform
from PIL import Image
from PlatformModel import PlatformModel
from Player import Player


class LevelLoader:
    __instance = None

    @staticmethod
    def getInstance() -> __instance:
        if LevelLoader.__instance is None:
            LevelLoader()
        return LevelLoader.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if LevelLoader.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # level variables (size, current level ...
            self.directory = os.path.join('Levels/')
            self.currentLevel = 0
            self.wordx = 0
            self.wordy = 0

            # level objects
            self.player = None
            self.enemies = pygame.sprite.Group()
            self.platform = pygame.sprite.Group()
            self.ladders = pygame.sprite.Group()
            self.points = pygame.sprite.Group()

            self.platformModel = PlatformModel()
            self.ladderModel = LadderModel()
            LevelLoader.__instance = self

    # Return a list of the position of the bits that are 1
    def findsetbits(self, number):
        bits = bin(number)
        setbits = ([i - 1 for i, digit in enumerate(reversed(bits), 1) if digit == '1'])
        return setbits

    def handleRed(self, red, i, j):
        setbits = self.findsetbits(red)

        # 0 equals player
        if 0 in setbits:
            player = Player(startx=(i * 32), starty=(j * 32))
            self.player = player

        # 1 equals enemy
        if 1 in setbits:
            enemy = Enemy(x=(i * 32), y=(j * 32))
            self.enemies.add(enemy)
        return

    def handleGreen(self, green, i, j):
        setbits = self.findsetbits(green)

        if 0 in setbits:
            point = EggPoint(xloc=(i * 32), yloc=(j * 32))
            self.points.add(point)

        return

    def handleBlue(self, blue, i, j):
        setbits = self.findsetbits(blue)

        # 0 equals platforms
        if 0 in setbits:
            platform = Platform(xloc=(i * 32), yloc=(j * 32), platformModel=self.platformModel)
            self.platform.add(platform)

        # 1 equals ladders
        if 1 in setbits:
            ladder = Ladder(xloc=(i * 32), yloc=(j * 32), ladderModel=self.ladderModel)
            self.ladders.add(ladder)
        return

    def loadLevel(self, leve_number):
        # Reset variables
        self.player = None
        self.enemies = pygame.sprite.Group()
        self.platform = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.points = pygame.sprite.Group()
        self.currentLevel = leve_number

        try:
            im = Image.open(self.directory + str(leve_number) + ".png")  # Can be many different formats.
        except FileNotFoundError:
            print("Level not found")
            return None , None, None, None, None, None

        levelSize = im.size
        self.wordx = im.size[0] * 32
        self.wordy = im.size[1] * 32

        pix = im.load()

        # i = column , j = line
        for i in range(levelSize[0]):
            for j in range(levelSize[1]):
                # print((i, j))
                # print(pix[i, j])
                p = pix[i, j]
                self.handleRed(p[0], i, j)
                self.handleGreen(p[1], i, j)
                self.handleBlue(p[2], i, j)

        return self.player, self.enemies, self.platform, self.ladders, self.points, (self.wordx, self.wordy)
