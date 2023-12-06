import os
import sys
import inspect
from dotenv import load_dotenv as dotenv
dotenv('monolith/.env/local_env.env')


class Configuration:

    INPUT_DIRECTORY_NAME = 'Inputs'
    OUTPUT_DIRECTORY_NAME = 'Outputs'
    CRAWL_INPUT_DIRECTORY_PATH = 'CrawlQueues'
    CRAWL_OUTPUT_DIRECTORY_PATH = 'Crawls'

    def __init__(self):
        self.verbosity = {"switch": os.getenv('VERBOSITY_SWITCH') == 'True',
                          "debug": os.getenv('VERBOSITY_DEBUG') == 'True'}
        self.crawl_type = os.getenv('CRAWL_TYPE')
        self.current_directory = os.getcwd()
        self.root_path = self.get_root_path()
        self.input_path = self.get_inputs_list()
        self.inputs = self.read_input_list()
        self.output_list = self.get_outputs_list()
        self.outputs = self.read_output_list()

    def get_root_path(self):
        frame = inspect.currentframe().f_back
        file_name = inspect.getfile(frame)
        root_name_index = file_name.find('/monolith/')
        if root_name_index > 0:
            return file_name[:file_name.find('/monolith/') + len('/monolith/')]

    def get_directory(self, path):
        path = path.strip()
        print(f"in get_directory with {path}")
        if os.path.exists(path):
            return path
        else:
            print("that path doesn't exist")

    def get_inputs_list(self):
        final_path = ""
        input_path = os.getenv('INPUT_DIRECTORY_PATH')
        if input_path is None:
            input_path = self.root_path
            input_path += f"/{Configuration.INPUT_DIRECTORY_NAME}"
            input_path += f"/{Configuration.CRAWL_INPUT_DIRECTORY_PATH}"
        if input_path is not None:
            print(input_path[:2])
            if input_path[:2] == "./":
                final_path = self.get_directory(
                    f'{self.root_path}{input_path[2:]}')
            else:
                final_path = self.get_directory(input_path)
        return final_path

    def get_outputs_list(self):
        final_path = ""
        output_path = os.getenv('OUTPUT_DIRECTORY_PATH')
        if output_path is not None:
            print(output_path[:2])
            if output_path[:2] == "./":
                final_path += f'{self.root_path}{output_path[2:]}'
            else:
                final_path = output_path
            self.get_directory(final_path)
        else:
            output_path = self.root_path
            input_path += f"/{Configuration.OUTPUT_DIRECTORY_NAME}"
            input_path += f"/{Configuration.CRAWL_OUTPUT_DIRECTORY_PATH}"
        return None

    def read_directory(self):
        return None

    def read_input_list(self):
        return None

    def read_output_list(self):
        return None
