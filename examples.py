from matplotlib import projections
import base_shapes
import func_collection
from triangular_mesh import tri_mesh
import numpy as np
from mayavi import mlab
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.tri as mtri


def plot_matplotlib(x, y, z, triangles):
    fig = plt.figure(figsize=(6, 6), dpi=140, facecolor='black')
    ax = fig.add_subplot(projection='3d')
    ax.set_axis_off()
    ax.set_facecolor('black')
    ax.set_box_aspect((np.ptp(x), np.ptp(y), np.ptp(z)))
    triang = mtri.Triangulation(x, y, triangles=triangles)
    ax.plot_trisurf(triang, z, cmap=plt.cm.rainbow,\
                    edgecolors='grey', linewidths=0.1)
    plt.show()


def plot_mayavi(x, y, z, triangles):
    mlab.triangular_mesh(x, y, z, triangles)
    mlab.show()


'''
def your_modell():
    start =
    end = 
    num_steps = 

    shape_2d = 
    scale_func = 
    rot_func = 
    path_func = 

    return tri_mesh(shape_2d, path_func, scale_func, rot_func,\
                    start=start, end=end, num_steps=num_steps)
'''


def screw():
    start = 0
    end = 2 * np.pi
    num_steps = 200

    shape_2d = base_shapes.n_gon(3)
    scale_func = lambda _: 1
    rot_func = lambda x: 4 * x
    path_func = func_collection.line

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


def sphere():
    start = -1
    end = 1
    num_steps = 200

    shape_2d = base_shapes.circle()
    scale_func = lambda x: np.sqrt(1 - (x)**2)
    rot_func = lambda _: 0
    path_func = func_collection.line

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


def star_helix():
    start = 0
    end = 2 * np.pi
    num_steps = 100

    shape_2d = base_shapes.star(spikiness=1.5)
    scale_func = lambda x: np.log(1 + x)
    rot_func = lambda x: x
    path_func = lambda x: func_collection.helix(x, dist=1)

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


def squircle_circle():
    start = 0
    end = 2 * np.pi
    num_steps = 40

    shape_2d = base_shapes.squircle(6, detail=25)
    scale_func = lambda _: 0.4
    rot_func = lambda x: x
    path_func = func_collection.circle

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


def triangle_parabola():
    start = -2 * np.pi
    end = 2 * np.pi
    num_steps = 2000

    shape_2d = base_shapes.n_gon(3)
    scale_func = lambda _: 1
    rot_func = lambda x: x * np.sin(x)
    path_func = func_collection.parabola

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


def mobius_loop():
    start = 0
    end = 2 * np.pi
    num_steps = 100

    shape_2d = np.array([[-1, 0, 0], [1, 0, 0]])
    scale_func = lambda _: 0.3
    rot_func = lambda x: x
    path_func = lambda x: np.array([0, np.cos(x), np.sin(x)])

    return tri_mesh(shape_2d, scale_func, rot_func, path_func,\
                    start=start, end=end, num_steps=num_steps)


if __name__ == '__main__':
   plot_matplotlib(*star_helix())