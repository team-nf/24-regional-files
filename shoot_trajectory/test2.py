from math import sin, cos, tan, atan2
from math import radians as rad
from math import degrees as deg
import cmath
import math


i = complex(0, 1)


def discriminant(a, b, c):
	s1 = (-b + cmath.sqrt(b**2 - 4*a*c)) / (2*a)
	s2 = (-b - cmath.sqrt(b**2 - 4*a*c)) / (2*a)
	return s1, s2



class QuantumPoint:
	def __init__(self, x_k_coef, x_1ok_coef, x_coef, y_k_coef, y_1ok_coef, y_coef):
		# x içinde k nın ve 1/knın katsayıları
		self.x_k_coef = x_k_coef
		self.x_1ok_coef = x_1ok_coef
		self.x_coef = x_coef

		# aynısının y hali
		self.y_k_coef = y_k_coef
		self.y_1ok_coef = y_1ok_coef
		self.y_coef = y_coef


	@classmethod
	def from_point(cls, x, y):
		x_k_coef = (y+x*i)/(2*i)
		x_1ok_coef = (x*i-y)/(2*i)

		y_k_coef = (y*i-x)/(2*i)
		y_1ok_coef = (y*i+x)/(2*i)

		return cls(x_k_coef, x_1ok_coef, 0, y_k_coef, y_1ok_coef, 0)


	def rotate(self, angle):
		x_1ok = self.x_1ok_coef*cos(angle) + self.y_1ok_coef*sin(angle)
		x_k = self.x_k_coef*cos(angle) + self.y_k_coef*sin(angle)
		x = self.x_coef*cos(angle) + self.y_coef*sin(angle)

		y_1ok = self.y_1ok_coef*cos(angle) - self.x_1ok_coef*sin(angle)
		y_k = self.y_k_coef*cos(angle) - self.x_k_coef*sin(angle)
		y = self.y_coef*cos(angle) - self.x_coef*sin(angle)

		self.x_1ok_coef, self.x_k_coef, self.x_coef = x_1ok, x_k, x
		self.y_1ok_coef, self.y_k_coef, self.y_coef = y_1ok, y_k, y


	def shift(self, right, up):
		self.x_coef -= right
		self.y_coef -= up


	def angle_collapse(self, angle_to_collapse):
		# for debug purposes
		k = math.e ** (i * angle_to_collapse)
		x = self.x_k_coef * k + self.x_1ok_coef / k + self.x_coef
		y = self.y_k_coef * k + self.y_1ok_coef / k + self.y_coef
		print("collapsed point: ({:.3f}, {:.3f})".format(x.real, y.real))
		return (x.real, y.real)



k = math.e ** (i * rad(45))
q = QuantumPoint.from_point(4, 3)


