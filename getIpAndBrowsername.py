from flask import Flask, request

myapp = Flask(__name__)

@myapp.route('/getIpandUsername/')
def getIpandUsername():
    return "hello! your IP address is  {Ip} and you are using {user} ".format(Ip = request.remote_addr, user = request.user_agent)

if __name__ == '__main__':
    myapp.run(debug = True)