import city.City
import settings
from city import City
import random
from ui import graphics
from storage import storage
import time
import constants


class Vehicle:
    def __init__(self, start, color):

        self.vertex = start
        self.start = start
        self.color = color
        self.collision = None


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
        self.move = self.degree_to_coordinates(self.degree)

        if self.color != 0:
            self.step()

    def is_occupied(self, x, y):
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

    def degree_to_coordinates(self, degree):
        t = degree % 360
        return constants.degree_to_coor_move[t]


    def collision_check(self, check_turn=False):
        center = self.find_center(self.x, self.y)
        self.isTurning = False
        if self.degree == 0:
            check_x = self.x + self.length + settings.car_rect_add + settings.car_distance
            check_x1 = self.x + self.length + settings.car_rect_add + 1
            check_y = center[1]
            check_y1 = center[1]
        elif self.degree == 90:
            check_x = center[0]
            check_x1 = center[0]
            check_y = self.y - settings.car_rect_add - settings.car_distance
            check_y1 = self.y - settings.car_rect_add - 1
        elif self.degree == 180:
            check_x = self.x - settings.car_rect_add - settings.car_distance
            check_x1 = self.x - settings.car_rect_add - 1
            check_y = center[1]
            check_y1 = center[1]
        elif self.degree == 270:
            check_x = center[0]
            check_x1 = center[0]
            check_y = self.y + self.length + settings.car_rect_add + settings.car_distance
            check_y1 = self.y + self.length + settings.car_rect_add + 1
        else:
            self.isTurning = True


        if self.isTurning == False:
            car = City.check_collision(check_x, check_y, self)
            car1 = City.check_collision(check_x1, check_y1, self)
            if car != False:
                self.collision = car
                return False
            elif car1 != False:
                self.collision = car1
                return False
            else:
                return True
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
                self.move = self.degree_to_coordinates(self.degree)

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


class Taxi(Vehicle):  # В разработке
    def __init__(self, start):
        super().__init__(start, 0)
        self.start_waiting = None
        self.image_taxi_call = storage.get_image('taxi_call')

        self.goal, self.path = City.new_path(self.vertex, isTaxi=True)
        self.call_x, self.call_y = self.vertex_to_taxi_coor(self.goal)



        self.step()


    def vertex_to_taxi_coor(self, vertex):
        row = City.define_row(vertex)
        col = City.define_col(vertex)
        if row % 2 == 1:
            if vertex % 2 == 0:
                y = (row // 2) * 200 + 12
            else:
                y = (row // 2) * 200 - 33
            x = (col // 2) * 200 + 110
        elif row % 2 == 0:
            if vertex % 2 == 0:
                x = (col // 2) * 200 - 18
            else:
                x = (col // 2) * 200 + 28
            y = ((row // 2) - 1) * 200 + 100
        return x, y


    def step(self):
        if len(self.path) == 0:

            if self.start_waiting == None:
                self.start_waiting = City.time_city

            elif City.time_city - self.start_waiting >= settings.taxi_wait_time:
                self.start_waiting == None
                self.goal, self.path = City.new_path(self.vertex, isTaxi=True)
                self.call_x, self.call_y = self.vertex_to_taxi_coor(self.goal)

        if self.start_waiting == None:
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

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y

        if self.start_waiting != None:
            if City.time_city - self.start_waiting >= settings.taxi_wait_time:
                self.start_waiting = None
                self.goal, self.path = City.new_path(self.vertex, isTaxi=True)
                self.call_x, self.call_y = self.vertex_to_taxi_coor(self.goal)
                self.step()

        if len(self.navigator) > 0 and self.start_waiting == None:
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
                # print('degree:', self.degree, 'x:', self.x, 'y:', self.y, 'dist:', self.start_dist)
                self.degree += self.navigator[0][0]
                self.degree = self.degree % 360
                self.isturned = True
                self.move = self.degree_to_coordinates(self.degree)

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
        super().draw()
        if self.start_waiting == None:
            graphics.draw_image(self.image_taxi_call, self.call_x, self.call_y)
        else:
            if City.time_city % 15 < 8:
                graphics.draw_image(self.image_taxi_call, self.call_x, self.call_y)