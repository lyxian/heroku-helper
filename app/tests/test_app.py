# RUN
# - python -m pytest -p no:cacheprovider tests -sv
# - pytest .. (if __init__.py exists in tests dir)

from utils import loadConfig
import requests
import pytest
from copy import deepcopy

@pytest.fixture
def payload():
    '''Returns valid payload for /getPass'''
    configVars = loadConfig()
    testApp = list(configVars['encryptionStore'])[0]
    return {
        'url': 'http://{}:{}/getPass'.format(configVars['LOCALHOST'], configVars['PORT']),
        'payload': {
            'app': testApp,
            'password': configVars['PASSWORD'],
            'key': configVars['encryptionStore'][testApp]['PASSWORD']
        }
    }

@pytest.fixture
def verbose():
    return False

def test_app_getPass_success(payload, verbose):
    if verbose:
        print(f'\nProper: {payload}')
    assert requests.post(payload['url'], json=payload['payload']).json().get('status') == 'OK'

def test_app_getPass_failure(payload, verbose):

    # App not found
    tmp = deepcopy(payload)
    tmp['payload']['app'] = 'NO'
    response = requests.post(tmp['url'], json=tmp['payload']).json()
    if verbose:
        print(f'\nApp not found: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'App not found in list!'
    
    # Missing parameters
    tmp = deepcopy(payload)
    tmp['payload'].pop('app')
    response = requests.post(tmp['url'], json=tmp['payload']).json()
    if verbose:
        print(f'Missing parameters: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'Wrong password and parameters!'
    tmp = deepcopy(payload)
    tmp['payload'].pop('password')
    response = requests.post(tmp['url'], json=tmp['payload']).json()
    if verbose:
        print(f'Missing parameters: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'Wrong password and parameters!'
    tmp = deepcopy(payload)
    tmp['payload'].pop('key')
    response = requests.post(tmp['url'], json=tmp['payload']).json()
    if verbose:
        print(f'Missing parameters: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'Wrong password and parameters!'
    
    # Wrong password
    tmp = deepcopy(payload)
    tmp['payload']['key'] = 1234
    response = requests.post(tmp['url'], json=tmp['payload']).json()
    if verbose:
        print(f'Wrong password: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'Wrong password and parameters!'
    
    # Wrong method
    response = requests.get(payload['url']).json()
    if verbose:
        print(f'Wrong method: {payload}')
    assert response.get('status') == 'NOT_OK' and response.get('ERROR') == 'Nothing here!'