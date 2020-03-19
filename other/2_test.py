from pymongo import MongoClient
import os
import pymongo
import pprint

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)
db = client.optimasi

def pewaktuan(a,b):
    hari = ["", "Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
    jam = ["", "08.00", "10.00", "13.00", "15.00"]
    result = []
    result.extend((hari[a],jam[b]))
    return result

hitung = db.komputasi.find().sort("fitnes",pymongo.DESCENDING).limit(5)
result = []
for i in hitung:
    result.append(i)

result_3 = []
for i in result:
    a, b = int(i.get('mhs')[1]),int(i.get('mhs')[2])
    result_3.append(pewaktuan(a,b))

for i in range(len(result_3)):
    print("{} / {}".format(result_3[i][0],result_3[i][1]))
