import networkx as nx
from createGraph import createGraph

'''
# Các nhãn của đồ thị:
Vertice: (Đang làm):
    osmid
    x: Toạ độ x
    y: Toạ độ y
    amenity: Nơi công cộng. Giá trị có thể là hospital, park,...
    shop: Cửa hàng. Giá trị là tên cửa hàng đó.
    name: Tên địa điểm
    address: Địa chỉ
    # Trong trường hợp vertice là các giao lộ hoặc ngã tư, thì chỉ có 3 nhãn osmid, x, y
Edge:
    osmid
    highway: Loại đường
    oneway: True - False
    length: float
'''

def dnis():
    G = createGraph()

