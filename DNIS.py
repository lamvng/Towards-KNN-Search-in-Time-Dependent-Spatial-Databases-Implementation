import networkx as nx
from createGraph import loadGraph

'''
# Các nhãn của đồ thị:
Vertices:
    osmid
    x
    y
    type: Kiểu địa điểm. Giá trị là bank, hospital, park, shop...
    name: Tên.
    address: Địa chỉ.
    # Tuỳ node, có những node là giao lộ, ngã tư, thì type, name và address là None.
Edges:
    osmid
    highway: Loại đường.
    oneway: True - False.
    length: float.
'''

def dnis():
    G = loadGraph()

