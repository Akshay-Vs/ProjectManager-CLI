import os

def install(requirements, command):
    with open(requirements, 'r') as file:
        data_arr = file.read().split('\n')
        for i in data_arr:
            print(f"Installing {i}...")
            os.system(f"{command} {i}")

if __name__ == '__main__':
    install("requirements.txt", "npm install")
