from gc import garbage
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



garbage1 = (G.nodes[5208801375]['y'], G.nodes[5208801375]['x'])
garbage2 = (G.nodes[5244032108]['y'], G.nodes[5244032108]['x'])
garbage3 = (G.nodes[4961599480]['y'], G.nodes[4961599480]['x'])
garbage4 = (G.nodes[9764485095]['y'], G.nodes[9764485095]['x'])
garbage5 = (G.nodes[1801672819]['y'], G.nodes[1801672819]['x'])

print(garbage1)
print(garbage2)
print(garbage3)
print(garbage4)
print(garbage5)
