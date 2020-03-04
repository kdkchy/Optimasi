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


for i in range(20):
    dataTable = []

    dataTable.append(a.get('mhs'))
    dataTable.append(a.get('dosbing'))
    dataTable.append(a.get('p1'))
    dataTable.append(a.get('p2'))

    random.shuffle(dataTable)

    my_list.append(dataTable)

pprint.pprint(my_list)
print()


for i in range(20):
    j = i + 1
    simpan_dataPerson.append(ambil_dataPerson[0][str(j)])