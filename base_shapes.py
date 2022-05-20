import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from scipy.spatial.transform import Rotation as R


def plt_polygon(vertices):
    fig, ax = plt.subplots()
    polygon = Polygon(vertices[:,:2])
    ax.add_patch(polygon)
    ax.set_xlim([min(vertices[:,0]), max(vertices[:,0])])
    ax.set_ylim([min(vertices[:,1]), max(vertices[:,1])])
    ax.set_aspect('equal')
    fig.tight_layout()
    ax.set_axis_off()
    plt.show()


def vertices_from_function(func, input_values=np.linspace(-1,1)):
    vertices = [func(val) for val in input_values]
    return np.array(vertices)


def line(scale=1):

    scale = float(scale)

    func = lambda x: [x, 0, 0]
    return vertices_from_function(func, [-scale, scale])


def n_gon(vertices=3):

    vertices = int(vertices)

    func = lambda phi: [-np.sin(phi), np.cos(phi), 0]
    phi = np.linspace(0, 2 * np.pi, int(vertices), endpoint=False)
    return vertices_from_function(func, phi)


def circle(detail=50):
    return n_gon(detail)


def star(spikiness=2.5, spikes=5):
    
    spikiness = float(spikiness)
    spikes = int(spikes)

    rot_vec = [0, 0, np.pi / spikes]
    rotation = R.from_rotvec(rot_vec)

    outer_polygon = n_gon(spikes)
    inner_polygon = outer_polygon / spikiness
    inner_polygon = rotation.apply(inner_polygon)

    vertices = np.zeros((2 * spikes, 3))
    vertices[0::2] = outer_polygon
    vertices[1::2] = inner_polygon
    return vertices


def squircle(exponent=4, detail=50):

    exponent = float(exponent)
    detail = int(detail)

    func = lambda x: [x, (1 - abs(x)**exponent)**(1 / exponent), 0]

    x_values = np.linspace(-1, 0, int(detail))
    upper_left = vertices_from_function(func, x_values)
    upper_right = upper_left.copy()
    upper_right[:,0] *= -1
    upper_half = np.append(upper_left, upper_right[::-1], axis=0)
    lower_half = upper_half.copy()[::-1]
    lower_half[:,1] *= -1
    return np.append(upper_half, lower_half, axis=0)


shape_dict = {
    'line': line,
    'polygon': n_gon,
    'circle': circle,
    'star': star,
    'squircle': squircle
}


if __name__ == '__main__':
    plt_polygon(n_gon(4))
    