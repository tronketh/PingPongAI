import numpy as np
import pygame
from game import constants
from game.coordinate_system.vector import Vector
from game.game_objects.bat import Bat, BatDirection
from game.game_objects.ball import Ball
from game.game_objects.collider_type import ColliderType

try:
    from ai.constants import REWARD, PENALTY
except ImportError:
    REWARD = 100
    PENALTY = 100


class PingPong:
    def __init__(self):
        successes, failures = pygame.init()
        print("{0} successes and {1} failures".format(successes, failures))
        pygame.font.init()
        pygame.display.set_caption('Ping Pong')

        self.font = pygame.font.SysFont('Comic Sans MS', constants.FONT_SIZE)
        self.screen = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
        self.clock = pygame.time.Clock()
        self.screen.fill(constants.BLACK)

        left_bat = Bat(position=Vector(constants.INDENTS, (constants.HEIGHT - constants.BAT_HEIGHT) / 2))
        right_bat = Bat(position=Vector(constants.WIDTH - constants.INDENTS,
                                        (constants.HEIGHT - constants.BAT_HEIGHT) / 2))
        self.bats = [left_bat, right_bat]
        self.current_bat = self.bats[1]
        self.current_bat.can_move = True
        self.ball = Ball(position=Vector(constants.WIDTH / 2, constants.HEIGHT / 2))
        self.game_objects = [self.ball, *self.bats]

        self.score = 0
        self.reward = 0
        self.game_over = False

    def reset(self):
        self.screen.fill(constants.BLACK)
        for obj in self.game_objects:
            obj.reset()
        self.current_bat = self.bats[1]
        self.current_bat.can_move = True

        self.score = 0
        self.reward = 0
        self.game_over = False

    def play(self):
        while not self.game_over:
            key_press = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__death()
                    quit()
                elif event.type == pygame.KEYDOWN:

                    break
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_w]:
                self.__play_step([1, 0, 0])
            elif pressed[pygame.K_s]:
                self.__play_step([0, 1, 0])
            else:
                self.__play_step([0, 0, 1])

    def play_ai(self, action):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__death()
                quit()

        self.__play_step(action)
        return self.reward, self.game_over, self.score

    def get_state(self):
        # [ball_up, ball_down] respect tp current bat
        ball_up, ball_down = False, False
        if self.ball.position.y < self.current_bat.position.y:
            ball_up = True
        elif self.ball.position.y > self.current_bat.position.y + self.current_bat.height:
            ball_down = True
        return [ball_up, ball_down]

    def __play_step(self, action):
        self.clock.tick(constants.FPS)
        self.reward = 0

        if np.array_equal(action, [1, 0, 0]):
            self.current_bat.change_direction(BatDirection.UP)
        elif np.array_equal(action, [0, 1, 0]):
            self.current_bat.change_direction(BatDirection.DOWN)

        if self.current_bat.ball_collision(self.ball):
            self.__flip_bat()
            self.reward = REWARD
            self.score += 1

        if self.__check_border_collision():
            self.reward = -PENALTY
            self.__death()

        self.__update()

    def __death(self):
        print(f'Score: {self.score}')
        self.game_over = True

    def __check_border_collision(self):
        if self.ball.position.x <= 0 or self.ball.position.x >= constants.WIDTH:
            return True
        elif self.ball.position.y <= self.ball.radius or self.ball.position.y >= constants.HEIGHT-self.ball.radius:
            self.ball.collision(ColliderType.BORDER)
            return False
        return False

    def __flip_bat(self):
        self.current_bat.can_move = False
        # self.current_bat.reset()
        idx = self.bats.index(self.current_bat)
        self.current_bat = self.bats[(idx + 1) % 2]
        self.current_bat.can_move = True

    def __update(self):
        self.screen.fill(constants.BLACK)
        for obj in self.game_objects:
            obj.update()
        text = self.font.render("Score: " + str(self.score), True, constants.WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.flip()
