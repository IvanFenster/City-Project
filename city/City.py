import settings
from storage import storage
from storage import Storage
from ui import graphics
from city.road import Road

road_list = []
for i in range(settings.tiles_num[0]):
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
            road_list.append(Road(i, j, type_in))




def update(delta_time):
    pass

def draw():
    for i in road_list:
        i.draw()
    #graphics.draw_image(storage.get_image('block1'), 10+50, 10+50)