from utils import loadConfig
import requests

configVars = loadConfig()

url = 'http://{}:{}/getPass'.format(configVars['LOCALHOST'], configVars['PORT'])
testApp = list(configVars['encryptionStore'])[0]
payload = {
    'app': testApp,
    'password': configVars['PASSWORD'],
    'key': configVars['encryptionStore'][testApp]['PASSWORD']
}

if 1:
    response = requests.post(url, json=payload)
    if response.ok:
        print(response.json())
    else:
        print(response.json())
        # print(response.content)
else:
    import yaml
    with open('secrets.yaml') as file:
        data = yaml.safe_load(file)
