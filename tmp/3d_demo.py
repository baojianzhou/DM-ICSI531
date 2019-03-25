'''
==============
3D scatterplot
==============

Demonstration of a basic scatterplot in 3D.
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


def fun_x(t):
    return np.cosh(t)


def fun_y(t):
    return np.sinh(t)


def fun_z(t):
    return 1. + 2. * np.exp(t)


def r(t):
    return np.asarray(np.cosh(t), np.sinh(t), 1. + 2. * np.exp(t))


def r_prime(t):
    return np.asarray(np.sinh(t), np.cosh(t), 2. * np.exp(t))


def norm_r_prime(t):
    return np.sqrt(np.sinh(t) ** 2. + np.cosh(t) ** 2. + 4. * np.exp(2. * t))


def t_fun(t):
    return r(t) / norm_r_prime(t)


def delta_fun(t):
    return norm_r_prime(t)


def delta_prime_fun(t):
    return (1.0 / norm_r_prime(t)) * (2 * np.sinh(t) * np.cosh(t) + 4. * np.exp(2. * t))


def t_prime(t):
    delta = delta_fun(t)
    delta_prime = delta_prime_fun(t)
    term1 = np.cosh(t) * delta - np.sinh(t) * delta_prime
    term2 = np.sinh(t) * delta - np.cosh(t) * delta_prime
    term3 = 2. * np.exp(t) * (delta - delta_prime)
    return np.asarray([term1 / (delta ** 2.), term2 / (delta ** 2.), term3 / (delta ** 2.)])


def norm_t_fun(t):
    xxx = t_prime(t)
    return np.sqrt(xxx[0] ** 2. + xxx[1] ** 2. + xxx[2] ** 2.)


def curvature(t):
    return norm_t_fun(t) / norm_r_prime(t)


def radius(t):
    return 1. / curvature(t)


def area_h(r, h):
    term1 = (r ** 2.) * np.arccos((r - h) / r)
    term2 = (r - h) * np.sqrt(2. * r * h - h ** 2.)
    return term1 - term2


def problem_5():
    for t in np.linspace(-5., 5.0, 100):
        print(curvature(t), radius(t), curvature(t) * radius(t))


def problem_1(r):
    k = 1. / r
    for h in [1e-3, 1e-4, 1e-5, 1e-6, 1e-7, 1e-8, 1e-9, 1e-10, 1e-11, 1e-12, 1e-13]:
        real = area_h(r, h) ** 2. / (h ** 3.)
        print(real - k)
        print(real - (8.0 / 9.0) * k)
        print(real - (32.0 / 9.0) * k)
        print(real - (2.0 / 3.0) * k)
        print(real - (1.0 / k))
        print('-' * 50)


problem_1(1.)

print(np.pi / 2. - 1. - 1. / 6. - 3. / 40.)
