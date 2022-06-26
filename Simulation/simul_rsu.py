import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import sys
import matplotlib.pyplot as plt

############################################## GENERATE COORDINATES ########################################
import numpy as np
import osmnx as ox

place = "Aveiro, Portugal"
#G = ox.graph_from_place(place, network_type="drive")
G = ox.graph_from_point((40.641250894859645, -8.65358752576108), dist=3000, network_type="drive")

Gp = ox.project_graph(G)
print(list(G))

points = ox.utils_geo.sample_points(ox.get_undirected(Gp), n=100)
X = points.x.values
Y = points.y.values
X0 = X.mean()
Y0 = Y.mean()

nodes, dists = ox.nearest_nodes(Gp, X, Y, return_dist=True)

node = ox.nearest_nodes(Gp, X0, Y0)

            #   node            coordinates     status
garbage_nodes = [26019653, 1272483346, 1485115748, 1563067182, 1709796842, 4874785502, 9840860673]

garbage_coordinates = [(40.631709, -8.6875641), (40.6258137, -8.6448027), (40.639794, -8.6435776), (40.621431, -8.6291841), (40.6669451, -8.6258256), (40.6451389, -8.6435942), (40.6327564, -8.6374649)]
# for simulation with obus
garbage_status = [-1, -1, -1, -1, -1, -1, -1]

# for simulation without obus
#garbage_status = [-1, -1, 3, -1, -1, 4, -1]
#garbage_status = [-1, 4, 3, -1, -1, 4, -1]

##############################################################################################################

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/denm")


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    
    print('Topic: ' + msg.topic)
    print('Message' + json.dumps(message))

    lat = message["fields"]["denm"]["management"]["eventPosition"]["latitude"]
    long = message["fields"]["denm"]["management"]["eventPosition"]["longitude"]
    
    
    index = garbage_coordinates.index((lat, long))
    print(index)

    garbage_status[index] = message["fields"]["denm"]["situation"]["eventType"]["subCauseCode"]


def calc_route():
    route=[]
    list_routes=[]

    for idx, status in enumerate(garbage_status):
        if status>0:
            list_routes.append(garbage_nodes[idx])

    while len(list_routes)-1>0:
        route_a = ox.shortest_path(G, list_routes[0], list_routes[1], weight="length")
        route += route_a
        list_routes.pop(0)

    print(len(route))

    fig, ax =  ox.plot_graph_route(G, route, route_color='y', route_linewidth=6, node_size=0, show=False, close=False)

    for x in garbage_coordinates:
        plt.plot(x[1],x[0], marker="o", markersize=10, markeredgecolor="red", markerfacecolor="green", zorder=10)

    plt.show()


rsu = mqtt.Client()
rsu.on_connect = on_connect
rsu.on_message = on_message
rsu.connect("192.168.98.11", 1883, 60)

t1 = threading.Thread(target=rsu.loop_start)

t1.start()

t1.join()

while(True):
    f = open("end_simul.txt", "r")
    if f.read()=="True":
        break

print("Simulation ended!")

#t1.loop_stop
#print("RSU Disconected")

print(garbage_status)

calc_route()

sys.exit(1)
