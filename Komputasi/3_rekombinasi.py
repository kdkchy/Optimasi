import pprint
from numpy import prod

my_list = [ [[0.0, 1.0, 3.0], [0.0, 1.0, 3.0], [0.0, 1.0, 3.0], [0.0, 1.0, 3.0]],
            [[1.0, 1.0, 2.0], [1.0, 4.0, 3.0], [1.0, 1.0, 2.0], [1.0, 4.0, 3.0]],
            [[0.0, 2.0, 4.0], [0.0, 2.0, 4.0], [0.0, 2.0, 4.0], [0.0, 2.0, 4.0]],
            [[1.0, 2.0, 3.0], [1.0, 3.0, 1.0], [1.0, 1.0, 4.0], [1.0, 2.0, 2.0]],
            [[1.0, 3.0, 2.0], [1.0, 4.0, 1.0], [1.0, 2.0, 3.0], [1.0, 5.0, 1.0]],
            [[1.0, 4.0, 1.0], [1.0, 1.0, 4.0], [1.0, 3.0, 2.0], [1.0, 5.0, 2.0]],
            [[1.0, 4.0, 2.0], [1.0, 1.0, 1.0], [1.0, 2.0, 2.0], [1.0, 3.0, 2.0]],
            [[1.0, 2.0, 1.0], [1.0, 2.0, 3.0], [1.0, 1.0, 1.0], [1.0, 2.0, 3.0]],
            [[1.0, 3.0, 3.0], [1.0, 3.0, 3.0], [1.0, 4.0, 1.0], [1.0, 5.0, 4.0]],
            [[1.0, 1.0, 1.0], [1.0, 5.0, 1.0], [1.0, 5.0, 3.0], [1.0, 4.0, 1.0]],
            [[1.0, 5.0, 3.0], [1.0, 5.0, 3.0], [1.0, 3.0, 3.0], [1.0, 1.0, 2.0]],
            [[1.0, 2.0, 2.0], [1.0, 2.0, 2.0], [1.0, 3.0, 4.0], [1.0, 5.0, 3.0]],
            [[1.0, 1.0, 4.0], [1.0, 2.0, 1.0], [1.0, 5.0, 2.0], [1.0, 1.0, 1.0]],
            [[1.0, 5.0, 4.0], [1.0, 4.0, 2.0], [1.0, 4.0, 2.0], [1.0, 2.0, 1.0]],
            [[1.0, 4.0, 3.0], [1.0, 5.0, 2.0], [1.0, 4.0, 3.0], [1.0, 1.0, 4.0]],
            [[1.0, 5.0, 1.0], [1.0, 3.0, 4.0], [1.0, 3.0, 1.0], [1.0, 4.0, 2.0]],
            [[1.0, 3.0, 1.0], [1.0, 3.0, 2.0], [1.0, 5.0, 4.0], [1.0, 3.0, 4.0]],
            [[1.0, 5.0, 2.0], [1.0, 1.0, 2.0], [1.0, 2.0, 1.0], [1.0, 3.0, 3.0]],
            [[1.0, 3.0, 4.0], [1.0, 5.0, 4.0], [1.0, 5.0, 1.0], [1.0, 3.0, 1.0]],
            [[0.0, 4.0, 4.0], [0.0, 4.0, 4.0], [0.0, 4.0, 4.0], [0.0, 4.0, 4.0]]]
num = 1
sama = 1
for i in range(20):
    # print()
    temp = my_list[0][0]
    for i in range(19):
        my_list[i][0] = my_list[i+1][0]
    my_list[19][0] = temp  
    for j in range(20):
        temp = my_list[0][1]
        for i in range(19):
            my_list[i][1] = my_list[i+1][1]
        my_list[19][1] = temp  
        for k in range(20):
            temp = my_list[0][2]
            for i in range(19):
                my_list[i][2] = my_list[i+1][2]
            my_list[19][2] = temp 
            for k in range(20):
                temp = my_list[0][3]
                for i in range(19):
                    my_list[i][3] = my_list[i+1][3]
                my_list[19][3] = temp  
                # pprint .pprint(my_list)

                """ALL LOGIC GOES HERE"""
                # print(num)
                # num = num + 1

                for j in range(len(my_list)):
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
                    if f == 1:
                        sama = sama +1
                        print(my_list[data])

                
            # print()

print(sama)
# pprint .pprint(my_list)