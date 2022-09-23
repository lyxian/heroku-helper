from cryptography.fernet import Fernet
import yaml
import os

def getToken():
    key = bytes(os.getenv('KEY'), 'utf-8')
    encrypted = bytes(os.getenv('SECRET_TELEGRAM'), 'utf-8')
    return Fernet(key).decrypt(encrypted).decode()

def encryptSecrets(silent=True):
    key = bytes(os.getenv('KEY'), 'utf-8')
    configPath = 'secrets.yaml'
    if os.path.exists(configPath):
        with open(configPath) as file:
            data = file.read().encode()
        encrypted = Fernet(key).encrypt(data).decode()
        os.environ['SECRET_YAML'] = encrypted
        if not silent:
            return f'SECRET_YAML={encrypted}'
        return
    else:
        raise Exception('No secrets.yaml found ..')

def loadSecrets():
    if not os.getenv('SECRET_YAML'):
        encryptSecrets()
    key = bytes(os.getenv('KEY'), 'utf-8')
    encrypted = bytes(os.getenv('SECRET_YAML'), 'utf-8')
    return yaml.safe_load(Fernet(key).decrypt(encrypted).decode())

if __name__ == '__main__':
    print(encryptSecrets(silent=False))
    # print(loadSecrets())