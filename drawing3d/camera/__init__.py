from .base import CameraBase
from .orthographic import OrthographicCamera
from .perspective import PerspectiveCamera
from .simple import SimpleCamera


def camera(type='perspective', *args, **kwargs):
    if type == 'perspective':
        return PerspectiveCamera(*args, **kwargs)
    elif type == 'orthographic':
        return OrthographicCamera(*args, **kwargs)
    elif type == 'simple':
        return SimpleCamera(*args, **kwargs)
    else:
        raise ValueError('Unknown camera type: %s' % type)
