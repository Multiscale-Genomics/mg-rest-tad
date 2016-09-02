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

