import logging
from datetime import datetime
from typing import Callable


def add_start_time(func):
    def wrapper(*args, **kwargs):
        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if len(args) > 1:
            original_msg = args[1]
            new_msg = f"[{start_time}] {original_msg}"
            args = (args[0], new_msg) + args[2:]
        return func(*args, **kwargs)

    return wrapper


class MyLogger:
    def __init__(self, filename: str = __name__):
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(filename)

    @add_start_time
    def debug(self, msg):
        self.logger.debug(msg)

    @add_start_time
    def info(self, msg):
        self.logger.info(msg)

    @add_start_time
    def warning(self, msg):
        self.logger.warning(msg)

    @add_start_time
    def error(self, msg):
        self.logger.error(msg)

    @add_start_time
    def critical(self, msg):
        self.logger.critical(msg)

    def log_function(self, origin_function: Callable):
        def func(*args, **kwargs):
            function_name = origin_function.__name__
            self.info(f"---- Function {function_name} Enter ----")
            result = origin_function(*args, **kwargs)
            self.info(
                f"---- Function {function_name} Exit ----"
            )
            return result

        return func
