from camera_base import CameraBase
from camera_orthographic import OrthographicCamera
from camera_perspective import PerspectiveCamera
from camera_simple import SimpleCamera


def camera(type='perspective', *args, **kwargs):
    if type == 'perspective':
        return PerspectiveCamera(*args, **kwargs)
    elif type == 'orthographic':
        return OrthographicCamera(*args, **kwargs)
    elif type == 'simple':
        return SimpleCamera(*args, **kwargs)
    else:
        raise ValueError('Unknown camera type: %s' % type)
