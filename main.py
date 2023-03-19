import os
import shutil
import platform
import requests
import time
from lib.configstream import ConfigStream
from pathlib import Path


class ProjectManager:
    def __init__(self):
        self.CONFIG_DIR = Path.home() / ".config" / "projectmanager"

    def create(self):
        print(os.path.exists(os.path.join(self.CONFIG_DIR, ".config.ini")))
        if os.path.exists(self.CONFIG_DIR):
            self.config = ConfigStream(self.CONFIG_DIR)
            self.project_dir = self.config.read_config("project_dir")
            self.username = self.config.read_config("username")
        else:
            self.project_dir = input("Enter project directory: ")
            self.username = input("Enter github username: ")
            self.config = ConfigStream(self.CONFIG_DIR)
            self.config.write_config("project_dir", self.project_dir)
            self.config.write_config("username", self.username)

        self.project_name = input("Enter project name: ")
        self.project_language = input("Enter primary language: ")
        self.project_framework = input("Enter framework name: ")
        self.project_packages = input("Enter additional packages: ")
        self.package_manager = input("Enter prefered package manager: ")
        self.year = time.strftime("%Y")

        if not self.project_framework:
            self.project_framework = "default"
        if not self.package_manager:
            self.package_manager = "default"
        if not self.project_language:
            self.project_language = "default"

        if self.project_language == "python":
            self.package_manager = "pip"
            self.activate_virtualenv()

        self.generate_config()
        self.generate_template()
        self.add_license()

    def generate_config(self):
        self.project_config_dir = (
            Path(self.project_dir)
            / self.project_language
            / self.project_framework
            / self.project_name
        )
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
                Path("templates") / self.project_language / self.project,
                self.project_config_dir,
            )
            self.__create_file("README.md", f"# {self.project_name}")
            self.__create_file("LICENSE", "MIT")
            print("Project template generated")

        except Exception as e:
            print(e)

    def activate_virtualenv(self):
        if platform.system() == "Windows":
            print("System is Windows")
            os.system("cd {self.project_config_dir} && venv\\Scripts\\activate.bat")
        elif platform.system() == "Linux":
            print("System is Linux")
            os.system(f"cd {self.project_config_dir} && source venv/bin/activate")
        elif platform.system() == "Darwin":
            print("System is Mac")
            os.system(f"cd {self.project_config_dir} && source venv/bin/activate")

    def install_packages(self):
        pass

    def create_readme(self):
        pass

    def add_license(self):
        license = requests.get("https://api.github.com/licenses/mit").json()
        license = (
            license["body"]
            .replace("[year]", self.year)
            .replace("[fullname]", self.username)
        )
        self.__create_file("LICENSE", license)
        print("License added")

    def git_push(self):
        pass

    def __create_file(self, filename, content):
        with open(f"{self.project_config_dir}/{filename}", "x") as file:
            file.write(content)


if __name__ == "__main__":
    project = ProjectManager()
    project.create()
    # project.activate_virtualenv()
    # project.download_license()
