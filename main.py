import os

import pygame
import pygame.gfxdraw
from pygame.locals import *

from LevelLoader import LevelLoader
from Manager.MusicManager import MusicManager
from Manager.ScoreManager import ScoreManager
from Player import State

# Setup
from Point import Point
from Subject_Observer.Subject import Subject
from Subject_Observer.created_events import POINT_EVENT, DEATH_EVENT

WORLDX, WORLDY = 980, 600
SCALE = 1
FPS = 30  # frame rate

# Command list
MOVE_UP, MOVE_UP_ALTERNATIVE = pygame.K_UP, pygame.K_w
MOVE_DOWN, MOVE_DOWN_ALTERNATIVE = pygame.K_DOWN, pygame.K_s
MOVE_LEFT, MOVE_LEFT_ALTERNATIVE = pygame.K_LEFT, pygame.K_a
MOVE_RIGHT, MOVE_RIGHT_ALTERNATIVE = pygame.K_RIGHT, pygame.K_d
JUMP, JUMP_ALTERNATIVE = pygame.K_SPACE, pygame.K_z
RESTART = pygame.K_r
PAUSE = pygame.K_p


# Window initial position
os.environ['SDL_VIDEO_WINDOW_POS'] = str(50) + "," + str(50)


# Check collisions between two objects
def check_collide(rect1, rect2):
    rect1_Ltop_vertex = [rect1.left, rect1.top]  # r1 min
    rect2_Ltop_vertex = [rect2.left, rect2.top]  # r2 min

    rect1_Rbot_vertex = [rect1.left + rect1.width, rect1.top + rect1.height]  # r1 max
    rect2_Rbot_vertex = [rect2.left + rect2.width, rect2.top + rect2.height]  # r2 max

    # = b.min.x - a.max.x
    d1x = rect2_Ltop_vertex[0] - rect1_Rbot_vertex[0]
    # = b.min.y - a.max.y
    d1y = rect2_Ltop_vertex[1] - rect1_Rbot_vertex[1]
    # = a.min.x - b.max.x
    d2x = rect1_Ltop_vertex[0] - rect2_Rbot_vertex[0]
    # = a.min.y - b.max.y
    d2y = rect1_Ltop_vertex[1] - rect2_Rbot_vertex[1]

    if d1x > 0 or d1y > 0 or d2x > 0 or d2y > 0:
        return False

    return True


class Game(Subject):
    def __init__(self):
        # Game details
        super().__init__()
        self.lastcommnad = None
        self.display = pygame.display.set_mode((SCALE * 1, SCALE * 1), HWSURFACE | DOUBLEBUF | RESIZABLE)  # initialize display
        self.clock = pygame.time.Clock()
        self.tick = FPS

        # Loading the level
        self.player, self.enemies, self.platforms, self.ladders, self.points, size = LevelLoader.getInstance().loadLevel(1)

        # Set display
        pygame.display.set_caption('Chuckie Egg')
        self.display = pygame.display.set_mode((SCALE * size[0], SCALE * size[1]), HWSURFACE | DOUBLEBUF | RESIZABLE)
        self.fake_screen = self.display.copy()
        ev = pygame.event.Event(VIDEORESIZE, {'size': (1000, 1000)})
        pygame.event.post(ev)

        # Add observers
        self.addObserver(ScoreManager.getInstance())
        self.addObserver(MusicManager.getInstance())

    # checks collisions between the player and the platforms
    def player_platform_collision(self):
        if self.player.state == State.LADDER:
            return

        self.player.fall = True
        for platform in self.platforms:
            if check_collide(platform.rect, self.player.rect):
                # Check collide with top
                if platform.rect.top <= self.player.rect.bottom <= platform.rect.top + 10:
                    self.player.rect.bottom = platform.rect.top
                    self.player.fall = False

                    if self.player.state == State.JUMPING:
                        self.player.state = State.IDLE
                        self.player.control(self.lastcommnad)

                # Check collide left side
                elif platform.rect.left + 2 <= self.player.rect.right <= platform.rect.left + 10:
                    self.player.rect.right = platform.rect.left

                # Check collide right side
                elif platform.rect.right - 10 <= self.player.rect.left <= platform.rect.right:
                    self.player.rect.left = platform.rect.right

    def player_border_limit(self):
        max_x = self.fake_screen.get_size()[0]
        max_y = self.fake_screen.get_size()[1]

        if self.player.rect.left > max_x:
            self.player.rect.right = 0
        if self.player.rect.right < 0:
            self.player.rect.x = max_x

        if self.player.rect.y > max_y + 4:
            ev = pygame.event.Event(DEATH_EVENT)
            pygame.event.post(ev)



    # checks collisions between the player and the ladders
    def player_ladder_collision(self):
        if self.player.state == State.LADDER:  # if in the ladder
            # get nearest ladder
            player_pos = pygame.math.Vector2(self.player.rect.x, self.player.rect.y)
            ladder = min([l for l in self.ladders],
                         key=lambda l: player_pos.distance_to(pygame.math.Vector2(l.rect.x, l.rect.y)))

            # Check if there is any ladder in the top or in the bottom of the ladder the player is on
            ladder_top = False
            ladder_bot = False

            for l in self.ladders:
                if l.rect.x == ladder.rect.x:
                    if l.rect.y == ladder.rect.y + 32:
                        ladder_bot = True
                    elif l.rect.y == ladder.rect.y - 32:
                        ladder_top = True

            # If there isn't any ladder next to the one the player is on (up or down) the player can them move
            if not ladder_top and self.player.rect.bottom < ladder.rect.top:
                self.player.rect.bottom = ladder.rect.top
                self.player.state = State.JUMPING

            if not ladder_bot and self.player.rect.bottom > ladder.rect.bottom:
                self.player.rect.bottom = ladder.rect.bottom
                self.player.state = State.JUMPING

        for ladder in self.ladders:
            if check_collide(ladder.rect, self.player.rect):
                self.player.near_ladder = True
                return
        self.player.near_ladder = False

    def player_point_collision(self):
        for point in self.points:
            if check_collide(point.rect, self.player.rect):
                ev = pygame.event.Event(POINT_EVENT, {'point': point})
                pygame.event.post(ev)
        return

    def player_enemies_collision(self):
        for enemy in self.enemies:
            if check_collide(enemy.rect, self.player.rect):
                ev = pygame.event.Event(DEATH_EVENT)
                pygame.event.post(ev)

    # checks collisions between the enemies and the platforms
    def enemy_platform_collision(self):
        for enemy in self.enemies:
            for platform in self.platforms:
                if check_collide(platform.rect, enemy.rect):
                    if platform.rect.top <= enemy.rect.bottom <= platform.rect.top + 10:
                        enemy.rect.bottom = platform.rect.top
                        enemy.movey = 0


    # updates all the entities
    def entities_update(self):
        # Update player
        self.player.update()
        self.player.gravity()

        # Update collisions with player
        self.player_border_limit()
        self.player_platform_collision()
        self.player_ladder_collision()
        self.player_point_collision()
        self.player_enemies_collision()

        # Update enemies
        for enemy in self.enemies:
            enemy.update()
        for enemy in self.enemies:
            enemy.gravity()
        self.enemy_platform_collision()
        return

    # Renders all objects in the scene
    ''' order of renders:
        -> platforms
        -> ladders
        -> enemies
        -> player
        (player always appears in front of other objects'''

    def render(self):
        self.fake_screen.fill("black")  # black background
        # Render platforms
        for platform in self.platforms:
            platform.render(display=self.fake_screen)

        for ladder in self.ladders:
            ladder.render(display=self.fake_screen)

        # Render Points
        for point in self.points:
            point.render(display=self.fake_screen)

        # Render enemies
        for enemy in self.enemies:
            enemy.render(display=self.fake_screen)

        # Render Player
        self.player.render(display=self.fake_screen)

        # ScoreManager.getInstance().render(display=self.fake_screen)

        # pass the fake_screen into the display screen
        self.display.blit(pygame.transform.scale(self.fake_screen, self.display.get_rect().size), (0, 0))
        # Render score
        ScoreManager.getInstance().render(display=self.display)
        pygame.display.flip()

    # Update
    def loop(self):
        running = True
        death = False
        pause = False

        while running:

            # Death state
            while death:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        death = False
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == RESTART:
                            pass

            # Pause state
            while pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pause = False
                        running = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == PAUSE:
                            pause = False

            # Main loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == VIDEORESIZE:
                    self.display = pygame.display.set_mode(event.size, HWSURFACE | DOUBLEBUF | RESIZABLE)

                # Keys pressed
                elif event.type == pygame.KEYDOWN:
                    # Up key
                    if event.key == MOVE_UP or event.key == MOVE_UP_ALTERNATIVE:
                        self.lastcommnad = "up"
                        self.player.control("up")
                    # Down key
                    elif event.key == MOVE_DOWN or event.key == MOVE_DOWN_ALTERNATIVE:
                        self.lastcommnad = "down"
                        self.player.control("down")
                    # Left key
                    elif event.key == MOVE_LEFT or event.key == MOVE_LEFT_ALTERNATIVE:
                        self.lastcommnad = "left"
                        self.player.control("left")
                    # Right key
                    elif event.key == MOVE_RIGHT or event.key == MOVE_RIGHT_ALTERNATIVE:
                        self.lastcommnad = "right"
                        self.player.control("right")
                    # Jump key
                    elif event.key == JUMP or event.key == JUMP_ALTERNATIVE:
                        self.lastcommnad = "jump"
                        self.player.control("jump")

                    elif event.key == PAUSE:
                        pause = True
                elif event.type == pygame.KEYUP:
                    self.lastcommnad = ""
                    self.player.control("")

                # Custom Game events
                elif event.type == POINT_EVENT:
                    self.dispatch(event)
                    point: Point = event.point
                    point.pickup()
                    point.kill()

                    # Load new level
                    if len(self.points) == 0:


                        # Load level objects
                        self.player, self.enemies, self.platforms, self.ladders, self.points, size = \
                            LevelLoader.getInstance().loadLevel(LevelLoader.getInstance().currentLevel + 1)

                        # Update buffer and screen size to fit the level
                        if size is not None:
                            screen_size = self.display.get_size()
                            self.display = pygame.display.set_mode((SCALE * size[0], SCALE * size[1]),HWSURFACE | DOUBLEBUF | RESIZABLE)
                            self.fake_screen = self.display.copy()
                            ev = pygame.event.Event(VIDEORESIZE, {'size': screen_size})
                            pygame.event.post(ev)

                        # Game
                        if self.player is None:
                            print("Game Over")
                            exit()

                elif event.type == DEATH_EVENT:
                    self.player.die()
                    self.dispatch(event)
                    death = True

            # Update entities
            self.entities_update()

            # Render the scene
            self.render()
            self.clock.tick(self.tick)


# Running the game
if __name__ == "__main__":
    def main():
        pygame.init()
        g = Game()
        g.loop()
        pygame.quit()


    main()
