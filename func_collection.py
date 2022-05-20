from typing import Callable
import numpy as np
from numpy import sin, cos
from numpy.polynomial import Polynomial


##################  |
# path functions #  |
##################  V

def line(scale: float = 1) -> Callable:

    scale = float(scale)

    return lambda x: scale * np.array([0, 0, x])


def circle(scale: float = 1) -> Callable:
    
    scale = float(scale)

    func = lambda x: scale * np.array([cos(x), sin(x), 0])

    return func


def helix(scale: float = 1, dist: float = 1/np.pi) -> Callable:
    
    scale = float(scale)
    dist = float(dist)

    func = lambda x: circle(scale)(x) + dist * np.array([0, 0, x])

    return func


def spiral(scale: float = 1) -> Callable:
    
    scale = float(scale)

    return lambda x: x * circle(scale)(x)


def parabola(scale: float = 1, width: float = 2) -> Callable:
    
    scale = float(scale)
    width = float(width)

    return lambda x: scale * np.array([x, ((1 / width) * x)**2, 0])


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


def arc(scale: float = 1, offset: float = 0) -> Callable:
    
    return lambda x: scale * np.sqrt(1 - (x-offset)**2)



#######################  |
# function dictionary #  |
#######################  V

func_dict = {
    'p':{
        'line': line,
        'parabola': parabola,
        'circle': circle,
        'helix': helix,
        'spiral': spiral
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
    'line': (0, 1, 20),
    'parabola': (-2, 2, 20),
    'circle': (-np.pi, np.pi, 20),
    'helix': (-2 * np.pi, 2 * np.pi, 40),
    'spiral': (0, 4 * np.pi, 40)
}