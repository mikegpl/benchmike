"""Module for running function evaluations in separate processes and measuring
time
    Classes:
    CodeBenchmark
"""

from multiprocessing import Process, Queue
from signal import signal, alarm, SIGALRM
from time import time

from benchmike import exceptions as err
from benchmike.customlogger import CustomLogger, LOGGER_NAME


class CodeBenchmark:
    """Class for measuring time of execution of function evaluation"""

    logger = CustomLogger(LOGGER_NAME)

    def __init__(self, path, timeout):
        self.measurements = []
        self.timeout = timeout
        self.queue = Queue()
        with open(path) as file:
            self.code = compile(file.read(), path, 'exec')
        self.logger.log(
            "Started with path {}, timeout {}".format(path, timeout))

    def run_benchmark(self, step, start, count):
        """Runs benchmark, saves data points to self.measurements, returns
        measurements"""
        size = start
        passes_to_make = count
        pass_count = 0
        time_left = time_elapsed = 0.0
        while time_elapsed < self.timeout and pass_count < passes_to_make:
            try:
                time_left = int(self.timeout - time_elapsed)
                if time_left == 0:
                    break
                data_point = self.make_measurement(size, time_left)
                time_elapsed += data_point[2]
                self.measurements.append((data_point[0], data_point[1]))
                size += step
                pass_count += 1
            except err.FunTimeoutError:
                print("Finished benchmarking")
                self.logger.log(
                    "Benchmark timeouted at {} passes".format(pass_count))
                break
            except err.FunctionsNotFoundError as ex:
                raise err.BenchmarkRuntimeError(ex.message)
            except RuntimeError:
                raise err.BenchmarkRuntimeError(
                    "Caught other type of runtime error")
            except Exception as ex:
                raise err.BenchmarkRuntimeError(repr(ex))
        self.logger.log(
            "Finished benchmarking with {} passes and {} s left".format(
                pass_count, time_left))
        return self.measurements

    @staticmethod
    def signal_handler(signum, frame):
        """Signal handler for run_code"""
        raise err.FunTimeoutError("Timeout error: process was too slow")

    def run_code(self, size, timeout):
        """This runs code in separate thread to measure time, requires
        set_up(size) and run(size) methods in code to be executed"""
        signal(SIGALRM, CodeBenchmark.signal_handler)
        exec(self.code, globals())
        alarm(timeout)
        whole_start_time = time()
        try:
            exec('set_up(size)')
            run_start_time = time()
            exec('run(size)')
            whole_end_time = run_end_time = time()
            self.queue.put((size, run_end_time - run_start_time,
                            whole_end_time - whole_start_time))

        except err.FunTimeoutError as ex:
            self.queue.put((size, ex, time() - whole_start_time))
        except TypeError:
            self.queue.put(
                (size, err.FunctionsNotFoundError(
                    "Could not find set_up() or run() methods in input file"),
                 time() - whole_start_time))
            self.logger.log("File doesn't contain required methods")
        except Exception as ex:
            self.queue.put((size, RuntimeError(ex), time() - whole_start_time))

    def make_measurement(self, size, timeout):
        """This will return tuple (size, run_time, full_time) or rethrow
        exception"""

        @self.logger.log_fun
        def run_process():
            p = Process(target=self.run_code,
                        args=(size, timeout))
            p.start()
            run_result = self.queue.get()
            p.join()
            return run_result

        result = run_process()

        if isinstance(result[1], err.FunTimeoutError):
            raise result[1]
        elif isinstance(result[1], err.FunctionsNotFoundError):
            raise result[1]
        elif isinstance(result[1], RuntimeError):
            raise result[1]
        elif result:
            return result
        else:
            raise Exception("Queue returned empty value")
