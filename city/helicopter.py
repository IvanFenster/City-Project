import math

import city.City
import settings as set
from city import City
import random
from ui import graphics
from storage import storage
import time
import constants
class Helicopter():
    def __init__(self, car):
        self.image1 = storage.im_dict['hel1']
        self.image2 = storage.im_dict['hel2']
        self.image3 = storage.im_dict['hel3']

        self.length = 100
        self.width = 100
        self.speed = set.heli_speed
        self.call = car.find_center()
        self.degree = 0
        self.car = car


        self.place_heli()

        self.stage = 0
        self.stop_time = None



    def place_heli(self):
        self.direction = random.choice([[1, 1], [-1, 1], [-1, -1], [1, -1]])
        if self.direction == [1, 1]:
            self.x = self.call[0] - (min(self.call[0], self.call[1]) + 110)
            self.y = self.call[1] - (min(self.call[0], self.call[1]) + 110)
            self.degree = -135
        elif self.direction == [-1, 1]:
            self.x = self.call[0] + (min(set.screen_size[0] - self.call[0], self.call[1]) + 110)
            self.y = self.call[1] - (min(set.screen_size[0] - self.call[0], self.call[1]) + 110)
            self.degree = 135
        elif self.direction == [1, -1]:
            self.x = self.call[0] - (min(self.call[0], set.screen_size[1] - self.call[1]) + 110)
            self.y = self.call[1] + (min(self.call[0], set.screen_size[1] - self.call[1]) + 110)
            self.degree = -45
        elif self.direction == [-1, -1]:
            self.x = self.call[0] + (min(set.screen_size[0] - self.call[0], set.screen_size[1] - self.call[1]) + 110)
            self.y = self.call[1] + (min(set.screen_size[0] - self.call[0], set.screen_size[1] - self.call[1]) + 110)
            self.degree = 45


    def direction_to_degree(self, direction):
        if direction == [1, 1]:
            return -135
        elif direction == [-1, 1]:
            return 135
        elif direction == [-1, -1]:
            return 45
        elif direction == [1, -1]:
            return -45


    def check_reaching(self):
        if self.direction == [-1, -1]:
            if self.x <= self.call[0] and self.y <= self.call[1]:
                return True
        else:
            if self.x * self.direction[0] - self.call[0] >= 0 or self.y * self.direction[1] - self.call[1] >= 0:
                return True



    def update(self):
        if not self.stage == 1:
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed

            """if City.time_city % 40 == 0:
             print(self.x, self.y)"""

        # Достиг цели
        if self.stage == 0 and self.check_reaching():
            self.stage = 1
            self.stop_time = City.time_city


        if self.stage == 1:
            # Начинает улетать
            if City.time_city - self.stop_time >= set.heli_wait_time:
                self.stage = 2
                self.stop_time = None

                self.car.followed = self
                self.car.is_collisioned = False
                
        if self.stage == 2:
            # Удаляем вертолет
            if self.x > set.screen_size[0] + 100 or self.x < -100 or self.y < -100 or self.y > set.screen_size[1] + 100:
                City.cars.remove(self.car)
                City.helicopters.remove(self)
                if self.car.isTaxi:
                    City.taxi.remove(self.car)



    def get_car(self):
        self.car.followed = self
        self.car.is_collisioned = False




    def draw(self):
        if City.time_city % 6 <= 1:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel1'], self.degree), self.x - self.length*3/4,
                                self.y - self.width*3/4)
        elif City.time_city % 6 <= 3:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel2'], self.degree), self.x - self.length*3/4,
                                self.y - self.width*3/4)
        elif City.time_city % 6 <= 5:
            graphics.draw_image(graphics.rotatet_image(storage.im_dict['hel3'], self.degree), self.x - self.length*3/4,
                                self.y - self.width*3/4)

