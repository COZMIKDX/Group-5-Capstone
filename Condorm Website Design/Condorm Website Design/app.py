from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URL'] = 'postgresql://postgres:Brad3nlive01@localhost/condorm'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URL'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(200))
    quantity = db.Column(db.Integer)

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

@app.route('/')
def mainpage():
    return render_template('main.html')

@app.route('/main')
def index():
    return render_template('main.html')
 
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/order')
def order():
    return render_template('order.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        product = request.form['products']
        quantity = request.form['quantity']
        if product == '' or quantity == '':
            return render_template('order.html', message = 'Please enter a valid product or quantity')
            
        data = Orders(product, quantity)
        db.session.add(data)
        db.session.commit()
        return render_template('submit.html')
    
@app.route('/resources')
def resources():
    return render_template('resources.html')

@app.route('/update')
def information():
    return render_template('update.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')
    
if __name__ == "__main__":
    app.run()