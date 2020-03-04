from pymongo import MongoClient
import pprint
import os
import random
from bson.objectid import ObjectId
import json

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
db = client.optimasi

ambil_dataPerson = list(db.dataPerson.find({"_id":ObjectId("5e5f5920b460288bf702e1be")}))
simpan_dataPerson = []

for i in range(20):
    j = i + 1
    simpan_dataPerson.append(ambil_dataPerson[0][str(j)])

random.shuffle(simpan_dataPerson)
for i in range(20):
    db.temp.insert({'id' : i, 'mhs' : simpan_dataPerson[i]})

random.shuffle(simpan_dataPerson) 
for i in range(20):
    db.temp.update({"id" : i}, {'$set' : {"dosbing" : simpan_dataPerson[i]}})

random.shuffle(simpan_dataPerson) 
for i in range(20):
    db.temp.update({"id" : i}, {'$set' : {"p1" : simpan_dataPerson[i]}})

random.shuffle(simpan_dataPerson) 
for i in range(20):
    db.temp.update({"id" : i}, {'$set' : {"p2" : simpan_dataPerson[i]}})


