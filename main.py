import numpy as np
from scipy.misc import derivative
from scipy.spatial.transform import Rotation as R
from mayavi import mlab
from base_shapes import star, squircle, n_gon

start = -5
end = 5
num_steps = 200
base = n_gon(5)

base = np.append(base, np.zeros((len(base), 1)), axis=1)


def unit_vector(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    else:
        return v / norm


def angle_between_vectors(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


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


def path_func(x):
    return np.array([x, 0, -x**2 + 25])


def scale_func(x):
    return 1


def rot_func(x):
    return np.pi * np.sin(x * 2 * np.pi / 5)


def get_points():
    points = []
    prev_tangent = np.array([0, 0, 1])
    base_x = np.array([1, 0, 0])
    base_y = np.array([0, 1, 0])
    for x in np.linspace(start, end, num_steps):
        tangent = derivative(path_func, x)
        path_rot_vec = np.cross(prev_tangent, tangent)
        path_rot_angle = angle_between_vectors(prev_tangent, tangent)
        path_rot_vec = unit_vector(path_rot_vec) * path_rot_angle
        path_rot = R.from_rotvec(path_rot_vec)
        plane_rot = R.from_rotvec([0, 0, rot_func(x)])
        base_x = path_rot.apply(base_x)
        base_y = path_rot.apply(base_y)
        rot_mat = np.array([base_x, base_y, tangent]).T
        global_rot = R.from_matrix(rot_mat) * plane_rot
        plane = scale_func(x) * base
        plane = global_rot.apply(plane)
        plane += path_func(x)
        points.append(plane)
        prev_tangent = tangent
    points = np.reshape(points, (len(base) * num_steps, 3))
    return points


if __name__ == '__main__':
    points = get_points()
    triangles = get_triangle_indices(len(base))
    x, y ,z = points.T
    mlab.triangular_mesh(x, y, z, triangles)
    mlab.show()