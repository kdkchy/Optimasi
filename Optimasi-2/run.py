from flask import Flask, jsonify, request,render_template, flash, redirect, url_for
from pymongo import MongoClient
import os
import pymongo
from bson.objectid import ObjectId
from komputasi.komputasi import getData, makeData, pewaktuan
import ast

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.optimasi

#Global Variable
clicked = []
result_2 = None

@app.route("/")
def home():

    jadwal = db.jadwal.find({ 'status' : 'skripsi'})
    skripsi = []
    for i in jadwal:
        skripsi.append(i)

    jadwal = db.jadwal.find({ 'status' : 'pra'})
    pra = []
    for i in jadwal:
        pra.append(i)

    return render_template('home.html', my_string_1="Jadwal Skripsi", my_string_2="Jadwal Pra Skripsi",
    title="Beranda", data=skripsi, data_2=pra)

@app.route("/rancang")
def rancang():
    db.komputasi.remove({})
    db.temp.remove({})
    db.populasi.remove({})
    dataMhs = db.dataMhs.find().sort("nim",pymongo.ASCENDING)
    result = []
    for i in dataMhs:
        result.append(i)

    dataDosen = db.dataDosen.find()
    result_2 = []
    for i in dataDosen:
        result_2.append(i)

    dataPenguji = db.dataDosen.find()
    result_3 = []
    for i in dataPenguji:
        result_3.append(i)
    return render_template(
        'rancang.html', my_string="Mahasiswa", my_string_2="Dosen Pembimbing", my_string_3="Penguji",
        title="Rancang", data=result, data_2=result_2, data_3=result_3)

@app.route("/inputMhs")
def inputMhs():
    return render_template('inputMhs.html', title="Input Mahasiswa", my_string="Lengkapi Data")

@app.route("/actinputMhs", methods=["POST"])
def actinputMhs():
    try:
        data = [""]
        for i in range(20):
            a = ast.literal_eval(str(request.form.get(str(i+1))))
            data.append(a)

        nama = request.form.get('nama')
        nim = request.form.get('nim')

        db.dataMhs.insert({
        "1":data[1],"2":data[2],"3":data[3],"4":data[4],
        "5":data[5],"6":data[6],"7":data[7],"8":data[8],
        "9":data[9],"10":data[10],"11":data[11],"12":data[12],
        "13":data[13],"14":data[14],"15":data[15],"16":data[16],
        "17":data[17],"18":data[18],"19":data[19],"20":data[20],
        "nama": nama,
        "nim" : nim,
        })


        flash('Data Tersimpan!')
        return redirect('/inputMhs')
    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")

    return render_template('inputMhs.html', title="Input Mahasiswa", my_string="Lengkapi Data")

@app.route("/inputDosen")
def inputDosen():
    return render_template('inputDosen.html',title="Input Dosen", my_string="Lengkapi Data")

@app.route("/actinputDosen", methods=["POST"])
def actinputDosen():
    try:
        data = [""]
        for i in range(20):
            a = ast.literal_eval(str(request.form.get(str(i+1))))
            data.append(a)

        nama = request.form.get('nama')

        db.dataDosen.insert({
        "1":data[1],"2":data[2],"3":data[3],"4":data[4],
        "5":data[5],"6":data[6],"7":data[7],"8":data[8],
        "9":data[9],"10":data[10],"11":data[11],"12":data[12],
        "13":data[13],"14":data[14],"15":data[15],"16":data[16],
        "17":data[17],"18":data[18],"19":data[19],"20":data[20],
        "nama": nama
        })


        flash('Data Tersimpan!')
        return redirect('/inputDosen')
    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")

    return render_template('inputDosen.html',title="Input Dosen", my_string="Lengkapi Data")


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

    global result_2
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

    ruanganList = []
    for i in range(len(ruangan)):
        hasilRuangan = db.ruangan.find({ 'waktu' : ruangan[i]})
        for i in hasilRuangan:
            ruanganList.append(i)

    zipdata = zip(result, mhs, dosbing, p1, p2, ruanganList)
    return render_template('hasil.html', my_string="Jadwal Tersedia",  title="Ketersediaan Jadwal", data=result,
    data_2=result_2, zipdata=zipdata, ruanganList=ruanganList)


@app.route('/actInsert', methods=["POST"])
def actInsert():
    try:
        status=request.values.get("status")
        harijam=request.values.get("mhs")
        tgl=request.values.get("tgl")
        dosbing=request.values.get("dosbing")
        p1=request.values.get("p1")
        p2=request.values.get("p2")
        ruangan=request.values.get("ruang")
        judul=request.values.get("judul")

        db.jadwal.insert({
        "status":status,
        "harijam": harijam,
        "tgl" : tgl,
        "ruangan" : ruangan,
        "mhs" : result_2[0].get('nama'),
        "nim" : result_2[0].get('nim'),
        "dosbing" : result_2[1].get('nama'),
        "p1" : result_2[2].get('nama'),
        "p2" : result_2[3].get('nama'),
        "judul" : judul
        })

        flash('Jadwal Terancang')
        return redirect('/')
    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")
    return redirect('/')

@app.route('/populasi')
def populasi():

    hasil = db.populasi.find()
    data = []
    for i in hasil:
        data.append(i)

    return render_template('populasi.html', title="Hasil", data=data)

if __name__ == '__main__':
    app.run(debug=True)
