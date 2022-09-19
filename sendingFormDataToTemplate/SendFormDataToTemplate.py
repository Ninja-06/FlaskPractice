from flask import Flask, render_template, url_for, request

myapp = Flask(__name__)

@myapp.route('/studentDetails')
def studentDetails():
    return render_template('studentDetails.html')


@myapp.route('/results', methods = ['POST', 'GET'])
def results():
    if request.method == "POST":
        result = request.form
        return render_template('result.html', result = result)


if __name__ == '__main__':
    myapp.run(debug = True)