import json
import paho.mqtt.client as mqtt
import threading
from time import sleep
import sys

############################################## GENERATE COORDINATES ########################################
import numpy as np
import osmnx as ox

place = "Aveiro, Aveiro, Portugal"
G = ox.graph_from_place(place, network_type="drive")
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
garbage_nodes = [5208801375, 5244032108, 4961599480, 9764485095, 1801672819]
garbage_coordinates = [(40.6375271, -8.6441449), (40.6433476, -8.6550174), (40.6295116, -8.6599187), (40.6588927, -8.6151015), (40.5740063, -8.5930985)]
# for simulation with obus
garbage_status = [-1, -1, -1, -1, -1]

# for simulation without obus
# garbage_status = [-1, -1, 2, -1, 2]

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

    fig, ax =  ox.plot_graph_route(G, route, route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)

    # fig, ax =  ox.plot_graph_route(G, route[0:30], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[30:60], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[60:90], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[90:120], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[120:150], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[150:180], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[180:210], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)
    # fig, ax =  ox.plot_graph_route(G, route[210:217], route_color='y', route_linewidth=6, node_size=0, orig_dest_size=300)

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

t1.loop_stop()
print("RSU Disconected")

print(garbage_status)

calc_route()

sys.exit(1)
