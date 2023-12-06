
import inspect
import os
import sys


class Verbosity:

    def __init__(self, config):
        print(
            f'init verbosity ({config["switch"]}) debug mode {config["debug"]}')
        self.switch = config["switch"]
        self.debug = config["debug"]
        self.frame = None
        self.file_name = None
        self.line_number = None
        self.class_name = None
        self.get_caller_info()
        self.announce("init")
        self.__repr__()

    def log_repr(self):
        msg = "Verbosity instance"
        msg += f"\n  line_number {str(self.line_number)}"
        msg += f"\n  class_name {str(self.class_name)}"
        if self.switch == True:
            print(self.frame)
        return msg

    def config(func):
        def wrapper_function(*args, **kwargs):
            if os.getenv('VERBOSITY_SWITCH') == 'True':
                func(*args, **kwargs)
        return wrapper_function

    def get_caller_info(self):
        self.frame = inspect.currentframe().f_back.f_back.f_back.f_back
        file_name = inspect.getfile(self.frame)
        self.file_name = f"...{file_name[file_name.find('/monolith/'):]}"
        self.class_name = self.class_name = self.frame.f_locals.get(
            'self', None).__class__.__name__ if 'self' in self.frame.f_locals.keys() else None
        self.line_number = self.frame.f_lineno

    @config
    def announce(self, verb):
        self.get_caller_info()
        msg = f"{verb} "
        msg += f"{self.class_name} @[{self.file_name}] ln {str(self.line_number)}"
        print(msg)
        return msg
