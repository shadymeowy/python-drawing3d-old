from drawing3d import draw3d

draw = draw3d(renderer='qt')

while True:
    draw.begin()
    draw.color = (255, 0, 0)
    draw.style((255, 0, 0), 1.0, 1)
    draw.line((0, 0, 0), (1, 1, 0))
    draw.circle((0, 0, 0), 1)
    draw.style((0, 255, 0), 1.0, 1)
    draw.cube((0, 0, 0), (0, 0, 1))
    draw.end(1 / 60)