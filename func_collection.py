import numpy as np


def circle(x, scale=1):
    return scale * np.array([np.cos(x), np.sin(x), 0])


def helix(x, scale=1):
    return circle(x, scale=scale) + np.array([0, 0, x])


def spiral(x, scale=1):
    return x * circle(x, scale=scale)


def line(x, scale=1):
    return scale * np.array([0, 0, x])


def parabola(x, scale=1, width=2):
    return scale * np.array([x, ((1 / width) * x)**2, 0])
