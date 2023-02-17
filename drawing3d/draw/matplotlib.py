import matplotlib.pyplot as plt

from ..draw.draw import Draw


class DrawMatplotlib(Draw):
    def __init__(self):
        super().__init__()
        plt.ion()

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')

        self.xlim = [0, 0]
        self.ylim = [0, 0]
        self.zlim = [0, 0]

    def begin(self):
        self.ax.cla()

    def end(self, dt=0):
        self.ax.set_aspect('equal')
        x_min, x_max = self.ax.get_xlim()
        y_min, y_max = self.ax.get_ylim()
        z_min, z_max = self.ax.get_zlim()
        if x_min < self.xlim[0]:
            self.xlim[0] = x_min
        if x_max > self.xlim[1]:
            self.xlim[1] = x_max
        if y_min < self.ylim[0]:
            self.ylim[0] = y_min
        if y_max > self.ylim[1]:
            self.ylim[1] = y_max
        if z_min < self.zlim[0]:
            self.zlim[0] = z_min
        if z_max > self.zlim[1]:
            self.zlim[1] = z_max
        self.ax.set_xlim(self.xlim)
        self.ax.set_ylim(self.ylim)
        self.ax.set_zlim(self.zlim)

        plt.draw()
        plt.gcf().canvas.draw_idle()
        plt.gcf().canvas.start_event_loop(dt)

    def style(self, color, alpha, size):
        if isinstance(color, tuple):
            color = '#%02x%02x%02x' % color
        self.color = color
        self.alpha = alpha
        self.size = size

    def point(self, p):
        self.ax.scatter([p[0]], [p[1]], [p[2]], color=self.color, alpha=self.alpha, s=self.size)

    def lines(self, points):
        x = [p[0] for p in points]
        y = [p[1] for p in points]
        z = [p[2] for p in points]
        self.ax.plot(x, y, z, color=self.color, alpha=self.alpha, linewidth=self.size)

    def lines_xyz(self, x, y, z):
        self.ax.plot(x, y, z, color=self.color, alpha=self.alpha, linewidth=self.size)

    def tri(self, p1, p2, p3):
        x = [p1[0], p2[0], p3[0]]
        y = [p1[1], p2[1], p3[1]]
        z = [p1[2], p2[2], p3[2]]
        self.ax.plot_trisurf(x, y, z, color=self.color, alpha=self.alpha)

    def text(self, p, text):
        self.ax.text(p[0], p[1], p[2], text, color=self.color, alpha=self.alpha, size=self.size)

    def image4(self, image, ps):
        raise NotImplementedError