import configparser
import pprint
input_file_name = "github.properties"


class ConfigFile:

    def __init__(self):
        filename = input_file_name
        self.config = configparser.RawConfigParser()
        self.config.read(filename)

    def set_config_file(self, filename):
        self.config = configparser.RawConfigParser()
        self.config.read(filename)

    def get_as_string(self, section, name):
        try:
            res = self.config.get(section, name)
        except (configparser.NoOptionError, configparser.NoSectionError) as e:
            res = None
        return res

    if __name__ == "__main__":
        pass


class Pprint:

    def __init__(self, indent=4):
        self.pp = pprint.PrettyPrinter(indent=indent)
        pass

    def my_print(self, p_str):
        self.pp.pprint(p_str)
