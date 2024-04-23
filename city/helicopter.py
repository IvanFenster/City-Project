import math

import city.City
import settings
from city import City
import random
from ui import graphics
from storage import storage
import time
import constants
class Helicopter():
    def __init__(self, call):
        self.image1 = storage.im_dict['hel1']
        self.image2 = storage.im_dict['hel2']
        self.image3 = storage.im_dict['hel3']

        self.length = 100
        self.width = 100
        self.speed = 1
        self.call = call
        self.degree = 0

        self.place_heli()



    def place_heli(self):
        self.direction = random.choice([[1, 1], [-1, 1], [-1, -1], [1, -1]])
        self.x = self.call[0] - self.direction[0] * 900
        self.y = self.call[1] - self.direction[1] * 900
        self.degree = self.direction_to_degree(self.direction)


    def direction_to_degree(self, direction):
        if direction == [1, 1]:
            return -135
        elif direction == [-1, 1]:
            return 135
        elif direction == [-1, -1]:
            return 45
        elif direction == [1, -1]:
            return -45


    def update(self):
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        print(self.x, self.y)



    def draw(self):
        if City.time_city % 6 <= 1:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel1'], self.degree), self.x - self.length / 2, self.y - self.width / 2)
        elif City.time_city % 6 <= 3:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel2'], self.degree), self.x - self.length / 2, self.y - self.width / 2)
        elif City.time_city % 6 <= 5:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel3'], self.degree), self.x - self.length / 2, self.y - self.width / 2)

