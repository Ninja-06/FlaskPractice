
from flask import Flask, render_template

myapp = Flask(__name__)


@myapp.route('/welcome/<user>')
def welcome(user):
    return render_template('welcome.html', user=user)


@myapp.route('/Participations/<int:ParticipationCount>')
def participation(ParticipationCount):
    return render_template('Participation.html', ParticipationCount=ParticipationCount)


@myapp.route('/ParticipationList')
def participationList():
    participationList = {"Problem A-2022": 85, "Problem B-2022": 90,
                         "Problem C-2022": 50, "Problem d-2022": 45}
    return render_template('ParticipationList.html', participationList=participationList)


if __name__ == '__main__':
    myapp.run(debug=True)
