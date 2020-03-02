from numpy import prod
from pymongo import MongoClient
import os

import json
import pprint

mongodb_host = os.environ.get('MONGO_HOST', 'localhost')
mongodb_port = int(os.environ.get('MONGO_PORT', '27017'))
client = MongoClient(mongodb_host, mongodb_port)   
db = client.optimasi


result = list(db.dataPerson.find())
data = []

for i in range(len(result)):
    item = []

    a = result[i]
    item.append(a.get('mhs'))
    item.append(a.get('dosbing'))
    item.append(a.get('p1'))
    item.append(a.get('p2'))

    data.append(item)


print(data)

