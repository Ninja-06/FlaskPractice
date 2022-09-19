from flask import Flask

myapp = Flask(__name__)

# passing values to variable user through url

@myapp.route('/Hii/<user>/')
def hiiUser(user):
    return "Hii {user}, Happy Coding :)".format(user = user)


#passing int values

@myapp.route('/Projects/<int:projectCount>/')
def projectcount(projectCount):
    return "Number of projects completed: {projectCount}".format(projectCount = projectCount)

if __name__ == '__main__':
    myapp.run(debug = True)