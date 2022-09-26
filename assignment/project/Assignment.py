import base64
from flask import Flask, request, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
import mysql.connector
import os
from PIL import Image


myapp = Flask(__name__)

myapp.secret_key = 'secret_key45'

def db_obj():

    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='user'
    )
    return db

@myapp.route('/')
def root():
    return b"no entries so far"

@myapp.route('/registeruser/', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        print("hello")

        if request.form['Username'] != "" and request.form['Upassword'] != "":
            
            Username = request.form['Username']
            Upassword = request.form['Upassword']
            session['Username'] = Username 
            session['Upassword'] = Upassword  
            db = db_obj()
            cursor = db.cursor()
            cursor.execute("INSERT INTO user.users(UId, Username, Upassword) VALUES(DEFAULT, %s, sha(%s))", (
                    Username, Upassword))
            db.commit()
            db.close()
            return render_template('uploadphoto.html')


        else:
            return "enter username and password both to register"

    return render_template('register.html')


@myapp.route('/uploadphoto/', methods = ['POST','GET'])
def uploadphoto():
    if request.method == 'POST' and session != {}:
            Username = session['Username']
            Upassword = session['Upassword']
            Uphoto = request.files['Uphoto']
            os.chdir("C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/user")

            Uphoto.save(secure_filename('user.jpg'))

            if os.path.getsize("C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/user/user.jpg") > 0:
                    db = db_obj()
                    cursor = db.cursor(buffered=True)
                    cursor.execute("SELECT user.users.UId FROM user.users WHERE users.Username = %s AND users.Upassword = sha(%s)",(Username, Upassword))
                    UId = cursor.fetchone()
                    cursor.execute("INSERT INTO user.userphoto (UId, Uphoto) VALUES(%s, LOAD_FILE(%s))", (str(UId[0]), "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/user/user.jpg"))
                    print(cursor)
                    db.commit()
                    db.close()
                    return redirect(url_for('addaddress'))
            else:
                "please upload your image once again"

    else:
        return render_template('uploadphoto.html')




@myapp.route('/addaddress/', methods = ['POST', 'GET'])
def addaddress():
    if request.method == 'POST':
        if session != {}:
            Username = session['Username']
            Upassword = session['Upassword']
            country = request.form['country']
            state = request.form['state']
            pincode = request.form['pincode']
            db = db_obj()
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "SELECT user.users.UId FROM user.users WHERE users.Username = %s AND users.Upassword = sha(%s)", (Username, Upassword))
            UId = cursor.fetchone()
            cursor.execute(
                    "INSERT INTO user.useraddress(country, state, pincode, UId) VALUES(%s, %s, %s, %s)", (country, state, str(pincode), str(UId[0])))
            print('outside')
            db.commit()
            db.close()
            session.pop('Username', None)
            session.pop('Upassword', None)
            return render_template('login.html')
        else:
            return "do registration here <a href = 'http://localhost:5000/registeruser'>registeruser</a> first "
    
    else:
        return render_template('addaddress.html')

           
         


@myapp.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        Username = request.form['Username']
        Upassword = request.form['Upassword']
        try:
            db = db_obj()
            cursor = db.cursor(buffered=True)
            cursor.execute(
                "SELECT users.UId, userphoto.Uphoto FROM user.users INNER JOIN  user.userphoto ON user.users.UId = user.userphoto.UId WHERE users.Username = %s AND users.Upassword = sha(%s)", (
                    Username, Upassword)
            )
            data = cursor.fetchone()
            if data == None:
                cursor.execute("SELECT users.UId FROM user.users WHERE users.Username = %s and users.Upassword =sha(%s)",(Username, Upassword) )
                data = cursor.fetchone()                   
            else:
                data = list(data)
                data[1] = base64.b64encode(data[1])
                data[1] = data[1].decode('UTF-8')
            
            db.commit()
            db.close()
            session['Username'] = Username
            session['Upassword'] = Upassword
            return render_template('loginrender.html',data = data, Username = Username)
        except mysql.connector.errors as err:
            return "error occurred please try again <a href = 'http://127.0.0.1:5000/login'>retry</a>"

    else:
        return render_template('login.html')


@myapp.route('/comment/', methods=['POST', 'GET'])
def comment():
    if request.method == 'POST':
        if request.form['comment'] != "" and session != {}:
            Username = session['Username']
            Upassword = session['Upassword']
            comment = request.form['comment']
            print(Username, Upassword, comment)
            try:
                db = db_obj()
                cursor = db.cursor( buffered=True)
                cursor.execute(
                    "SELECT UId FROM user.users WHERE users.Username = %s AND users.Upassword = sha(%s)", (Username, Upassword))
                UId = cursor.fetchone()
                cursor.execute(
                    "INSERT INTO user.usercomment(comment, UId) VALUES(%s, %s)", (comment, str(UId[0])))
                db.commit()
                db.close()
                return "thanks for your comment"

            except mysql.connector.errors as err:
                return "error occured please comment again <a href = \"http://127.0.0.1:5000/comment/\" >comment</a>"

        else:
            return "you will not be able to comment as you are not logged in <a href = 'http://127.0.0.1:5000/login'>login</a>"
    else:
        return render_template('comment.html')


@myapp.route('/logout/')
def logout():
    session.pop('Username', None)
    session.pop('Upassword', None)
    return redirect(url_for('login'))


@myapp.route('/update/', methods=['POST', 'GET'])
def update():
    db = db_obj()
    cursor = db.cursor(buffered=True)
    Username = session['Username']
    Upassword = session['Upassword']
    print(Username, Upassword)
    cursor.execute("SELECT Users.Username , useraddress.country, useraddress.state, useraddress.pincode FROM (user.Users INNER JOIN User.Useraddress ON user.Users.UId = user.useraddress.UId) WHERE user.users.Username = %s and users.Upassword = sha(%s)", (Username, Upassword))
    userData = cursor.fetchall()
    db.commit()

    if request.method == 'POST' and session != {}:
        Username = request.form['Username']
        country = request.form['country']
        state = request.form['state']
        pincode = request.form['pincode']
        print(Username, country, state, pincode)
        cursor.execute(
            "SELECT UId FROM user.users WHERE users.Username = %s AND users.Upassword = sha(%s)", (Username, Upassword))
        UId = cursor.fetchone()
        UId = str(UId[0])
        cursor.execute("UPDATE user.Users INNER JOIN User.Useraddress ON user.Users.UId = user.useraddress.UId  SET  users.Username = %s, useraddress.country = %s, useraddress.state = %s, useraddress.pincode = %s WHERE user.users.UId = %s", (Username, country, state, str(pincode), UId))
        db.commit()
        db.close()
        return "updation successful"

    return "update the fields you want to update <br><form action = 'http://localhost:5000/update'  method = 'POST'>  <p><label>Username</label> <input type = text name = Username  value = "+userData[0][0]+" /></p>   <label>Country</label><input type = text name = country value = "+userData[0][1]+" /></p>  <label>State</label><input type = text name = state value = "+userData[0][2]+" /></p> <label>Pincode</label><input type = text name = pincode value = "+str(userData[0][3])+" /></p><p><button type = submit>update profile</button></p></form>"


@myapp.route('/deleteuser/')
def delete():
    if session != {}:
        Username = session['Username']
        Upassword = session['Upassword']

        try:
            db = db_obj()
            cursor = db.cursor(buffered=True)
            cursor.execute("SELECT users.UId FROM user.users WHERE user.users.Username = %s and user.users.Upassword = sha(%s)",(Username, Upassword))
            UId = cursor.fetchone()
            cursor.execute("DELETE FROM User.users WHERE user.Users.UId = %s", (str(UId[0]),))
            db.commit()
            db.close()
            return "deleted user"
        
        except mysql.connector.errors as err:
            return "error occured during deletion if you have not delete address and comment try to delete that first"
    else :
        return "login to delete account"



@myapp.route('/deleteaddress/')
def deleteaddress():
    if session != {}:
        Username = session['Username']
        Upassword = session['Upassword']
        db = db_obj()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT users.UId FROM user.users WHERE user.users.Username = %s and user.users.Upassword = sha(%s)",(Username, Upassword))
        UId = cursor.fetchone()
        cursor.execute("DELETE FROM user.useraddress WHERE useraddress.UId = %s", (str(UId[0]),))
        db.commit()
        db.close()
        return"user address was deleted successfully"
    else:
        return "login to delete your address"

@myapp.route('/deletephoto/')
def deletephoto():
    if session != {}:
        Username = session['Username']
        Upassword = session['Upassword']
        db = db_obj()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT users.UId FROM user.users WHERE user.users.Username = %s and user.users.Upassword = sha(%s)",(Username, Upassword))
        UId = cursor.fetchone()
        print(UId)
        cursor.execute("DELETE FROM user.userphoto WHERE userphoto.UId = %s", (str(UId[0]),))
        db.commit()
        db.close()
        return "your photo was deleted successfully"
    else:
        return "login to delete your photo"

@myapp.route('/deletecomments/')
def deletecomments():
    if session != {}:
        Username = session['Username']
        Upassword = session['Upassword']
        db = db_obj()
        cursor = db.cursor(buffered=True)
        cursor.execute("SELECT users.UId FROM user.users WHERE user.users.Username = %s and user.users.Upassword = sha(%s)",(Username, Upassword))
        UId = cursor.fetchone()
        cursor.execute("DELETE FROM user.usercomment WHERE usercomment.UId = %s", (str(UId[0]),))
        db.commit()
        db.close()
        return "all of comments are deleted succesfully"
    else:
        return "login to delete your comments"

@myapp.route('/Listuseraddress/')
def Listuseraddress():
  if session != {}:
    db = db_obj()
    cursor = db.cursor()
    cursor.execute("SELECT users.Username, useraddress.country, useraddress.state, useraddress.pincode FROM user.users INNER JOIN user.useraddress ON user.users.UId = user.useraddress.UId")
    data = cursor.fetchall()
    db.commit()
    db.close()
    return render_template('Listaddress.html', data = data)
  else:
     return "login to view users addresses "


@myapp.route('/Listusercomments/')
def Listusercomments():
    if session != {}:
        db = db_obj()
        cursor = db.cursor()
        cursor.execute("SELECT users.Username, usercomment.comment FROM user.users INNER JOIN user.usercomment ON users.UId = usercomment.UId")
        data = cursor.fetchall()
        db.commit()
        db.close()
        return render_template('view.html', data = data)
    
    else:
        return"login to view comments"


@myapp.route('/searchusers/', methods = ['POST', 'GET'])
def searchusers():
    if request.method == 'POST':
        if session != {}:
            Username = request.form['searchbox']
            db = db_obj()
            cursor = db.cursor()
            cursor.execute("SELECT COUNT(users.Username) FROM user.users WHERE users.Username = %s ",(Username, ))
            count = cursor.fetchone()
            if count == 0:
                return " no users found"
            else:
                return str(count[0])+" users found"
        else:
            return "login to view other users"
    else:
        return render_template('searchuser.html')


if __name__ == '__main__':
    myapp.run(debug=True)
