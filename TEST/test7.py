import numpy as np
import osmnx as ox

place = "Aveiro, Aveiro, Portugal"
G = ox.graph_from_place(place, network_type="drive")
Gp = ox.project_graph(G)
print(Gp)

points = ox.utils_geo.sample_points(ox.get_undirected(Gp), n=100)
X = points.x.values
Y = points.y.values
X0 = X.mean()
Y0 = Y.mean()

nodes, dists = ox.nearest_nodes(Gp, X, Y, return_dist=True)

node = ox.nearest_nodes(Gp, X0, Y0)

orig = list(G)[0]
dest = list(G)[120]
route = ox.shortest_path(G, orig, dest, weight="length")

list=[]
for x in route:
    print("coordenadas no 1", G.nodes[x]['x'], G.nodes[x]['y'])
    list.append([G.nodes[x]['x'], G.nodes[x]['y']])

print(route)

print(list)