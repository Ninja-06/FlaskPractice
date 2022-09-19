# redirecting using url_for

from distutils.log import debug
from flask import Flask, redirect, url_for

myapp = Flask(__name__)


@myapp.route('/Access/')
def Access():
    return "you can access customer details"



@myapp.route('/AccessDenied/<role>/')
def AccessDenied(role):
    return"oops! sorry your role is {role} , you cannot access the Customer Details it requires admin permissions".format(role = role)




@myapp.route('/Login/<role>/')
def verification(role):
       if role.lower() == "manager" or role.lower() == "dba":
             return redirect(url_for('Access'))
       else:
             return redirect(url_for('AccessDenied', role = role))



if __name__ == '__main__':
    myapp.run(debug = True)