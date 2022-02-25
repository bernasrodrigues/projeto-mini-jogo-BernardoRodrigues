import os

import pygame

from Point import Point
from Subject_Observer.Subject import Subject
from Subject_Observer.created_events import POINT_EVENT, DEATH_EVENT


class ScoreManager(Subject):
    __instance = None

    @staticmethod
    def getInstance() -> __instance:
        if ScoreManager.__instance is None:
            ScoreManager()
        return ScoreManager.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super().__init__()
        if ScoreManager.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # level variables (size, current level ...
            self.score = 0
            self.highscore = 0

            # Read highscore
            try:
                file = open(os.path.join("highscore", "highscore.txt"), "r")
                self.highscore = int(file.read())
                file.close()
            except FileNotFoundError:
                print("No highscore")

            # display score
            self.font = pygame.font.Font('freesansbold.ttf', 32)
            self.text1 = self.font.render('Score: 0', True, "white")
            self.text2 = self.font.render('Highscore: ' + str(self.highscore), True, "white")
            self.rect1 = self.text1.get_rect()
            self.rect2 = self.text2.get_rect()
            self.rect2.y += 48

            ScoreManager.__instance = self





    def notify(self, event):
        if event.type == POINT_EVENT:
            point: Point = event.point
            self.score += point.getscore()

        if event.type == DEATH_EVENT:
            if self.score > self.highscore:
                file = open(os.path.join("highscore", "highscore.txt"), 'w+')
                file.write(str(self.score))
                file.close()

    def render(self, display, debug=False):
        self.text1 = self.font.render("Score: " + str(self.score), True, "white")
        if self.score > self.highscore:
            self.text2 = self.font.render("Highscore: " + str(self.score), True ,"white")

        display.blit(self.text1, self.rect1)
        display.blit(self.text2, self.rect2)

