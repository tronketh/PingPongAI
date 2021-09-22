import math
from enum import Enum

from game.coordinate_system.point import Point
from game.game_objects.ball import Ball
from game.game_objects.game_object import GameObject
from game import constants
from game.game_objects.collider_type import ColliderType

import pygame


class BatDirection(Enum):
    UP = 'up'
    DOWN = 'down'


class Bat(GameObject):
    def __init__(self, position: Point = Point(0, 0),
                 height=constants.BAT_HEIGHT, width=constants.BAT_WIDTH, speed=constants.BAT_SPEED,
                 radius_of_curvature=constants.BAT_RADIUS):
        super(Bat, self).__init__(speed=speed, position=position)
        self.radius_of_curvature = radius_of_curvature
        self.height = height
        self.width = width
        self.direction = None
        self.can_move = False

    def reset(self):
        super(Bat, self).reset()
        self.direction = None
        self.can_move = False

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, self.color, pygame.Rect(*self.position, self.width, self.height))

    def ball_collision(self, ball: Ball):
        x_dist = Point.x_distance(ball.position, self.position)
        y_dist = Point.y_distance(ball.position, self.position, absolute=True)
        if x_dist <= self.width + ball.radius:
            if self.height >= y_dist >= 0:
                ball.collision(ColliderType.BAT, self.__get_collision_delta(ball.position, ball.position.x))
                return True
        return False

    def __get_collision_delta(self, point_of_impact: Point, ball_x):
        y_dist = Point.y_distance(point_of_impact, self.position)
        y_dist -= self.height / 2
        s = -y_dist / self.radius_of_curvature
        radians = math.asin(s)
        delta_angle = math.degrees(radians)
        if ball_x > self.position.x:
            delta_angle += 45
        else:
            delta_angle *= -1
        delta_angle = 0
        return delta_angle

    def move(self):
        if self.can_move:
            _, y = pygame.display.get_surface().get_size()
            if self.direction == BatDirection.UP and self.position.y >= 0:
                self.position.y -= self.speed
            elif self.direction == BatDirection.DOWN and self.position.y <= y - self.height:
                self.position.y += self.speed
        self.direction = None

    def change_direction(self, direction: BatDirection):
        self.direction = direction
