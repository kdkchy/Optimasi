from numpy import prod
import pymongo
from pymongo import MongoClient
import pprint
import os

import json
import pprint

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
db = client.optimasi

result = list(db.dataPerson.find())
list= []

for i in range(len(result)):
    dataTable = []

    a = result[i]
    dataTable.append(a.get('mhs'))
    dataTable.append(a.get('dosbing'))
    dataTable.append(a.get('p1'))
    dataTable.append(a.get('p2'))

    list.append(dataTable)

pprint.pprint(list)
print()

hasil = []

for j in range(len(list)):
    item = {}
    # menghitung data pertama pada list 
    data = j

    """RUMUS"""
    # menghitung status
    hx = (list[data][0][0]+list[data][1][0]+list[data][2][0]+list[data][3][0])/4

    """RUMUS"""
    # menghitung jam dan hari
    YZ = []
    for i in range(4):
        result = (3*list[data][i][1]+5*list[data][i][2])
        YZ.append(result)
    YZprod = int(prod(YZ))
    
    """RUMUS"""
    # menghitung kasus akar
    for i in range(4):
        if (YZprod**(1/4) == 3*list[data][0][1]+5*list[data][0][2]):
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


    hasil.append(item)

result = db.komputasi.find().sort("fitnes",pymongo.DESCENDING)

hasilakhir = []
for ulang in result:
    hasilakhir.append(ulang)


pprint.pprint(hasilakhir)
db.komputasi.remove({})
