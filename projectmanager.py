import os
import sys
from filestream import Filestream

class ProjectManager:    
    def __init__(self):
        self.project = None
        self.language= None
        self.framework = None
        self.packages = None
        self.initializer = None

    def get(self):
        self.project = input("Enter project name: ")
        self.framework = input("Enter framework name: ")
        self.packages = input("Enter additional packages: ")

    def framework_manager(self):
        fs = Filestream()
        self.available_framework = fs.readarr()

    def extracter(self):
        if self.project is None or self.framework is None:
            print("No project name or framework name specified")

        if self.framework in self.available_framework:
            map(f"pip install {self.packages}", self.packages).split(' ')

    def write(self):
        fs = Filestream()