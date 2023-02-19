from .backends.draw import Draw


def draw3d(*args, renderer='qt', **kwargs):
    renderer = renderer.lower()
    if renderer == 'qt':
        from .backends.qt import DrawQt
        return DrawQt(*args, **kwargs)
    elif renderer == 'matplotlib':
        from .backends.matplotlib import DrawMatplotlib
        return DrawMatplotlib(*args, **kwargs)
    else:
        raise ValueError('Unknown renderer: %s' % renderer)
