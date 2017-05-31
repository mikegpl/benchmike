import logging

LOGGER_NAME = 'benchmike_log'


class CustomLogger:
    """Custom class for loggin function activity and simple messages"""

    def __init__(self, log_name):
        self.log_name = log_name
        logging.basicConfig(level=logging.DEBUG, filename=log_name)
        self.clear_log()

    def log(self, msg):
        """Log message"""
        logging.info(msg)

    def log_fun(self, f):
        """Log function application result"""

        def tmp(*args):
            result = f(*args)
            self.log(f.__name__ + str(args) + " = " + str(result))
            return result

        return tmp

    def clear_log(self):
        with open(self.log_name, "w"):
            pass
