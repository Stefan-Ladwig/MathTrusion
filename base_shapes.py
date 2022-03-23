import numpy as np
import matplotlib.pyplot as plt


def plt_polygon(vertices):
    fig, ax = plt.subplots()
    for i in range(len(vertices)):
        plt.plot([vertices[i, 0], vertices[(i + 1) % len(vertices), 0]],\
                [vertices[i, 1], vertices[(i + 1) % len(vertices), 1]], 'r-')  
    ax.set_aspect('equal')
    plt.show()


def rotate_vector(vector, rot_angle):
    rot_mat = np.array([[np.cos(rot_angle), -np.sin(rot_angle)],\
                        [np.sin(rot_angle), np.cos(rot_angle)]])
    return np.matmul(rot_mat, vector)


def vertices_from_function(func, input_values=np.linspace(-1,1)):
    vertices = [func(val) for val in input_values]
    return np.array(vertices)


def n_gon(n):
    def func(phi):
        return [np.cos(phi), np.sin(phi)]
    phi = np.linspace(0, 2 * np.pi, n, endpoint=False)
    return vertices_from_function(func, phi)


def star(spikiness=2.5, num_spikes=5):
    rot_angle = np.pi / num_spikes
    inner_polygon = n_gon(num_spikes)
    outer_polygon = spikiness * inner_polygon
    inner_polygon = np.array([rotate_vector(v, rot_angle)\
                              for v in inner_polygon])
    vertices = np.zeros((2 * num_spikes, 2))
    for i in range(num_spikes):
        vertices[2 * i] = outer_polygon[i]
        vertices[2 * i + 1] = inner_polygon[i]
    return vertices


def squircle(exponent=4):
    def func(x):
        return [x, (1 - abs(x)**exponent)**(1 / exponent)]
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
    