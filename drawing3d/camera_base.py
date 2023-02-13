from abc import ABC, abstractmethod

class CameraBase(ABC):
    @abstractmethod
    def __init__(self, image_size):
        pass
    
    @property
    @abstractmethod
    def image_size(self):
        pass

    @image_size.setter
    @abstractmethod
    def image_size(self, image_size):
        pass

    @property
    @abstractmethod
    def att(self):
        pass

    @att.setter
    @abstractmethod
    def att(self, att):
        pass

    @abstractmethod
    def project(self, p, visible_only=True):
        pass

    @abstractmethod
    def projects(self, ps, visible_only=True):
        pass

    @abstractmethod
    def estimate_size(self, p, size):
        pass
    
    @abstractmethod
    def move(self, *v):
        pass

    @abstractmethod
    def rotate(self, *a):
        pass