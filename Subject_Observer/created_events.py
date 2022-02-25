# Class just to store the created events  (not on main.py to prevent circular import errors)

import pygame

POINT_EVENT = pygame.USEREVENT + 1
DEATH_EVENT = pygame.USEREVENT + 2
NEXT_LEVEL_EVENT = pygame.USEREVENT + 3
