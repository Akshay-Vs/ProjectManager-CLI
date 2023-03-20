import os
import shutil
import platform
import requests
import time
import logging
import subprocess
from pathlib import Path
from lib.configstream import ConfigStream
from lib.readme import generate_readme
from lib.utils import github_utils as github


class ProjectManager:
    def __init__(self):
        self.CONFIG_DIR = Path.home() / ".config" / "projectmanager"
        self.logging = logging.getLogger(__name__)
        self.logging.setLevel(logging.DEBUG)
        log_file = os.path.join(os.getcwd(), "logs/projectmanager.log")

        # Set up logging to file
        file_handler = logging.FileHandler(log_file, mode="w")
        file_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        self.logging.addHandler(file_handler)

        # Set up logging to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(levelname)-8s %(message)s")
        console.setFormatter(formatter)
        self.logging.addHandler(console)

    def create(self):
        self.logging.debug("Starting project creation process...")
        if os.path.exists(self.CONFIG_DIR):
            self.config = ConfigStream(self.CONFIG_DIR)
            self.project_dir = self.config.read_config("project_dir")
            self.username = self.config.read_config("username")
            self.token = self.config.read_config("token")
        else:
            self.project_dir = input("Enter project directory: ")
            self.username = input("Enter github username: ")
            self.token = input("Enter github token: ")
            self.config = ConfigStream(self.CONFIG_DIR)
            self.config.write_config("project_dir", self.project_dir)
            self.config.write_config("username", self.username)
            self.config.write_config("token", self.token)

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
        self.install_packages()
        self.add_license()
        self.create_github_repo()
        self.generate_readme()
        self.push_to_github()

    def generate_config(self):
        """
        Generates project config files
        """
        # project working directory
        self.project_config_dir = (
            Path(self.project_dir)
            / self.project_language
            / self.project_framework
            / self.project_name
        )
        os.makedirs(self.project_config_dir)
        self.logging.info("Generating project config...")
        self.project_config = ConfigStream(self.project_config_dir)
        self.project_config.write_config("project_name", self.project_name)
        self.project_config.write_config("language", self.project_language)
        self.project_config.write_config("framework", self.project_framework)
        self.project_config.write_config("packages", self.project_packages)
        self.project_config.write_config("package_manager", self.package_manager)

    def generate_template(self):
        """
        Generates project template
        """
        try:
            shutil.copytree(
                Path("templates") / self.project_language / self.project,
                self.project_config_dir,
            )
            self.__create_file("README.md", f"# {self.project_name}")
            self.__create_file("LICENSE", "MIT")
            self.logging.info("Project template generated")

        except Exception as e:
            self.logging.error(f"Error generating project template: {e}")

    def activate_virtualenv(self):
        """
        Activate the virtualenv for the project.
        """
        if platform.system() == "Windows":
            self.logging.info("System is Windows")
            os.system("cd {self.project_config_dir} && venv\\Scripts\\activate.bat")
        elif platform.system() == "Linux":
            self.logging.info("System is Linux")
            os.system(f"cd {self.project_config_dir} && source venv/bin/activate")
        elif platform.system() == "Darwin":
            self.logging.info("System is Mac")
            os.system(f"cd {self.project_config_dir} && source venv/bin/activate")

    def install_packages(self):
        """
        Install required packages for the project.
        """
        if self.project_language == "python" or self.package_manager == "pip":
            self.logging.info("Installing packages...")
            os.system(
                f"{self.package_manager} install {self.project_packages} -r requirements.txt"
            )
        elif (
            self.project_language == "javascript"
            or self.package_manager == "npm"
            or self.package_manager == "yarn"
        ):
            self.logging.info("Installing packages...")
            os.system(f"{self.package_manager} install {self.project_packages}")

        elif self.project_language == "rust" or self.package_manager == "cargo":
            self.logging.info("Installing packages...")
            os.system(f"{self.package_manager} install {self.project_packages}")
        elif self.project_language == "go":
            self.logging.info("Installing packages...")
            os.system(f"{self.package_manager} get {self.project_packages}")
        else:
            self.logging.info("No package manager not found")

    def add_license(self, license="mit"):
        """
        Add a license to the project.
        """
        license = requests.get(
            "https://api.github.com/licenses/{license}"
        ).json()  # download license from github api
        license = (
            license["body"]
            .replace("[year]", self.year)
            .replace("[fullname]", self.username)
        )
        self.__create_file("LICENSE", license)
        self.logging.info("License added")

    def create_github_repo(self):
        """
        Create a github repo and upload files to it.
        """
        github.create_repo(self.token, self.project_name)  # Create a github repo
        files = os.listdir(self.project_config_dir)
        for (
            file
        ) in files:  # iterate through files in project directory and upload to github
            github.upload_files(self.token, self.username, self.project_name, file)

    def push_to_github(self):
        """
        Push the project to github.
        """
        os.chdir(self.project_config_dir)
        subprocess.run(["git", "init"], cwd=os.getcwd())
        subprocess.run(["git", "add", "."], cwd=os.getcwd())
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=os.getcwd())
        subprocess.run(
            [
                "git",
                "remote",
                "add",
                "origin",
                f"https://github.com/{self.username}/{self.project_name}.git",
            ],
            cwd=os.getcwd(),
        )
        subprocess.run(["git", "push", "-u", "origin", "master"], cwd=os.getcwd())

    def create_readme(self):
        """
        Create a readme file for the project.
        """
        generate_readme(self.token, self.username, self.project_name)

    def __create_file(self, filename, content):
        with open(f"{self.project_config_dir}/{filename}", "x") as file:
            file.write(content)


if __name__ == "__main__":
    project = ProjectManager()
    project.create()
    # project.activate_virtualenv()
    # project.download_license()
