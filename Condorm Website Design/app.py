from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Brad3nlive01@localhost/condorm'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fogscmxflbvfpn:cdc2900b405304e95b4cae360506a382899386eb3f54c4c2fc24c65734c49622@ec2-54-242-43-231.compute-1.amazonaws.com:5432/d2j0ha8pcp3qr8'

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
    return render_template('login.html')

@app.route('/main', methods= ['POST', 'GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'bldresse' and password == 'password123':
            return render_template('main.html')
    if request.method == 'GET':
        return render_template('main.html')
    return render_template('login.html', message = 'Invalid username or password')
    
 
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

@app.route('/created', methods = ['POST'])
def created():
    if request.method == 'POST':
        user = request.form['username']
        passw = request.form['password']
        repass = request.form['repass']
        dormname = request.form['dormname']
        roomnum = request.form['roomnum']
        if user == '' or passw == '' or dormname == '' or roomnum == '':
            return render_template('registration.html', message = 'Missing required information!')
        if repass != passw:
            return render_template('registration.html', message = "Password's do not match up. Try Again!")
        else:
            return render_template('created.html')
    
if __name__ == "__main__":
    app.run()