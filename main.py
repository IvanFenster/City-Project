import settings
from city import City
from ui import events
from ui import graphics

FPS = 60
running = True
clock = events.Clock()

# Приветствие. Его нужно удалить
# greetings()

while running:
    for event in events.get_event_queue():
        if event.type == events.QUIT:
            running = False
        if event.type == events.MOUSEBUTTONDOWN:
            pass

    graphics.fill("white")
    # рисуем лабиринт
    City.draw()

    graphics.flip()
    clock.tick(FPS)
    # обновляем весь лабиринт
    City.update(1 / FPS)
