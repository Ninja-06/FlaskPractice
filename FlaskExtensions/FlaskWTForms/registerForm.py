from wsgiref.validate import validator
from flask_wtf import Form
from wtforms import validators, EmailField, SelectField, StringField, RadioField, IntegerField, SubmitField, StringField

class registerForm(Form):
    name = StringField ("Name of the participant", [validators.DataRequired("please enter your name")])
    email = EmailField("email Address", [validators.DataRequired("please enter your email address"), validators.email("please enter your email address")])
    gender = RadioField("Gender", choices = [('M', 'Male'), ('F', 'Female')])
    address = StringField("Address")
    age = IntegerField("age")
    language = SelectField("language", choices=['python', 'java', 'c++', 'c', 'golang'])
    register = SubmitField("register")

C:/Users/ZMO-WIN-RajlakshmiB-/OneDrive/Desktop/uploadedimages


