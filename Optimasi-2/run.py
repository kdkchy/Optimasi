from flask import Flask, jsonify, request,render_template, flash
from pymongo import MongoClient
import os
import pymongo
from bson.objectid import ObjectId
from komputasi.komputasi import getData, makeData

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.optimasi

#Global Variable
clicked=[]

@app.route("/")
def home():

    jadwal = db.jadwal.find()
    result = []
    for i in jadwal:
        result.append(i)

    return render_template('home.html', my_string_1="Jadwal Skripsi", my_string_2="Jadwal Pra Skripsi", title="Beranda", data=result)

@app.route("/rancang")
def rancang():
    dataMhs = db.dataMhs.find()
    result = []
    for i in dataMhs:
        result.append(i)
    # print(result)

    dataDosen = db.dataDosen.find()
    result_2 = []
    for i in dataDosen:
        result_2.append(i)
    return render_template(
        'rancang.html', my_string="Mahasiswa",my_string_2="Dosen",
        title="Rancang", data=result, data_2=result_2)


@app.route('/actRancang', methods=['POST'])
def actRancang():
    global clicked
    if request.method == "POST":
        clicked=request.json['data']

    getData(clicked[0],clicked[1],clicked[2],clicked[3]) #pembuatan populasi
    makeData()  #komputasi

    return "Success"

@app.route('/komputasi')
def komputasi():
    hitung = db.komputasi.find().sort("fitnes",pymongo.DESCENDING).limit(5)
    result = []
    for i in hitung:
        result.append(i)
    # db.komputasi.remove({})
    # db.temp.remove({})
    result_2 = []

    dataMhs = db.dataMhs.find_one({"_id":ObjectId(clicked[0])})
    dataPembimbing = db.dataDosen.find_one({"_id":ObjectId(clicked[1])})
    dataPenguji_1 = db.dataDosen.find_one({"_id":ObjectId(clicked[2])})
    dataPenguji_2 = db.dataDosen.find_one({"_id":ObjectId(clicked[3])})

    result_2.extend((dataMhs, dataPembimbing, dataPenguji_1, dataPenguji_2))
    return render_template('hasil.html', my_string="Jadwal Tersedia",  title="Ketersediaan Jadwal", data=result,
    data_2=result_2, dataMhs=dataMhs, dataPembimbing=dataPembimbing, dataPenguji_1=dataPenguji_1, dataPenguji_2=dataPenguji_2)

if __name__ == '__main__':
    app.run(debug=True)
