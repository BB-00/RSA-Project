import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

global brk1
global brk2
global brk3
global brk4

brk1 = 0
brk2 = 0
brk3 = 0
brk4 = 0


############################################# GENERATE COORDINATES ########################################
import numpy as np
import osmnx as ox
import random

place = "Aveiro, Portugal"
#G = ox.graph_from_place(place, network_type="drive")
G = ox.graph_from_point((40.641250894859645, -8.65358752576108), dist=3000, network_type="drive")

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

rc = ['r', 'y', 'c', 'g']
fig, ax = ox.plot_graph_routes(G, list_routes_nodes, route_colors=rc, route_linewidth=6, node_size=0, show=False, close=False)

list_routes_coordinates=[]
for route in range(4):
    route = list_routes_nodes[i]
    list_coordinates=[]
    for node in route:
        print("coordenadas no 1", G.nodes[node]['y'], G.nodes[node]['x'])
        list_coordinates.append([G.nodes[node]['y'], G.nodes[node]['x']])
    list_routes_coordinates.append(list_coordinates)
    print(list_coordinates)

#############################################################################################################

########################################## CHECK DISTANCES from CANS ########################################

import math
import matplotlib.pyplot as plt

coord_garbage_cans = [(40.631709, -8.6875641), (40.6258137, -8.6448027), (40.639794, -8.6435776), (40.621431, -8.6291841), (40.6669451, -8.6258256), (40.6451389, -8.6435942), (40.6327564, -8.6374649)]

for coord in coord_garbage_cans:
    plt.plot(coord[1],coord[0], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green", zorder=10)

plt.show()


def proximity(coord):
    for idx, x in enumerate(coord_garbage_cans):
        if math.dist([x[0], x[1]],  [coord[0], coord[1]]) < 0.01:
            return (True, idx)
    return (False, -1)

##############################################################################################################


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/cam")
    client.subscribe("vanetza/out/denm")


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    
    print('Topic: ' + msg.topic)
    print('Message' + json.dumps(message))


subcause1 = random.randint(1,4)
subcause2 = random.randint(1,4)
subcause3 = random.randint(1,4)
subcause4 = random.randint(1,4)
subcause5 = random.randint(1,4)
subcause6 = random.randint(1,4)
subcause7 = random.randint(1,4)

list_subcauses = [subcause1, subcause2, subcause3, subcause4, subcause5, subcause6, subcause7]

def generate(client, id):

    if not len(list_routes_coordinates[id-1]):
        print("Car ", id, " as finished its route!")

    else:
        coord = list_routes_coordinates[id-1].pop(0)
        f = open('../vanetza/examples/in_cam.json')
        m = json.load(f)
        m["latitude"] = coord[0]
        m["longitude"] = coord[1]
        m["stationID"] = id+2
        m = json.dumps(m)
        client.publish("vanetza/in/cam",m)
        f.close()
        ret = proximity(coord)
        if ret[0] is True:
            f = open('../vanetza/examples/in_denm.json')
            m = json.load(f)
            m["management"]["eventPosition"]["latitude"] = coord_garbage_cans[ret[1]][0]
            m["management"]["eventPosition"]["longitude"] = coord_garbage_cans[ret[1]][1]
            m["situation"]["eventType"]["subCauseCode"] = list_subcauses[ret[1]]
            mes = json.dumps(m)
            client.publish("vanetza/in/denm",mes)
            f.close()
    
        sleep(0.5)


car1 = mqtt.Client()
car1.on_connect = on_connect
car1.on_message = on_message
car1.connect("192.168.98.111", 1883, 60)

car2 = mqtt.Client()
car2.on_connect = on_connect
car2.on_message = on_message
car2.connect("192.168.98.112", 1883, 60)

car3 = mqtt.Client()
car3.on_connect = on_connect
car3.on_message = on_message
car3.connect("192.168.98.113", 1883, 60)

car4 = mqtt.Client()
car4.on_connect = on_connect
car4.on_message = on_message
car4.connect("192.168.98.114", 1883, 60)


t1 = threading.Thread(target=car1.loop_start)
t2 = threading.Thread(target=car2.loop_start)
t3 = threading.Thread(target=car3.loop_start)
t4 = threading.Thread(target=car4.loop_start)

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()


f = open("end_simul.txt", "w")
f.write("False")
f.close()

while(True):
    if not len(list_routes_coordinates[0]) and not len(list_routes_coordinates[1]) and not len(list_routes_coordinates[2]) and not len(list_routes_coordinates[3]):
        break
    else:
        generate(car1, 1)
        generate(car2, 2)
        generate(car3, 3)
        generate(car4, 4)

car1.loop_stop()
print("Car 1 disconnected")

car2.loop_stop()
print("Car 2 disconnected")

car3.loop_stop()
print("Car 3 disconnected")

car4.loop_stop()
print("Car 4 disconnected")

f = open("end_simul.txt", "w")
f.write("True")
f.close()