from game.coordinate_system.vector import Vector
from game.game_objects.game_object import GameObject
from game import constants
from game.game_objects.collider_type import ColliderType

import pygame
from random import uniform


class Ball(GameObject):
    def __init__(self, position: Vector = Vector(0, 0), radius=constants.BALL_RADIUS,
                 speed=Vector(constants.BALL_SPEED, 0)):
        super(Ball, self).__init__(speed=speed, position=position, color=constants.BLUE)
        self.radius = radius
        angle = uniform(-constants.BALL_ANGLE_ALPHA, constants.BALL_ANGLE_ALPHA) * 90
        self.speed.rotate(angle)

    def reset(self):
        super(Ball, self).reset()
        angle = uniform(-constants.BALL_ANGLE_ALPHA, constants.BALL_ANGLE_ALPHA) * 90
        self.speed = Vector(constants.BALL_SPEED, 0)
        self.speed.rotate(angle)

    def move(self):
        self.position += self.speed

    def draw(self):
        screen = pygame.display.get_surface()
        pygame.draw.circle(screen, self.color, list(self.position), self.radius)

    def collision(self, obj: ColliderType, angle_delta=0):
        self.speed.rotate(angle_delta)
        if obj == ColliderType.BORDER:
            self.speed.y *= -1
        elif obj == ColliderType.BAT:
            self.speed.x *= -1
            self.speed.rotate(angle_delta)
