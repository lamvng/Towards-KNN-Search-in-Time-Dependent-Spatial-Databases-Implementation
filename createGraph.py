import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as et
import os
from collections import OrderedDict
from distance import calGeoDistance
from geopy.point import Point

os.chdir(os.getcwd())
# Parse all nodes in OSM file
# Return a list, whose element is a node dictionary: osmid, x, y, type, name, address
# D:\Important\PFIEV\GIS\Project\Towards-KNN-Search-in-Time-Dependent-Spatial-Databases-Implementation\map\hanoi_bk.osm
def parseXML():
    node_list = []
    data = et.parse('.//map//hanoi_bk.osm')
    root = data.getroot()
    keys = ['amenity', 'shop', 'leisure', 'name', 'addr:street', 'highway', 'tourism'] # Key in tag, in the osm file
    for node in root.findall('./node'):
        node_dict = OrderedDict()
        node_dict.fromkeys(['id', 'lat', 'lon', 'type', 'name' 'address', 'obj']) # Key in dict
        id = int(node.attrib['id'])
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        node_dict['id'] = id
        node_dict['lat'] = lat
        node_dict['lon'] = lon
        node_dict['type'] = None
        node_dict['name'] = None
        node_dict['address'] = None
        node_dict['obj'] = None
        for tag in node.iter('tag'):
            attrib = tag.attrib
            for key in keys:
                if key == attrib['k']:
                    if key == 'name':
                        node_dict['name'] = attrib['v']
                    elif key in ['amenity', 'shop', 'leisure', 'highway', 'tourism']:
                        node_dict['type'] = attrib['v']
                    elif key == 'addr:street':
                        node_dict['address'] = attrib['v']
        node_list.append(node_dict)
    return node_list


# Return all nodes of interest
def findPoI(G):
    poi_list = []
    for node in G.nodes():
        if nx.is_isolate(G, node) == True:
            poi_list.append(node)
    return poi_list


# Calculate the distance from POI to roads, return the nearest one
# poi: G node
def distance(poi_list, G):
    for poi in poi_list:
        # lat = y, lon = x
        point = Point(latitude = G.nodes[poi]['y'], longitude = G.nodes[poi]['x'])
        distance_list = []
        for (u,v) in G.edges():
            distance_dict = OrderedDict()
            distance_dict.fromkeys(['point1', 'point2', 'distance'])
            point1 = Point(latitude = G.nodes[u]['y'], longitude = G.nodes[u]['x'])
            point2 = Point(latitude = G.nodes[v]['y'], longitude = G.nodes[v]['x'])
            d = calGeoDistance(point, point1, point2)
            distance_dict['point1'] = u # Node 1 ID
            distance_dict['point2'] = v # Node 2 ID
            distance_dict['distance'] = d
            distance_list.append(distance_dict)

        min = distance_list[0] # min = dict
        for elem in distance_list:
            if elem['distance'] < min['distance']:
                min = elem

        # obj: List of nearest poi, in the node's attributes
        obj_list_1 = G.nodes[min['point1']]['obj'] # Extract obj of node 1, whose distance to poi is min
        obj_list_2 = G.nodes[min['point2']]['obj'] # Extract obj of node 2, whose distance to poi is min
        if obj_list_1 == None:
            obj_list_1 = [poi]
        else:
            obj_list_1.append(poi)
        if obj_list_2 == None:
            obj_list_2 = [poi]
        else:
            obj_list_2.append(poi)

        G.add_node(min['point1'], obj = obj_list_1)
        G.add_node(min['point2'], obj = obj_list_2)
    return G


# Create graph with node type
def createGraph():
    node_list = parseXML()
    G = ox.graph_from_file('.//map//hanoi_bk.osm', retain_all = True) # Return a networkx graph
    keys = ['type', 'name', 'address', 'obj']
    for node in node_list:
        id = node['id']
        if G.has_node(id):
            for key in keys:
                if key not in G.nodes[id] and key in node:
                    if key == 'type':
                        G.add_node(id, type = node['type'])
                    if key == 'name':
                        G.add_node(id, name = node['name'])
                    if key == 'address':
                        G.add_node(id, address = node['address'])
                if key == 'obj':
                    G.add_node(id, obj = node['obj'])


            continue

    poi_list = findPoI(G)
    G = distance(poi_list, G)
    return G



# Save graph to file
def saveGraph():
    G = createGraph()
    nx.write_gpickle(G,'.//graph//graph.gpickle')


# Load graph from file
# D:\Important\PFIEV\GIS\Project\Towards-KNN-Search-in-Time-Dependent-Spatial-Databases-Implementation\graph\graph.gpickle
def loadGraph():
    G = nx.read_gpickle('.//graph//graph.gpickle')
    return G


saveGraph()

# G = loadGraph()