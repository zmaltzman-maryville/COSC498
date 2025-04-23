import re
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

# Prepare URL to make tracking number a link
def get_tracking_page_url(number, carrier):
    # Remove non-alphanumeric characters from the tracking number
    sanitized = re.sub("\\W", "", number)
    carrier = carrier.upper()
    
    if carrier == "USPS":
        return f"https://tools.usps.com/go/TrackConfirmAction?tRef=fullpage&tLc=2&text28777=&tLabels={sanitized}%2C&tABt=false"
    elif carrier == "UPS":
        return f"https://www.ups.com/track?track=yes&trackNums={sanitized}"
    elif carrier == "FEDEX":
        return f"https://www.fedex.com/fedextrack/?trknbr={sanitized}" 
    else:
        return None

# Homepage for viewing packages a user has registered
@bp.route("/")
def home():
    # Retrieve packages based on cookie's user ID
    if g.user:
        packages = get_packages(g.user['id'])
        for package in packages:
            if package['tracking_number'] and package['carrier']:
                url = get_tracking_page_url(package['tracking_number'], package['carrier'])
                package['url'] = url
        options = get_package_options()
        return render_template("home/index.html", packages = packages, options = options)
    # User is not logged in. Load landing page instead
    else:
        return render_template("home/landing.html")

# Function for pulling package data from DB
def get_packages(user_id, package_id = None):
    db = get_db()
    # If package_id is passed in, check to see if a match exists
    if package_id:
        query = 'SELECT * FROM package WHERE user_id = ? AND id = ?'
        values = (str(user_id), package_id)
    # Otherwise, just return all packages for given user
    else:
        query = 'SELECT * FROM package WHERE user_id = ?'
        values = (str(user_id))

    packages = db.execute(
        query, values
        ).fetchall()
    
    if not packages:
        print("No packages found for user id:", user_id)
        return None
    else:
        return packages
    
# Shared between adding and editing    
def parse_package_form(form):
    # Dictionary to hold form info
    entries = {}

    # Iterate over form data
    for key, val in form.items():
        if val != '':
            entries[key] = val
        # Replace empty string with None for DB purposes
        else:
            entries[key] = None

    # Delivered is a checkbox; absent if unchecked
    if 'delivered' in form:
        entries['delivered'] = 1
    else:
        entries['delivered'] = 0

    return entries        

# Route and function to submit a new package
@bp.route("/add", methods = ['GET', 'POST'])
@login_required
def add_package():
    # POST means user sent package info from page
    if request.method == 'POST':
        entries = parse_package_form(request.form)

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

# Function and route to update an existing package
@bp.route("/edit/<package_id>", methods = ['GET', 'POST'])
@login_required
def edit_package(package_id):
    if request.method == 'POST':
        entries = parse_package_form(request.form)

        # Make list of user ID and form data
        values = list(entries.values()) + [g.user['id'], package_id]
        db = get_db()
        db.execute(
            """UPDATE package
            SET user_description = ?, 
            recipient = ?, 
            tracking_number = ?,
            carrier = ?,
            current_status = ?, 
            order_date = ?,
            delivery_date = ?,
            delivered = ?
            WHERE user_id = ?
            AND id = ?""",
            tuple(values)
        )
        db.commit()
        return redirect(url_for("home.home"))

    # See if there's a package with this ID for this user
    results = get_packages(g.user['id'], package_id)
    if results == None:
        flash("You don't have a package with that ID.")
        return redirect(url_for("home.home"))
    else:
        return render_template("home/edit.html", package = results[0])

# Function and route to delete entries    
@bp.route("/remove/<int:package_id>", methods = ['POST'])
@login_required
def remove_package(package_id):
    # Ensure package_id exists and is an integer
    if not package_id or type(package_id) != int:
        flash("An invalid package ID was received.")
        return redirect(url_for('home.home'))
    
    # Only able to delete entries associated with cookie
    db = get_db()
    db.execute(
        """ DELETE FROM package
        WHERE id = ?
        AND user_id = ?
        """,
        (package_id, g.user['id'])
    )
    db.commit()

    return redirect(url_for('home.home'))