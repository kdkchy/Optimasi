
from flask import Flask,request
import json
app = Flask(__name__)

@app.route("/")
def hello():
    return "Welcome to Python Flask!"


from flask import render_template

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    print(user)
    return json.dumps({'status':'OK','user':user,'pass':password});


if __name__ == '__main__':
    app.run(debug=True)
