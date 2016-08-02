#   Foremast - Pipeline Tooling
#
#   Copyright 2016 Gogo, LLC
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

"""Test utils."""

import pytest
from unittest import mock
from foremast.utils import *
from foremast.exceptions import *

@mock.patch('foremast.utils.banners.LOG')
def test_utils_banner(mock_log):
    banner('test', border='+', width=10)
    mock_log.info.assert_called_with('+' * 10)


def test_utils_deep_chain_map():

    first = {'key1': {
            'subkey1': 1,
        },
    }
    second = {'key1': {
            'subkey2': 2,
        },
     }

    result = {'key1': {
            'subkey1': 1,
            'subkey2': 2,
        }
     }

    assert DeepChainMap(first, second) == result
    with pytest.raises(KeyError):
        assert DeepChainMap(first, second)['key2'] == result


def test_utils_pipeline_check_managed():

    assert check_managed_pipeline('app [onetime]', 'app') == 'onetime'
    assert check_managed_pipeline('app [us-east-1]', 'app') == 'us-east-1'

    params = (
        # pipeline, app, result
        ['app', 'app', 'app'],  # no region
        ['app app [us-east-1]', 'app', 'us-east-1'],  # no app
        ['app [us-east-1]', 'example', 'us-east-1'],  # app / pipeline not matching
    )
    for param in params:
        with pytest.raises(ValueError):
            assert check_managed_pipeline(param[0], param[1]) == param[2]


def test_utils_generate_packer_filename():
    a = generate_packer_filename('aws', 'us-east-1', 'chroot')
    assert a == 'aws_us-east-1_chroot.json'


@mock.patch('requests.get')
def test_utils_find_elb(requests_get_mock):
    results = [
        {'account': 'dev', 'region': 'us-east-1', 'dnsname': 'appdns' }
    ]
    requests_get_mock.return_value.json.return_value = results
    a = find_elb('app', 'dev', 'us-east-1')
    assert a == 'appdns'

    with pytest.raises(SpinnakerElbNotFound):
        # we already filter by app, so sending incorrect env/region combo
        # will trigger the error
        find_elb('app', 'devbad', 'us-east-1')
