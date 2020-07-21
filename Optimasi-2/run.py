from flask import Flask, jsonify, request,render_template, flash, redirect, url_for
from pymongo import MongoClient
import os
import pymongo
from bson.objectid import ObjectId
from komputasi.komputasi import getData, makeData, pewaktuan, simpanPopulasi, decode, terjadwal
import ast

from flask_wtf import Form
from wtforms import DateField
from datetime import date

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.optimasi

#Global Variable
clicked = []
result_2 = None
waktuKode = None
hariKegiatan = None

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

    dataDosen = db.dataDosen.find().sort("nama",pymongo.ASCENDING)
    result_2 = []
    for i in dataDosen:
        result_2.append(i)

    dataPenguji = db.dataDosen.find().sort("nama",pymongo.ASCENDING)
    result_3 = []
    for i in dataPenguji:
        result_3.append(i)
    return render_template(
        'rancang.html', my_string="Mahasiswa", my_string_2="Dosen Pembimbing", my_string_3="Penguji",
        title="Rancang", data=result, data_2=result_2, data_3=result_3)

@app.route("/inputMhs")
def inputMhs():
    return render_template('inputMhs.html', title="Input Mahasiswa", my_string="Lengkapi Data")

@app.route("/actinputMhs", methods=["POST", "GET"])
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

        flash('Lengkapi Matakuliah!')
        return redirect(url_for('inputKegiatanMhs', nim=nim))
    except:
        return render_template(
                'msg.html', my_string="Id Sama!", title="Insert")
    return render_template('inputMhs.html', title="Input Mahasiswa", my_string="Lengkapi Data")

@app.route("/inputKegiatanMhs/<nim>")
def inputKegiatanMhs(nim):
    data = db.dataMhs.find({"nim" : nim})
    dataId = nim

    hasil = {}
    for i in range(20):
        hasil[i+1] = data[0].get(str(i+1))

    hasil_2 = {}
    global hariKegiatan
    hariKegiatan = []
    for i in range(20):
        if(hasil[i+1][0]==1):
            hasil_2[i+1] = [str(i+1), hasil[i+1]]
            hariKegiatan.append([str(i+1), pewaktuan(1,hasil_2[i+1][1][1],hasil_2[i+1][1][2])])
            
    return render_template('inputKegiatanMhs.html', title="Input Kegiatan", my_string="Tambahkan Matakuliah", hari=hariKegiatan, dataId=dataId)

@app.route("/actInputKegiatanMhs", methods=["POST"])
def actInputKegiatanMhs():
    try:
        nim = request.values.get('dataId')



        dataTabel = {}
        print(hariKegiatan[0])
        for i in range(len(hariKegiatan)):
            dataTabel[hariKegiatan[i][0]] = request.values.get(hariKegiatan[i][0])

        dataTabel['nim'] = nim

        db.jadwalMhs.insert(
        dataTabel
        )

        flash('Data Tersimpan!')
        return redirect(url_for('inputMhs'))
    except:
        return render_template(
                'msg.html', my_string="Gagal Tersimpan!", title="Insert")
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

        nama = request.values.get('nama')
        nip = request.values.get('nip')

        db.dataDosen.insert({
        "1":data[1],"2":data[2],"3":data[3],"4":data[4],
        "5":data[5],"6":data[6],"7":data[7],"8":data[8],
        "9":data[9],"10":data[10],"11":data[11],"12":data[12],
        "13":data[13],"14":data[14],"15":data[15],"16":data[16],
        "17":data[17],"18":data[18],"19":data[19],"20":data[20],
        "nama": nama, "nip" : nip
        })


        flash('Lengkapi Matakuliah!')
        return redirect(url_for('inputKegiatanDosen', nip=nip))
    except:
        return render_template(
                'msg.html', my_string="Id Sama", title="Insert")

    return render_template('inputDosen.html',title="Input Dosen", my_string="Lengkapi Data")

@app.route("/inputKegiatanDosen/<nip>")
def inputKegiatanDosen(nip):
    data = db.dataDosen.find({"nip" : nip})
    dataId = nip

    hasil = {}
    for i in range(20):
        hasil[i+1] = data[0].get(str(i+1))

    hasil_2 = {}
    global hariKegiatan
    hariKegiatan = []
    for i in range(20):
        if(hasil[i+1][0]==1):
            hasil_2[i+1] = [str(i+1), hasil[i+1]]
            hariKegiatan.append([str(i+1), pewaktuan(1,hasil_2[i+1][1][1],hasil_2[i+1][1][2])])
            
    return render_template('inputKegiatanDosen.html', title="Input Kegiatan", my_string="Tambahkan Matakuliah", hari=hariKegiatan, dataId=dataId)

@app.route("/actInputKegiatanDosen", methods=["POST"])
def actInputKegiatanDosen():
    try:
        nip = request.values.get('nip')

        dataTabel = {}
        print(hariKegiatan[0])
        for i in range(len(hariKegiatan)):
            dataTabel[hariKegiatan[i][0]] = request.values.get(hariKegiatan[i][0])

        dataTabel['nip'] = nip

        db.jadwalDosen.insert( 
        dataTabel
        )

        flash('Data Tersimpan!')
        return redirect(url_for('inputDosen'))
    except:
        return render_template(
                'msg.html', my_string="Gagal Tersimpan!", title="Insert")
    return render_template('inputDosen.html', title="Input Dosen", my_string="Lengkapi Data")

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

    global waktuKode
    mhs, dosbing, p1, p2, ruangan, waktuKode = [], [], [], [], [], []

    for i in result:
        item = []
        a, b, c = int(i.get('mhs')[0]), int(i.get('mhs')[1]),int(i.get('mhs')[2])
        mhs.append(pewaktuan(a,b,c))
        item.append([a,b,c])
        a, b, c = int(i.get('dosbing')[0]), int(i.get('dosbing')[1]),int(i.get('dosbing')[2])
        dosbing.append(pewaktuan(a,b,c))
        item.append([a,b,c])
        a, b, c = int(i.get('p1')[0]), int(i.get('p1')[1]),int(i.get('p1')[2])
        p1.append(pewaktuan(a,b,c))
        item.append([a,b,c])
        a, b, c = int(i.get('p2')[0]), int(i.get('p2')[1]),int(i.get('p2')[2])
        p2.append(pewaktuan(a,b,c))
        item.append([a,b,c])
        ruangan.append([b,c])
        a , b = int(i.get('mhs')[1]),int(i.get('mhs')[2])
        waktuKode.append([decode(a,b), item])

    ruanganList = []
    for i in range(len(ruangan)):
        hasilRuangan = db.ruangan.find({ 'waktu' : ruangan[i]})
        for i in hasilRuangan:
            ruanganList.append(i)

    zipdata = zip(result, mhs, dosbing, p1, p2, ruanganList)
    # print(result_2)

    return render_template('hasil.html', my_string="Jadwal Tersedia",  title="Ketersediaan Jadwal", data=result,
    data_2=result_2, zipdata=zipdata, ruanganList=ruanganList)

@app.route('/actInsert', methods=["POST"])
def actInsert():
    try:
        status=request.values.get("status")
        harijam=request.values.get("mhs")
        tgl=request.values.get("tgl")
        ruangan=request.values.get("ruang")
        judul=request.values.get("judul")
        loop=int(request.values.get("angkaLoop"))

        db.jadwal.insert({
        "status":status,
        "harijam": harijam,
        "tgl" : tgl,
        "ruangan" : ruangan,
        "mhs" : result_2[0].get('nama'),
        "nim" : result_2[0].get('nim'),
        "dosbing" : result_2[1].get('nama'),
        "dosbingNIP" : result_2[1].get('nip'),
        "p1" : result_2[2].get('nama'),
        "p1NIP" : result_2[2].get('nip'),
        "p2" : result_2[3].get('nama'),
        "p2NIP" : result_2[3].get('nip'),
        "judul" : judul,
        "K" : waktuKode[loop-1][0],
        "Kmhs" : waktuKode[loop-1][1][0],
        "Kdosbing" : waktuKode[loop-1][1][1],
        "Kp1" : waktuKode[loop-1][1][2],
        "Kp2" : waktuKode[loop-1][1][3]
        })

        x = str(waktuKode[loop-1][0])
        y = terjadwal(waktuKode[loop-1][0])
        z = "Ujian "+status
        zz = "Pembimbing "+status
        zzz = "Narasumber "+status

        #pencarian ruangan
        waktu = [y[1],y[2]]
        print(waktu)
        dataR = db.ruangan.find_one({"waktu" : waktu})
        r = dataR.get('ruangan')
        print(dataR)
        new = []
        for i in r:
            new.append(i.replace(ruangan,"-"))
        
        db.ruangan.update({"waktu" : waktu}, 
        {"$set" : { "ruangan" : new}})

        db.dataMhs.update({"nim" : result_2[0].get('nim')},
        {"$set" : {
        x : y
        }
        })
        db.jadwalMhs.update({"nim" : result_2[0].get('nim')},
        { "$set" :{ 
        x : z }
        })


        db.dataDosen.update({"nip" : result_2[1].get('nip')},
        {"$set" : {
        x : y
        }
        })
        db.jadwalDosen.update({"nip" : result_2[1].get('nip')},
        {"$set" : { 
        x : zz
        }})


        db.dataDosen.update({"nip" : result_2[2].get('nip')},
        {"$set" : {
        x : y
        }
        })
        db.jadwalDosen.update({"nip" : result_2[2].get('nip')},
        {"$set" : { 
        x : zzz
        }})


        db.dataDosen.update({"nip" : result_2[3].get('nip')},
        {"$set" : {
        x : y
        }
        })
        db.jadwalDosen.update({"nip" : result_2[3].get('nip')},
        {"$set" : { 
        x : zzz
        }})

        flash('Jadwal Terancang')
        return redirect('/')
    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")
    return redirect('/')

@app.route('/delete/<string:id>/<string:status>')
def delete(id,status):
    hasil = db.jadwal.find({"nim" : id, "status" : status})

    result = []
    for i in hasil:
        result.append(i)

    k=str(result[0].get('K'))
    mhsNama=result[0].get('mhs')
    kMhs=result[0].get('Kmhs')

    dsbingNama=result[0].get('dosbing')
    kDsb=result[0].get('Kdosbing')
    dNip=result[0].get('dosbingNIP')

    p1Nama=result[0].get('p1')
    kp1=result[0].get('Kp1')
    p1Nip=result[0].get('p1NIP')

    p2Nama=result[0].get('p2')
    kp2=result[0].get('Kp2')
    p2Nip=result[0].get('p2NIP')

    kosong = ""

    db.dataMhs.update({"nama" : mhsNama},
    {"$set" : {
    k : kMhs
    }})
    db.dataDosen.update({"nama" : dsbingNama},
    {"$set" : {
    k : kDsb
    }})
    db.dataDosen.update({"nama" : p1Nama},
    {"$set" : {
    k : kp1
    }})
    db.dataDosen.update({"nama" : p2Nama},
    {"$set" : {
    k : kp2
    }})

    db.jadwalMhs.update({"nim" : id},
    {"$set" : {
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : dNip},{"$set" :{
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : p1Nip},{"$set" :{
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : p2Nip},{"$set" :{
    k : kosong
    }})

    #pencarian ruangan

    waktu = [kMhs[1],kMhs[2]]
    dataR = db.ruangan.find_one({"waktu" : waktu})
    r = dataR.get('ruangan')
    new = []
    for i in r:
        new.append(i.replace("-", result[0].get('ruangan')))
    
    db.ruangan.update({"waktu" : waktu}, 
    {"$set" : { "ruangan" : new}})

    hasil = db.jadwal.remove({"nim" : id, "status" : status})
    return render_template('msg.html', my_string="Jadwal Terlaksana!", title="Terlaksana")

@app.route('/jadwalUlang/<string:id>/<string:status>')
def jadwalUlang(id,status):
    hasil = db.jadwal.find({"nim" : id, "status" : status})

    result = []
    for i in hasil:
        result.append(i)

    k=str(result[0].get('K'))
    mhsNama=result[0].get('mhs')
    kMhs=result[0].get('Kmhs')

    dsbingNama=result[0].get('dosbing')
    kDsb=result[0].get('Kdosbing')
    dNip=result[0].get('dosbingNIP')

    p1Nama=result[0].get('p1')
    kp1=result[0].get('Kp1')
    p1Nip=result[0].get('p1NIP')

    p2Nama=result[0].get('p2')
    kp2=result[0].get('Kp2')
    p2Nip=result[0].get('p2NIP')

    db.dataMhs.update({"nama" : mhsNama},
    {"$set" : {
    k : kMhs
    }})

    db.dataDosen.update({"nama" : dsbingNama},
    {"$set" : {
    k : kDsb
    }})

    db.dataDosen.update({"nama" : p1Nama},
    {"$set" : {
    k : kp1
    }})

    db.dataDosen.update({"nama" : p2Nama},
    {"$set" : {
    k : kp2
    }})

    kosong = ""
    db.jadwalMhs.update({"nim" : id},
    {"$set" : {
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : dNip},{"$set" :{
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : p1Nip},{"$set" :{
    k : kosong
    }})
    db.jadwalDosen.update({"nip" : p2Nip},{"$set" :{
    k : kosong
    }})


    #pencarian ruangan

    waktu = [kMhs[1],kMhs[2]]
    dataR = db.ruangan.find_one({"waktu" : waktu})
    r = dataR.get('ruangan')
    new = []
    for i in r:
        new.append(i.replace("-", result[0].get('ruangan')))
    
    db.ruangan.update({"waktu" : waktu}, 
    {"$set" : { "ruangan" : new}})


    hasil = db.jadwal.remove({"nim" : id, "status" : status})
    return redirect('/rancang')

@app.route('/populasi')
def populasi():

    data = simpanPopulasi()
    db.populasi.insert(data)

    #data = db.populasi.find()
    return render_template('populasi.html', title="Rekombinasi", data=data)

@app.route("/ruangan")
def ruangan():
    data = db.ruangan.find()
    ruangan = []
    for i in data:
        ruangan.append(i)
    return render_template('ruangan.html',title="Ruangan", data=ruangan)

@app.route("/dosentampil/<string:id>")
def dosentampil(id):
    data = db.dataDosen.find_one({'_id': ObjectId(id)})
    nip=data.get('nip')
    data_2 = db.jadwalDosen.find_one({'nip' : nip})

    hasil = {}
    for i in range(20):
        hasil[i+1]= data_2.get(str(i+1))

    return render_template('dosenTampil.html',title="Data Dosen", data_2=hasil, data=data, my_string="")

@app.route("/dosenUpdate/<string:id>")
def dosenUpdate(id):
    data = db.dataDosen.find_one({"nip" : id})

    return render_template('dosenUpdate.html',title="Update Kegiatan", data=data)

@app.route("/actupdateDosen", methods=["POST"])
def actupdateDosen():
    try:
        nip=request.values.get("nip")
        kegiatan=request.values.get("kegiatan")
        x=request.values.get("harijam")
        y=terjadwal(x)

        db.dataDosen.update({"nip" : nip},
        {"$set" : {
        x : y
        }
        })

        y[0]=0
        db.jadwalDosen.update({"nip" : nip},
        {"$set" : {
        x : kegiatan,
        "kode" : [int(x),y]
        }
        })


        flash('Jadwal Terupdate')
        return redirect('/rancang')
    except:
        return render_template(
                'msg.html', my_string="Databases Connection Error!", title="Insert")
    return redirect('/rancang')
    
@app.route("/dosenReset/<string:id>")
def dosenReset(id):
    data = db.jadwalDosen.find_one({"nip" : id})
    k=data.get('kode')

    x=str(k[0])
    y=k[1]
    

    db.dataDosen.update({"nip" : id},
        {"$set" : {
        x : y
        }
        })

    db.jadwalDosen.update({"nip" : id},
        {"$set" : {
        x : "",
        "kode" : ""
        }
        })

    return redirect('/rancang')

@app.route("/mhstampil/<string:id>")
def mhstampil(id):
    data = db.dataMhs.find_one({'_id': ObjectId(id)})
    nim=data.get('nim')
    data_2 = db.jadwalMhs.find_one({'nim' : nim})

    hasil = {}
    for i in range(20):
        hasil[i+1]= data_2.get(str(i+1))
    return render_template('mhsTampil.html',title="Data Mahasiswa", data_2=hasil, data=data, my_string="")

@app.route("/bantuan")
def bantuan():

    return render_template('bantuan.html',title="Bantuan dan Info", my_string="")

if __name__ == '__main__':
    app.run(debug=True)
