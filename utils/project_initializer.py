# this file should contains create project structure ,environmenn, dependencies, readme, gitignore, license, contributing, changelog, code of conduct, security, support, codeowners, issue template, pull request template, github actions
import os
import logging
from lib.configstream import ConfigStream


class Initialize():
    def __init__(self,project_dir, project_name):
        self.project_dir = project_dir
        self.project_name = project_name
        self.config = ConfigStream(project_dir)
        logging.basicConfig(filename="utils.log", level=logging.DEBUG)

    def createProjectDirectory(self):
        self.config.write_config("project_dir",self.project_dir)
        self.config.write_config("project_name",self.project_name)
        if os.path.exists(self.project_dir):
            logging.info("Project directory exists")
            os.mkdir(f"{self.project_dir}/{self.project_name}")
    
