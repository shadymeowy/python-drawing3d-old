from abc import ABC, abstractmethod


class DrawBase(ABC):
    def __init__(self):
        self.color = 'red'
        self.alpha = 1.0
        self.size = 1

    def style(self, color, alpha=1.0, size=1):
        self.color = color
        self.alpha = alpha
        self.size = size

    @abstractmethod
    def begin(self):
        pass

    @abstractmethod
    def end(self, dt=0):
        pass

    @abstractmethod
    def point(self, p):
        pass

    @abstractmethod
    def lines(self, points):
        pass

    @ abstractmethod
    def tri(self, p1, p2, p3):
        pass

    @ abstractmethod
    def text(self, p, text):
        pass
    
    @ abstractmethod
    def image4(self, image, ps):
        pass

    @ abstractmethod
    def set_image(self, image, key):
        pass

    @ abstractmethod
    def drop_image(self, key):
        pass