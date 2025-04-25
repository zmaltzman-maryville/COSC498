import pytest

from trackpack.db import get_db

# Get data for form posts
def get_payload():
    payload = {
        "user_description": "Box 4",
        "recipient": "B4Recipient",
        "tracking_number": "B4Tracking",
        "carrier": "B4Carrier",
        "current_status": "B4Current",
        "order_date": "B4Order",
        "delivery_date": "B4Delivery",
        "delivered": "1",
        }
    
    return payload

# Confirm that the landing page loads
def test_landing(client):
    response = client.get('/')
    assert b"Welcome to TrackPack!" in response.data

# Test that routes requiring login redirect when no user
@pytest.mark.parametrize("path", ("/add", "/edit/1", "/remove/1"))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"

# Make sure the home page loads
def test_home_page(client, auth):
    auth.login()
    response = client.get('/')
    # Check that the tracking numbers became links
    assert b"https://tools.usps.com/go/TrackConfirmAction" in response.data
    assert b"https://www.ups.com/track" in response.data
    assert b"https://www.fedex.com/fedextrack/?trknbr" in response.data

# Confirm new packages can be added
def test_add(client, auth):
    auth.login()
    response = client.get('/')
    # Confirm that Box 4 does not already exist
    assert b"Box 4" not in response.data

    # Now try to add Box 4
    payload = get_payload()
    response = client.post("/add", data = payload)
    # Should redirect home
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    response = client.get("/")

    # Confirm that the details from Box 4 exist
    del payload["delivered"]
    for value in payload.values():
        assert value.encode('utf-8') in response.data

# Test that packages can be updated
def test_edit(client, auth):
    auth.login()
    response = client.get("/")
    # Confirm Box 4 does not already exist
    assert b"Box 4" not in response.data

    # Attempt to replace Box 3's data with Box 4 payload
    payload = get_payload()
    response = client.post("/edit/3", data = payload)
    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    
    # See that the packages have changed
    response = client.get("/")
    assert b"Box 3" not in response.data
    assert b"Box 4" in response.data