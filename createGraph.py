import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as et
from collections import OrderedDict

# Parse all nodes in OSM file
# Return a list, whose element is a node dictionary: osmid, x, y, type, name, address
# D:\Important\PFIEV\GIS\Project\Towards-KNN-Search-in-Time-Dependent-Spatial-Databases-Implementation\map\hanoi_bk.osm
def parseXML():
    node_list = []
    data = et.parse(path)
    root = data.getroot()
    for node in root.findall('./node'):
        node_dict = OrderedDict()
        node_dict.fromkeys(['id', 'lat', 'lon', 'type', 'name' 'address'])
        id = int(node.attrib['id'])
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        node_dict['id'] = id
        node_dict['lat'] = lat
        node_dict['lon'] = lon
        node_dict['type'] = None
        node_dict['name'] = None
        node_dict['address'] = None
        for tag in node:
            keys = ['amenity', 'shop', 'leisure', 'name', 'addr:street']
            for key in keys:
                syntax = "field[@k='{}']".format(key)
                find = tag.find(syntax)
                if find is not None:
                    node_dict[key] = find.attrib['v']
                    print(key)
            '''
            amenity = tag.find("field[@k='amenity']")
            shop = tag.find("field[@k='shop']")
            leisure = tag.find("field[@k='leisure']")
            name = tag.find("field[@k='name']")
            addr = tag.find("field[@k='addr:street']")
            if amenity is not None:
                node_dict['type'] = tag.find("field[@k='amenity']").attrib['v']
            elif shop is not None:
                node_dict['type'] = tag.find("field[@k='shop']").attrib['v']
            elif leisure is not None:
                node_dict['type'] = tag.find("field[@k='name']").attrib['v']
            if name is not None:
                node_dict['name'] = tag.find("field[@k='name']").attrib['v']
            if addr is not None:
                node_dict['address'] = tag.find("field[@k='addr:street']").attrib['v']
            '''
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
                if key not in G.nodes[id]:
                    nx.set_node_attributes(G, key, node[key]) # BUG
            continue
    return G


# Save graph to file
def saveGraph():
    G = createGraph()
    nx.write_gpickle(G,'.//graph//graph.gpickle')


# Load graph from file
def loadGraph():
    G = nx.read_gpickle('.//graph//graph.gpickle')
    return G

node_list = parseXML()
G = createGraph()
saveGraph()