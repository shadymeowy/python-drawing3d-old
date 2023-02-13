from .draw.draw import Draw


def draw3d(*args, renderer='pyside6', **kwargs):
    renderer = renderer.lower()
    if renderer == 'pyside6':
        from .draw.pyside6 import DrawPySide6
        return DrawPySide6()
    elif renderer == 'matplotlib':
        from .draw.matplotlib import DrawMatplotlib
        return DrawMatplotlib()
    else:
        raise ValueError('Unknown renderer: %s' % renderer)
