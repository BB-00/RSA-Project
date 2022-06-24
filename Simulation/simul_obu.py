import json
import paho.mqtt.client as mqtt
import threading
from time import sleep



############################################## GENERATE COORDINATES ########################################
import numpy as np
import osmnx as ox
import random

place = "Aveiro, Aveiro, Portugal"
G = ox.graph_from_place(place, network_type="drive")

print(list(G))

Gp = ox.project_graph(G)

points = ox.utils_geo.sample_points(ox.get_undirected(Gp), n=100)
X = points.x.values
Y = points.y.values
X0 = X.mean()
Y0 = Y.mean()

nodes, dists = ox.nearest_nodes(Gp, X, Y, return_dist=True)

node = ox.nearest_nodes(Gp, X0, Y0)

list_start_end=[]
list_routes_nodes=[]

for i in range(4):
    orig = random.randint(0, len(list(G)))
    dest = random.randint(0, len(list(G)))

    list_start_end.append((list(G)[orig], list(G)[dest]))
    route = ox.shortest_path(G, list_start_end[i][0], list_start_end[i][1], weight="length")
    list_routes_nodes.append(route)

list_routes_coordinates=[]
for route in list_routes_nodes:
    list_coordinates=[]
    for node in route:
        print("coordenadas no 1", G.nodes[node]['y'], G.nodes[node]['x'])
        list_coordinates.append([G.nodes[node]['y'], G.nodes[node]['x']])
    list_routes_coordinates.append(list_coordinates)
    print(list_coordinates)

##############################################################################################################

########################################## CHECK DISTANCES ####################################################

# import math

# coordinates = [(-8.5611055, 40.573359), (-8.5628781, 40.5706289), (-8.5688327, 40.5691592), (-8.5690897, 40.569113), (-8.5710666, 40.5700192), (-8.5734596, 40.5714269), (-8.5736954, 40.5715956), (-8.5737525, 40.5716359), (-8.5738483, 40.5717124), (-8.5738971, 40.5717634), (-8.5784589, 40.5759076), (-8.5786158, 40.5761523), (-8.5786123, 40.5761951), (-8.5787086, 40.5762944)]
# #                               0%                       25%                        50%                       75%                     100%
# coord_garbage_can = [(40.6375271, -8.6441449), (40.6433476, -8.6550174), (40.6295116, -8.6599187), (40.6588927, -8.6151016), (40.5740063, -8.5930985)]

# min= 1234123123

# for x in coordinates:
#     print(x)

#     if(math.dist( [x[0] , x[1]] , [coord_garbage_can[0][0] , coord_garbage_can[0][1]] ) ) < min:
#         min = math.dist([x[0],x[1]],[coord_garbage_can[0][0] , coord_garbage_can[0][1] ] )
#         store = x

# print(min)
# print(store)


#inside if / if dist < Number, publishes denm to the client, block the others

##############################################################################################################


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")
    #client.subscribe("vanetza/out/denm")
    # ...


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    
    print('Topic: ' + msg.topic)
    print('Message' + json.dumps(message))

    # lat = message["latitude"]
    # ...


def generate(client, id):
    f = open('../vanetza/examples/in_cam.json')
    m = json.load(f)
    coord = list_routes_coordinates[id].pop(0)
    m["latitude"] = coord[0]
    m["longitude"] = coord[1]
    m = json.dumps(m)
    client.publish("vanetza/in/cam",m)
    # if proximity(coord) is True:
    #     print()
    
    
    f.close()
    sleep(1)



carro1 = mqtt.Client()
carro1.on_connect = on_connect
carro1.on_message = on_message
carro1.connect("192.168.98.111", 1883, 60)

carro2 = mqtt.Client()
carro2.on_connect = on_connect
carro2.on_message = on_message
carro2.connect("192.168.98.112", 1883, 60)

carro3 = mqtt.Client()
carro3.on_connect = on_connect
carro3.on_message = on_message
carro3.connect("192.168.98.113", 1883, 60)

carro4 = mqtt.Client()
carro4.on_connect = on_connect
carro4.on_message = on_message
carro4.connect("192.168.98.114", 1883, 60)


threading.Thread(target=carro1.loop_forever).start()
threading.Thread(target=carro2.loop_forever).start()
threading.Thread(target=carro3.loop_forever).start()
threading.Thread(target=carro4.loop_forever).start()



while(True):
    generate(carro1, 1)
    generate(carro2, 2)
    generate(carro3, 3)
    generate(carro4, 4)