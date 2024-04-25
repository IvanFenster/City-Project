import settings
from ui import graphics


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance



# Класс, который загружает изображения
# Этот класс — singletone, так как должен существовать в одном экземпляре.
@singleton
class Storage:
    def __init__(self):
        self.im_dict = {}
        self.im_dict["road_vert"] = graphics.load_image('images/road_vert.png')
        self.im_dict["road_horiz"] = graphics.load_image('images/road_horiz.png')
        self.im_dict["intersection"] = graphics.load_image('images/intersection.png')
        self.im_dict["edge_top"] = graphics.load_image('images/edge_top.png')
        self.im_dict["edge_down"] = graphics.load_image('images/edge_down.png')
        self.im_dict["edge_right"] = graphics.load_image('images/edge_right.png')
        self.im_dict["edge_left"] = graphics.load_image('images/edge_left.png')

        for i in range(settings.last_block_option + 1):
            self.im_dict[f'block{i}'] = graphics.load_image(f'images/block{i}.png')

        self.im_dict['taxi_call'] = graphics.load_image('images/taxi_call.png')
        self.im_dict['hel1'] = graphics.load_image('images/hel1.png')
        self.im_dict['hel2'] = graphics.load_image('images/hel2.png')
        self.im_dict['hel3'] = graphics.load_image('images/hel3.png')
        for i in range(settings.last_car_option + 1):
            self.im_dict[f'car{i}'] = graphics.load_image(f'images/car{i}.png')

    # Функция для доступа к изображениям
    def get_image(self, type):
        return self.im_dict[type]


storage = Storage()
