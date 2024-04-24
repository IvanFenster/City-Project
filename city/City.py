import settings
from storage import storage
from storage import Storage
from ui import graphics
from city.tiles import Road
from city.tiles import Block
import random
from city.vehicle import Vehicle
from city.vehicle import Taxi
from city.helicopter import Helicopter

# Создание лабиринта
road_list = []
for i in range(settings.tiles_num[0]):
    n_list = []
    for j in range(settings.tiles_num[1]):
        type_in = 'block'

        if j % 4 == 0 and i == 0:
            type_in = 'edge_left'
        elif j % 4 == 0 and i == settings.tiles_num[0]-1:
            type_in = 'edge_right'
        elif j == 0 and i % 4 == 0:
            type_in = 'edge_top'
        elif j == settings.tiles_num[1]-1 and i % 4 == 0:
            type_in = 'edge_down'
        elif j == 0:
            type_in = 'road_horiz'

        elif i % 4 == 0 and j % 4 == 0:
            type_in = 'intersection'
        elif i % 4 == 0:
            type_in = 'road_vert'
        elif j % 4 == 0:
            type_in = 'road_horiz'
        if type_in != "block":
            n_list.append(Road(i, j, type_in))
    road_list.append(n_list)


block_list = []
for i in range(settings.tiles_num[0]):
    n_list = []
    for j in range(settings.tiles_num[1]):
        rand_num = random.randint(0, settings.last_block_option)
        type_in = 'block' + str(rand_num)
        n_list.append(Block(i, j, type_in))
    block_list.append(n_list)


def define_row(vert):
    k = vert % 18
    t = vert // 18
    if k <= 9:
        return 2 * t
    else:
        return 2 * t + 1

def define_col(vert):
    k = vert % 18
    if k <= 9:
        t = k // 2
        return t * 2
    else:
        return ((k // 2) - 5) * 2 + 1


# Создание графа
graph = [[] for _ in range(82)]
usable_vert = [i for i in range(10, 72)]
usable_vert += [1, 9, 72, 80]
goal_for_taxi = usable_vert.copy()
for i in [1, 9, 72, 80, 63, 45, 27, 17, 15, 13, 11, 18, 36, 54, 64, 66, 68, 70]:
    goal_for_taxi.remove(i)


for i in range(len(goal_for_taxi)):
    vert = goal_for_taxi[i]
    col = define_col(vert)
    row = define_row(vert)
    if row % 2 == 1:
        if vert % 2 == 0:
            y = 100 * (col - 1) + 50


row = -1
col = 0
for i in range(10, 72):
    row = define_row(i)
    col = define_col(i)

    if col % 2 == 1:
        if row != 7:
            if i % 2 == 0:
                graph[i].append(i + 10)
            else:
                graph[i].append(i + 7)
        if row != 1:
            if i % 2 == 0:
                graph[i].append(i - 7)
            else:
                graph[i].append(i - 10)
        if col != 1 and i % 2 == 1:
            graph[i].append(i - 2)
        if col != 7 and i % 2 == 0:
            graph[i].append(i + 2)

    elif col % 2 == 0:
        if row != 6 and i % 2 == 0:
            graph[i].append(i + 18)
        if row != 2 and i % 2 == 1:
            graph[i].append(i - 18)
        if col != 0:
            if i % 2 == 0:
                graph[i].append(i + 9)
            else:
                graph[i].append(i - 10)
        if col != 8:
            if i % 2 == 1:
                graph[i].append(i - 9)
            else:
                graph[i].append(i + 10)

graph[0] = [10, 18]
graph[8] = [17, 26]
graph[73] = [55, 64]
graph[81] = [63, 71]

graph[11].append(1)
graph[19].append(1)
graph[16].append(9)
graph[27].append(9)
graph[62].append(80)
graph[70].append(80)
graph[65].append(72)
graph[54].append(72)


"""
for i in range(len(graph)):
    print(i, ":", graph[i])
"""


def new_path(now, isTaxi=False):
    queue = []
    color = [0 for _ in range(82)]
    dist = [0 for _ in range(82)]
    prev = [-2 for _ in range(82)]
    cur_vert = now
    if isTaxi:
        goal = random.choice(goal_for_taxi)
    else:
        goal = random.choice(usable_vert)
    if goal == now:
        return new_path(now, isTaxi=isTaxi)
    queue.append(cur_vert)
    color[cur_vert] = 1

    while len(queue) > 0:
        v = queue[0]
        queue.pop(0)
        for u in graph[v]:
            if color[u] == 0:
                color[u] = 1
                dist[u] = dist[v] + 1
                prev[u] = v
                queue.append(u)

    dist_to_goal = dist[goal]
    pr = prev[goal]
    path = []
    while pr != now:
        path.append(pr)
        pr = prev[pr]
    path.reverse()
    path.append(goal)

    return goal, path

cars = []
taxi = []
helicopters = []

start_vert = [0, 8, 73, 81]
end_vert = [1, 9, 72, 80]

cur_car_num = 0
time_city = 0

cur_taxi_num = 0


#cars.append(Taxi(0))



def spawn_cars():
    global cur_car_num, cur_taxi_num

    gates_spawn = [0, 0, 0, 0]

    if cur_car_num < settings.car_num:
        dif = settings.car_num - cur_car_num
        spanw_now = min(dif, 4)
        cur_car_num += spanw_now
        opt = [0, 1, 2, 3]
        for i in range(spanw_now):
            gate = random.choice(opt)
            opt.remove(gate)
            gates_spawn[gate] = 1

        for i in range(4):
            if gates_spawn[i] == 1:
                if (random.randint(0, 1) == 1 or spanw_now != 4)and cur_taxi_num < settings.taxi_num :
                    s = Taxi(start_vert[i])
                    cars.append(s)
                    cur_taxi_num += 1
                    taxi.append(s)
                else:
                    cars.append(Vehicle(start_vert[i], random.randint(1, settings.last_car_option)))


def recursive_check(car, who):
    if car.collision == who:
        return True
    if car.collision != None:
        if car.collision.collision == who:
            return True
        if car.collision.collision != None:
            if car.collision.collision.collision == who:
                return True
    return False


def check_collision(x, y, who):
    for car in cars:
        if car.is_occupied(x, y) != 0:
            if recursive_check(car, who):
                # Затор
                if (car.prev_x == car.x and car.prev_y == car.y) and (who.prev_x == who.x and who.prev_y == who.y):
                    if car.heli_called == False and car.accid_avail and who.accid_avail:
                        car.heli_called = True
                        who.heli_called = True
                        helicopters.append(Helicopter(car))
                        print('Accident!')
                        print("x: ", car.x, "y:", car.y)


                    if car.accid_avail:
                        return car
                    else:
                        return False
            return car
    return False


def call_helicopter():
    pass

def update(delta_time):
    global time_city, cur_car_num, cur_taxi_num

    time_city += 1
    cur_car_num = len(cars)
    cur_taxi_num = len(taxi)

    if time_city % 200 == 1:
        spawn_cars()


    for i in cars:
        i.update()

    for i in helicopters:
        i.update()


def draw():
    global time_city

    for i in road_list:
        for j in i:
            j.draw()
    for i in block_list:
        for j in i:
            j.draw()

    for i in cars:
        if type(i) != "<class 'city.vehicle.Taxi'>":
            i.draw()

    for i in taxi:
        i.draw()

    for i in helicopters:
        i.draw()

    """for i in taxi:
        if i.start_waiting == None:
            graphics.draw_image(i.image_taxi_call, i.call_x, i.call_y)
        else:
            if time_city % 15 < 8:
                graphics.draw_image(i.image_taxi_call, i.call_x, i.call_y)"""

    #graphics.draw_image(storage.im_dict['taxi_call'], 228, 105)


    if settings.debug:
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 90), 24, 510)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 0), 24, 424)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], -90), 203, 110)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 180), 203, 203)