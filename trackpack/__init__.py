import os
from flask import Flask

# Factory method to return app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # TODO write script to export key and launch app
        SECRET_KEY="dev",
        # Using SQLite DB for sake of project
        DATABASE=os.path.join(app.instance_path, "trackpack.sqlite"),
    )

    if test_config is None:
        # Attempt to load configs if they exist
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Loading passed in config to run in test mode
        app.config.update(test_config)

    # Confirm instance directory exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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
