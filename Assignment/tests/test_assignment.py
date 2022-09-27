import base64
import pytest
import flask
from flask import url_for
from project import Assignment
import tempfile
import os
from werkzeug.datastructures import ImmutableMultiDict


@pytest.fixture
def client():
    # to configure db 
    db_fd, Assignment.myapp.config['DATABASE'] = tempfile.mkstemp()
    Assignment.myapp.config['TESTING'] = True

    with Assignment.myapp.test_client() as client:
        with Assignment.myapp.app_context():
            Assignment.db_obj()
        yield client

# closing tempfile pointer and clsing the db connection
    print(db_fd, Assignment.myapp.config['DATABASE'])
    os.close(db_fd)
    os.unlink(Assignment.myapp.config['DATABASE'])


def test_empty_db(client):
    response = client.get("/")
    assert b"no entries so far" in response.data

def test_register_user(client):
    # details = {'Username':'Vidhi', 'Upassword':'vidhi123'}
    # in this either you can give dict data or immutableMultidict data
    details = ImmutableMultiDict([('Username', 'vidhi'), ('Upassword', 'vidhi123')])
    response = client.post('/registeruser/',content_type = 'multipart/form-data', data = details)
    assert flask.session['Username'] == 'vidhi'
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert response.text == '''<!DOCTYPE html>
<head>
    <title>
        Register
    </title>
</head>
<body>
    <h1>upload photo</h1>
    <form action = "http://localhost:5000/uploadphoto/" method = 'POST' enctype = multipart/form-data>

            <p>
                <label>Upload Photo: </label>
                <input name = "Uphoto" type = "file" accept="image/*"/>
            </p>

            <p>
                <button type = submit>submit</button>
            </p>
    </form>
</body>
</html>'''
    photo = open("C:/Users/ZMO-WIN-RajlakshmiB-/Pictures/images/tiger.jpg", mode = 'rb')
    uploadPhotoResponse = client.post('/uploadphoto/', content_type = 'multipart/form-data', data = {'Uphoto' : photo}, follow_redirects = True)
    assert uploadPhotoResponse.status_code == 200
    assert flask.session['Username'] == 'vidhi'
    assert uploadPhotoResponse.content_type == 'text/html; charset=utf-8'
    assert uploadPhotoResponse.request.path == url_for('addaddress')

    address = {'country':'New Zealand', 'state':'Auckland', 'pincode':306709}
    addaddress = client.post('/addaddress/', content_type = 'multipart/form-data', data = address)
    assert addaddress.status_code == 200
    assert addaddress.content_type == 'text/html; charset=utf-8'
    assert flask.session =={}
    assert addaddress.text == '''<!DOCTYPE html>
<head>
    <title>
        login
    </title>
</head>
<body>
    <form action = "http://localhost:5000/login" method = post>
        <label>Username: </label>
        <p>
            <input type = text name = 'Username'/>
        </p>
        <label>password: </label>
        <p>
            <input type = password name = 'Upassword'/>
        </p>
        <p>
            <input type = 'submit' name = login/>
        </p>
    </form>
</body>
</html>'''
    

def test_login(client):
    credentials = {'Username':'Vidhi', 'Upassword':'vidhi123'}
    loginRes = client.post('/login/', content_type = 'multipart/form-data', data = credentials)
    image = base64.b64encode(b"C:/Users/ZMO-WIN-RajlakshmiB-/Pictures/images/tiger.jpg")
    image = image.decode('UTF-8')
    assert loginRes.status_code == 200
    assert loginRes.content_type == 'text/html; charset=utf-8'
    assert b"login render" in loginRes.data
    assert b"Name:Vidhi" in loginRes.data
    assert flask.session ==  {'Username': 'Vidhi', 'Upassword': 'vidhi123'}

def test_comment(client):
    test_login(client)
    comment = {"comment":"good"}
    response = client.post('/comment/', content_type = "multipart/form-data", data = comment)
    assert response.status_code == 200
    assert response.content_type == "text/html; charset=utf-8"
    assert flask.session == {'Username': 'Vidhi', 'Upassword': 'vidhi123'}
    assert "thanks for your comment" in response.text

def test_Listusercomments(client):
    test_login(client)
    response = client.get('/Listusercomments/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert b"great experience" in response.data

def test_Listuseraddress(client):
    test_login(client)
    response = client.get('/Listuseraddress/')
    assert response.status_code == 200
    assert response .content_type == 'text/html; charset=utf-8'
    assert b"India" in response.data

def test_search_users(client):
    test_login(client)
    response = client.post('/searchusers/', data = {'searchbox': 'Shreya'})
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert b"8" in response.data
                                        
       
def test_update(client):
    test_login(client)
    response = client.post('/update/', content_type = 'multipart/form-data', data = {'Username':'Vidhi', 'country':'New Zealand', 'state':'Northland', 'pincode':509809 })
    assert response.status_code == 200
    assert response.content_type =='text/html; charset=utf-8'
    assert b"updation successful" in response.data

def test_logout(client):
    test_login(client)
    response = client.get('/logout/', follow_redirects = True)
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert len(response.history) == 1
    assert response.request.path == '/login/'
    assert b"Username" in response.data
    assert b"Upassword" in response.data
    assert b"login" in response.data


def test_deletephoto(client):
    test_login(client)
    response = client.get('/deletephoto/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert "your photo was deleted successfully" in response.text

def test_deleteaddress(client):
    test_login(client)
    response = client.get('/deleteaddress/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert "user address was deleted successfully" in response.text

def test_deletecomment(client):
    test_login(client)
    response = client.get('/deletecomments/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert "all of comments are deleted succesfully" in response.text

def test_deleteuser(client):
    test_login(client)
    response = client.get('/deleteuser/')
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert "deleted user" in response.text

def test_changePassword(client):
    test_login(client)
    response = client.post('/changePassword/', content_type = 'multipart/form-data', data = {'oldPassword':'vidhi123', 'newPassword':'vidhi456'})
    assert response.status_code == 200
    assert response.content_type == 'text/html; charset=utf-8'
    assert "password was changed successfully" in response.text