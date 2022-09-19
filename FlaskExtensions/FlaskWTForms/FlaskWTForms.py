from flask import Flask, render_template, request
from registerForm import registerForm


myapp = Flask(__name__)

myapp.secret_key = 'development Key'

@myapp.route('/register', methods = ['POST', 'GET'])
def register():
    form = registerForm()
    if request.method == 'POST':
        print(form.validate())
        if form.validate() == False:
            print("hello error")
            return render_template('register.html', form = form)
        else:
            print("hello  no error")
            return render_template('success.html')
    else :
        return render_template('register.html', form = form)


if __name__ == '__main__':
    myapp.run(debug = True)