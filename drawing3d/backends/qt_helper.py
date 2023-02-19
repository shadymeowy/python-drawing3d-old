try:
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *
    from PySide6.QtOpenGL import *
    from PySide6.QtOpenGLWidgets import *

    COLOR_NAMES = {name: QColor.fromString(name) for name in QColor.colorNames()}

    def app_exec(app):
        getattr(app, 'exec')()

except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
    from PySide2.QtOpenGL import *

    COLOR_NAMES = {name: QColor(name) for name in QColor.colorNames()}

    def app_exec(app):
        app.exec_()
