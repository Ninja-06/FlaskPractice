from pickle import TRUE
from flask import Flask, make_response

myapp = Flask(__name__)


@myapp.route('/getData')
def getdata():
    infoDict = {"Name":"Piya", "age": "23", "Cart":["black jacket", "Watch"], "Address":"Goa"}
    res = make_response(infoDict, 200) 
    return res
if __name__ == '__main__':
    myapp.run(debug = True)