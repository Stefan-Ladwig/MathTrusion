import numpy as np
from scipy.misc import derivative
from scipy.spatial.transform import Rotation as R
from mayavi import mlab
from base_shapes import star, squircle, n_gon


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


def calc_triangle_indices(num_vertices, num_steps):
    triangles = []
    offset = np.ones(3)

    for i in range(num_vertices):
        triangles.append([i, int(num_vertices + (1 + i) % num_vertices),\
                          int((1 + i) % num_vertices)])
        triangles.append([i, int(num_vertices + (1 + i) % num_vertices),\
                          int(num_vertices + i % num_vertices)])
    triangles = np.array(triangles)

    big_offset = num_vertices * offset
    triangle_base = triangles
    for j in range(1, num_steps - 1):
        triangles = np.append(triangles,  triangle_base + j * big_offset,\
                              axis=0)
    return triangles


def calc_3d_object(shape_2d, path_func, scale_func, rot_func,\
                   start=0, end=1, num_steps=1000):

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

        base_x = path_rot.apply(base_x)
        base_y = path_rot.apply(base_y)
        base_z = unit_vector(tangent)
        rot_mat = np.array([base_x, base_y, base_z]).T

        plane_rot = R.from_rotvec([0, 0, rot_func(x)])

        global_rot = R.from_matrix(rot_mat) * plane_rot

        plane = scale_func(x) * shape_2d
        plane = global_rot.apply(plane)
        plane += path_func(x)

        points.append(plane)
        prev_tangent = tangent

    points = np.reshape(points, (len(shape_2d) * num_steps, 3))
    return points


def test():
    start = 0
    end = 8*np.pi
    num_steps = 1000
    shape_2d = n_gon(5)

    shape_2d = np.append(shape_2d, np.zeros((len(shape_2d), 1)), axis=1)


    def path_func(x):
        return np.array([np.sin(x), np.cos(x), x])


    def scale_func(x):
        return 0.5


    def rot_func(x):
        return 0


    triangles = calc_triangle_indices(len(shape_2d), num_steps)

    points = calc_3d_object(shape_2d, path_func, scale_func, rot_func,\
                            start=start, end=end, num_steps=num_steps)
    x, y ,z = points.T

    mlab.triangular_mesh(x, y, z, triangles)
    mlab.show()


if __name__ == '__main__':
    test()
