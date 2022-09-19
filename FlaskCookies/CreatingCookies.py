from flask import Flask, render_template, make_response, request

myapp = Flask(__name__)


@myapp.route('/survey')
def survey():
    return render_template('survey.html')


@myapp.route('/setCookie', methods=['POST', 'GET'])
def setCookies():
    if request.method == 'POST':
        data = dict()
        for key, value in request.form.items():
            data[key] = value
    print(type(data))
    res = make_response(render_template('response.html'))
    res.set_cookie("UserFeedback", value=str(data))
    return res


@myapp.route('/getCookie')
def getCookie():
    Feedback = request.cookies.get('UserFeedback')
    return Feedback


if __name__ == '__main__':
    myapp.run(debug=True)
