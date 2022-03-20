import numpy as np
from scipy.misc import derivative
from mayavi import mlab
from base_shapes import star, squircle

start = 0
end = 2 * np.pi
num_steps = 200
base = squircle(7)

base = np.append(base, np.zeros((len(base), 1)), axis=1)


def get_triangle_indices(len_base):
    triangles = []
    offset = np.ones(3)

    for i in range(len_base):
        triangles.append([i, int(len_base + (1 + i) % len_base),\
                          int((1 + i) % len_base)])
        triangles.append([i, int(len_base + (1 + i) % len_base),\
                          int(len_base + i % len_base)])
    triangles = np.array(triangles)

    big_offset = len_base * offset
    triangle_base = triangles
    for j in range(1, num_steps - 1):
        triangles = np.append(triangles,  triangle_base + j * big_offset,\
                              axis=0)
    return triangles


def spiral(x):
    return np.array([np.cos(x), np.sin(x), x])


def scale(x):
    return np.sqrt(x)


def calc_point(x):
    return spiral(x) + scale(x) * base


def get_points():
    points = np.array([calc_point(x) for x in\
                    np.linspace(start, end, num_steps)])
    points = np.reshape(points, (len(base) * num_steps, 3))
    return points


if __name__ == '__main__':
    points = get_points()
    triangles = get_triangle_indices(len(base))
    x, y ,z = points.T
    mlab.triangular_mesh(x, y, z, triangles)
    mlab.savefig('3dmodel.obj')
    mlab.show()