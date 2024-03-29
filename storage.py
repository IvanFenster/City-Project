from ui import graphics
class Storage:
    def __init__(self):
        self.road_vert = graphics.load_image('images/road_vert.png')
        self.road_horiz = graphics.load_image('images/road_horiz.png')
        self.intersection = graphics.load_image('images/intersection.png')
        self.edge_top = graphics.load_image('images/edge_top.png')
        self.edge_down = graphics.load_image('images/edge_down.png')
        self.edge_right = graphics.load_image('images/edge_right.png')
        self.edge_left = graphics.load_image('images/edge_left.png')


storage = Storage()