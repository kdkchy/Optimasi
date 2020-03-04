from numpy import prod
import numpy as np
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


ambil_dataPerson = list(db.dataPerson.find({"_id":ObjectId("5e5e0385ccabaf6a2c4a160a")}))
simpan_dataPerson = []


for i in range(len(ambil_dataPerson)):
    dataTable = []

    a = ambil_dataPerson[i]
    dataTable.append(a.get('senin_08'))
    dataTable.append(a.get('senin_10'))
    dataTable.append(a.get('senin_13'))
    dataTable.append(a.get('senin_15'))
    dataTable.append(a.get('selasa_08'))
    dataTable.append(a.get('selasa_10'))
    dataTable.append(a.get('selasa_13'))
    dataTable.append(a.get('selasa_15'))
    dataTable.append(a.get('rabu_08'))
    dataTable.append(a.get('rabu_10'))
    dataTable.append(a.get('rabu_13'))
    dataTable.append(a.get('rabu_15'))
    dataTable.append(a.get('kamis_08'))
    dataTable.append(a.get('kamis_10'))
    dataTable.append(a.get('kamis_13'))
    dataTable.append(a.get('kamis_15'))
    dataTable.append(a.get('jumat_08'))
    dataTable.append(a.get('jumat_10'))
    dataTable.append(a.get('jumat_13'))
    dataTable.append(a.get('jumat_15'))

    random.shuffle(dataTable)

    simpan_dataPerson.append(dataTable)


for i in range(20):
    print(simpan_dataPerson[0][i])

# my_array = np.array(simpan_dataPerson)
# print(my_array)

# trns = np.transpose(simpan_dataPerson)
# pprint.pprint(trns)

# dataTable = []

# item= []
# for i in simpan_dataPerson[0]:
#     item.append(i)
# dataTable.append(item)

# item= []
# for i in simpan_dataPerson[0]:
#     item.append(i)
# dataTable.append(item)

# item= []
# for i in simpan_dataPerson[0]:
#     item.append(i)
# dataTable.append(item)

# item= []
# for i in simpan_dataPerson[0]:
#     item.append(i)
# dataTable.append(item)


# my_array = np.array(dataTable)
# print(my_array)

# print()
# arr1_transpose = np.transpose(my_array)
# print(arr1_transpose)

# my_array = ([[111],[222]],
#             [[333],[444]],
#             [[555],[666]],
#             [[777],[888]])
# print(np.transpose(my_array))


# my_array = np.array([[[1,2],[2,2]],[[3,3],[3,4]]])
# print(np.transpose(my_array))

# a = np.array([
#     [[1,2,3],[1,2,3],[1,2,3],[1,2,3]],
#     [[2,3,4],[2,3,4],[2,3,4],[2,3,4]],
#     [[3,4,5],[3,4,5],[3,4,5],[3,5]]
# ])
# print(np.transpose(a))
# print()

# a = np.array('i',[
#     [[1,2,3],[2,3,4],[3,4,5]],
#     [[1,2,3],[2,3,4],[3,4,5]],
#     [[1,2,3],[2,3,4],[3,5]],
#     [[1,2,3],[2,3,4],[3,4,5]]
# ])
# print(np.transpose(a))
