import pprint

my_list = [ [[1],[2],[3]],
            [[4],[5],[6]],
            [[7],[8],[9]],
            [[10],[11],[12]] ]




rotasi = [ [[1],[2],[my_list[1][2]]],
            [[4],[5],[my_list[2][2]]],
            [[7],[8],[my_list[3][2]]],
            [[10],[11],[my_list[0][2]]] ]

for i in range(4):
    my_list[i][2]=my_list[i-1][2]
    print(i)

pprint .pprint(my_list)