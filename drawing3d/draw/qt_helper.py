try:
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *

    COLOR_NAMES = {name: QColor.fromString(name) for name in QColor.colorNames()}

    def app_exec(app):
        getattr(app, 'exec')()

except ImportError:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *

    COLOR_NAMES = {name: QColor(name) for name in QColor.colorNames()}

    def app_exec(app):
        app.exec_()
