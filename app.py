import os
from datetime import datetime

from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


app = Flask(__name__, static_folder='static')
csrf = CSRFProtect(app)

# WEBSITE_HOSTNAME exists only in production environment
if 'WEBSITE_HOSTNAME' not in os.environ:
    # local development, where we'll use environment variables
    print("Loading config.development and environment variables from .env file.")
    app.config.from_object('azureproject.development')
else:
    # production
    print("Loading config.production.")
    app.config.from_object('azureproject.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

# Initialize the database connection
db = SQLAlchemy(app)

# Enable Flask-Migrate commands "flask db init/migrate/upgrade" to work
migrate = Migrate(app, db)

# The import must be done after db initialization due to circular import issue
from models import SaleOrder, SaleOrderItem

@app.route('/', methods=['GET'])
def index():
    print('Request for index page received')
    saleorders = SaleOrder.query.all()
    return render_template('index.html', saleorders=saleorders)

@app.route('/<int:id>', methods=['GET'])
def details(id):
    saleorder = SaleOrder.query.where(SaleOrder.id == id).first()
    saleorderitems = SaleOrderItem.query.where(SaleOrderItem.saleorder == id)
    return render_template('details.html', saleorder=saleorder, saleorderitems=saleorderitems)

@app.route('/create', methods=['GET'])
def create_saleorder():
    print('Request for add saleorder page received')
    return render_template('create_saleorder.html')

@app.route('/add', methods=['POST'])
@csrf.exempt
def add_saleorder():
    try:
        order_number = request.values.get('order_number')
        customer = request.values.get('customer')
        order_date = request.values.get('order_date')
        total_amount = request.values.get('total_amount')
    except (KeyError):
        # Redisplay the question voting form.
        return render_template('add_saleorder.html', {
            'error_message': "You must include a saleorder order_number, customer, order_date and total_amount",
        })
    else:
        saleorder = SaleOrder()
        saleorder.order_number = order_number
        saleorder.customer = customer
        saleorder.order_date = order_date
        saleorder.total_amount = total_amount
        db.session.add(saleorder)
        db.session.commit()

        return redirect(url_for('details', id=saleorder.id))

@app.route('/saleorderitem/<int:id>', methods=['POST'])
@csrf.exempt
def add_saleorderitem(id):
    try:
        product = request.values.get('product')
        quantity = request.values.get('quantity')
        item_description = request.values.get('item_description')
        subtotal = request.values.get('subtotal')
    except (KeyError):
        #Redisplay the question voting form.
        return render_template('add_saleorderitem.html', {
            'error_message': "Error adding saleorder item",
        })
    else:
        saleorderitem = SaleOrderItem()
        saleorderitem.saleorder = id
        saleorderitem.creation_date = datetime.now()
        saleorderitem.product = product
        saleorderitem.quantity = int(quantity)
        saleorderitem.item_description = item_description
        saleorderitem.subtotal = float(subtotal)
        db.session.add(saleorderitem)
        db.session.commit()

    return redirect(url_for('details', id=id))

@app.context_processor
def utility_processor():
    def star_rating(id):
        saleorderitems = SaleOrderItem.query.where(SaleOrderItem.saleorder == id)

        quantities = []
        salorderitem_count = 0
        for item in saleorderitems:
            quantities += [item.quantity]
            salorderitem_count += 1

        avg_quantity = sum(quantities) / len(quantities) if quantities else 0
        stars_percent = round((avg_quantity / 5.0) * 100) if salorderitem_count > 0 else 0
        return {'avg_quantity': avg_quantity, 'saleorderitem_count': salorderitem_count, 'stars_percent': stars_percent}

    return dict(star_rating=star_rating)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()
