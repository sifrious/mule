# This is the main logic of the application
from pprint import pprint
import logging
#
from .configuration import Configuration
from .verbosity import Verbosity


class Scrape(Verbosity):

    def __init__(self):
        config = Configuration()
        super().__init__(config.verbosity)
        self.default = True
        self.queue = self.determine_queue_type(config)
        self.scrape_page()

    def scrape_page(self):
        self.announce("entered")

    def determine_queue_type(self, config):
        if config.crawl_type == 'Dynamic':
            from .queuedynamic import Queue
            return Queue(config)
        elif config.crawl_type == 'Static':
            from .queuestatic import Queue
            return Queue(config)
        else:
            exit()
