import numpy as np

NORMAL_XY = np.array([0., 0., 1.])
NORMAL_YZ = np.array([1., 0., 0.])
NORMAL_XZ = np.array([0., 1., 0.])

E_X = np.array([1., 0., 0.])
E_Y = np.array([0., 1., 0.])
E_Z = np.array([0., 0., 1.])


def orthogonal_vectors(v):  # TODO: optimize
    """
        v: vector
        return: vector, vector
    """
    d1 = np.dot(v, E_X)
    d2 = np.dot(v, E_Y)
    d3 = np.dot(v, E_Z)
    if d1 < d2:
        if d1 < d3:
            v1 = np.cross(v, E_X)
        else:
            v1 = np.cross(v, E_Z)
    else:
        if d2 < d3:
            v1 = np.cross(v, E_Y)
        else:
            v1 = np.cross(v, E_Z)
    v1 = v1 / np.linalg.norm(v)
    v2 = np.cross(v, v1)
    v2 = v2 / np.linalg.norm(v)
    return v1, v2
