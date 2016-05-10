"""Retrieve Account Credential from Gate API."""
import logging

import murl
import requests

from ..consts import API_URL

LOG = logging.getLogger(__name__)


def get_env_credential(env='dev'):
    """Get Account Credential from Spinnaker for _env_.

    Args:
        env (str): Environment name to find credentials for.

    Returns:
        dict: Complete credentials for _env_.

            {
                'accountId': '123098123',
                'accountType': 'dev',
                'assumeRole': 'role/spinnakerManaged',
                'bastionEnabled': False,
                'challengeDestructiveActions': False,
                'cloudProvider': 'aws',
                'defaultKeyPair': 'dev_access',
                'discoveryEnabled': False,
                'eddaEnabled': False,
                'environment': 'dev',
                'front50Enabled': False,
                'name': 'dev',
                'primaryAccount': False,
                'provider': 'aws',
                'regions': [
                    {
                        'availabilityZones': ['us-east-1b', 'us-east-1c',
                                              'us-east-1d', 'us-east-1e'],
                        'deprecated': False,
                        'name': 'us-east-1',
                        'preferredZones':
                        ['us-east-1b', 'us-east-1c', 'us-east-1d', 'us-east-1e'
                         ]
                    }, {
                        'availabilityZones':
                        ['us-west-2a', 'us-west-2b', 'us-west-2c'],
                        'deprecated': False,
                        'name': 'us-west-2',
                        'preferredZones':
                        ['us-west-2a', 'us-west-2b', 'us-west-2c']
                    }
                ],
                'requiredGroupMembership': [],
                'sessionName': 'Spinnaker',
                'type': 'aws'
            }
    """
    url = murl.Url(API_URL)
    url.path = '/'.join(['credentials', env])
    credential_response = requests.get(url.url)

    assert credential_response.ok, 'Could not get credentials from Spinnaker.'

    credential = credential_response.json()
    LOG.debug('Credentials found:\n%s', credential)
    return credential