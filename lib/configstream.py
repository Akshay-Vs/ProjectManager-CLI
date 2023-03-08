import os
import sys
import configparser
import logging
import csv


class Configstream:
    # Read and write config files
    def __init__(self, path=os.path.expanduser("~/")):
        self.CONFIG_FILE_PATH = os.path.expanduser(
            f"{path}.config/projectmanager/config.ini"
        )
        logging.basicConfig(filename="config.log", level=logging.DEBUG)
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
        )

        # create config file if it does not exist
        if os.path.exists(self.CONFIG_FILE_PATH):
            logging.debug("Config file exists")
            self.config = configparser.ConfigParser()
            self.config_data = self.config.read(self.CONFIG_FILE_PATH)
            logging.info("Config file read")

        else:
            logging.info("Config file does not exist")
            self.config = configparser.ConfigParser()
            self.config["DEFAULT"] = {"type": "config"}

            if not os.path.exists(f"{path}.config/projectmanager"): os.mkdir(os.path.expanduser(f"{path}.config/projectmanager"))
            with open(self.CONFIG_FILE_PATH, "x") as configfile:
                self.config.write(configfile)
            logging.info(f"Config file created at {self.CONFIG_FILE_PATH}")

    def create_config_section(self, section):
        self.config.add_section(section)
        logging.info(f"Config section {section} created")
        self.save_config()

    def write_config(self, option, value, section="DEFAULT"):
        r"Write new option and value to config"
        self.config.set(section, option, value)
        logging.info(f"Config file updated: [{section}] {option}:{value}")
        self.save_config()

    def write_config_list(self, option, value, section="DEFAULT"):
        r"convert an array to csv and write to config"
        value = ",".join(map(str, value))  # array to csv
        self.config.set(section, option, value)
        logging.debug("Config Array converted to comma seperated value")
        logging.info(f"Config file updated: [{section}] {option}:{value}")
        self.save_config()

    def read_config_list(self, option, section="DEFAULT"):
        r"Read csv from config and return list"
        value = self.config.get(section, option)
        return value.split(",")

    def read_config(self, option, section="DEFAULT"):  # return value of an option
        return self.config.get(section, option)

    def save_config(self):
        with open(self.CONFIG_FILE_PATH, "w") as configfile:
            self.config.write(configfile)
        logging.info("Config file saved")

    def remove_config_option(self, option, section="DEFAULT"):
        logging.debug(f"COnfig Requested to remove option {option}")
        if self.config.has_option(option, section):
            self.config.remove_option(option, section)
            self.save_config()
            logging.critical(f"Config option {option} deleted")
        else:
            logging.warning(f"Config option {option} not found")

    def remove_config_section(self, section):
        logging.debug(f"Config Requested to remove section {section}")
        if self.config.has_section(section):
            self.config.remove_section(section)
            self.save_config()
            logging.critical(f"Config section {section} removed")
        else:
            logging.warning(f"Config section {section} not found")

    def delete_config_file(self):
        os.remove(self.CONFIG_FILE_PATH)
        logging.critical("Config file deleted")

    # def print_config_file(self):
    #     for section in self.config.sections():
    #         print(f"[{section}]")
    #         for key, value in self.config[section].options():
    #             print(f"{key}:{value}")


if __name__ == "__main__":
    config = Configstream()
    config.write_config("path", "myprojects")
    config.write_config_list("packages", ["node", "test"])
    print(config.read_config("path"))
    print(config.read_config_list("packages"))
    config.create_config_section('Section1')
    config.remove_config_option("path")
    config.remove_config_section('DEFAULT')
    config.delete_config_file()
