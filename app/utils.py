from cryptography.fernet import Fernet
import os

def getToken():
    key = bytes(os.getenv("KEY"), "utf-8")
    encrypted = bytes(os.getenv("SECRET_TELEGRAM"), "utf-8")
    return Fernet(key).decrypt(encrypted).decode()

import yaml
def loadConfig():
    configPath = 'secrets.yaml'
    if os.path.exists(configPath):
        with open(configPath) as file:
            data = yaml.safe_load(file)
        return data
    else:
        return {}

if __name__ == '__main__':
    pass