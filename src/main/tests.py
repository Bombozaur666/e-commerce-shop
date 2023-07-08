import pytest


def test_no_content(client):
    resp = client.get('/S')
    assert resp.status_code == 200
