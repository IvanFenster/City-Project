import settings
from storage import storage
from storage import Storage
from ui import graphics
from city.tiles import Road
from city.tiles import Block
from random import randint

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
        rand_num = randint(0, 3)
        type_in = 'block' + str(rand_num)
        n_list.append(Block(i, j, type_in))
    block_list.append(n_list)



# Создание графа
graph = [[] for _ in range(70)]
row = -1
col = 0
for i in range(4, 66):
    if (row % 2 == 0 and (i-12) % 18 == 0) or (row % 2 == 1 and (i-4) % 18 == 0):
        row += 1
    if row % 2 == 0:
        col = (((i-4) % 18) // 2) * 2 + 1
    elif row % 2 == 1:
        col = (((i-12) % 18) // 2) * 2





def update(delta_time):
    pass

def draw():
    for i in road_list:
        for j in i:
            j.draw()
    for i in block_list:
        for j in i:
            j.draw()