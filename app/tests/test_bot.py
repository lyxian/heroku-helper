# RUN
# - python -m pytest -p no:cacheprovider tests -sv
# - python -m pytest -p no:cacheprovider tests -svk 'not app' --print
# - python -m pytest -p no:cacheprovider tests -svk 'not getPass'
# - python -m pytest -p no:cacheprovider tests --ignore=tests/test_app.py
# - pytest .. (if __init__.py exists in tests dir)

from bot import TelebotHelper
from utils import loadSecrets
import requests
import pytest

class TelebotHelper_Test(TelebotHelper):
    def __init__(self):
        super().__init__()
        self.configVars['Telegram']['Admins'] = [0, 1]

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
            'error': '<u>TEST</u> - VALID PAYLOAD'
        }
    }

@pytest.fixture
def payload_fail():
    '''Returns invalid payload for /postError'''
    configVars = loadSecrets()
    testApp = list(configVars['encryptionStore'])[0]
    return {
        'appName': testApp,
        'timeStamp': 1664128466,
        'logs': '<u>TEST</u> - INVALID SEND MESSAGE'
    }

@pytest.fixture
def verbose():
    '''Returns default verbose setting'''
    return False

def test_app_postError_success(payload):
    assert requests.post(payload['url'], json=payload['payload']).json().get('status') == 'OK'

def test_bot_sendMessage_failure(payload_fail, verbose):
    responses = TelebotHelper_Test().sendMessage(**payload_fail)
    ERROR = []
    for key in responses:
        if not responses[key]['ok']:
            description = responses[key]['description']
            ERROR += [f'Failed to send error logs to \'{key}\' due to: {description}']
    if verbose:
        ERRORS = '\n'.join(ERROR)
        print(f'=====APP ERROR=====\n{ERRORS}\n=====ERROR END=====')
    assert len(ERROR) > 0