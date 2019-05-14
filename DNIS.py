import networkx as nx
import osmnx as os 
from createGraph import loadGraph
# from createGraph import createGraph

'''
# Graph Attributes:
Node: (Not done):
    osmid
    x: Coordinate
    y: Coordinate
    tag: Type
Edge: 
    osmid
    highway: Road type
    oneway: True - False
    length: float
'''

G = loadGraph()

# write another funtion to calcule time travel with time dependece graph

def cal_time_travel(G, vi, vj, t_vi = 0):
    """
    G : graph
    vi : departure
    vi : destination
    t_vi : departure time from vi
    """
    
    time_travel = 0
    dict_temp = G.get_edge_data(vi,vj)
    time_travel = dict_temp[0]["length"]

    return time_travel

def DNIS(Graph, query_location, time_start, type_of_interest, k):
    
    """
    Initialise :
                S: set of explored nodes
                T: set of node where T = list G.node - S
                lv: fastest time travel from q
                vi: last node added to S
                NNs: array of kNN
                tt: set of fastest time travel
    """
    
    G = Graph
    q = query_location
    

    # G = nx.Graph()
    # q = G.node[1]

    # init NNs and tt
    NNs = []
    tt = []
    # init set S
    S = []
    S.append(q)
    # init  T = G.node - S
    T = list(G.node)
    T.remove(q)
    # init thr first vi
    vi = q

    # init lv of nodes
    nx.set_node_attributes(G, -1, "lv")
    G.node[q]["lv"] = 0
    
    # loop to find kNN
    leuleu = 0
    while len(S) != len(list(G.node)):
        # explore neighbors of vi
        for vj in G.neighbors(vi):
            time_travel_temp = cal_time_travel(G,vi,vj)
            fe_tvi = G.node[vi]["lv"] + time_travel_temp
            if G.node[vj]["lv"] < 0:
                G.node[vj]["lv"] = fe_tvi
            else: 
                G.node[vj]["lv"] = min(G.node[vj]["lv"],fe_tvi)
                print ("G.node[",vi,"][lv]:",G.node[vj]["lv"])
        # add the newest vi to S
        print("end loop ",leuleu)
        leuleu += 1
        min_lv = -1
        w = T[0]
        for vj in T:
            if G.node[vj]["lv"] > 0:
                if min_lv < 0:
                    min_lv = G.node[vj]["lv"]
                    w = vj
                if min_lv > G.node[vj]["lv"]:
                    min_lv = G.node[vj]["lv"]
                    w = vj
        S.append(w)
        if len(T) != 0:
            T.remove(w)
        vi = w
        # confirm type_of_interest
        try:
            if G.node[vi]["type"] == type_of_interest :
                NNs.append(vi)
                tt.append(G.node[vi]["lv"])
                print("----------------------------------find a new object----------------------------------")
            if len(NNs) >= k:
                break
        except KeyError:
            continue

    return NNs, tt
# G = nx.Graph()
"""
#### test data
print(G.edges)
print(G.get_edge_data(1904391952, 1904391935))
dic = G.get_edge_data(1904391952, 1904391935)
print(dic[0]["length"])

"""

#### test DNIS
for i in G.neighbors(6413899095):
    print(i)
NNs, tt = DNIS(G, 6413899095, 0, "restaurant", 2)

print("kNN: ",NNs)
print("fastest time travel: ",tt)


for i in G.neighbors(446044222):
    print(i)
print ("-------- done --------")