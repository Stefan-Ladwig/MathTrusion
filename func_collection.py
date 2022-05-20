from typing import Callable
import numpy as np
from numpy import sin, cos
from numpy.polynomial import Polynomial


##################  |
# path functions #  |
##################  V

def line() -> Callable:

    return lambda x: np.array([0, 0, x])


def circle() -> Callable:

    func = lambda x: np.array([cos(x), sin(x), 0])

    return func


def helix(dist: float = 1/np.pi) -> Callable:

    dist = float(dist)

    func = lambda x: circle()(x) + dist * np.array([0, 0, x])

    return func


def spiral() -> Callable:

    return lambda x: x * circle()(x)


def parabola(width: float = 1) -> Callable:
    width = float(width)

    return lambda x: np.array([x, ((1 / width) * x)**2, 0])


##############################  |
# scale / rotation functions #  |
##############################  V

def constant(constant: float = 1) -> Callable:

    return Polynomial([constant])


def linear(constant: float = 0, slope: float = 1) -> Callable:

    return Polynomial([constant, slope])


def quadratic(a0: float = 0, a1: float = 0, a2: float = 1) -> Callable:

    return Polynomial([a0, a1, a2])


def periodic(scale: float = 1, period: float = 2 * np.pi,\
             offset: float = 0) -> Callable:
    
    return lambda x: scale * np.sin(x * 2 * np.pi / period + offset)


def arc(scale: float = 1, portion: float = 1) -> Callable:
    
    return lambda x: scale * np.sqrt(1 - (2 * x - 1)**2)



#######################  |
# function dictionary #  |
#######################  V

func_dict = {
    'p':{
        'circle': circle,
        'helix': helix,
        'spiral': spiral,
        'line': line,
        'parabola': parabola
    },
    's/r':{
        'constant': constant,
        'linear': linear,
        'quadratic': quadratic,
        'periodic': periodic,
        'arc': arc
    }
}

default_intervalls = {
    'circle': (-np.pi, np.pi, 20),
    'helix': (-2 * np.pi, 2 * np.pi, 40),
    'spiral': (0, 4 * np.pi, 40),
    'line': (0, 1, 20),
    'parabola': (-2, 2, 20)
}