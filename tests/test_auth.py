import pytest
from flask import g
from flask import session

from trackpack.db import get_db

# Test basic functionality of registration
def test_register(client, app):
    # Test that page loads
    assert client.get("/auth/register").status_code == 200

    # Test that creating an account redirects to the login page
    response = client.post("/auth/register", data={"username": "a", "password": "a"})
    assert response.headers["Location"] == "/auth/login"

    # Test that user exists now that registration is complete
    with app.app_context():
        assert (
            get_db().execute("SELECT * FROM user WHERE username = 'a'").fetchone()
            is not None
        )

# Parametrize various invalid registration attempts
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (
        ("", "", b"Username is required."),
        ("a", "", b"Password is required."),
        ("test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, password, message):
    response = client.post(
        "/auth/register", data={"username": username, "password": password}
    )
    assert message in response.data

# Test legitimate login credentials
def test_login(client, auth):
    # Test that page loads
    assert client.get("/auth/login").status_code == 200

    # Test that it redirects to the home page after logging in
    response = auth.login()
    assert response.headers["Location"] == "/"

    # Test that user is in the global space
    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user["username"] == "test"

# Test invalid login attempts
@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Incorrect username."), ("test", "a", b"Incorrect password.")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data

# Test clearing of user from global space on logout
def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
