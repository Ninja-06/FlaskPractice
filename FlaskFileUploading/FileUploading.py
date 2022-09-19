from flask import Flask, request
from werkzeug.utils import secure_filename
import os 
myapp = Flask(__name__)
myapp.config['MAX_CONTENT_PATH'] = 40000


@myapp.route('/index')
def fileUpload():
    return '''<h1>hello, please upload your illustration :)</h1> 
              <form action = 'http://127.0.0.1:5000/uploaded' method = 'POST' enctype = multipart/form-data>
              <p><input type = "file" name = "illustration" /></p>
              <p><button type = submit>upload</button></p>
              </form>'''


@myapp.route('/uploaded', methods = ['POST', 'GET'])
def uploaded():
    if request.method == 'POST':
        f = request.files['illustration']
        os.chdir('dir you want to store your photo')
        print(os.getcwd())
        f.save(secure_filename(f.filename))
    return '''your file is successfully uploaded. 
              thanks for participating!!!'''


if __name__ == '__main__':
    myapp.run(debug = True)