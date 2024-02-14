# from math import sin, cos, tan, atan2
from math import radians as rad
from math import degrees as deg

from numpy import cos, sin, tan, arctan2
from numpy.polynomial import Polynomial
import numpy as np

import cmath
import math


i = complex(0, 1)


class QuantumPoint:
    def __init__(self, x_poly, y_poly):
        self._range_set = False
        self.debug = True

        self.x_poly = x_poly
        self.y_poly = y_poly


    @classmethod
    def from_coeffs(cls, x_a, x_b, x_c, y_a, y_b, y_c):
        x_poly = Polynomial([x_c, x_b, x_a], symbol="k")
        y_poly = Polynomial([y_c, y_b, y_a], symbol="k")
        return cls(x_poly, y_poly)


    @classmethod
    def from_point(cls, x, y):
        x_k_coef = (y+x*i)/(2*i)
        x_1ok_coef = (x*i-y)/(2*i)

        y_k_coef = (y*i-x)/(2*i)
        y_1ok_coef = (y*i+x)/(2*i)

        return cls.from_coeffs(x_k_coef, 0, x_1ok_coef, y_k_coef, 0, y_1ok_coef)


    def set_angle_range(self, angle_min, angle_max, degrees=True):
        print("range set")
        self._range_set = True
        self.angle_min = rad(angle_min) if degrees else angle_min
        self.angle_max = rad(angle_max) if degrees else angle_max


    def apply_func(self, func, args=(), kwargs={}):
        for i in range(3):
            rv = func(self.x_poly.coef[i], self.y_poly.coef[i], *args, **kwargs)
            self.x_poly.coef[i], self.y_poly.coef[i] = rv


    def _rotate_func(self, x, y, angle, *a, **kw):
        new_x = x*cos(angle) + y*sin(angle)
        new_y = y*cos(angle) - x*sin(angle)
        return new_x, new_y


    def rotate(self, angle):
        self.apply_func(self._rotate_func, (angle,))


    def shift(self, right, up):
        self.x_poly.coef[1] -= right
        self.y_poly.coef[1] -= up


    def angle_collapse(self, angle_to_collapse):
        # for debug purposes
        k = math.e ** (i * angle_to_collapse)
        x = self.x_poly.coef[2] * k + self.x_poly.coef[1] + self.x_poly.coef[0] / k
        y = self.y_poly.coef[2] * k + self.y_poly.coef[1] + self.y_poly.coef[0] / k

        if self.debug:
            print("[angle_collapse]: collapsed point at angle {}: ({:.3f}, {:.3f})".format(
                deg(angle_to_collapse), x.real, y.real))

        return (x.real, y.real)


    def solve_k(self, k):
        # k = e**(i*alpha)
        # ln(k) / i = alpha
        return cmath.log(k)/i


    def apply_range(self, *angles):
        if self._range_set:
            return [angle for angle in angles if self.angle_min < angle < self.angle_max]
        return list(angles)


    def debug_print(self, function_name, angles):
        if self.debug:
            if len(angles) == 0:
                print(f"[{function_name}]: no solution found")

            else:
                if self._range_set:
                    print(f"[{function_name}]: solutions after range application:")

                for i, angle in enumerate(angles):
                    print(f"[{function_name}]: {i+1}th solution: {deg(angle):.3f}")


    def collapse_x(self, x=0):
        # Example solver function
        new_poly = Polynomial(self.x_poly.coef.copy(), symbol="k")
        new_poly.coef[1] -= x
        s1, s2 = new_poly.roots()

        angles = self.apply_range(
            self.solve_k(s1).real,
            self.solve_k(s2).real,
        )

        self.debug_print("collapse_x", angles)
        return angles


    def collapse_y(self, y=0):
        # Example solver function
        new_poly = Polynomial(self.y_poly.coef.copy(), symbol="k")
        new_poly.coef[1] -= y
        s1, s2 = new_poly.roots()

        angles = self.apply_range(
            self.solve_k(s1).real,
            self.solve_k(s2).real,
        )

        self.debug_print("collapse_x", angles)
        return angles


def get_closest_angle(current_angle, angles):
    if len(angles) == 0: return None
    return min(angles, key=lambda angle: abs(angle - current_angle))



def example_calculation(
    h: float,
    d: float,
    r: float = 0.,
    u: float = 0.,
    rotation: float = 0.,
    angle_range = (20., 90.),
    current_angle: float = 0.,
):
    """
    h: height of the target
    d: distance to the target
    r: distance in the x axis from rotation point to shooter (if any)
    u: distance in the y axis from rotation point to shooter (if any)
    rotation: rotation angle of the shooter (if any)
    angle_range: range of angles to consider
    current_angle: current angle of the shooter (to find the closest angle in the range)
    """

    # example usage to get angle
    q = QuantumPoint.from_point(d, h)
    q.set_angle_range(*angle_range, degrees=True)
    q.debug = True

    # shooterın dönme noktasına göre konumunu tanımla
    q.shift(r, u)
    q.rotate(rotation)

    # olabilecek açıları bul
    angles = q.collapse_y(0)

    # range içinde olan en yakın açılar arasından en yakın olanı seç
    return get_closest_angle(current_angle, angles)


# q = QuantumPoint.from_point(3, 3)
# q.angle_collapse(rad(45))
# q.collapse_y(0)
# q.set_angle_range(20, 110, degrees=True)
# q.collapse_y(0)

example_calculation(
    h = 180,
    d = 513,
    r = 45,
    u = 15,
    rotation = 0,
    angle_range = (0, 90),
    current_angle = 0,
)