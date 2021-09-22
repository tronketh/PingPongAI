from game.coordinate_system.point import Point
from game.game_objects.game_object import GameObject
from game import constants
from game.game_objects.collider_type import ColliderType

import pygame
from random import uniform


class Ball(GameObject):
    def __init__(self, position: Point = Point(0, 0), radius=constants.BALL_RADIUS, speed=constants.BALL_SPEED):
        super(Ball, self).__init__(speed=speed, position=position, color=constants.BLUE)
        self.radius = radius
        self.angle = uniform(-constants.BALL_ANGLE_ALPHA, constants.BALL_ANGLE_ALPHA) * 90
        # angle will be positive always
        if self.angle < 0:
            self.angle += 360

    def reset(self):
        super(Ball, self).reset()
        self.angle = uniform(-constants.BALL_ANGLE_ALPHA, constants.BALL_ANGLE_ALPHA) * 90
        # angle will be positive always
        if self.angle < 0:
            self.angle += 360

    def move(self):
        self.position.project(self.angle, self.speed)

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, list(self.position), self.radius)

    def collision(self, obj: ColliderType, angle_delta=0):
        if obj == ColliderType.BORDER:
            self.angle = 360 - self.angle
        elif obj == ColliderType.BAT:
            self.angle = 180 - self.angle + (2 * angle_delta)

        if self.angle < 0:
            self.angle += 360
        elif self.angle >= 360:
            self.angle -= 360
