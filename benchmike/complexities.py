"""This module provides classes for matching time complexities of algorithms
and saving results to files.
    Classes:
    Complexity
        Constant
        Logarithmic
        Linear
        Linearithmic
        Quadratic
        Polynomial
        SuperPolynomial
"""
from math import log2, sqrt, isclose


class Linear:
    """Base complexity class"""
    requires_inverse = False

    @staticmethod
    def get_n(size):
        """Return T(N) for scaling used in linear regression"""
        return size

    @staticmethod
    def get_t(time):
        """Return N(T) for scaling used in linear regression"""
        return time

    @staticmethod
    def get_time(size, a_1=1, a_0=0):
        """Return estimated code runtime"""
        return a_1 * size + a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        """Return max input size for specified runtime"""
        return int((time - a_0) / a_1)

    @staticmethod
    def get_description():
        """Returns description of complexity class, e.g. O(1)"""
        return 'O(n) - linear'


class Constant(Linear):
    """O(1) complexity class"""

    @staticmethod
    def get_n(size):
        return 1

    @staticmethod
    def get_description():
        return 'O(1) - constant'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        return a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        if time < a_0:
            return 0
        return "inf"


class Logarithmic(Linear):
    """O(log n) complexity class"""

    @staticmethod
    def get_n(size):
        return log2(size)

    @staticmethod
    def get_description():
        return 'O(log n) - logarithmic'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        return a_1 * log2(size) + a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        return int(2 ** ((time - a_0) / a_1))


class Linearithmic(Linear):
    """O(n*log n) complexity class"""

    @staticmethod
    def get_n(size):
        return size * log2(size)

    @staticmethod
    def get_description():
        return 'O(n * log n) - linearithmic'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        time = a_1 * size * log2(size) + a_0
        return 0.0 if time < 0.0 else time

    @staticmethod
    def get_max_size(time, a_1, a_0):
        return int(inverse(lambda x: a_1 * x * log2(x) + a_0, time))


class Quadratic(Linear):
    """O(n^2) complexity class"""

    @staticmethod
    def get_n(size):
        return size * size

    @staticmethod
    def get_description():
        return 'O(n^2) - quadratic'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        return (a_1 * size ** 2) + a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        return int(sqrt((time - a_0) / a_1))


class Polynomial(Linear):
    """O(n^k) complexity class"""

    @staticmethod
    def get_n(size):
        return int(size ** 3)

    @staticmethod
    def get_description():
        return 'O(n^k) - O(n^3) or worse polynomial'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        return (a_1 * size ** 3) + a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        return int(((time - a_0) / a_1) ** (1. / 3))


class SuperPolynomial(Linear):
    """O(2^n) complexity class"""

    @staticmethod
    def get_n(size):
        return int(2 ** size)

    @staticmethod
    def get_description():
        return 'O(2^n) - superpolynomial'

    @staticmethod
    def get_time(size, a_1=0, a_0=0):
        return a_1 * 2 ** size + a_0

    @staticmethod
    def get_max_size(time, a_1, a_0):
        return int(log2((time - a_0) / a_1))


def inverse(fun, value):
    """Calculate argument of f given its value"""
    epsilon = 1e-09
    start = middle = 1e-09
    end = 1e9
    while abs(end - start) > epsilon:
        middle = (start + end) / 2
        if isclose(fun(middle) - value, 0.0):
            break
        elif fun(middle) - value > 0 and fun(start) < value:
            end = middle
        else:
            start = middle
    return middle
