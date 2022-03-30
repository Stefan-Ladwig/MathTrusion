from asyncio import constants
from typing import Callable
import numpy as np
from numpy import sin, cos
from numpy.polynomial import Polynomial


##################  |
# path functions #  |
##################  V

def circle(scale: float = 1, orientation: str = 'xy') -> Callable:
    
    if orientation == 'xy':
        func = lambda x: scale * np.array([cos(x), sin(x), 0])
    elif orientation == 'yz':
        func = lambda x: scale * np.array([0, cos(x), sin(x)])
    elif orientation == 'zx':
        func = lambda x: scale * np.array([sin(x), 0, cos(x)])

    return func


def helix(scale: float = 1, dist: float = 1/np.pi,\
          orientation: str = 'xy') -> Callable:
    
    if orientation == 'xy':
        func = lambda x: circle(scale, orientation)(x)\
                                + dist * np.array([0, 0, x])
    elif orientation == 'yz':
        func = lambda x: circle(scale, orientation)(x)\
                                + dist * np.array([x, 0, 0])
    elif orientation == 'zx':
        func = lambda x: circle(scale, orientation)(x)\
                                + dist * np.array([0, x, 0])

    return func


def spiral(scale: float = 1, orientation: str = 'xy') -> Callable:
    
    func = lambda x: x * circle(scale, orientation)(x)

    return func


def line(scale: float = 1) -> Callable:
    
    func = lambda x: scale * np.array([0, 0, x])

    return func


def parabola(scale: float = 1, width: float = 2) -> Callable:
    
    func = lambda x: scale * np.array([x, ((1 / width) * x)**2, 0])

    return func


##############################  |
# scale / rotation functions #  |
##############################  V

def constant(constant: float = 1) -> Callable:

    func = Polynomial([constant])

    return func


def linear(constant: float = 0, slope: float = 1) -> Callable:

    func = Polynomial([constant, slope])

    return func


def quadratic(a0: float = 0, a1: float = 0, a2: float = 1) -> Callable:

    func = Polynomial([a0, a1, a2])

    return func


def periodic(scale: float = 1, period: float = 2 * np.pi,\
             offset: float = 0) -> Callable:
    
    func = lambda x: scale * np.sin(x + offset)

    return func


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
    }
}