import numpy as np

from .base import CameraBase


class SimpleCamera(CameraBase):
    def __init__(self, image_size, real_size=(1, 1)):
        self._image_size = image_size
        self.pos = np.array([0., 0., -1.])
        self.att = np.array([0., 0., 0.])
        self.real_size = real_size
        self._att = np.array([0., 0., 0.])

    @property
    def image_size(self):
        return self._image_size

    @image_size.setter
    def image_size(self, image_size):
        self._image_size = image_size

    @property
    def att(self):
        return self._att

    @att.setter
    def att(self, att):
        self._att = att

    def project(self, p, visible_only=True):
        p = np.array(p, dtype=np.float64)
        p = p - self.pos
        w = self._image_size[0]
        h = self._image_size[1]
        x = (p[0] / self.real_size[0] + 0.5) * w
        y = (p[1] / self.real_size[1] + 0.5) * h
        if visible_only and (x < -w or x > 2 * w or y < -h or y > 2 * h):
            return None
        return np.array((x, y))

    def estimate_size(self, p, size):
        return size / self.real_size[0] * self._image_size[0]

    def projects(self, ps, visible_only=True):
        p_ = []
        for p in ps:
            p = self.project(p, visible_only)
            p_.append(p)
            if p is None:
                return None
        return p_

    def move(self, *v):
        v = np.array(v, dtype=np.float64)
        self.pos += v
        return self.pos

    def rotate(self, *a):
        return self.att
