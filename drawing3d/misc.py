import numpy as np

NORMAL_XY = np.array([0., 0., 1.])
NORMAL_YZ = np.array([1., 0., 0.])
NORMAL_XZ = np.array([0., 1., 0.])

E_X = np.array([1., 0., 0.])
E_Y = np.array([0., 1., 0.])
E_Z = np.array([0., 0., 1.])


def intersection_plane_line(pp, pn, lp, ln):
    """
        pp: point on the plane
        pn: normal vector of the plane
        lp: point on the line
        ln: vector of the line
        return: point on the line that intersects with the plane
    """
    pn = pn / np.linalg.norm(pn)
    ln = ln / np.linalg.norm(ln)
    d = np.dot(pp - lp, pn) / np.dot(ln, pn)
    return lp + ln * d


def perspective_get_vecs(r, vfov, hfov):
    """
        r: camera attitude
        vfov: vertical field of view
        hfov: horizontal field of view
        return: vector, vector_v, vector_h
    """
    vfov = np.deg2rad(vfov)
    hfov = np.deg2rad(hfov)
    vfov_half = vfov / 2
    hfov_half = hfov / 2
    vec = r.apply((1, 0, 0))
    vec_v = r.apply((0, 0, 1))
    vec_h = r.apply((0, -1, 0))
    vec_v = vec_v * np.tan(vfov_half)
    vec_h = vec_h * np.tan(hfov_half)
    return vec, vec_v, vec_h


def iperspective_project(r, vfov, hfov, w, h, p_r):
    """
        r: camera attitude
        vfov: vertical field of view
        hfov: horizontal field of view
        w: image width
        h: image height
        p_r: point on image
        return: point on image plane relative to camera # TODO
    """
    vec, vec_v, vec_h = perspective_get_vecs(r, vfov, hfov)
    p_r = p_r - np.array((w, h)) / 2
    p_r = p_r / np.array((w, h)) * 2
    p_r = p_r * np.array((np.dot(vec_h, vec_h), np.dot(vec_v, vec_v)))
    p_r = p_r[0] * vec_h / np.dot(vec_h, vec_h) + p_r[1] * vec_v / np.dot(vec_v, vec_v)
    p_r = p_r + vec
    return p_r


def perspective_project(p, r, vfov, hfov, w, h, p1):
    """
        p: camera position
        r: camera attitude
        vfov: vertical field of view
        hfov: horizontal field of view
        w: image width
        h: image height
        p1: point on image plane relative to camera
        return: point on image
    """
    vec, vec_v, vec_h = perspective_get_vecs(r, vfov, hfov)
    p_p = intersection_plane_line(p + vec, vec, p1, p - p1)
    p_r = p_p - p - vec
    p_r = np.array((np.dot(p_r, vec_h), np.dot(p_r, vec_v)))
    p_r = p_r / np.array((np.dot(vec_h, vec_h), np.dot(vec_v, vec_v)))
    p_r = p_r * np.array((w, h)) / 2
    p_r = p_r + np.array((w, h)) / 2
    return p_r, p_p


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
