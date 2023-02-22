import os
import time

import numpy as np
import multiprocessing as mp

from ..backends.draw import Draw
from ..camera import camera
from ..misc import *
from ..proxy import ProxyInterface
from .qt_helper import *


CONTROL_KEYS = {
    Qt.Key.Key_A: ((-0.5, 0, 0), (0, 0, 0)),
    Qt.Key.Key_D: ((0.5, 0, 0), (0, 0, 0)),
    Qt.Key.Key_Space: ((0, -0.5, 0), (0, 0, 0)),
    Qt.Key.Key_C: ((0, 0.5, 0), (0, 0, 0)),
    Qt.Key.Key_W: ((0, 0, 0.5), (0, 0, 0)),
    Qt.Key.Key_S: ((0, 0, -0.5), (0, 0, 0)),
    Qt.Key.Key_Up: ((0, 0, 0), (-1, 0, 0)),
    Qt.Key.Key_Down: ((0, 0, 0), (1, 0, 0)),
    Qt.Key.Key_Right: ((0, 0, 0), (0, -1, 0)),
    Qt.Key.Key_Left: ((0, 0, 0), (0, 1, 0)),
    Qt.Key.Key_Q: ((0, 0, 0), (0, 0, 1)),
    Qt.Key.Key_E: ((0, 0, 0), (0, 0, -1)),
}

if "NO_GL" in os.environ and os.environ["NO_GL"] == "1":
    print("NO_GL is set, using QWidget instead of QOpenGLWidget")
    WidgetClass = QWidget
    USE_GL = False
else:
    WidgetClass = QOpenGLWidget
    USE_GL = True


class QCanvas3D(WidgetClass):
    def __init__(
            self,
            size=(700, 700),
            pos=(0, 0, 0),
            att=(0, 0, 0),
            controls=True,
            cam_type='perspective',
            name='',
            parent=None,
            antialias=True,
            **kwargs):
        super(QCanvas3D, self).__init__(parent)
        self.window_size = size
        self.controls = controls
        self.antialias = antialias
        if USE_GL:
            self.setAutoFillBackground(False)
            if self.antialias:
                fmt = QSurfaceFormat()
                fmt.setSamples(8)
                self.setFormat(fmt)
        self.cam = camera(cam_type, size, **kwargs)
        self.cam.pos = np.array(pos, dtype=np.double)
        self.cam.att = np.array(att, dtype=np.double)
        self.setWindowTitle(name)
        self.resize(self.cam.image_size[0], self.cam.image_size[1])
        self.pressed_keys = set()

    def paintEvent(self, e):
        painter = QPainter()
        painter.begin(self)
        if self.antialias:
            painter.setRenderHints(QPainter.Antialiasing)
            painter.setRenderHints(QPainter.TextAntialiasing)
            painter.setRenderHints(QPainter.SmoothPixmapTransform)
        painter.fillRect(self.rect(), QBrush(QColor(255, 255, 255)))
        self.draw(painter, self.cam)
        painter.end()
        painter = None

    def keyPressEvent(self, e):
        key = e.key()
        if key == Qt.Key.Key_Escape:
            self.close()
        if key in CONTROL_KEYS:
            self.pressed_keys.add(key)

    def keyReleaseEvent(self, e):
        key = e.key()
        if key in CONTROL_KEYS and key in self.pressed_keys:
            self.pressed_keys.remove(key)

    def mousePressEvent(self, e):
        self.last_pos = e.pos()

    def mouseMoveEvent(self, e):
        if self.last_pos is None:
            return
        dx = (e.x() - self.last_pos.x()) / 10
        dy = (e.y() - self.last_pos.y()) / 10
        if self.controls:
            self.cam.rotate(-dy, dx, 0)
        self.last_pos = e.pos()
        self.update()

    def mouseReleaseEvent(self, e):
        self.last_pos = None

    def resizeEvent(self, e):
        self.cam.image_size = (self.width(), self.height())
        self.update()
        super(QCanvas3D, self).resizeEvent(e)

    def update(self):
        for key in self.pressed_keys:
            action = CONTROL_KEYS[key]
            if self.controls:
                self.cam.move(*action[0])
                self.cam.rotate(*action[1])
        super(QCanvas3D, self).update()

    def draw(self, painter, cam):
        pass


class DrawApp(Draw):
    def __init__(self):
        Draw.__init__(self)
        self.size = 1
        self.alpha = 1.0
        self.color = QColor(0, 0, 0)

    def run(self, *args, **kwargs):
        self.cmd = []
        self.app = QApplication([])
        self.image_buffer = {}
        self.timer = QTimer()
        self.timer.timeout.connect(self.tick)
        self.widget = QCanvas3D(*args, **kwargs)
        self.widget.draw = self.draw
        self.widget.show()
        self.timer.start(1000 / 60)
        app_exec(self.app)

    def tick(self):
        self.update()
        self.widget.update()

    def draw(self, painter, cam):
        self.painter = painter
        self.cam = cam
        for cmd in self.cmd:
            getattr(self, cmd[0])(*cmd[1], **cmd[2])

    def style(self, color='black', alpha=1.0, size=1.0):
        self.size = size
        self.color = color
        self.alpha = alpha
        self.update_style()

    def lines(self, points):
        points = self.widget.cam.projects(points)
        if points is None:
            return
        qpoints = [QPointF(p[0], p[1]) for p in points]
        self.painter.drawPolyline(qpoints)

    def point(self, p):
        # s = self.cam.estimate_size(p, self.size / 256)
        s = self.size / 4
        p = self.cam.project(p)
        if p is None:
            return
        path = QPainterPath()
        path.addEllipse(p[0] - s, p[1] - s, s * 2, s * 2)
        self.painter.fillPath(path, self.brush)

    def tri(self, p1, p2, p3):
        p = self.cam.projects([p1, p2, p3])
        if p is None:
            return
        qpoints = [QPointF(p[0], p[1]) for p in p]
        self.painter.setPen(QPen(Qt.NoPen))
        self.painter.drawPolygon(qpoints)
        self.painter.setPen(self.pen)

    def text(self, p, text):
        p = self.cam.project(p)
        if p is None:
            return
        self.painter.drawText(*p, text)

    def image4(self, image, ps):
        if isinstance(image, tuple):
            if image not in self.image_buffer:
                return
            image = self.image_buffer[image]
        image = np.array(image, dtype=np.uint8)
        w, h = image.shape[1], image.shape[0]
        if image.shape[2] == 3:
            image = QImage(image, w, h, QImage.Format_RGB888)
        elif image.shape[2] == 4:
            image = QImage(image, w, h, QImage.Format_RGBA8888)
        else:
            raise ValueError('Invalid image shape')
        ps = self.cam.projects(ps)
        if ps is None:
            return
        qpoints = [QPointF(p[0], p[1]) for p in ps]
        w, h = image.width(), image.height()
        src = QPolygonF([
            QPointF(0, 0),
            QPointF(w, 0),
            QPointF(w, h),
            QPointF(0, h),
        ])
        self.painter.setTransform(QTransform.quadToQuad(src, qpoints))
        self.painter.drawImage(0, 0, image)
        self.painter.resetTransform()

    def set_image(self, image, key):
        self.image_buffer[key] = image

    def drop_image(self, key):
        self.image_buffer.pop(key)

    def begin(self):
        pass

    def end(self):
        pass

    def update_style(self):
        if isinstance(self.color, str):
            self.color = COLOR_NAMES[self.color]
        elif isinstance(self.color, tuple):
            self.color = QColor(*self.color)
        self.color = QColor(self.color.red(), self.color.green(), self.color.blue(), self.alpha * 255)
        self.brush = QBrush(self.color, Qt.SolidPattern)
        self.pen = QPen(self.color, self.size * 2.0)
        if self.painter:
            self.painter.setBrush(self.brush)
            self.painter.setPen(self.pen)


class DrawQt(ProxyInterface):
    def __init__(self, *args, **kwargs):
        Draw.__init__(self)
        self.queue = mp.Queue()
        self.queue_res = mp.Queue()
        ProxyInterface.__init__(self, DrawApp, self.queue)
        args = (self.queue, self.queue_res, args, kwargs)
        self.process = mp.Process(target=self._run, args=args)
        self.process.daemon = True
        self.process.start()

    def _run(self, queue, queue_res, args, kwargs):
        self.queue = queue
        self.queue_res = queue_res
        self.app = DrawApp()
        self.app.update = self._update
        self.app.run(*args, **kwargs)

    def _update(self):
        if not self.queue_res.empty():
            res = self.queue_res.get()
            if res[1] is None:
                del self.app.image_buffer[res[0]]
            else:
                self.app.image_buffer[res[0]] = res[1]
        if self.queue.empty():
            return
        while not self.queue.empty():
            cmd = self.queue.get()
        self.app.cmd = cmd

    def begin(self):
        pass

    def end(self, dt=0):
        self.commit()
        time.sleep(dt)

    def __enter__(self):
        pass

    def __exit__(self, *args):
        self.commit()

    def close(self):
        self.process.terminate()
        self.process.join()

    def set_image(self, image, key):
        self.queue_res.put((key, image))

    def drop_image(self, key):
        self.queue_res.put((key, None))
