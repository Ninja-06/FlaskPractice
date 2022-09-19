from flask import Flask, render_template, request, flash, get_flashed_messages, redirect, url_for

myapp = Flask(__name__)
myapp.secret_key = 'randomKey'
@myapp.route('/')
def welcome():
    return render_template('welcome.html')

@myapp.route('/Feedback/', methods = ['POST', 'GET'])
def Feedback():
    error = None
    print("h")
    if request.method == 'POST':
        print("post")
        if  request.form.get('Ratings') != "" :
              flash("Thanks for your feedback")
              print(request.form.get('Ratings'))
              return redirect(url_for('welcome'))
    
        else:
                error = "Please give your feedback"
                print(error)
                return render_template('Feedback.html', error = error)
    return render_template('Feedback.html', error = error)

if __name__ == '__main__':
    myapp.run(debug = True)