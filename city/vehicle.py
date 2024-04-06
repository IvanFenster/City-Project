import settings
from city import City
import random
from ui import graphics
from storage import storage


class Vehicle:
    def __init__(self, start):

        self.vertex = start
        self.start = start
        #self.vertex = random.choice([0, 8, 73, 81])
        if self.vertex == 0:
            self.x = 3
            self.y = -100 + 10
            self.degree = -90
        elif self.vertex == 8:
            self.x = 803
            self.y = -100 + 10
            self.degree = -90
        elif self.vertex == 73:
            self.x = 24
            self.y = 717
            self.degree = 90
        elif self.vertex == 81:
            self.x = 824
            self.y = 717
            self.degree = 90
        self.goal, self.path = City.new_path(self.vertex)
        #self.goal, self.path = 70, [64, 66, 68, 70]
        self.path_index = 0

        self.navigator = []
        self.isturned = False

        self.speed = settings.speed
        self.move = self.use_degree(self.degree)

        self.step()


    def step(self):
        if len(self.path) == 0:
            if self.goal in City.end_vert:
                City.cars.remove(self)
                City.cur_car_num -= 1
                return
            self.goal, self.path = City.new_path(self.vertex)

        #print(self.start, 'x:', self.x, 'y:', self.y)
        self.destin = self.path[0]
        row = City.define_row(self.vertex)
        diff = self.destin - self.vertex
        if row % 2 == 1:
            if abs(diff) == 2:
                self.navigator = [[0, 50 * 4]]
            elif abs(diff) == 10:
                self.navigator = [[0, 93], [-90, 86]]
            elif abs(diff) == 7:
                self.navigator = [[0, 114], [90, 107]]
        if row % 2 == 0:
            if abs(diff) == 18:
                self.navigator = [[0, 50 * 4]]
            elif abs(diff) == 9:
                self.navigator = [[0, 93], [-90, 86]]
            elif abs(diff) == 10:
                self.navigator = [[0, 114], [90, 107]]

    def use_degree(self, degree):
        t = degree % 360

        if t == 0:
            return [1, 0]
        if t == 90:
            return [0, -1]
        if t == 180:
            return [-1, 0]
        if t == 270:
            return [0, 1]


    def update(self):
        if len(self.navigator) > 0:
            if self.navigator[0][1] == 0:
                self.navigator.pop(0)
                self.isturned = False
                if len(self.navigator) == 0:
                    self.path.pop(0)
                    self.vertex = self.destin
                    self.step()

                    return
            if self.isturned == False:
                self.degree += self.navigator[0][0]
                self.isturned = True
                self.move = self.use_degree(self.degree)
            if self.navigator[0][1] >= self.speed:
                self.navigator[0][1] -= self.speed
                self.x += self.move[0] * self.speed
                self.y += self.move[1] * self.speed
            elif self.navigator[0][1] >= 0:
                dif = self.navigator[0][1] - self.speed
                self.navigator[0][1] = 0
                self.x += self.move[0] * dif
                self.y += self.move[1] * dif


    def draw(self):
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], self.degree), self.x, self.y)





