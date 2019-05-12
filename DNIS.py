import networkx as nx
from createGraph import createGraph

'''
# Các nhãn của đồ thị:
Vertice: (Đang làm):
    osmid
    lat: Latitude.
    lon: Longtitude.
    type: Kiểu địa điểm. Giá trị là bank, hospital, park, shop...
    name: Tên.
    address: Địa chỉ.
    # Trong trường hợp vertice là các giao lộ hoặc ngã tư, thì chỉ có 3 nhãn osmid, x, y
Edge:
    osmid
    highway: Loại đường.
    oneway: True - False.
    length: float.
'''

def dnis():
    G = createGraph()

