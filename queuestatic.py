# monolith.queuestatic.py
# for crawl-like scraping through a list

from .verbosity import Verbosity


class Queue:

    def __init__(self, config):
        self.logger = Verbosity(config.verbosity)
        self.default = True
