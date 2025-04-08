import sqlite3
from datetime import datetime

import click
from flask import current_app
from flask import g

# Return a Python dictionary instead of sqlite row object
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
        for idx, value in enumerate(row))

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        # g.db.row_factory = sqlite3.Row
        g.db.row_factory = make_dicts

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")

# Adds example packages to DB for testing
def add_sample_packages():
    db = get_db()
    samples = [
        (1, "Vitamins", None, "123456789", "UPS", "In Transit", "04/03/25", None, False),
        (1, "Batteries", "Me", "987654321", "FedEx", "Delivered", "04/01/25", "04/02/25", True)
    ]
    for sample in samples:
        db.execute(
            """INSERT INTO package 
            (user_id, user_description, recipient, 
            tracking_number, carrier, current_status, 
            order_date, delivery_date, delivered) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            sample
        )
    db.commit()

@click.command("add-samples")
def add_samples_command():
    add_sample_packages()
    click.echo("Samples added")

sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(add_samples_command)
