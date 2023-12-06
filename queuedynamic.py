# monolith.queuedynamic.py
# for traditional crawling

from .verbosity import Verbosity


class Queue:

    def __init__(self, config):
        self.logger = Verbosity(config.verbosity)
        self.default = True
