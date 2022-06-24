import osmnx as ox
import networkx as nx
ox.config(log_console=True, use_cache=True)
# define the start and end locations in latlng
start_latlng = (37.78497,-122.43327)
end_latlng = (37.65523737586062, -122.44801590150094)
# location where you want to find your route
place     = 'San Francisco, California, United States'
# find shortest route based on the mode of travel
mode      = 'drive'        # 'drive', 'bike', 'walk'
# find shortest path based on distance or time
optimizer = 'time'        # 'length','time'
# create graph from OSM within the boundaries of some 
# geocodable place(s)
graph = ox.graph_from_place(place, network_type = mode)

print(graph, "AHAHAHAHA")

# find the nearest node to the start location
orig_node = ox.nearest_nodes(graph, X=start_latlng[0], Y=start_latlng[1])
print(orig_node)
# find the nearest node to the end location
dest_node = ox.nearest_nodes(graph, X=end_latlng[0], Y=end_latlng[1])
print(dest_node)

#  find the shortest path
shortest_route = nx.shortest_path(graph,orig_node,dest_node,weight=optimizer)

print(shortest_route)


orig_node = ox.nearest_nodes(G, X=37.78497, Y=-122.43327)

dest_node = ox.nearest_nodes(G, X=37.65523737586062, Y=-122.44801590150094)