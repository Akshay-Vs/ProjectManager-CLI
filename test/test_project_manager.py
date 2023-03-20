import unittest
import os
import shutil
import sys
import logging
from unittest.mock import patch, Mock

sys.path.append("..")
# sys.path.append("/home/akshay/Myspace/Projects/Python/ProjectManager-CLI/lib/utils/")

from main import ProjectManager

class TestProjectManager(unittest.TestCase):
    def setUp(self):
        # Configure logger
        self.logging = logging.getLogger(__name__)
        self.logging.setLevel(logging.DEBUG)
        log_file = os.path.join(os.getcwd(), "logs/test_project_manager.log")

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

    @patch('builtins.input', side_effect=['/home/user/projects', os.getenv("TEST_USERNAME"), os.getenv("GITHUB_TEST_TOKEN"), 'test_project', 'python', 'django', 'django-bootstrap4', '', 'pip'])
    def test_create(self, mock_input):
        pm = ProjectManager()
        pm.create()

        # Check if project directory has been created
        self.assertTrue(os.path.exists('/home/user/projects/python/django/test_project'))
        self.logging.info('Project directory created.')

        # Check if project config file has been generated
        self.assertTrue(os.path.exists('/home/user/projects/python/django/test_project/config.ini'))
        self.logging.info('Project config file generated.')

        # Check if required files have been generated
        self.assertTrue(os.path.exists('/home/user/projects/python/django/test_project/README.md'))
        self.assertTrue(os.path.exists('/home/user/projects/python/django/test_project/LICENSE'))
        self.assertTrue(os.path.exists('/home/user/projects/python/django/test_project/requirements.txt'))
        self.logging.info('Required files generated.')

        # Clean up
        shutil.rmtree('/home/user/projects/python')
        self.logging.info('Project directory removed.')

if __name__ == '__main__':
    unittest.main()
