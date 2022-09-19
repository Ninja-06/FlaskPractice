from flask import Flask, render_template, url_for

myapp = Flask(__name__)

@myapp.route('/DoraemonBlog')
def blogPost():
    return render_template('Blog.html')

if __name__ == '__main__':
    myapp.run(debug = True)