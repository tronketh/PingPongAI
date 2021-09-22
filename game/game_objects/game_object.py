from abc import ABCMeta
from abc import abstractmethod

from game.coordinate_system.point import Point


class GameObject(metaclass=ABCMeta):
    def __init__(self, speed, position: Point, color=[255, 255, 255]):
        self.speed = speed
        self.position = position
        self.initial_position = position.copy()
        self.color = color

    def update(self):
        self.move()
        self.draw()

    def reset(self):
        self.position = self.initial_position.copy()

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def move(self):
        pass
