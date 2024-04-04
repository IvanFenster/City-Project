from city import City
import random
from ui import graphics
from storage import storage


class Vehicle:
    def __init__(self):
        #self.vertex = random.choice([0, 2, 67, 69])
        self.vertex = 0
        self.goal, self.path = City.new_path(self.vertex)
        self.path_index = 0
        self.x = 3
        self.y = -100 + 10
        self.navigator = []
        self.isturned = False
        self.degree = -90
        self.speed = 2
        self.move = self.use_degree(self.degree)

        self.step()


    def step(self):
        destin = self.path[self.path_index + 1]
        row = City.define_row(self.vertex)
        diff = destin - self.vertex
        if row % 2 == 0:
            if abs(diff) == 2:
                self.navigator = [[0, 50*4]]
            elif abs(diff) == 10:
                self.navigator = [[0, 93], [-90, 86]]
            elif abs(diff) == 7:
                self.navigator = [[0, 114], [-90, 114]]
        if row % 2 == 1:
            if abs(diff) == 18:
                self.navigator = [[0, 50*4]]
            elif abs(diff) == 9:
                self.navigator = [[0, 93], [-90, 86]]
            elif abs(diff) == 10:
                self.navigator = [[0, 114], [-90, 114]]


    def use_degree(self, degree):
        t = degree % 360

        if t == 0:
            self.move = [1, 0]
        if t == 90:
            self.move = [0, -1]
        if t == 180:
            self.move = [-1, 0]
        if t == 270:
            self.move = [0, 1]


    def update(self):
        if self.navigator[0][1] == 0:
            self.navigator.pop(0)
            self.isturned = False
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





