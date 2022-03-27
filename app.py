# Nama Kelompok :
# 1. Pratama Ardy P - 20092002
# 2. Siti Nurul Ulumi - 19090105
# username password 
# 20092002 20092002
# 19090105 19090105

from crypt import methods
from enum import unique
import json
import os, random, string
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, request

app_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(app_dir, "database.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), unique=False, nullable=False)
    token = db.Column(db.String(100), unique=True, nullable=True)

#db.create_all()

@app.route("/adduser", methods=["POST"])
def add_user():
    username = request.form['username']
    password = request.form['password']

    new_users = User(username=username, password=password)

    db.session.add(new_users)
    db.session.commit()
    return jsonify({
        'msg': 'user berhasil ditambahkan',
        'username' : username,
        'password' : password,
        'status' : 200
    })

@app.route("/api/v1/login", methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username, password=password).first()

    if user :
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

        User.query.filter_by(username=username, password=password).update({'token':token})
        db.session.commit()

        return jsonify({
            'msg': 'Anda berhasil login',
            'username' : username,
            'token': token,
            'status': 200
        })

    else:
        return jsonify({
            'msg': 'Login anda gagal',
            'status': 404,
            })

@app.route("/api/v2/users/info", methods=["POST"])
def info():
    token = request.values.get('token')
    user = User.query.filter_by(token=token).first()
    if user:
        return jsonify({
            'msg' : 'get data user berhasil',
            'username' : user.username,
            'status': 200
        })

    else:
        return jsonify({
            'msg': 'tokrn salah'
        })

if __name__=='__main__':
    app.run(debug=True, port=4000)