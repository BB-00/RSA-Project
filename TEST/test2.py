import osmnx as ox
import networkx as nx



#G = ox.graph_from_place('Piedmont, CA, USA', network_type='drive')

start_latlng = (37.78497,-122.43327)
end_latlng = (37.78071,-122.41445)

place     = 'San Francisco, California, United States'
# find shortest route based on the mode of travel
mode      = 'drive'        # 'drive', 'bike', 'walk'
# find shortest path based on distance or time
optimizer = 'time'        # 'length','time'
# create graph from OSM within the boundaries of some 
# geocodable place(s)
graph = ox.graph_from_place(place, network_type = mode)


route = nx.shortest_path(graph, start_latlng, end_latlng)
fig, ax = ox.plot_graph_route(G, route, route_linewidth=6, node_size=0, bgcolor='k')