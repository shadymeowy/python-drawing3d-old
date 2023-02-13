import numpy as np
from scipy.spatial.transform import Rotation as R

from camera_base import CameraBase


class PerspectiveCamera(CameraBase):
    def __init__(self, image_size, fov=90):
        self._image_size = image_size
        self.pos = np.array([0., 0., -1.])
        self._att = np.array([0., 0., 0.])
        self.fov = fov

    @property
    def image_size(self):
        return self._image_size

    @image_size.setter
    def image_size(self, image_size):
        self._image_size = image_size
        self._hfov_c = np.tan(np.deg2rad(self._fov / 2.)) * self._image_size[1] / self._image_size[0]
        self._vfov_c = np.tan(np.deg2rad(self._fov / 2.))

    @property
    def fov(self):
        return self._fov

    @fov.setter
    def fov(self, fov):
        self._fov = fov
        self._hfov_c = np.tan(np.deg2rad(self._fov / 2.)) * self._image_size[1] / self._image_size[0]
        self._vfov_c = np.tan(np.deg2rad(self._fov / 2.))

    @property
    def att(self):
        return self._att

    @att.setter
    def att(self, att):
        self._att = att
        self._att_r = R.from_euler('xyz', att, degrees=True)
        self._att_r_inv = self._att_r.inv()

    def project(self, p, visible_only=True):
        p = np.array(p, dtype=np.float64)
        p = p - self.pos
        p = self._att_r.apply(p)
        w = self._image_size[0]
        h = self._image_size[1]
        if p[2] < 0:
            return None
        x = (p[0] / p[2] * self._hfov_c + 0.5) * w
        y = (p[1] / p[2] * self._vfov_c + 0.5) * h
        if visible_only and (x < -w or x > 2 * w or y < -h or y > 2 * h):
            return None
        return np.array((x, y))

    def estimate_size(self, p, size):
        p = np.array(p, dtype=np.float64)
        p = p - self.pos
        p = self._att_r.apply(p)
        if p[2] < 0:
            return None
        x = (p[0] / p[2] * self._hfov_c + 0.5) * self._image_size[0]
        p_ = p + np.array([size, 0, 0])
        x_ = (p_[0] / p_[2] * self._hfov_c + 0.5) * self._image_size[0]
        return np.abs(x - x_)

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
        v = self._att_r_inv.apply(v)
        self.pos += v
        return self.pos

    def rotate(self, *a):
        a = np.array(a, dtype=np.float64)
        a = R.from_euler('xyz', a, degrees=True)
        self._att_r = a * self._att_r
        self._att = self._att_r.as_euler('xyz', degrees=True)
        self._att_r_inv = self._att_r.inv()
        return self._att
