"""Transformation matrices."""

from math import cos, sin, tan
from typing import Sequence, Union

import numpy as np

from .common import Line, Point
from ..geometry.geometry import line_angle, vec_along_line, is_line, is_point


def identity_matrix() -> 'ndarray':
    """
    Return the identity matrix
    [[1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]].

    Returns:
        np.ndarray: The identity matrix.
    """
    return np.identity(3)


def xform_matrix(
    a: float, b: float, c: float, d: float, e: float, f: float
) -> 'ndarray':
    """
    Return a transformation matrix in row form
    [[a, b, 0], [c, d, 0], [e, f, 1.0]].

    Args:
        a (float): The a component of the transformation matrix.
        b (float): The b component of the transformation matrix.
        c (float): The c component of the transformation matrix.
        d (float): The d component of the transformation matrix.
        e (float): The e component of the transformation matrix.
        f (float): The f component of the transformation matrix.

    Returns:
        np.ndarray: The transformation matrix.
    """
    return np.array([[a, b, 0], [c, d, 0], [e, f, 1.0]])


def translation_matrix(dx: float, dy: float) -> 'ndarray':
    """
    Return a translation matrix in row form
    [[1.0, 0, 0], [0, 1.0, 0], [dx, dy, 1.0]].

    Args:
        dx (float): The translation distance along the x-axis.
        dy (float): The translation distance along the y-axis.

    Returns:
        np.ndarray: The translation matrix.
    """
    return np.array([[1.0, 0, 0], [0, 1.0, 0], [dx, dy, 1.0]])


def inv_translation_matrix(dx: float, dy: float) -> 'ndarray':
    """
    Return the inverse of a translation matrix in row form
    [[1.0, 0, 0], [0, 1.0, 0], [-dx, -dy, 1.0]].

    Args:
        dx (float): The translation distance along the x-axis.
        dy (float): The translation distance along the y-axis.

    Returns:
        np.ndarray: The inverse translation matrix.
    """
    return np.array([[1.0, 0, 0], [0, 1.0, 0], [-dx, -dy, 1.0]])


def rot_about_origin_matrix(theta: float) -> 'ndarray':
    """
    Return a rotation matrix in row form
    [[cos(theta), sin(theta), 0], [-sin(theta), cos(theta), 0], [0, 0, 1.0]].

    Args:
        theta (float): The rotation angle in radians.

    Returns:
        np.ndarray: The rotation matrix.
    """
    c = cos(theta)
    s = sin(theta)
    return np.array([[c, s, 0], [-s, c, 0], [0, 0, 1.0]])


def rotation_matrix(theta: float, about=(0, 0)) -> 'ndarray':
    """
    Construct a rotation matrix that can be used to rotate a point
    about another point by theta float.
    Return a rotation matrix in row form
    dx, dy = about
    [[cos(theta), sin(theta), 0],
    [-sin(theta), cos(theta), 0],
    cos(theta)dx-sin(theta)dy+x, cos(theta)dy+sin(theta)dx+y, 1]].

    Args:
        theta (float): The rotation angle in radians.
        about (tuple, optional): The point to rotate about, defaults to (0, 0).

    Returns:
        np.ndarray: The rotation matrix.
    """
    dx, dy = about[:2]
    # translate 'about' to the origin
    trans_mat = translation_matrix(-dx, -dy)
    # rotate around the origin
    rot_mat = rot_about_origin_matrix(theta)
    # translate it back to initial pos
    inv_trans_mat = translation_matrix(dx, dy)
    # compose the transformation matrix
    return trans_mat @ rot_mat @ inv_trans_mat


def inv_rotation_matrix(theta: float, about=(0, 0)) -> 'ndarray':
    """
    Construct the inverse of a rotation matrix that can be used to rotate a point
    about another point by theta float.
    Return a rotation matrix in row form
    dx, dy = about
    [[cos(theta), -sin(theta), 0],
    [sin(theta), cos(theta), 0],
    -cos(theta)dx-sin(theta)dy+x, -sin(theta)dx+cos(theta)dy+y, 1]].

    Args:
        theta (float): The rotation angle in radians.
        about (tuple, optional): The point to rotate about, defaults to (0, 0).

    Returns:
        np.ndarray: The inverse rotation matrix.
    """
    dx, dy = about[:2]
    # translate 'about' to the origin
    trans_mat = translation_matrix(-dx, -dy)
    # rotate around the origin
    rot_mat = rot_about_origin_matrix(theta)
    # translate it back to initial pos
    inv_trans_mat = translation_matrix(dx, dy)
    # compose the transformation matrix
    return inv_trans_mat @ rot_mat.T @ trans_mat


def glide_matrix(mirror_line: Line, distance: float) -> 'ndarray':
    """
    Return a glide-reflection matrix in row form.
    Reflect about the given vector then translate by dx
    along the same vector.

    Args:
        mirror_line (Line): The line to mirror about.
        distance (float): The distance to translate along the line.

    Returns:
        np.ndarray: The glide-reflection matrix.
    """
    mirror_mat = mirror_about_line_matrix(mirror_line)
    x, y = vec_along_line(mirror_line, distance)[:2]
    trans_mat = translation_matrix(x, y)

    return mirror_mat @ trans_mat


def inv_glide_matrix(mirror_line: Line, distance: float) -> 'ndarray':
    """
    Return the inverse of a glide-reflection matrix in row form.
    Reflect about the given vector then translate by dx
    along the same vector.

    Args:
        mirror_line (Line): The line to mirror about.
        distance (float): The distance to translate along the line.

    Returns:
        np.ndarray: The inverse glide-reflection matrix.
    """
    mirror_mat = mirror_about_line_matrix(mirror_line)
    x, y = vec_along_line(mirror_line, distance)[:2]
    trans_matrix = translation_matrix(x, y)

    return trans_matrix @ mirror_mat


def scale_matrix(scale_x: float, scale_y: float = None) -> 'ndarray':
    """
    Return a scale matrix in row form.

    Args:
        scale_x (float): Scale factor in x direction.
        scale_y (float, optional): Scale factor in y direction, defaults to None.

    Returns:
        np.ndarray: A scale matrix in row form.
    """
    if scale_y is None:
        scale_y = scale_x
    return np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1.0]])


def inv_scale_matrix(scale_x: float, scale_y: float = None) -> 'ndarray':
    """
    Return the inverse of a scale matrix in row form.

    Args:
        scale_x (float): Scale factor in x direction.
        scale_y (float, optional): Scale factor in y direction, defaults to None.

    Returns:
        np.ndarray: The inverse of a scale matrix in row form.
    """
    if scale_y is None:
        scale_y = scale_x
    return np.array([[1 / scale_x, 0, 0], [0, 1 / scale_y, 0], [0, 0, 1.0]])


def scale_in_place_matrix(scale_x: float, scale_y: float, point: Point) -> 'ndarray':
    """
    Return a scale matrix in row form that scales about a point.

    Args:
        scale_x (float): Scale factor in x direction.
        scale_y (float): Scale factor in y direction.
        point (Point): Point about which the scaling is performed.

    Returns:
        np.ndarray: A scale matrix in row form that scales about a point.
    """
    dx, dy = point[:2]
    trans_mat = translation_matrix(-dx, -dy)
    scale_mat = np.array([[scale_x, 0, 0], [0, scale_y, 0], [0, 0, 1.0]])
    inv_trans_mat = translation_matrix(dx, dy)
    return trans_mat @ scale_mat @ inv_trans_mat


def shear_matrix(theta_x: float, theta_y: float = 0) -> 'ndarray':
    """
    Return a shear matrix in row form.

    Args:
        theta_x (float): Angle of shear in x direction.
        theta_y (float, optional): Angle of shear in y direction, defaults to 0.

    Returns:
        np.ndarray: A shear matrix in row form.
    """
    return np.array([[1, tan(theta_y), 0], [tan(theta_x), 1, 0], [0, 0, 1.0]])


def inv_shear_matrix(theta_x: float, theta_y: float = 0) -> 'ndarray':
    """
    Return the inverse of a shear matrix in row form.

    Args:
        theta_x (float): Angle of shear in x direction.
        theta_y (float, optional): Angle of shear in y direction, defaults to 0.

    Returns:
        np.ndarray: The inverse of a shear matrix in row form.
    """
    return np.array([[1, -tan(theta_x), 0], [-tan(theta_y), 1, 0], [0, 0, 1.0]])


def mirror_matrix(about: Union[Line, Point]) -> 'ndarray':
    """
    Return a matrix to perform reflection about a line or a point.

    Args:
        about (Union[Line, Point]): A line or point about which the reflection is performed.

    Returns:
        np.ndarray: A matrix to perform reflection about a line or a point.

    Raises:
        RuntimeError: If about is not a line or a point.
    """
    if is_line(about):
        res = mirror_about_line_matrix(about)
    elif is_point(about):
        res = mirror_about_point_matrix(about)
    else:
        raise RuntimeError(f"{about} is invalid!")
    return res


def mirror_about_x_matrix() -> 'ndarray':
    """
    Return a matrix to perform reflection about the x-axis.

    Returns:
        np.ndarray: A matrix to perform reflection about the x-axis.
    """
    return np.array([[1.0, 0, 0], [0, -1.0, 0], [0, 0, 1.0]])


def mirror_about_y_matrix() -> 'ndarray':
    """
    Return a matrix to perform reflection about the y-axis.

    Returns:
        np.ndarray: A matrix to perform reflection about the y-axis.
    """
    return np.array([[-1.0, 0, 0], [0, 1.0, 0], [0, 0, 1.0]])


def mirror_about_line_matrix(line: Line) -> 'ndarray':
    """
    Return a matrix to perform reflection about a line.

    Args:
        line (Line): The line about which the reflection is performed.

    Returns:
        np.ndarray: A matrix to perform reflection about a line.
    """
    p1, p2 = line
    x1, y1 = p1[:2]
    theta = line_angle(p1, p2)
    two_theta = 2 * theta

    # translate the line to the origin
    # T = translation_matrix(-x1, -y1)
    # rotate about the origin by 2*theta
    # R = rot_about_origin_matrix(2*theta)
    # translate back
    # inv_t = translation_matrix(x1, y1)
    # return T @ R @ inv_t

    # We precompute the matrix
    c2 = cos(two_theta)
    s2 = sin(two_theta)
    return np.array(
        [
            [c2, s2, 0],
            [s2, -c2, 0],
            [-x1 * c2 + x1 - y1 * s2, -x1 * s2 + y1 * c2 + y1, 1.0],
        ]
    )


def mirror_about_origin_matrix() -> 'ndarray':
    """
    Return a matrix to perform reflection about the origin.

    Returns:
        np.ndarray: A matrix to perform reflection about the origin.
    """
    return np.array([[-1.0, 0, 0], [0, -1.0, 0], [0, 0, 1.0]])


def mirror_about_point_matrix(point: Point) -> 'ndarray':
    """
    Return a matrix to perform reflection about a point.

    Args:
        point (Point): The point about which the reflection is performed.

    Returns:
        np.ndarray: A matrix to perform reflection about a point.
    """
    x, y = point[:2]
    # T = translation_matrix(-x, -y)
    # M = mirror_about_origin_matrix()
    # inv_t = translation_matrix(x, y)
    # return T @ M @ inv_t
    # We precompute the matrix

    return np.array([[-1.0, 0, 0], [0, -1.0, 0], [2 * x, 2 * y, 1.0]])


def rotate(points: Sequence[Point], theta: float, about: Point = (0, 0)) -> 'ndarray':
    """
    Rotate points by theta about a point.

    Args:
        points (Sequence[Point]): The points to rotate.
        theta (float): The angle to rotate by.
        about (Point, optional): The point to rotate about, defaults to (0, 0).

    Returns:
        np.ndarray: The rotated points.
    """
    return points @ rotation_matrix(theta, about)


def translate(points: Sequence[Point], dx: float, dy: float) -> 'ndarray':
    """
    Translate points by dx, dy.

    Args:
        points (Sequence[Point]): The points to translate.
        dx (float): The translation distance along the x-axis.
        dy (float): The translation distance along the y-axis.

    Returns:
        np.ndarray: The translated points.
    """
    return points @ translation_matrix(dx, dy)


def mirror(points: Sequence[Point], about: Line) -> 'ndarray':
    """
    Mirror points about a line.

    Args:
        points (Sequence[Point]): The points to mirror.
        about (Line): The line to mirror about.

    Returns:
        np.ndarray: The mirrored points.
    """
    return points @ mirror_matrix(about)


def glide(points: Sequence[Point], mirror_line: Line, distance: float) -> 'ndarray':
    """
    Glide (mirror about a line then translate along the same line) points about a line.

    Args:
        points (Sequence[Point]): The points to glide.
        mirror_line (Line): The line to mirror about.
        distance (float): The distance to translate along the line.

    Returns:
        np.ndarray: The glided points.
    """
    return points @ glide_matrix(mirror_line, distance)


def shear(points: Sequence[Point], theta_x: float, theta_y: float = 0) -> 'ndarray':
    """
    Shear points by theta_x in x direction and theta_y in y direction.

    Args:
        points (Sequence[Point]): The points to shear.
        theta_x (float): The angle of shear in x direction.
        theta_y (float, optional): The angle of shear in y direction, defaults to 0.

    Returns:
        np.ndarray: The sheared points.
    """
    return points @ shear_matrix(theta_x, theta_y)


def scale(points: Sequence[Point], scale_x: float, scale_y: float) -> 'ndarray':
    """
    Scale points by scale_x in x direction and scale_y in y direction.

    Args:
        points (Sequence[Point]): The points to scale.
        scale_x (float): The scale factor in x direction.
        scale_y (float): The scale factor in y direction.

    Returns:
        np.ndarray: The scaled points.
    """
    return points @ scale_matrix(scale_x, scale_y)


def scale_in_place(
    points: Sequence[Point], scale_x: float, scale_y: float, point: Point
) -> 'ndarray':
    """
    Scale points about a point by scale_x in x direction and scale_y in y direction.

    Args:
        points (Sequence[Point]): The points to scale.
        scale_x (float): The scale factor in x direction.
        scale_y (float): The scale factor in y direction.
        point (Point): The point about which the scaling is performed.

    Returns:
        np.ndarray: The scaled points.
    """
    return points @ scale_in_place_matrix(scale_x, scale_y, point)
