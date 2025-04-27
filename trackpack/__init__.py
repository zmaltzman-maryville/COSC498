import os
from flask import Flask
import secrets

# Factory method to return app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # Using SQLite DB for sake of project
        DATABASE=os.path.join(app.instance_path, "trackpack.sqlite"),
    )

    # Confirm instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # If a config file does not exist, we will create one.
    if not os.path.exists(app.instance_path + "\\config.py"):
        # Secret key for the cookie being generated
        secret_key = secrets.token_hex()
        with open(app.instance_path + "\\config.py", 'w') as config_file:
            config_file.write(f"SECRET_KEY = '{secret_key}'")
    else:
        pass

    # Load appropriate config file
    if test_config is None:
        # Loading standard active config
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Loading passed in config to run in test mode
        app.config.update(test_config)

    # Register CLI options from DB
    from . import db
    db.init_app(app)

    # Load blueprints for routes
    from . import auth
    from . import home
    app.register_blueprint(auth.bp)
    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="home")

    return app
