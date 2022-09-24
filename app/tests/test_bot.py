# RUN
# - python -m pytest -p no:cacheprovider tests -sv
# - python -m pytest -p no:cacheprovider tests --ignore=tests/test_app.py
# - pytest .. (if __init__.py exists in tests dir)

from utils import loadSecrets
import requests
import pytest
from copy import deepcopy

@pytest.fixture
def payload():
    '''Returns valid payload for /postError'''
    configVars = loadSecrets()
    testApp = list(configVars['encryptionStore'])[0]
    return {
        'url': 'http://{}:{}/postError'.format(configVars['LOCALHOST'], configVars['PORT']),
        'payload': {
            'app': testApp,
            'password': configVars['PASSWORD'],
            'key': configVars['encryptionStore'][testApp]['PASSWORD'],
            'error': 'NOT_FOUND'
        }
    }

def test_app_postError_success(payload):
    assert requests.post(payload['url'], json=payload['payload']).json().get('status') == 'OK'