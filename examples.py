import base_shapes
import func_collection
from triangular_mesh import tri_mesh
import numpy as np
from mayavi import mlab


def screw():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.n_gon(4)
    scale_func = lambda _: 1
    rot_func = lambda x: 4 * x
    path_func = func_collection.line

    mesh = tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def sphere():
    start = -1
    end = 1
    num_steps = 200

    shape_2d = base_shapes.circle()
    scale_func = lambda x: np.sqrt(1 - (x)**2)
    rot_func = lambda _: 0
    path_func = func_collection.line

    mesh = tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def star_helix():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.star()
    scale_func = lambda x: np.log(1 + x)
    rot_func = lambda x: x
    path_func = func_collection.helix

    mesh = tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def squircle_circle():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.squircle()
    scale_func = lambda _: 0.5
    rot_func = lambda x: x
    path_func = func_collection.circle

    mesh = tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


if __name__ == '__main__':
    star_helix()
