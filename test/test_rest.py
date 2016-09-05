"""
Copyright 2016 EMBL-European Bioinformatics Institute

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import pytest
import tempfile
import json

from context import app

@pytest.fixture
def client(request):
    db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
    app.app.config['TESTING'] = True
    client = app.app.test_client()
    
    def teardown():
        os.close(db_fd)
        os.unlink(app.app.config['DATABASE'])
    request.addfinalizer(teardown)

    return client

def test_assembly(client):
    rv = client.get('/rest/v0.0/getTADs')
    assert b'GCA' in rv.data

