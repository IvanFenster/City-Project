import settings
from city import City
import random
from ui import graphics
from storage import storage
import time


class Vehicle:
    def __init__(self, start, color):

        self.vertex = start
        self.start = start
        self.color = color

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

        self.length = settings.car_length
        self.width = settings.car_width

        self.rect_start = [self.x, self.y]
        self.rect_end = [self.x + self.length, self.y + self.width]

        self.goal, self.path = City.new_path(self.vertex)
        self.path_index = 0
        self.image = storage.get_image('car'+str(self.color))

        self.navigator = []
        self.isturned = False
        self.where_go = ''

        self.speed = settings.speed
        self.move = self.use_degree(self.degree)

        self.step()

    def check_coordinates(self, x, y):
        if (x >= self.rect_start[0] - settings.car_rect_add and y >= self.rect_start[1] - settings.car_rect_add and
                self.rect_end[0] + settings.car_rect_add >= x and self.rect_end[1] + settings.car_rect_add >= y):
            return True
        else:
            return False


    def find_center(self, x, y):
        if self.degree % 180 == 90:
            center = [x + self.length / 2, y + self.width / 2]
        else:
            center = [x + self.width / 2, y + self.length / 2]
        return center


    def step(self):

        if len(self.path) == 0:  # Если последняя точка маршрута
            if self.goal in City.end_vert:  # Если машина уехала из города
                City.cars.remove(self)
                City.cur_car_num -= 1
                return
            self.goal, self.path = City.new_path(self.vertex)

        self.destin = self.path[0]
        row = City.define_row(self.vertex)
        diff = self.destin - self.vertex
        if row % 2 == 1:
            if abs(diff) == 2:
                self.navigator = [[0, 90], [0, 110]]
                self.where_go = 'straight'
            elif abs(diff) == 10:
                self.navigator = [[0, 93-settings.turn_length], [-45, settings.turn_length], [-45, 86-settings.turn_length]]
                self.where_go = 'right'
            elif abs(diff) == 7:
                self.navigator = [[0, 114-settings.turn_length], [45, settings.turn_length], [45, 107-settings.turn_length]]
                self.where_go = 'left'
        if row % 2 == 0:
            if abs(diff) == 18:
                self.navigator = [[0, 90], [0, 110]]
                self.where_go = 'straight'
            elif abs(diff) == 9:
                self.navigator = [[0, 93-settings.turn_length], [-45, settings.turn_length], [-45, 86-settings.turn_length]]
                self.where_go = 'right'
            elif abs(diff) == 10:
                self.navigator = [[0, 114-settings.turn_length], [45, settings.turn_length], [45, 107-settings.turn_length]]
                self.where_go = 'left'

    def use_degree(self, degree):
        t = degree % 360

        if t == 0:
            return [1, 0]
        elif t == 90:
            return [0, -1]
        elif t == 180:
            return [-1, 0]
        elif t == 270:
            return [0, 1]
        elif t == 45:
            return [1, -1]
        elif t == 135:
            return [-1, -1]
        elif t == 225:
            return [-1, 1]
        elif t == 315:
            return [1, 1]


    def collision_check(self, check_turn=False):
        center = self.find_center(self.x, self.y)
        self.isTurning = False
        if self.degree == 0:
            check_x = self.x + self.length + settings.car_rect_add + settings.car_distance
            check_y = center[1]
        elif self.degree == 90:
            check_x = center[0]
            check_y = self.y - settings.car_rect_add - settings.car_distance
        elif self.degree == 180:
            check_x = self.x - settings.car_rect_add - settings.car_distance
            check_y = center[1]
        elif self.degree == 270:
            check_x = center[0]
            check_y = self.y + self.length + settings.car_rect_add + settings.car_distance
        else:
            self.isTurning = True


        if self.isTurning == False:
            if City.check_collision(check_x, check_y):
                return True
            else:
                return False
        else:
            return True


    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        if len(self.navigator) > 0:
            if self.navigator[0][1] == 0:  # Если доехали до поворота или середины дороги

                self.navigator.pop(0)
                self.isturned = False
                if len(self.navigator) == 0:
                    self.path.pop(0)
                    self.vertex = self.destin
                    self.step()
                    return

            if self.isturned == False:
                self.start_dist = self.navigator[0][1]
                #print('degree:', self.degree, 'x:', self.x, 'y:', self.y, 'dist:', self.start_dist)
                self.degree += self.navigator[0][0]
                self.degree = self.degree % 360
                self.isturned = True
                self.move = self.use_degree(self.degree)

            if self.navigator[0][1] <= 10 and len(self.navigator) > 1 and self.where_go != 'straight':
                self.speed = settings.speed / 2

            elif self.navigator[0][1] > 10:
                self.speed = settings.speed

            if self.navigator[0][1] >= self.speed:
                new_x = self.x + self.move[0] * self.speed
                new_y = self.y + self.move[1] * self.speed
                if self.collision_check():
                    self.x = new_x
                    self.y = new_y
                    self.navigator[0][1] -= self.speed
            elif self.navigator[0][1] >= 0:
                dif = self.navigator[0][1] - self.speed
                new_x = self.x + self.move[0] * dif
                new_y = self.y + self.move[1] * dif
                if self.collision_check(check_turn=True):
                    self.x = new_x
                    self.y = new_y
                    self.navigator[0][1] = 0



        self.rect_start = [self.x, self.y]
        self.rect_end = [self.x + self.length, self.y + self.width]





    def draw(self):
        graphics.draw_image(graphics.rotatet_image(self.image, self.degree), self.x, self.y)


class Taxi(Vehicle):
    def __init__(self, start):
        self.vertex = start
        self.start = start


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

        self.length = settings.car_length
        self.width = settings.car_width

        self.goal, self.path = City.new_path(self.vertex, isTaxi=True)
        self.path_index = 0
        self.image = storage.get_image('taxi')

        self.navigator = []
        self.isturned = False

        self.speed = settings.speed
        self.move = self.use_degree(self.degree)

        self.step()

    def step(self):
        if len(self.path) == 0:
            time.sleep(5)
            self.goal, self.path = City.new_path(self.vertex, isTaxi=True)



        self.destin = self.path[0]
        row = City.define_row(self.vertex)
        diff = self.destin - self.vertex
        if row % 2 == 1:
            if abs(diff) == 2:
                self.navigator = [[0, 50 * 4]]
            elif abs(diff) == 10:
                self.navigator = [[0, 93-settings.turn_length], [-45, settings.turn_length], [-45, 86-settings.turn_length]]
            elif abs(diff) == 7:
                self.navigator = [[0, 114-settings.turn_length], [45, settings.turn_length], [45, 107-settings.turn_length]]
        if row % 2 == 0:
            if abs(diff) == 18:
                self.navigator = [[0, 50 * 4]]
            elif abs(diff) == 9:
                self.navigator = [[0, 93-settings.turn_length], [-45, settings.turn_length], [-45, 86-settings.turn_length]]
            elif abs(diff) == 10:
                self.navigator = [[0, 114-settings.turn_length], [45, settings.turn_length], [45, 107-settings.turn_length]]

