from numpy import prod
import json
import pprint

list = [
    [[1,2,4],[1,3,1],[1,2,4],[0,2,4]],
    [[1,3,1],[1,2,4],[0,3,1],[0,3,1]],
    [[1,3,2],[0,3,2],[0,3,3],[0,3,3]],
    [[0,3,3],[0,3,3],[0,3,2],[0,3,2]]
    ]
# print("Data : {}".format(list))

hasil = []

for j in range(len(list)):
    item = {}
    # menghitung data pertama pada list
    data = j

    # menghitung status
    hx = (list[data][0][0]+list[data][1][0]+list[data][2][0]+list[data][3][0])/4

    # menghitung jam dan hari
    YZ = []
    for i in range(4):
        result = (3*list[data][i][1]+5*list[data][i][2])
        YZ.append(result)
    YZprod = prod(YZ)
    print("data ke-{}".format(data+1))
    print("Hx = {}".format(hx))
    print("yz1-4 = {}".format(YZ))
    print("YZ = {}".format(YZprod))

    for i in range(4):
        if (YZprod**(1/4) == 3*list[data][0][1]+5*list[data][0][2]):
            a = 0
        else:
            a = 1
    print(a)

    f = 1/(a + hx + 1)
    print(f)

    print()
    item.update([('status' , hx), ('jam dan hari' , YZ), ('hasil' , YZprod), ('kasus akar' , a),("fitness",f)])
    hasil.append(item)


# json_object = json.loads(hasil)
# json_formatted_str = json.dumps(json_object, indent=2)
print(hasil)
print()
hasil.insert(0, hasil[:])
pp = pprint.PrettyPrinter(width=41, compact=True)
# pp.pprint(hasil)