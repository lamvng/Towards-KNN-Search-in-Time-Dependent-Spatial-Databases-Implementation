import osmnx as ox
import networkx as nx
import xml.etree.ElementTree as et


# Parse all nodes in OSM file
# Return a list, whose element is a node dictionary: osmid, x, y, type, name, address
def parseXML():
    node_list = []
    data = et.parse('.//map//hanoi_bk.osm')
    root = data.getroot()
    for node in root.findall('./node'):
        node_dict = dict()
        node_dict.fromkeys(['id', 'lat', 'lon', 'type', 'name' 'address'])
        id = int(node.attrib['id'])
        lat = node.attrib['lat']
        lon = node.attrib['lon']
        node_dict['id'] = id
        node_dict['lat'] = lat
        node_dict['lon'] = lon
        for tag in root.findall('.//osm//node//tag'):
            amenity_value = tag.find("field[@k='amenity']").attrib['v']
            shop_value = tag.find("field[@k='shop']").attrib['v']
            leisure_value = tag.find("field[@k='leisure']").attrib['v']
            name_value = tag.find("field[@k='name']").attrib['v']
            addr_value = tag.find("field[@k='addr:street']").attrib['v']
            if amenity_value is not None:
                node_dict['type'] = amenity_value
            elif shop_value is not None:
                node_dict['type'] = shop_value
            elif leisure_value is not None:
                node_dict['type'] = leisure_value
            if name_value is not None:
                node_dict['name'] = name_value
            if addr_value is not None:
                node_dict['address'] = addr_value
        node_list.append(node_dict)
    return node_list

# Create graph with node type
def createGraph():
    node_list = parseXML()
    osm = ox.graph_from_file('.//map//hanoi_bk.osm') # Return a networkx graph
    G = osm
    return G