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

        self.derection = random.choice([[1, 1], [-1, 1], [-1, -1], [1, -1]])

        self.center = self.find_center(self.x, self.y)


    def place_heli(self, call):
        self.x = call[0] - self.spawn[0] * 900
        self.y = call[1] - self.spawn[1] * 900




    def find_center(self):
        x = self.x + self.length
        y = self.y + self.width
        return [x, y]

    def draw(self):
        pass


