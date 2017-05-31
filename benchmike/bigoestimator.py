"""Module for estimating code time complexity based on TOE measurements and
presenting them in RiGCzd form"""
import matplotlib.pyplot as plt
import numpy as np
from inspect import getsourcelines

from benchmike import complexities as cp
from benchmike.customlogger import CustomLogger, LOGGER_NAME


class ComplexityEstimator:
    """Class responsible for estimating time complexity of code and generating
    result files"""
    complexities = {
        'O(log n) - logarithmic': cp.Logarithmic,
        'O(n) - linear': cp.Linear,
        'O(n * log n - linearithmic': cp.Linearithmic,
        'O(n^2) - quadratic': cp.Quadratic,
        'O(n^k) - polynomial': cp.Polynomial,
        'O(2^n) - superpolynomial': cp.SuperPolynomial,
    }
    logger = CustomLogger(LOGGER_NAME)

    def __init__(self, size_time_list):
        self.size_time_list = size_time_list
        self.factors = None

    def estimate_complexity(self):
        """Returns estimated complexity and coefficients to generated
        time(size) function"""

        zipped = list(map(list, zip(*self.size_time_list)))
        sizes = zipped[0]
        times = zipped[1]
        fitted = []

        for key in self.complexities:
            complexity = self.complexities[key]

            # due to overflow error when converting int to float
            if sizes[len(
                    sizes) - 1] > 1000 and complexity == cp.SuperPolynomial:
                continue

            coefficients = np.vstack([
                [complexity.get_n(n) for n in sizes],
                np.ones(len(sizes))]).T
            values = [complexity.get_t(t) for t in times]
            regression = np.linalg.lstsq(coefficients, values)
            fitted.append({'complexity': complexity,
                           'regression': regression})

        # sort by sum of residuals from leasts squares method
        fitted = sorted(fitted,
                        key=lambda fit: fit['regression'][1][0] if
                        fit['regression'][1] else np.inf)

        results = [(x['complexity'], x['regression']) for x in fitted]
        factors = []
        if fitted[0]['regression'][1][0] < 1e-8:
            results.insert(0, (cp.Constant, None))
            factors.append((cp.Constant, 0, sum(times) / len(times)))

        print("Printing complexities, from best fit to least")
        for result in results:
            if result[1] and result[1][1]:
                print("Complexity: {}".format(result[0].get_description()))
                factors.append((result[0], result[1][0][0], result[1][0][1]))
                self.logger.log("Result: {} with a = {}, b = {}".format(
                    result[0].get_description(), result[1][0][0],
                    result[1][0][1]))
            else:
                print("Complexity: {}, no regression data".format(
                    result[0].get_description()))

        print("\nBenchMike's verdict: I'm almost sure it's {}\n".format(
            factors[0][0].get_description()))
        self.factors = factors
        self.logger.log("Verdict: {}\n".format(
            factors[0][0].get_description()))
        return factors[0][0], factors[0][1], factors[0][2]


class EstimationPlotter:
    """Class for plotting estimated complexity along with data points"""

    def __init__(self, xy_list):
        self.xy_list = xy_list
        self.plotted = []
        self.x_max = xy_list[len(xy_list) - 1][0]

    def add_function_plot(self, name, function, a, b, x_max):
        """Add function to main plot"""
        self.plotted.append((name, function))
        plt.plot(
            *EstimationPlotter.eval_func(lambda x: a * function(x) + b, x_max),
            label=name)

    def plot_fitted(self, factors, how_many):
        """Plot how_many complexities along with data points"""
        print("Plotting {} best fit complexities".format(how_many))
        for i in range(min(len(factors), how_many)):
            self.add_function_plot(factors[i][0].get_description(),
                                   factors[i][0].get_n,
                                   factors[i][1],
                                   factors[i][2], self.x_max)
        plt.scatter(*zip(*self.xy_list), label='data')
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
                   ncol=2, mode="expand", borderaxespad=0.)
        plt.show()

    @staticmethod
    def eval_func(func, x_max):
        """Helper function for evaluating function on points from range"""
        delta = 1
        xs = []
        ys = []
        x = 1
        while x < x_max:
            xs.append(x)
            ys.append(func(x))
            x += delta
        return xs, ys


class CodeGenerator:
    """Class for generating result files containg code of methods for
    calculating max input size for specified time and time of execution for
    specified input size
    """

    def __init__(self, complexity, factors):
        self.complexity = complexity
        self.a_1, self.a_0 = factors
        self.imports = 'from math import sqrt, log2, isclose\n'

    def save_execution_time_fun(self, filename):
        """Generate time(size) function code and save it to file"""
        file_contents = self.imports + '\n'
        file_contents += self.fun_to_str(self.complexity.get_time, 1)

        exec_time_fun = 'def time_fun(size):\n'
        exec_time_fun += '\treturn get_time(size, {}, {})'.format(self.a_1,
                                                                  self.a_0)
        file_contents += exec_time_fun + '\n'
        with open(filename, 'w+') as file:
            file.write(file_contents)

        print("Successfully written to {}".format(filename))

    def save_max_input_size_fun(self, filename):
        """Generate max_size(time) function code and save it to file"""
        file_contents = self.imports + '\n'
        file_contents += self.fun_to_str(self.complexity.get_max_size, 1)

        if self.complexity == cp.Linearithmic:
            file_contents += self.fun_to_str(cp.inverse, 0)

        max_size_fun = 'def size_fun(size):\n'
        max_size_fun += '\treturn get_max_size(size, {}, {})'.format(self.a_1,
                                                                     self.a_0)
        file_contents += max_size_fun + '\n'
        with open(filename, 'w+') as file:
            file.write(file_contents)

        print("Successfully written to {}".format(filename))

    def get_execution_time_fun(self):
        """Same as save_execution_time_fun, except returns result function as
        lambda expression"""
        return lambda x: self.complexity.get_time(x, self.a_1, self.a_0)

    def get_max_input_size_fun(self):
        """Same as save_max_size_fun, except returns result function as
        lambda expression"""
        return lambda x: self.complexity.get_max_size(x, self.a_1, self.a_0)

    @staticmethod
    def fun_to_str(function, skip):
        """Helper function for generating code of method"""
        result = ''
        fun_code = getsourcelines(function)[0][skip:]
        i = 0
        for line in fun_code:
            if '\"\"\"' in line:
                continue
            if "def" in line:
                code = line.lstrip()
            else:
                code = line
            if code != '' and i != 0:
                code = '\t' + code
            result += code
            i += 1
        return result
