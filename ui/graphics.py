import pygame

import settings
from ui import screen

Image = pygame.Surface
flip = pygame.display.flip


def fill(color):
    screen.fill(color)


# принимает размеры картинки в координатах лабиринта
def load_image(path, size=(1, 1)):
    img = pygame.image.load(path)
    #return pygame.transform.scale(img, (size[0] * settings.tile_size[0], size[1] * settings.tile_size[1]))
    return img

# клиенты будут передавать координаты лабиринта
def draw_image(image, x, y):
    """Здесь нужен pygame blit с пересчетом на settings.tile_size"""
    screen.blit(image, (x, y))
    pass


# клиенты будут передавать координаты лабиринта
def draw_circle(color, x, y, r):
    """Здесь нужен pygame draw.circle с пересчетом на settings.tile_size"""
    pygame.draw.circle(screen, color, (x*settings.tile_size[0] + settings.view_left_top[0], y*settings.tile_size[1] + settings.view_left_top[1]), r*settings.tile_size[0])

    pass

def rotatet_image(image, degree):
    return pygame.transform.rotate(image, degree)