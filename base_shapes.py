import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R


def plt_polygon(vertices):
    _, ax = plt.subplots()
    l = len(vertices)
    for i in range(len(vertices)):
        plt.plot([vertices[i, 0], vertices[(i + 1) % l, 0]],\
                 [vertices[i, 1], vertices[(i + 1) % l, 1]], 'r-')  
    ax.set_aspect('equal')
    plt.show()


def vertices_from_function(func, input_values=np.linspace(-1,1)):
    vertices = [func(val) for val in input_values]
    return np.array(vertices)


def n_gon(n):
    def func(phi):
        return [np.cos(phi), np.sin(phi), 0]
    phi = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return vertices_from_function(func, phi)


def star(spikiness=2.5, num_spikes=5):
    rot_vec = [0, 0, np.pi / num_spikes]
    rotation = R.from_rotvec(rot_vec)

    outer_polygon = n_gon(num_spikes)
    inner_polygon = outer_polygon / spikiness
    inner_polygon = rotation.apply(inner_polygon)

    vertices = np.zeros((2 * num_spikes, 3))
    vertices[0::2] = outer_polygon
    vertices[1::2] = inner_polygon
    return vertices


def squircle(exponent=4):
    def func(x):
        return [x, (1 - abs(x)**exponent)**(1 / exponent), 0]

    x_values = np.linspace(-1, 0, 200)
    upper_left = vertices_from_function(func, x_values)
    upper_right = upper_left.copy()
    upper_right[:,0] *= -1
    upper_half = np.append(upper_left, upper_right[::-1], axis=0)
    lower_half = upper_half.copy()[::-1]
    lower_half[:,1] *= -1
    return np.append(upper_half, lower_half, axis=0)


if __name__ == '__main__':
    plt_polygon(squircle(0.6))
    