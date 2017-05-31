"""Main module of benchmike, tool for estimating time complexity of Python code
    Classes:
    BenchMike

    Procedures:
    main
"""
from benchmike import argparser as parser
from benchmike import benchmark as mark
from benchmike import exceptions as err

from benchmike import bigoestimator as bigoes


class BenchMike:
    """Main class, binds benchmarking class and benchmark data processing
    classes, allows performing multiple benchmarking runs"""

    def __init__(self):
        self.args = None
        self.benchmarker = None
        self.estimator = None
        self.plotter = None
        self.generator = None

    def run(self, code, timeout=30, timefile='time_source.py',
            sizefile='size_source.py', step=100, start=100, count=100):
        """ Main method of BenchMike, allows multiple benchmarking runs
        """
        self.args = code, timeout, timefile, sizefile, step, start, count
        self.benchmarker = mark.CodeBenchmark(code, timeout)
        data_points = self.benchmarker.run_benchmark(step, start, count)

        self.estimator = bigoes.ComplexityEstimator(data_points)
        complexity, a, b = self.estimator.estimate_complexity()
        factors = self.estimator.factors

        self.plotter = bigoes.EstimationPlotter(data_points)
        self.plotter.plot_fitted(factors, 2)

        self.generator = bigoes.CodeGenerator(complexity, (a, b))
        self.generator.save_execution_time_fun(timefile)
        self.generator.save_max_input_size_fun(sizefile)


def main():
    """Main procedure of benchmike module"""
    try:
        args = parser.parse()
        parser.validate_args(*args)
        benchmike = BenchMike()
        benchmike.run(*args)
    except err.BenchmarkRuntimeError as ex:
        print(ex.message)
        print("An error occurred while benchmarking, exit")
        return
    except Exception as e:
        print("Some other exception: " + repr(e))
        return


if __name__ == '__main__':
    main()
