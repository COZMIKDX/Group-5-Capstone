from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from forms import *

app = Flask(__name__)
app.secret_key = 'meme'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Brad3nlive01@localhost/condorm'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fogscmxflbvfpn:cdc2900b405304e95b4cae360506a382899386eb3f54c4c2fc24c65734c49622@ec2-54-242-43-231.compute-1.amazonaws.com:5432/d2j0ha8pcp3qr8'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True, nullable = False)
    firstname = db.Column(db.String(), nullable = False)
    lastname = db.Column(db.String(), nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    dormname = db.Column(db.String(), nullable = False)
    roomnum = db.Column(db.Integer(), nullable = False)
    admin = db.Column(db.Boolean(), nullable = False)

    def __init__(self, username, firstname, lastname, email, password, dormname, roomnum, admin):
        self.username = username
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.dormname = dormname
        self.roomnum = roomnum
        self.admin = admin

class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key = True)

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

class Products(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key = True)
    product = db.Column(db.String(200))
    quantity = db.Column(db.Integer)

    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity



@app.route('/', methods = ['POST', 'GET'])
def mainpage():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        return redirect(url_for('index'))
    return render_template('login.html', form = login_form)


@app.route('/main')
def index():
    return render_template('main.html')
    
 
@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/order')
def order():
    return render_template('order.html', products = Products.query.all())

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

@app.route('/registration', methods = ['GET', 'POST'])
def registration():

    reg_form = RegistrationForm()

    if reg_form.validate_on_submit():
        username = reg_form.username.data
        firstname = reg_form.firstname.data
        lastname = reg_form.lastname.data
        email = reg_form.email.data
        password = reg_form.password.data
        dormname = reg_form.dormname.data
        roomnum = reg_form.roomnum.data
        admin = False

        user_object = User.query.filter_by(username= username).first()
        email_object = User.query.filter_by(email = email).first()

        if user_object:
            return render_template('registration.html', form = reg_form, message = "Someone has taken that username!")
        if email_object:
            return render_template('registration.html', form = reg_form, message = "Someone has taken that email!")
        user = User(username = username,firstname = firstname, lastname = lastname, email = email, password = password, dormname = dormname, roomnum = roomnum, admin = admin)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('mainpage'))
    return render_template('registration.html', form = reg_form)

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
    
