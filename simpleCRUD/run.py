from flask import Flask, jsonify, request,render_template, flash
from pymongo import MongoClient
import os
from bson.objectid import ObjectId

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
 

@app.route("/")
def home():
    db = client.rental 
    person = db.person.find()
    result = []
    
    for i in person:
        result.append(i)
    return render_template('home.html', my_string="Welcome Home!", title="Home", data=result)

@app.route("/insert")
def insert():

    return render_template(
        'insert.html', my_string="Let's insert some data!",
        title="Insert")

@app.route("/actinsert", methods=["POST"])
def actinsert():
    try:
        name=request.values.get("name")
        address=request.values.get("address")

        db = client.rental
        db.person.insert({"name":name, "address": address})

        return render_template(
                'msg.html', my_string="Data Has Been Stored.", title="Insert")

    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")


@app.route("/update/<id>")
def update(id):
 
    db = client.rental 
    person = db.person.find({"_id":ObjectId(id)})
    result = []
    for i in person:
        result.append(i)

    return render_template(
        'update.html', my_string="You can also update your data directly.",
        title="Update",data=result)

@app.route("/actupdate", methods=["POST"])
def actupdate():
    if (request.method == 'POST'):
        try:
            name=request.values.get("name")
            address=request.values.get("address")
            id=request.values.get("id")
            db = client.rental

            db.person.update(
                {"_id":ObjectId(id)},
                {'$set':{
                "name" : name,
                "address" : address
                }
            })
            return render_template(
                'msg.html', my_string="Data Has Been Updated.", title="Update")
        except:
            return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Update")

@app.route("/remove")
def remove():
    key = request.values.get("_id")
    db = client.rental
    db.person.remove({"_id":ObjectId(key)})
    return render_template(
                'msg.html', my_string="Data Has Been Deleted.", title="Delete")

if __name__ == '__main__':
    app.run(debug=True)
