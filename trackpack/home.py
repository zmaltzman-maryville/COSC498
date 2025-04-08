from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from .db import get_db
from .auth import login_required

bp = Blueprint("home", __name__)

# Package options are reused across functions
def get_package_options():
    options = {
            'user_description': 'Description',
            'recipient': 'Recipient',
            'tracking_number': 'Tracking Number',
            'carrier': 'Carrier',
            'current_status': 'Current Status',
            'order_date': 'Order Date',
            'delivery_date': 'Delivery Date',
        }
    
    return options

@bp.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        print(request.form)
        if 'remove' in request.form.keys():
            package_id = int(request.form["remove"])
            print("Package ID:", package_id)
            db = get_db()
            db.execute(
                """ DELETE FROM package
                WHERE id = ?
                AND user_id = ?
                """,
                (package_id, g.user['id'])
            )
            db.commit()

    # Retrieve packages based on cookie's user ID
    if g.user:
        packages = get_packages(g.user['id'])
        options = get_package_options()
        return render_template("home/index.html", packages = packages, options = options)
    else:
        return render_template("home/index.html")

def get_packages(user_id):
    db = get_db()
    packages = db.execute(
        'SELECT * FROM package WHERE user_id = ?', str(user_id)
        ).fetchall()
    
    if not packages:
        print("No packages found for user id:", user_id)
        return None
    else:
        # print(packages)
        return packages
    
@bp.route("/add", methods = ['GET', 'POST'])
@login_required
def add_package():
    # POST means user sent package info from page
    if request.method == 'POST':
        # Dictionary to hold form info
        entries = {}

        # Iterate over form data
        for key, val in request.form.items():
            if val != '':
                entries[key] = val
            # Replace empty string with None for DB purposes
            else:
                entries[key] = None

        # Delivered is a checkbox; absent if unchecked
        if 'delivered' in request.form:
            entries['delivered'] = 1
        else:
            entries['delivered'] = 0

        # Make list of user ID and form data
        values = [g.user['id']] + list(entries.values())

        # Insert into database
        db = get_db()
        db.execute(
            """INSERT INTO package 
            (user_id, user_description, recipient, 
            tracking_number, carrier, current_status, 
            order_date, delivery_date, delivered) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            tuple(values)
        )
        db.commit()

        return redirect(url_for("home.home"))
    
    return render_template("home/add.html")