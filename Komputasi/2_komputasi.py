from numpy import prod
import pymongo
from pymongo import MongoClient
import pprint
import os
import random
from bson.objectid import ObjectId


import json
import pprint

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
db = client.optimasi


result = list(db.temp.find())
my_list = []

for i in range(len(result)):
    dataTable = []

    a = result[i]
    dataTable.append(a.get('mhs'))
    dataTable.append(a.get('dosbing'))
    dataTable.append(a.get('p1'))
    dataTable.append(a.get('p2'))

    my_list.append(dataTable)

pprint.pprint(my_list)
print()

hasil = []

for j in range(len(my_list)):
    item = {}
    # menghitung data pertama pada my_list 
    data = j

    """RUMUS"""
    # menghitung status
    hx = (my_list[data][0][0]+my_list[data][1][0]+my_list[data][2][0]+my_list[data][3][0])/4

    """RUMUS"""
    # menghitung jam dan hari
    YZ = []
    for i in range(4):
        result = (3*my_list[data][i][1]+5*my_list[data][i][2])
        YZ.append(result)
    YZprod = int(prod(YZ))
    
    """RUMUS"""
    # menghitung kasus akar
    for i in range(4):
        if (YZprod**(1/4) == 3*my_list[data][0][1]+5*my_list[data][0][2]):
            a = 0
        else:
            a = 1

    """RUMUS"""
    # fungsi fitness
    f = 1/(a + hx + 1)
   
    # print()
    item.update([('status' , hx), ('jam dan hari' , YZ), ('hasil' , YZprod), ('kasus akar' , a),('fitnes', f)])
    
    #data disimpan di databases
    db.komputasi.insert({'status': hx, 'jam dan hari' : YZ, 'hasil' : YZprod, 'kasus akar' : a, 'fitnes' : f})

    db.temp.update({"id" : j}, {'$set' : {"fitness" : f}})
    hasil.append(item)
   

result = db.temp.find().sort("fitness",pymongo.DESCENDING)

hasilakhir = []
for ulang in result:
    hasilakhir.append(ulang)

print("Fitness tertinggi (table - temp)")
pprint.pprint(hasilakhir)

print("_____________________________________________________________")
result = db.komputasi.find().sort("fitnes",pymongo.DESCENDING)

hasilakhir = []
for ulang in result:
    hasilakhir.append(ulang)

print("Fitness tertinggi (table - komputasi)")
pprint.pprint(hasilakhir)
db.komputasi.remove({})