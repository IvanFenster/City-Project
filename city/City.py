import settings
from storage import storage
from storage import Storage
from ui import graphics
from city.tiles import Road
from city.tiles import Block
import random
from city.vehicle import Vehicle

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
        rand_num = random.randint(0, 3)
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
useful_vert = [i for i in range(10, 72)]
useful_vert += [1, 9, 72, 80]

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



for i in range(len(graph)):
    print(i, ":", graph[i])



def new_path(now):
    queue = []
    color = [0 for _ in range(82)]
    dist = [0 for _ in range(82)]
    prev = [-2 for _ in range(82)]
    cur_vert = now
    goal = random.choice(useful_vert)
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
cars.append(Vehicle(0))
cars.append(Vehicle(8))
cars.append(Vehicle(73))
cars.append(Vehicle(81))


def update(delta_time):
    if settings.debug == False:
        for i in cars:
            i.update()


def draw():
    for i in road_list:
        for j in i:
            j.draw()
    for i in block_list:
        for j in i:
            j.draw()

    for i in cars:
        i.draw()

    if settings.debug:
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 90), 24, 510)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 0), 24, 424)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], -90), 203, 110)
        graphics.draw_image(graphics.rotatet_image(storage.im_dict['car'], 180), 203, 203)