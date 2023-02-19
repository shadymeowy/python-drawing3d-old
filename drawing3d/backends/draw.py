from scipy.spatial.transform import Rotation as R

from .base import DrawBase
from ..misc import *


class Draw(DrawBase):
    def lines_xyz(self, x, y, z):
        points = np.column_stack((x, y, z))
        self.lines(points)

    def line(self, p1, p2):
        self.lines([p1, p2])

    def quad(self, p1, p2, p3, p4):
        self.tri(p1, p2, p3)
        self.tri(p1, p3, p4)

    def arrow(self, p, v, length=1, ratio=0.1, n=NORMAL_XY):
        v1, v2 = orthogonal_vectors(n)
        start = p
        end = p + v * length
        end2 = end - v * length * 0.2
        self.line(start, end)
        self.line(end, end2 + np.cross(v, n) * ratio)
        self.line(end, end2 - np.cross(v, n) * ratio)

    def arrow3(self, p, v, length=1, ratio=0.1):  # TODO: better arrow
        start = p
        end = p + v * length
        end2 = end - v * length * ratio
        v1, v2 = orthogonal_vectors(v)
        self.line(start, end)
        self.line(end, end2 + v1 * ratio)
        self.line(end, end2 - v1 * ratio)
        self.line(end, end2 + v2 * ratio)
        self.line(end, end2 - v2 * ratio)

    def circle(self, p, r, n=NORMAL_XY, res=100):
        v1, v2 = orthogonal_vectors(n)
        self.ellipse(p, v1 * r, v2 * r, res)

    def ellipse(self, p, v1, v2, res=100):
        angles = np.linspace(0, 2 * np.pi, res)
        p_ = p + v1 * np.cos(angles)[:, None] + v2 * np.sin(angles)[:, None]
        self.lines(p_)

    def attitude(self, p, r, color=('red', 'green', 'blue')):
        if not isinstance(r, R):
            r = R.from_euler('xyz', r, degrees=True)
        self.style(color=color[0])
        self.arrow3(p, r.apply((1, 0, 0)))
        self.style(color=color[1])
        self.arrow3(p, r.apply((0, 1, 0)))
        self.style(color=color[2])
        self.arrow3(p, r.apply((0, 0, 1)))

    def cube(self, p, n=NORMAL_XY):
        n = np.array(n, dtype=np.float64)
        n /= np.linalg.norm(n)
        v1, v2 = orthogonal_vectors(n)
        p = [
            p + v1 * 0.5 + v2 * 0.5 + n * 0.5,
            p + v1 * 0.5 - v2 * 0.5 + n * 0.5,
            p - v1 * 0.5 - v2 * 0.5 + n * 0.5,
            p - v1 * 0.5 + v2 * 0.5 + n * 0.5,
            p + v1 * 0.5 + v2 * 0.5 - n * 0.5,
            p + v1 * 0.5 - v2 * 0.5 - n * 0.5,
            p - v1 * 0.5 - v2 * 0.5 - n * 0.5,
            p - v1 * 0.5 + v2 * 0.5 - n * 0.5,
        ]
        l = [
            (p[0], p[1], p[2], p[3], p[0]),
            (p[4], p[5], p[6], p[7], p[4]),
            (p[0], p[4]),
            (p[1], p[5]),
            (p[2], p[6]),
            (p[3], p[7]),
        ]
        for line in l:
            self.lines(line)

    def rect(self, p, size, v_x=E_X, v_y=E_Y):
        v_x = np.array(v_x) * size[0] / 2
        v_y = np.array(v_y) * size[1] / 2
        p = np.array(p)
        ps = [
            p + v_x + v_y,
            p + v_x - v_y,
            p - v_x - v_y,
            p - v_x + v_y
        ]
        self.quad(*ps)

    def rect_multi(self, p, size, v_x=E_X, v_y=E_Y, count=10):
        count //= 2
        v_x = np.array(v_x)
        v_y = np.array(v_y)
        v_x /= np.linalg.norm(v_x)
        v_y /= np.linalg.norm(v_y)
        v_x = v_x * size[0] / count / 2
        v_y = v_y * size[1] / count / 2
        p = np.array(p)
        for i in range(-count, count):
            for j in range(-count, count):
                ps = [
                    p + v_x * i + v_y * j,
                    p + v_x * (i + 1) + v_y * j,
                    p + v_x * (i + 1) + v_y * (j + 1),
                    p + v_x * i + v_y * (j + 1)
                ]
                self.quad(*ps)

    def line_multi(self, p1, p2, count=10):
        d = (p2 - p1) / count
        for i in range(count):
            self.line(p1 + d * i, p1 + d * (i + 1))

    def image(self, image, p, size, v_x=E_X, v_y=E_Y):
        v_x = np.array(v_x) * size[0]
        v_y = np.array(v_y) * size[1]
        p = np.array(p)
        ps = [p, p + v_x, p + v_x + v_y, p + v_y]
        self.image4(image, ps)
