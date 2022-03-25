from typing import Callable
import numpy as np
from scipy.misc import derivative
from scipy.spatial.transform import Rotation as R


def normalized_vector(vector: np.ndarray) -> np.ndarray:
    '''
    Return normalized vector,
    which is the vector of legth 1 with the same direction.
    If vector has length 0, the nullvector is returned.

    Parameters
    ----------
    vector : numpy array
        Numpy array of shape (n,1) or (n,)
        representing the vector to normalize.
    
    Returns
    -------
    numpy array
        Normalized vector as numpy array
    '''
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    else:
        return vector / norm


def angle_between_vectors(v1: np.ndarray, v2: np.ndarray) -> float:
    '''
    Return angle between the two given vectors in radians.
    their shape has to match.

    Parameters
    ----------
    v1 : numpy array
        First vector
    v2 : numpy array
        Second vector
    
    Returns
    -------
    float
        Angle between v1 and v2 in radians
    '''
    v1_u = normalized_vector(v1)
    v2_u = normalized_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def triangle_indices(num_vertices: int, num_steps: int) -> np.ndarray:
    '''
    Compute array of tripletts which define the indices of the points
    of a triangle in the array that is returned by points_3d.

    In other words: compute indices that define the faces of a 3D-modell.

    Parameters
    ----------
    num_vertices : int
        The number of vertices of the 2D-object that is the base
        for the 3D-modell that is to be created.
    num_steps : int
        The amount of steps for the extrusion
    
    Returns
    -------
    ndarray
        Array of triangle-index-tripletts
    '''
    triangles = []
    offset = np.ones(3)

    for i in range(num_vertices):
        triangles.append([i, int(num_vertices + (1 + i) % num_vertices),\
                          int((1 + i) % num_vertices)])
        triangles.append([i, int(num_vertices + (1 + i) % num_vertices),\
                          int(num_vertices + i % num_vertices)])
    triangles = np.array(triangles)

    big_offset = num_vertices * offset
    triangle_base = triangles
    for j in range(1, num_steps - 1):
        triangles = np.append(triangles,  triangle_base + j * big_offset,\
                              axis=0)
    return triangles


def points_3d(shape_2d: np.ndarray,\
              scale_func: Callable, rot_func: Callable, path_func: Callable,\
              start: float, end: float, num_steps: int) -> np.ndarray:
    '''
    Create a 3D modell as follows:
    divide intervall from start to end in num_steps parts,
    for each step use scale_func to scale and rot_func to rotate
    shape_2d, then translate the shape to the output of path_func.
    Each function will be called with the same value at every step.

    Parameters
    ----------
    shape_2d : ndarray
        The base shape used for the extrusion of shape (n,3)
    scale_func : Callable
        Takes a float as input and returns a float.
        This defines the scaling of shape_2d for every step
    rot_func : Callable
        Takes a float as input and returns a float.
        This defines the rotation of shape_2D around the z-axis
        for every step before being translated with path_func.
    path_func : Callable
        Takes float as input and returns a numpy array of shape (,3)
        representing a point in 3D space.
    start : float
        first value, that is given to transformation functions
    end : float
        last value, that is given to transformation functions
    num_steps : integer
        number of calculation steps between start and end.
        this determines the model's level of detail

    Returns
    -------
    Array of tripletts, where each triplett represents a vertex
    of the modell in 3D space
    '''
    points = []
    prev_tangent = np.array([0, 0, 1])
    base_x = np.array([1, 0, 0])
    base_y = np.array([0, 1, 0])

    for x in np.linspace(start, end, num_steps):

        tangent = derivative(path_func, x)
        path_rot_vec = np.cross(prev_tangent, tangent)
        path_rot_angle = angle_between_vectors(prev_tangent, tangent)
        path_rot_vec = normalized_vector(path_rot_vec) * path_rot_angle
        path_rot = R.from_rotvec(path_rot_vec)

        base_x = path_rot.apply(base_x)
        base_y = path_rot.apply(base_y)
        base_z = normalized_vector(tangent)
        rot_mat = np.array([base_x, base_y, base_z]).T

        plane_rot = R.from_rotvec([0, 0, rot_func(x)])

        global_rot = R.from_matrix(rot_mat) * plane_rot

        plane = scale_func(x) * shape_2d
        plane = global_rot.apply(plane)
        plane += path_func(x)

        points.append(plane)
        prev_tangent = tangent

    points = np.reshape(points, (len(shape_2d) * num_steps, 3))
    return points


def tri_mesh(shape_2d: np.ndarray,\
             scale_func: Callable, rot_func: Callable, path_func: Callable,\
             start: float = 0, end: float = 1, num_steps: int = 200) -> tuple:
    '''
    This is just a wrapper for triangle_indices and points_3d.
    The output is the output of those functions as a tuple,
    with the output of points_3d being seperated into its
    x, y and z part.
    Refer to their description for more details.

    Parameters
    ----------
    shape_2d : ndarray
        The base shape used for the extrusion of shape (n,3)
    scale_func : Callable
        Takes a float as input and returns a float.
        This defines the scaling of shape_2d for every step
    rot_func : Callable
        Takes a float as input and returns a float.
        This defines the rotation of shape_2D around the z-axis
        for every step before being translated with path_func.
    path_func : Callable
        Takes float as input and returns a numpy array of shape (,3)
        representing a point in 3D space.
    start : float
        First value, that is given to transformation functions.
        Default value is 0
    end : float
        Last value, that is given to transformation functions.
        Default value is 1
    num_steps : integer
        Number of calculation steps between start and end.
        this determines the model's level of detail.
        Default value is 200
    
    Returns
    -------
    tuple
        Containing the output of points_3d divided in x, y and z portion
        and the output of triangle_indices.
        Refer to their description for more details.
    
    '''
    triangles = triangle_indices(len(shape_2d), num_steps)

    points = points_3d(shape_2d, scale_func, rot_func, path_func,\
                            start=start, end=end, num_steps=num_steps)
    x, y ,z = points.T
    return (x, y, z, triangles)