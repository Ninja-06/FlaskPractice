# flask http methods
from flask import Flask, redirect, request, url_for

myapp = Flask(__name__)


@myapp.route('/Successful/<request_method>')
def successful ( request_method):
    return "blogPost was succesfully Created using {request_method} method".format(request_method = request_method)



@myapp.route('/CreateBlog/', methods = ['POST', 'GET'])
def create ():
    if request.method == 'GET':
        return redirect(url_for('successful',  request_method = request.method ))
    else:
        return redirect(url_for('successful', request_method = request.method ))


if __name__ == '__main__':
    myapp.run(debug = True)