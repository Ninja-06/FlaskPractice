from flask import Flask, render_template, session,  redirect, url_for, request

myapp = Flask(__name__)
myapp.secret_key = 'R@ndomSctKey34'


@myapp.route('/commented/')
def commented():
    if 'comment' in session:
        if 'comment' is not None:
            comment = session['comment']
            msg = 'you commented as '+comment+'<p><a href = "http://127.0.0.1:5000/deleteSessionData">click on this to remove your comment stored in session</p></a>'
            return msg
    else:
        return '''you have not commented <p><a href = 'http://127.0.0.1:5000/WriteComment'>click on this to type your comment</p></a>'''


@myapp.route('/WriteComment/',  methods = ['POST', 'GET'])
def WriteComment():
    if request.method == 'POST':
        session['comment'] = request.form['comment']
        return redirect (url_for('commented'))

    return render_template('WriteComment.html')


@myapp.route('/deleteSessionData')
def deleteSessionData():
    # remove session data
    session.pop('comment', None)
    return redirect(url_for('Commented'))


if __name__ == '__main__':
    myapp.run(debug=True)
