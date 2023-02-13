from setuptools import setup

setup(
    name='python-drawing3d',
    version='0.0.1',
    description='Easy 3D drawing library elevating 2D drawing libraries for visualization purposes',
    author='Tolga Demirdal',
    url='https://github.com/shadymeowy/python-drawing3d',
    setup_requires=[],
    install_requires=['numpy', 'scipy', 'PySide6'],
    packages=['drawing3d', 'drawing3d.draw', 'drawing3d.camera'],
    entry_points={
    },
)
