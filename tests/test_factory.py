from trackpack import create_app

# Confirms the factory can return an app
def test_config():
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing