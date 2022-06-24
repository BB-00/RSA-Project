import osmnx as ox
import networkx as nx

G = ox.graph_from_place('Portugal', network_type='drive')


# start_latlng = (40.9257, -8.54123)
# end_latlng = (40.378484, -8.453572)

# optimizer = 'time'

# orig_node = ox.nearest_nodes(G, X=start_latlng[0], Y=start_latlng[1])
# print(orig_node)
# # find the nearest node to the end location
# dest_node = ox.nearest_nodes(G, X=end_latlng[0], Y=end_latlng[1])
# print(dest_node)

# shortest_route = nx.shortest_path(G,orig_node,dest_node,weight=optimizer)

ox.plot_graph(G)