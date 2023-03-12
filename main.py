import os
import shutil
from lib.configstream import ConfigStream


class ProjectManager:
    def __init__(self):
        self.CONFIG_DIR = os.path.expanduser("~/.config/projectmanager")

    def create(self):
        print(os.path.exists(f"{self.CONFIG_DIR}/config.ini"))
        if os.path.exists(f"{self.CONFIG_DIR}/config.ini"):
            self.config = ConfigStream(self.CONFIG_DIR)
            self.project_dir = self.config.read_config("project_dir")

        else:
            self.project_dir = input("Enter project directory: ")
            self.config = ConfigStream(self.CONFIG_DIR)
            self.config.write_config("project_dir", self.project_dir)

        self.project_name = input("Enter project name: ")
        self.project_language = input("Enter primary language: ")
        self.project_framework = input("Enter framework name: ")
        self.project_packages = input("Enter additional packages: ")
        self.package_manager = input("Enter prefered package manager: ")

        if not self.project_framework:
            self.project_framework = "default"
        if not self.package_manager:
            self.package_manager = "default"
        if not self.project_language:
            self.project_language = "default"

        self.generate_config()
        self.generate_template()

    def generate_config(self):
        self.project_config_dir = f"{self.project_dir}/{self.project_language}/{self.project_framework}/{self.project_name}"
        os.makedirs(self.project_config_dir)
        print("Generating project config")
        self.project_config = ConfigStream(self.project_config_dir)
        self.project_config.write_config("project_name", self.project_name)
        self.project_config.write_config("language", self.project_language)
        self.project_config.write_config("framework", self.project_framework)
        self.project_config.write_config("packages", self.project_packages)
        self.project_config.write_config("package_manager", self.package_manager)

    def generate_template(self):
        try:
            shutil.copytree(
                f"templates/{self.project_language}/{self.project_framework}",
                self.project_config_dir,
            )
            self.__create_file("README.md", f"# {self.project_name}")
            self.__create_file("LICENSE", "MIT")
            print("Project template generated")
            
        except Exception as e:
            print(e)

    def activate_virtualenv(self):
        pass

    def install_packages(self):
        pass

    def create_readme(self):
        pass

    def download_license(self):
        pass

    def git_push(self):
        pass

    def __create_file(self, filename, content):
        with open (f"{self.project_config_dir}/{filename}", "x") as file:
            file.write(content)


if __name__ == "__main__":
    project = ProjectManager()
    project.create()
