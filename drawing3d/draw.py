from draw_base import DrawBase
from vector_helper import *


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
        self.style(color=color[0])
        self.arrow3(p, r.apply((1, 0, 0)))
        self.style(color=color[1])
        self.arrow3(p, r.apply((0, 1, 0)))
        self.style(color=color[2])
        self.arrow3(p, r.apply((0, 0, 1)))

    def camera(self, p, r, vfov, hfov):
        vec, vec_v, vec_h = perspective_get_vecs(r, vfov, hfov)
        p1 = p + vec + vec_v + vec_h
        p2 = p + vec + vec_v - vec_h
        p3 = p + vec - vec_v - vec_h
        p4 = p + vec - vec_v + vec_h
        self.line(p, p + vec)
        self.line(p, p1)
        self.line(p, p2)
        self.line(p, p3)
        self.line(p, p4)
        self.quad(p1, p2, p3, p4)
        self.arrow(p + vec, vec_v)
        self.arrow(p + vec, vec_h)
        self.lines((p1, p2, p3, p4, p1))

    def cube(self, p, n=NORMAL_XY):
        n = np.array(n)
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

    def plane(self, p, count=10, size=(10, 10), n=NORMAL_XY):
        v1, v2 = orthogonal_vectors(n)
        dsize = np.array(size) / count
        x_n = np.arange(-size[0] / 2, size[0] / 2, dsize[0])
        y_n = np.arange(-size[1] / 2, size[1] / 2, dsize[1])
        for x in x_n:
            for y in y_n:
                p1 = p + v1 * x + v2 * y
                p2 = p + v1 * (x + dsize[0]) + v2 * y
                p3 = p + v1 * (x + dsize[0]) + v2 * (y + dsize[1])
                p4 = p + v1 * x + v2 * (y + dsize[1])
                self.quad(p1, p2, p3, p4)
