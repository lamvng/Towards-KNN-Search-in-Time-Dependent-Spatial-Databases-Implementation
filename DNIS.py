import os
import io
import osmnx as ox
import networkx as nx
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

def writeOnLine (y,x,osmid,typeObj,name,address,obj,lv):
    newline = 'y: ' + str(y) + ', x: ' + str(x) + ', osmid: ' + str(osmid) + ', type: ' + str(typeObj) + ', name: ' + str(name) 
    newline = newline + ', address: ' + str(address) + ', obj: ' + str(obj) + ', time travel: ' + str(lv) + '\n'
    return newline

def writeFileResult(fileNameWrite,NNs):
    fw = open(fileNameWrite,'w',encoding="utf-8")
    
    for i in range(len(NNs)):
        y = G.node[NNs[i]]["y"]
        x = G.node[NNs[i]]["x"]
        osmid = G.node[NNs[i]]["osmid"]
        typeObj =  G.node[NNs[i]]["type"]
        name = G.node[NNs[i]]["name"]
        address = G.node[NNs[i]]["address"]
        obj = G.node[NNs[i]]["obj"]
        lv = G.node[NNs[i]]["lv"]
        newline = writeOnLine(y,x,osmid,typeObj,name,address,obj,lv)
        newline =  'dia diem ' + str(i+1) + ' : ' + newline 
        fw.write(newline)
    fw.close
    return

def DNIS(Graph, query_location, time_start, type_of_interest, k):
    
    """
    Initialise :
                S: set of explored nodes
                T: set of node where T = list G.node - S
                lv: fastest time travel from q
                vi: last node added to S
                NNs: array of kNN
    """
    
    G = Graph
    q = query_location
    

    # G = nx.Graph()
    # q = G.node[1]

    # init NNs 
    NNs = []
    # init set S
    S = []
    S.append(q)
    # init  T = G.node - S
    T = list(G.node)
    T.remove(q)
    # init thr first vi
    vi = q
    Neighbor_of_q = list(G.neighbors(q))
    if len(Neighbor_of_q) == 0:
        for i in G.nodes:
            if G.node[i]["obj"] != None:
                for j in G.node[i]["obj"]:
                    if G.node[q]["osmid"] == j:
                        vi = G.node[i]["osmid"]
                        break

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
            Gnode = []
            Gnode = list(G.node[vi]["obj"]) 
            for i in Gnode:
                if G.node[i]["type"] == type_of_interest and G.node[i]["osmid"] != q:
                    G.node[i]["lv"] = G.node[vi]["lv"]
                    NNs.append(i)
                    NNs =  list(set(NNs))
                    print("---------------------------------------------find a new object---------------------------------------------")
            if len(NNs) >= k:
                break
        except TypeError:
            continue
    return NNs
# G = nx.Graph()
# print(G.edges)
#### test data
"""
for i  in G.nodes:
    T = list(G.neighbors(i))
    if len(T) == 0:
        print(G.node[i])

"""
#### test DNIS

NNs = DNIS(G, 738814794, 0, "convenience", 10)

print("kNN: ",NNs)


for i in range(len(NNs)):
    for j in range(len(NNs)):
        if G.node[NNs[i]]["lv"] < G.node[NNs[j]]["lv"]:
            temp = NNs[i]
            NNs [i] = NNs[j]
            NNs[j] = temp 
print("kNN: ",NNs)        


j = 0
for i in NNs:
    j = j+1
    print("dia diem", j, ": ", G.node[i])
    print("time travel:",G.node[i]["lv"])

writeFileResult("newResult.txt",NNs)

print ("-------- done --------")

