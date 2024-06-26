from storage import storage
import settings
from ui import graphics

# Классы отвечающие за дороги и кварталы

class Tiles:
    def __init__(self, xn, yn, type):
        self.xn = xn
        self.yn = yn
        self.x = xn * settings.tile_size[0] + settings.view_left_top[0]
        self.y = yn * settings.tile_size[1] + settings.view_left_top[1]
        self.type = type
        self.image = storage.get_image(type)

    def draw(self):
        graphics.draw_image(self.image, self.x, self.y)


class Road(Tiles):
   def __init__(self, xn, yn, type):
       super().__init__(xn, yn, type)
       self.x = xn * settings.tile_size[0] + settings.view_left_top[0]
       self.y = yn * settings.tile_size[1] + settings.view_left_top[1]


class Block(Tiles):
    def __init__(self, xn, yn, type):
        super().__init__(xn, yn, type)
        self.x = xn * settings.tile_size[0]*4 + settings.tile_size[0] + settings.view_left_top[0]
        self.y = yn * settings.tile_size[1]*4 + settings.tile_size[1] + settings.view_left_top[1]
