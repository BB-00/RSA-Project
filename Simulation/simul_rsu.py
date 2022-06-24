from gc import garbage
import json
import paho.mqtt.client as mqtt
import threading
from time import sleep

############################################## GENERATE COORDINATES ########################################
import numpy as np
import osmnx as ox

place = "Aveiro, Aveiro, Portugal"
G = ox.graph_from_place(place, network_type="drive")

# print(list(G))

Gp = ox.project_graph(G)

points = ox.utils_geo.sample_points(ox.get_undirected(Gp), n=100)
X = points.x.values
Y = points.y.values
X0 = X.mean()
Y0 = Y.mean()

nodes, dists = ox.nearest_nodes(Gp, X, Y, return_dist=True)

node = ox.nearest_nodes(Gp, X0, Y0)

            #   node            coordinates     status
garbage = [(5208801375, (40.6375271, -8.6441449), -1), (5244032108, (40.6433476, -8.6550174), -1), (4961599480,(40.6295116, -8.6599187), -1), (9764485095, (40.6588927, -8.6151016), -1), (1801672819,(40.5740063, -8.5930985),-1)]

##############################################################################################################

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("vanetza/out/denm")


# É chamada automaticamente sempre que recebe uma mensagem nos tópicos subscritos em cima
def on_message(client, userdata, msg):
    message = json.loads(msg.payload.decode('utf-8'))
    
    print('Topic: ' + msg.topic)
    print('Message' + json.dumps(message))

    # lat = message["latitude"]
    # ...




# def calc_route():
#     print()


rsu = mqtt.Client()
rsu.on_connect = on_connect
rsu.on_message = on_message
rsu.connect("192.168.98.11", 1883, 60)

t1 = threading.Thread(target=rsu.loop_forever)

t1.start()

t1.join()

while(True):
    # calc_route()
    a=0