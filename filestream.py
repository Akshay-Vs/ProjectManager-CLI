import os
import sys

class Filestream:
    def __init__(self, path):
        self.path = path
        
    def createInputStream(self):
        pass

    def writeStream(self):
        return super().writeInput()
    
    def readarr(self) -> list:
        with open(self.path, 'r') as file:
            return file.read().replace('\n', '').split(',')

if __name__ == '__main__':
    fs = Filestream('frameworks.txt')
    print(fs.readarr())

