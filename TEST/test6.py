import math

coordinates = [(-8.5611055, 40.573359), (-8.5628781, 40.5706289), (-8.5688327, 40.5691592), (-8.5690897, 40.569113), (-8.5710666, 40.5700192), (-8.5734596, 40.5714269), (-8.5736954, 40.5715956), (-8.5737525, 40.5716359), (-8.5738483, 40.5717124), (-8.5738971, 40.5717634), (-8.5784589, 40.5759076), (-8.5786158, 40.5761523), (-8.5786123, 40.5761951), (-8.5787086, 40.5762944)]

garbage_can = [(40.64185398601324, -8.653554472381604)]

min= 1234123123

for x in coordinates:
    print(x)

    if(math.dist( [x[1] , x[0]] , [garbage_can[0][0] , garbage_can[0][1]] ) )< min:
        min = math.dist([x[1],x[0]],[garbage_can[0][0] , garbage_can[0][1] ] )
        store = x

print(min)
print(store)


#inside if / if dist < Number, publishes denm to the client, block the others