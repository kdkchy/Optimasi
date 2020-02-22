from flask import Flask, render_template, request, url_for, g
import mysql.connector as mariadb
from werkzeug.urls import url_parse
import time

app = Flask(__name__)

@app.errorhandler(404) 
def not_found(e): 
  return render_template("404.html", my_string="Ooppss! Page not found!", title="404"),404


@app.before_request
def before_request():
    g.start = time.time()


def after_request():
    diff = time.time() - g.start
    return diff

def connect():
    conn = mariadb.connect(
        host="localhost",
        user="root",
        passwd="123",
        database='rental'
    )
    return conn
    

@app.route("/")
def home():

    conn = connect()
    cur = conn.cursor()
    sql = "SELECT * FROM members"
    cur.execute(sql)
    results = cur.fetchall()
    data=[]
    for i in results:
        data.append(i)
    return render_template(
        'home.html', my_string="Welcome home!", title="Home", data=data, time=after_request())

@app.route("/insert")
def insert():
    return render_template(
        'insert.html', my_string="Let's insert some data!",
        title="Insert")


@app.route('/update/<int:id>')
def update(id):

    conn = connect()
    cur = conn.cursor()
    sql = "Select * from members where member_id='{}'".format(id)
    cur.execute(sql)
    results = cur.fetchall()
    data=[]
    for i in results:
        data.append(i)
    return render_template(
        'update.html', my_string="You can also update your data directly.",
        title="Update",data=data)


@app.route("/actupdate", methods=['POST'])
def actupdate():
    if (request.method == 'POST'):
        try:
            id=request.form['id']
            name=request.form['name']
            address=request.form['address']
            conn = connect()

            cur = conn.cursor()
            sql = "UPDATE members set name='{}', address='{}' where member_id='{}'".format(name,address,id)
            cur.execute(sql)
            conn.commit()
            return render_template(
                'msg.html', my_string="Data Has Been Updated.", title="Update")
        except:
            return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Update")

@app.route("/act", methods=['POST'])
def act():
    if (request.method == 'POST'):
        try:
            name=request.form['name']
            address=request.form['address']
            conn = connect()
            cur = conn.cursor()
            sql = "INSERT INTO members(name,address) VALUES ('{}','{}')".format(name,address)
            cur.execute(sql)
            conn.commit()
            return render_template(
                'msg.html', my_string="Data Has Been Stored.", title="Insert")
        except:
            return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")

if __name__ == '__main__':
    app.run(debug=True)
