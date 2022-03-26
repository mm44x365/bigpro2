#http://127.0.0.1:7001/
#Nama:Pratama Ardy P, Nim:20092002
#Nama:Siti Nurul Ulumi,Nim:19090105

from flask import Flask
from flask_httpauth import HTTPTokenAuth

app = Flask(__name__)
auth = HTTPTokenAuth(scheme='Bearer')

tokens = {
    "secret-token-1": "20092002",
    "secret-token-2": "19090105"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

@app.route('/')
@auth.login_required
def index():
    return "Anda login dengan nim, {}!".format(auth.current_user())

if __name__ == '__main__':
    app.run(debug = True, port=7001)


