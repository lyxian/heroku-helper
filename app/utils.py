from cryptography.fernet import Fernet
import os

def getToken():
    key = bytes(os.getenv("KEY"), "utf-8")
    encrypted = bytes(os.getenv("SECRET_TELEGRAM"), "utf-8")
    return Fernet(key).decrypt(encrypted).decode()

import yaml
def getCurrLoc(*args):
    if not args and os.path.exists('secrets.yaml'):
        with open('secrets.yaml', 'r') as file:
            yamlData = yaml.safe_load(file)
        return yamlData
    else:
        return {}

if __name__ == '__main__':
    pass