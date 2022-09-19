from flask import Flask

app = Flask(__name__)

def whichFunction():
    return "In this for add_url_rule() is use dto bind function to url"

app.add_url_rule('/add_url_rule', 'add_url_rule', whichFunction )

if __name__ == '__main__':
    app.run(debug = True)
      