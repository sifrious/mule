import os
import sys
import inspect
from dotenv import load_dotenv as dotenv
from pprint import pprint
dotenv('monolith/.env/local_env.env')


class Configuration:

    INPUT_DIRECTORY_NAME = 'Inputs'
    OUTPUT_DIRECTORY_NAME = 'Outputs'
    CRAWL_INPUT_DIRECTORY_PATH = 'CrawlQueues'
    CRAWL_OUTPUT_DIRECTORY_PATH = 'Crawls'

    def __init__(self):
        self.errors = []
        self.verbosity = {"switch": os.getenv('VERBOSITY_SWITCH') == 'True',
                          "debug": os.getenv('VERBOSITY_DEBUG') == 'True'}
        self.setvenv = self.establish_venv()
        if self.setvenv == True:
            self.crawl_type = os.getenv('CRAWL_TYPE')
            self.current_directory = os.getcwd()
            self.root_path = self.get_root_path()
            self.root_path_len = len(self.root_path)
            self.input_path = ""
            self.input_list = self.get_inputs_list()
            self.inputs = self.read_input_list()
            self.output_path = ""
            self.output_list = self.get_outputs_list()
            self.outputs = self.read_output_list()
        if len(self.errors) > 0:
            print(
                f"Cannot configure. Identified {str(len(self.errors))} in Configuration.")
            for error in self.errors:
                print(error)

    def establish_venv(self):
        def using_venv():
            return (hasattr(sys, 'real_prefix') or
                    (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))
        if using_venv():
            return True
        else:
            msg = "this program requires configuration within an venv to work"
            msg += "\ncreate a venv using the guide in the README.md file to proceed"
            msg += " with the configuration process."
            msg += "\nERROR: Cannot Configure Application"
            self.errors.append('msg')
            return False

    def get_root_path(self):
        frame = inspect.currentframe().f_back
        file_name = inspect.getfile(frame)
        root_name_index = file_name.find('/monolith/')
        if root_name_index > 0:
            return file_name[:file_name.find('/monolith/') + len('/monolith/')]

    def get_directory(self, path, result_type):
        # Uncomment block for debug info
        # frame = inspect.currentframe().f_back
        # line_number = frame.f_lineno
        # print(f"called get_directory from {line_number}")

        def append_directory_dict(path, result_type):
            contents = {"path": path,
                        "folders": [],
                        "filepaths": [],
                        "files": {}}
            for root, dirs, files in os.walk(path):
                for file in files:
                    contents["filepaths"].append(os.path.join(root, file))
                    extension_index = file.find(".")
                    if extension_index >= 0:
                        file_array = file.split(".")
                        extension = file_array[-1]
                        if extension not in contents["files"]:
                            contents["files"][extension] = []
                        contents["files"][extension].append(file)
                for directory in dirs:
                    contents["folders"].append(os.path.join(root, directory))
                contents["path"] = root
                contents["relative_path"] = root[self.root_path_len-1:]
                contents["directories"] = dirs
                contents["files"]["list"] = files
            return contents
        if os.path.exists(path):
            contents = {"path": path}
            searched_paths = []
            paths = [path]
            while len(paths) > 0:
                new_content = append_directory_dict(paths[0], result_type)
                contents[new_content["relative_path"]] = new_content
                searched_paths.append(paths[0])
                paths.remove(paths[0])
                for path in new_content["folders"]:
                    paths.append(path)
        else:
            error_msg = f"{path} does not exist. Could not populate {result_type} directory dict."
            self.errors.append(error_msg)

    def get_inputs_list(self):
        final_path = ""
        input_path = os.getenv('INPUT_DIRECTORY_PATH')
        if input_path is None:
            input_path = self.root_path
            input_path += f"/{Configuration.INPUT_DIRECTORY_NAME}"
            input_path += f"/{Configuration.CRAWL_INPUT_DIRECTORY_PATH}"
        if input_path is not None and self.root_path is not None:
            if input_path[:2] == "./":
                self.input_path = f'{self.root_path}{input_path[2:]}'
                return self.get_directory(self.input_path, 'input')
            else:
                self.input_path = input_path
                return self.get_directory(self.input_path, 'input')

    def get_outputs_list(self):
        final_path = ""
        output_path = os.getenv('OUTPUT_DIRECTORY_PATH')
        if output_path is None:
            output_path = self.root_path
            output_path += f"/{Configuration.OUTPUT_DIRECTORY_NAME}"
            output_path += f"/{Configuration.CRAWL_OUTPUT_DIRECTORY_PATH}"
        if output_path is not None:
            if output_path[:2] == "./":
                self.output_path = f'{self.root_path}{output_path[2:]}'
                return self.get_directory(self.output_path, 'output')
            else:
                self.output_path = output_path
                return self.get_directory(final_path, 'output')

    def read_directory(self):
        return None

    def read_input_list(self):
        return None

    def read_output_list(self):
        return None
