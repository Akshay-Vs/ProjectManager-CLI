# this file should contains create project structure ,environmenn, dependencies, readme, gitignore, license, contributing, changelog, code of conduct, security, support, codeowners, issue template, pull request template, github actions

class utils:
    def __init__(self): pass

    def createProjectDirectory(self):
        os.makedirs(self.project)
        os.chdir(self.project)