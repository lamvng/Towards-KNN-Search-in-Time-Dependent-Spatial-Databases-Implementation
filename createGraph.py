import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as et
from collections import OrderedDict

# Parse all nodes in OSM file
# Return a list, whose element is a node dictionary: osmid, x, y, type, name, address
# D:\Important\PFIEV\GIS\Project\Towards-KNN-Search-in-Time-Dependent-Spatial-Databases-Implementation\map\hanoi_bk.osm
def parseXML():
    node_list = []
    data = et.parse('.//map//hanoi_bk.osm')
    root = data.getroot()
    keys = ['amenity', 'shop', 'leisure', 'name', 'addr:street'] # Key in tag, in the osm file
    for node in root.findall('./node'):
        node_dict = OrderedDict()
        node_dict.fromkeys(['id', 'lat', 'lon', 'type', 'name' 'address']) # Key in dict
        id = int(node.attrib['id'])
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        node_dict['id'] = id
        node_dict['lat'] = lat
        node_dict['lon'] = lon
        node_dict['type'] = None
        node_dict['name'] = None
        node_dict['address'] = None
        for tag in node.iter('tag'):
            attrib = tag.attrib
            for key in keys:
                if key == attrib['k']:
                    if key == 'name':
                        node_dict['name'] = attrib['v']
                    elif key in ['amenity', 'shop', 'leisure']:
                        node_dict['type'] = attrib['v']
                    elif key == 'addr:street':
                        node_dict['address'] = attrib['v']
        node_list.append(node_dict)
    return node_list

# Create graph with node type
def createGraph():
    node_list = parseXML()
    G = ox.graph_from_file('.//map//hanoi_bk.osm', retain_all = True) # Return a networkx graph
    keys = ['type', 'name', 'address']
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
            continue
    return G


# Save graph to file
def saveGraph():
    G = createGraph()
    nx.write_gpickle(G,'.//graph//graph.gpickle')


# Load graph from file
def loadGraph():
    G = nx.read_gpickle('D:\Important\PFIEV\GIS\Project\Towards-KNN-Search-in-Time-Dependent-Spatial-Databases-Implementation\graph\graph.gpickle')
    return G

node_list = parseXML()
G = createGraph()
saveGraph()
