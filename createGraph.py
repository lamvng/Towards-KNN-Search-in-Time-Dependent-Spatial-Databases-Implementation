import osmnx as ox
import networkx as nx
import os

def createGraph():
    G = ox.graph_from_file('.\map\hanoi_bk.osm')
    return G
