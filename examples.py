import base_shapes
import func_collection
from triangular_mesh import tri_mesh
import numpy as np
from mayavi import mlab


'''
def your_modell():
    start =
    end = 
    num_steps = 

    shape_2d = 
    scale_func = 
    rot_func = 
    path_func = 

    mesh = tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()
'''


def screw():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.n_gon(3)
    scale_func = lambda _: 1
    rot_func = lambda x: 4 * x
    path_func = func_collection.line

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
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

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def star_helix():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.star(spikiness=1.5)
    scale_func = lambda x: np.log(1 + x)
    rot_func = lambda x: x
    path_func = func_collection.helix

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def squircle_circle():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.squircle(6)
    scale_func = lambda _: 0.4
    rot_func = lambda x: x
    path_func = func_collection.circle

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def triangle_parabola():
    start = -2 * np.pi
    end = 2 * np.pi
    num_steps = 2000

    shape_2d = base_shapes.n_gon(3)
    scale_func = lambda _: 1
    rot_func = lambda x: x * np.sin(x)
    path_func = func_collection.parabola

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


def mobius_loop():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = np.array([[-1, 0, 0], [1, 0, 0]])
    scale_func = lambda _: 0.3
    rot_func = lambda x: x
    path_func = lambda x: np.array([0, np.cos(x), np.sin(x)])

    mesh = tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)
    mlab.triangular_mesh(*mesh)
    mlab.show()


if __name__ == '__main__':
   mobius_loop()