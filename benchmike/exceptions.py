"""Module containing custom exceptions used in package:
        FunTimeOutError
        FunctionsNotFoundError
        BenchmarkRuntimeError
        InvalidArgumentError
        """


class FunTimeoutError(Exception):
    """Exception raised when process which runs benchmark exceeds
     specified runtime"""

    def __init__(self, message):
        super().__init__()
        self.message = "Error: " + message


class FunctionsNotFoundError(Exception):
    """Exception raised when file does not contain required functions"""

    def __init__(self, message):
        super().__init__()
        self.message = "Error: " + message


class BenchmarkRuntimeError(Exception):
    """Exception raised when any error occurs while performing
     benchmark pass"""

    def __init__(self, message):
        super().__init__()
        self.message = "Error: " + message


class InvalidArgumentError(Exception):
    """Exception raised when invalid argument was entered as input"""

    def __init__(self, message):
        super().__init__()
        self.message = "Error: " + message
