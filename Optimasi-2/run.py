from flask import Flask, jsonify, request,render_template, flash
from pymongo import MongoClient
import os
import pymongo
from bson.objectid import ObjectId
from komputasi.komputasi import getData, makeData, pewaktuan
import calendar

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
    db.komputasi.remove({})
    db.temp.remove({})
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

    result_2 = []
    dataMhs = db.dataMhs.find_one({"_id":ObjectId(clicked[0])})
    dataPembimbing = db.dataDosen.find_one({"_id":ObjectId(clicked[1])})
    dataPenguji_1 = db.dataDosen.find_one({"_id":ObjectId(clicked[2])})
    dataPenguji_2 = db.dataDosen.find_one({"_id":ObjectId(clicked[3])})
    result_2.extend((dataMhs, dataPembimbing, dataPenguji_1, dataPenguji_2))

    mhs, dosbing, p1, p2, ruangan = [], [], [], [], []
    for i in result:
        a, b, c = int(i.get('mhs')[0]), int(i.get('mhs')[1]),int(i.get('mhs')[2])
        mhs.append(pewaktuan(a,b,c))
        a, b, c = int(i.get('dosbing')[0]), int(i.get('dosbing')[1]),int(i.get('dosbing')[2])
        dosbing.append(pewaktuan(a,b,c))
        a, b, c = int(i.get('p1')[0]), int(i.get('p1')[1]),int(i.get('p1')[2])
        p1.append(pewaktuan(a,b,c))
        a, b, c = int(i.get('p2')[0]), int(i.get('p2')[1]),int(i.get('p2')[2])
        p2.append(pewaktuan(a,b,c))
        ruangan.append([b,c])

    print(ruangan)

    ruanganList = []
    for i in range(len(ruangan)):
        hasilRuangan = db.ruangan.find({ 'waktu' : ruangan[i]})
        for i in hasilRuangan:
            ruanganList.append(i)

    for i in range(len(ruanganList)):
        print(ruanganList[i].get('ruangan')[0])

    zipdata = zip(result, mhs, dosbing, p1, p2, ruanganList)
    return render_template('hasil.html', my_string="Jadwal Tersedia",  title="Ketersediaan Jadwal", data=result,
    data_2=result_2, zipdata=zipdata, ruanganList=ruanganList)


@app.route('/actInsert', methods=["POST"])
def actInsert():
    try:
        status=request.values.get("status")
        mhs=request.values.get("mhs")
        dosbing=request.values.get("dosbing")
        p1=request.values.get("p1")
        p2=request.values.get("p2")
        ruangan=request.values.get("ruang")

        judul=request.values.get("judul")

        db.jadwal.insert({"status":status, "hari dan jam": mhs})

        return render_template(
                'msg.html', my_string="Data Has Been Stored.", title="Insert")

    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")
    return render_template('msg.html', my_string="Sukses")

if __name__ == '__main__':
    app.run(debug=True)
