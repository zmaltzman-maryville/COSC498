import pytest

from trackpack.db import get_db

def test_home(app, client, auth):
    # Test pulling home page
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    # Try to log in
    auth.login()
    response = client.get('/')
    assert b"test" in response.data
    assert b"Vitamins" in response.data
    assert b"Batteries" in response.data

