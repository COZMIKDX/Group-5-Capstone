from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField, SubmitField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from passlib.hash import pbkdf2_sha256

from app import User

def checker(form, field):
    username_entered = form.username.data
    password_entered = field.data

    user_object = User.query.filter_by(username = username_entered).first()
    if user_object is None:
        raise ValidationError("Username or password is incorrect")
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError("Username or password is incorrect")
    
class RegistrationForm(FlaskForm):
    username = StringField('username', 
                validators=[InputRequired(message = "Username required"),
                Length(min = 4, max = 20, message= "Username must be between 4 and 20 characters")])
    firstname = StringField('firstname', 
                validators=[InputRequired(message = "First Name required")])
    lastname = StringField('lastname', 
                validators=[InputRequired(message = "Last Name required")])
    email = StringField('email',
                validators=[InputRequired(message= "Email required"),
                Email(message = 'Invalid Email'),
                Length(max= 50)])
    password = PasswordField('password', 
                validators=[InputRequired(message = "Password required"),
                Length(min = 4, max = 20, message= "Password must be between 4 and 20 characters")])
    repass = PasswordField('repass', 
                validators=[InputRequired(message = "Password required"),
                EqualTo('password', message = "Passwords must match")])
    dormname = SelectField('dormname',
                choices = ['Founders', 'Futrall', 'Gibson','Gregson','Holcombe','Hotz','Humphreys','Pomfret','Reid','Yocum'])
    roomnum = IntegerField('roomnum',
                validators=[InputRequired(message = "Room Number required")])
    submitbtn = SubmitField('Create Account')

class LoginForm(FlaskForm):
    username = StringField('username', 
                validators=[InputRequired(message = "Username required")])
    password = PasswordField('password', 
                validators=[InputRequired(message = "Password required"),
                checker])
    submitbtn = SubmitField('Login')

class UpdateForm(FlaskForm):
    dormname = SelectField('dormname',
                choices = ['Founders', 'Futrall', 'Gibson','Gregson','Holcombe','Hotz','Humphreys','Pomfret','Reid','Yocum'])
    roomnum = IntegerField('roomnum',
                validators=[InputRequired(message = "Room Number required")])
    submitbtn = SubmitField('Update Information')
