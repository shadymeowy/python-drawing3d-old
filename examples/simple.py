from drawing3d import draw3d

draw = draw3d(renderer='qt')

while True:
    draw.begin()

    draw.style('blue', alpha=0.5)
    draw.quad((0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0))

    draw.style('red')
    draw.line((0, 0, 0), (1, 1, 0))
    draw.circle((0, 0, 0), 1)

    draw.style('green', size=2)
    draw.cube((0, 0, 0), (0, 0, 1))

    draw.end(1 / 60)
