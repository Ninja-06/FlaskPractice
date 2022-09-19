from flask import Flask

# takes name of current module as argument

app = Flask(__name__)

# route() is a decorator which tells application which url should call the below function

@app.route('/welcome')
def welcome():
    return "Hello this is my first flask application"

if __name__ == '__main__':
   app.run(debug=True)