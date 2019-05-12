import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as et

# Parse all nodes in OSM file
def parseXML():
    node_list = []
    data = et.parse('.//map//test.osm')
    root = data.getroot()
    for node in root.findall('.//osm//node'):
        node_dict = dict()
        node_dict.fromkeys(['id', 'x', 'y', 'address', 'tag'])
        id = int(node.attrib['id'])
        x = node.attrib['x']
        y = node.attrib['y']
        for tag in root.findall('.//osm//node//tag'):
                tag_dict = dict()
                tag_dict.fromkeys(['amenity', 'shop', 'name'])
                if tag.find("field[@k='amenity']") is not None:
                        amenity = tag.find("field[@k='amenity']").attrib['v']
                        tag_dict['amenity'] = amenity
                if tag.find("field[@k='shop']") is not None:
                        shop = tag.find("field[@k='shop']").attrib['v']
                        tag_dict['shop'] = shop
                if tag.find("field[@k='name']") is not None:
                        name = tag.find("field[@k='name']").attrib['v']
                        tag_dict['name'] = name



                
# Create graph with node type
def createGraph():
    G = ox.graph_from_file('.//map//hanoi_bk.osm')
    return G
