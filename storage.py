from ui import graphics
class Storage:
    def __init__(self):
        self.im_dict = {}
        self.im_dict["road_vert"] = self.road_vert = graphics.load_image('images/road_vert.png')
        self.im_dict["road_horiz"] = self.road_horiz = graphics.load_image('images/road_horiz.png')
        self.im_dict["intersection"] = self.intersection = graphics.load_image('images/intersection.png')
        self.im_dict["edge_top"] = self.edge_top = graphics.load_image('images/edge_top.png')
        self.im_dict["edge_down"] = self.edge_down = graphics.load_image('images/edge_down.png')
        self.im_dict["edge_right"] = self.edge_right = graphics.load_image('images/edge_right.png')
        self.im_dict["edge_left"] = self.edge_left = graphics.load_image('images/edge_left.png')

        self.im_dict['block0'] = self.edge_left = graphics.load_image('images/block0.png', (3, 3))
        self.im_dict['block1'] = self.edge_left = graphics.load_image('images/block1.png', (3, 3))
        self.im_dict['block2'] = self.edge_left = graphics.load_image('images/block2.png', (3, 3))
        self.im_dict['block3'] = self.edge_left = graphics.load_image('images/block3.png', (3, 3))

    def get_image(self, type):
        return self.im_dict[type]

storage = Storage()