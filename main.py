import os
import sys
from lib.configstream import Filestream
from utils import utilsmanager

class ProjectManager(utilsmanager.utils):   
    def __init__(self):
        self.project = None
        self.language= None
        self.framework = None
        self.packages = None
        self.package_manager = None

    def create(self):
        self.project = input("Enter project name: ")
        self.language = input("Enter primary language: ")
        self.framework = input("Enter framework name: ")
        self.packages = input("Enter additional packages: ")
        self.package_manager = input("Enter prefered package manager: ")
        self.createProject()

    def createProject(self):
        if self.language == 'python':
            self.createPythonProject()
        elif self.language == 'javascript':
            self.createJavascriptProject()
        elif self.language == 'java':
            self.createJavaProject()
        elif self.language == 'c++':
            self.createCppProject()
        else:
            print("Language not supported")

    def createPythonProject(self):
        self.package_manager = 'pip'
        self.createProjectDirectory()
        # self.createProjectFiles()
        # self.createProjectStructure()
        # self.createProjectEnvironment()
        # self.createProjectDependencies()
        # self.createProjectReadme()
        # self.createProjectGitignore()
        # self.createProjectLicense()
        # self.createProjectContributing()
        # self.createProjectChangelog()
        # self.createProjectCodeOfConduct()
        # self.createProjectSecurity()
        # self.createProjectSupport()
        # self.createProjectCodeowners()
        # self.createProjectIssueTemplate()
        # self.createProjectPullRequestTemplate()
        # self.createProjectGithubActions()
        
    

    