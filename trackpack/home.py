from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from .db import get_db

bp = Blueprint("home", __name__)

@bp.route("/", methods = ['GET', 'POST'])
def home():
    if request.method == 'POST':
        # if request.form['name'] == 'add':
        print(request.form)
        for key, val in request.form.items():
            print(key, val)

    if g.user:
        packages = get_packages(g.user['id'])
        options = {
            'user_description': 'Description',
            'recipient': 'Recipient',
            'tracking_number': 'Tracking Number',
            'carrier': 'Carrier',
            'current_status': 'Current Status',
            'order_date': 'Order Date',
            'delivery_date': 'Delivery Date',
        }
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