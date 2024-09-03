# -*- coding: utf-8 -*-
"""
Created on Wed Jul 19 17:16:08 2023

@author: luis.caro
"""

import networkx as nx
import pandas as pd
import math
import copy

from defaultapp.bkhapps.common.Utilities import (UT_CountOcurrences, 
                       UT_CreateColorAttributeFromKeyComponent)

from networkx.algorithms import bipartite


#%%
def UTNx_AddCentralities(xG,xamplifier):
    
    numberOfNodes=xG.number_of_nodes()
    
    total_degree_centrality_dict=\
        {key: (xamplifier*value/(2*(numberOfNodes-1))) for (key, value) in xG.degree}
    nx.set_node_attributes(xG, total_degree_centrality_dict,
                           'total_degree_centrality')
    unscaled_total_degree_centrality_dict=\
        {key: value for (key, value) in xG.degree}
    nx.set_node_attributes(xG, unscaled_total_degree_centrality_dict, 
                           'unscaled_total_degree_centrality')
    in_degree_centrality_dict=\
        {key: (value/(numberOfNodes-1)) for (key, value) in xG.in_degree}
    nx.set_node_attributes(xG, in_degree_centrality_dict,
                           'in_degree_centrality')
    unscaled_in_degree_centrality_dict=\
        {key: value for (key, value) in xG.in_degree}
    nx.set_node_attributes(xG, unscaled_in_degree_centrality_dict, 
                           'unscaled_in_degree_centrality')
    out_degree_centrality_dict=\
        {key: (value/(numberOfNodes-1)) for (key, value) in xG.out_degree}
    nx.set_node_attributes(xG, out_degree_centrality_dict, 
                           'out_degree_centrality')
    unscaled_out_degree_centrality_dict=\
        {key: value for (key, value) in xG.out_degree}
    nx.set_node_attributes(xG, unscaled_out_degree_centrality_dict, 
                           'unscaled_out_degree_centrality')

#%%
def UTNx_getCentralization(centrality, c_type):
    
    print('.-.-.-.-.-.-.-.-.- oihub_UtlitiesNetworkx/UTNx_getCentralization')
    # print('>>>>>>>>>>> centrality ()UTNx_getCentralization')
    # print(len(centrality))
    # print('>>>>>>>>>>> c_type ()UTNx_getCentralization')
    # print(c_type)    
    
    c_denominator = float(1)
    n_val = float(len(centrality))
    if (c_type=="degree"):
        c_denominator = (n_val-1)*(n_val-2)
    if (c_type=="close"):
        c_top = (n_val-1)*(n_val-2)
        c_bottom = (2*n_val)-3
        c_denominator = float(c_top/c_bottom)
    if (c_type=="between"):
        c_denominator = (n_val*n_val*(n_val-2))
    if (c_type=="eigen"):
        
        """
		M = nx.to_scipy_sparse_matrix(G, nodelist=G.nodes(),weight='weight',dtype=float)
		eigenvalue, eigenvector = linalg.eigs(M.T, k=1, which='LR') 
		largest = eigenvector.flatten().real
		norm = sp.sign(largest.sum())*sp.linalg.norm(largest)
		centrality = dict(zip(G,map(float,largest)))
		"""
    c_denominator = math.sqrt(2)/2 * (n_val - 2)
    c_node_max = max(centrality.values())
    c_sorted = sorted(centrality.values(),reverse=True)
    c_numerator = 0
    for value in c_sorted:
        if c_type == "degree":
            #remove normalisation for each value
            c_numerator += (c_node_max*(n_val-1) - value*(n_val-1))
        else:
            c_numerator += (c_node_max - value)
	
# 	print ('numerator:' + str(c_numerator)  + "\n")	
# 	print ('denominator:' + str(c_denominator)  + "\n")	

	
    network_centrality = float(c_numerator/c_denominator)
	
    if c_type == "between":
        network_centrality = network_centrality * 2
		
    return network_centrality


# G = nx.DiGraph()  # or MultiDiGraph, etc
# nx.add_path(G, [0, 1, 2, 3, 4])
# G.edges(data=True)
# G.add_edge(2, 3, weight=5)
# G.add_edge(0, 3, weight=5)

# a=nx.degree_centrality(G)

# getCentralization(a, 'degree')


# [e for e in G.edges]
# # [(0, 1), (1, 2), (2, 3)]
# G.edges.data()  # default data is {} (empty dict)
# # OutEdgeDataView([(0, 1, {}), (1, 2, {}), (2, 3, {'weight': 5})])
# G.edges.data("weight", default=1)
# # OutEdgeDataView([(0, 1, 1), (1, 2, 1), (2, 3, 5)])
# G.edges([0, 2])  # only edges incident to these nodes
# #OutEdgeDataView([(0, 1), (2, 3)])
# G.edges(0)  # only edges incident to a single node (use G.adj[0]?)
# #OutEdgeDataView([(0, 1)])
# G.out_edges([1])
# a=G.in_edges()

#%%

def UTNx_BipartiteProjectedGraph(xfvspGraph, xamplifier, xpartite,
                                 xprojectionType='simple',
                                 xupdate_centralities = True):
    """
    @author: luis.caro
    Proyecta un grafo bipartita funcionario -> proyecto, a funcionarios
    y calcula degree, closeness, y betweennes, centrality
    """
    
    print('.-.-.-.-.-.-.-.-.- UTNx_BipartiteProjectedGraph')

    # print('>>>>>>>>>>> xfvspGraph.nodes (UTNx_BipartiteProjectedGraph)')
    # print(xfvspGraph.nodes(data=True))
    # print('>>>>>>>>>>> xfvspGraph.edges (UTNx_BipartiteProjectedGraph)')
    # print(xfvspGraph.edges(data=True))
    
    
    partiteNodes = \
        list(set(n for n,d in xfvspGraph.nodes(data=True) \
            if d['bipartite']==xpartite))
    # print('>>>>>>>>>>>>>>>>> partiteNodes (UTNx_BipartiteProjectedGraph)')
    # print(partiteNodes)
    
    if xprojectionType == 'simple':
        projectedGraph = bipartite.projected_graph(xfvspGraph, partiteNodes)
    elif xprojectionType == 'weighted':
        projectedGraph = bipartite.weighted_projected_graph(xfvspGraph, partiteNodes)
    else:
        projectedGraph = \
            bipartite.overlap_weighted_projected_graph(xfvspGraph, partiteNodes)
    
    # print('>>>>>>>>>>> projectedGraph.nodes (UTNx_BipartiteProjectedGraph)')
    # print(projectedGraph.nodes(data=True))
    # print('>>>>>>>>>>> projectedGraph.edges (UTNx_BipartiteProjectedGraph)')
    # print(projectedGraph.edges(data=True))
    
    if xupdate_centralities == True:
        new_sizes = dict(map(lambda node: (node[0], 
                                           node[1]*xamplifier), 
                             dict(projectedGraph.degree).items()))
        #nx.set_node_attributes(fvspProjGraphToFuncionarios, new_sizes, 'node_size')
        
        connections = dict(map(lambda node: (node[0],node[1]),
                               dict(projectedGraph.degree).items()))
        nx.set_node_attributes(projectedGraph, connections, 'connections')
        
        degree_centrality_dict=nx.degree_centrality(projectedGraph)
        nx.set_node_attributes(projectedGraph,
                               degree_centrality_dict, 'degree_centrality')
        amp_degree_centrality_dict=degree_centrality_dict
        amp_degree_centrality_dict.update((x, y*xamplifier) \
                                          for x, y in amp_degree_centrality_dict.items())
        nx.set_node_attributes(projectedGraph,
                               amp_degree_centrality_dict, 'amp_degree_centrality')
        
        closeness_centrality_dict=nx.closeness_centrality(projectedGraph)
        nx.set_node_attributes(projectedGraph,
                               closeness_centrality_dict, 'closeness_centrality')
        amp_closeness_centrality_dict=closeness_centrality_dict
        amp_closeness_centrality_dict.update((x, y*xamplifier) \
                                             for x, y in amp_closeness_centrality_dict.items())
        nx.set_node_attributes(projectedGraph,
                               amp_closeness_centrality_dict, 'amp_closeness_centrality')
        
        betweenness_centrality_dict=nx.betweenness_centrality(projectedGraph)
        nx.set_node_attributes(projectedGraph,
                               betweenness_centrality_dict, 'betweenness_centrality')
        amp_betweenness_centrality_dict=betweenness_centrality_dict
        amp_betweenness_centrality_dict.update((x, y*xamplifier) \
                                               for x, y in \
                                                   amp_betweenness_centrality_dict.items())
        nx.set_node_attributes(projectedGraph,
                               amp_betweenness_centrality_dict, 'amp_betweenness_centrality')
    
    # print('>>>>>>>>>>> projectedGraph.nodes (UTNx_BipartiteProjectedGraph)')
    # print(projectedGraph.nodes(data=True))
    
    return projectedGraph, partiteNodes



# df=pd.DataFrame({'x':[1,2,3,4,5,6,1,2,3,4],
#                  'y':['a','a','a','a','a','a','b','b','b','b']})

# g=UT_BipartiteGraph(df, 1, 'x', 'y')
# g.nodes(data=True)
# g.nodes['node_size']

# for n1 in g.nodes:
#     print(g.nodes[n1]['node_size'])

# g.nodes[1]['node_size']

# node_sizes=[g.nodes[n1]['node_size'] for n1 in g.nodes]
# max_node_sizes=max(node_sizes)
# max_node_sizes

#%%

# import pandas as pd
# # pd.options.display.max_columns = 20
# import numpy as np
# rng = np.random.RandomState(seed=5)
# ints = rng.randint(1, 11, size=(3, 2))
# a = ["A", "B", "C"]
# b = ["D", "A", "E"]
# df = pd.DataFrame(ints, columns=["weight", "cost"])
# df
# df[0] = a
# df["b"] = b
# df[["weight", "cost", 0, "b"]]
# #    weight  cost  0  b
# # 0       4     7  A  D
# # 1       7     1  B  A
# # 2      10     9  C  E
# G = nx.from_pandas_edgelist(df, 0, "b", ["weight", "cost"])
# G["E"]["C"]["weight"]
# 10
# G["E"]["C"]["cost"]
# 9
# edges = pd.DataFrame(
#     {
#         "source": [0, 1, 2],
#         "target": [2, 2, 3],
#         "weight": [3, 4, 5],
#         "color": ["red", "blue", "blue"],
#     }
# )
# G = nx.from_pandas_edgelist(edges, edge_attr=True)
# G[0][2]["color"]
# 'red'



def UTNx_BipartiteGraph(xsourceDF, xamplifier, xpart1, xpart2,
                        min_node_size=5):
    """
    @author: luis.caro
    Devuelve un grafo bipartita xpart1 -> xpart2
    """
    
    edges=UT_CountOcurrences(xsourceDF,[xpart1,xpart2])
    edges.rename(columns={'Count':'weight'},inplace=True)

    fvspGraph = nx.from_pandas_edgelist(edges, xpart1, xpart2, ['weight'],
                                        create_using=nx.Graph())

    # fvspGraph = nx.from_pandas_edgelist(xsourceDF, xpart1,
    #                                     xpart2,create_using=nx.Graph())
    
    fvspGraph.add_nodes_from(xsourceDF[xpart1], bipartite=0) # Add the node attribute "bipartite"
    fvspGraph.add_nodes_from(xsourceDF[xpart2], bipartite=1)
    
    for node in fvspGraph.nodes:
        if fvspGraph.nodes[node]['bipartite'] == 0:
            fvspGraph.add_node(node, nodetype=xpart1)
        else:
            fvspGraph.add_node(node, nodetype=xpart2)
    
    colorsDict = dict(map(lambda node: (node[0], 'black' if node[1] == 0 else 'red'),
                          dict(fvspGraph.nodes(data='bipartite')).items()))
    
    nx.set_node_attributes(fvspGraph, colorsDict, 'node_color')
    
    
    #..-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    node_size_dict=\
            {key: max(min_node_size,
                      (xamplifier*value/(2*(fvspGraph.number_of_nodes()-1)))) \
             for (key, value) in fvspGraph.degree}
    nx.set_node_attributes(fvspGraph, node_size_dict,
                           'node_size')
    
    #:_:_:__:_:_:_:_:_:_:_:_:_:_:_:_
    
    # new_sizes = dict(map(lambda node: (node[0], 
    #                                    max(3,node[1]*xamplifier)), 
    #                      dict(fvspGraph.degree).items()))
    # nx.set_node_attributes(fvspGraph, new_sizes, 'node_size')
    
    connections = dict(map(lambda node: (node[0],node[1]),
                           dict(fvspGraph.degree).items()))
    nx.set_node_attributes(fvspGraph, connections, 'connections')
    
    return fvspGraph

#%% https://stackoverflow.com/questions/62383699/converting-networkx-graph-to-data-frame-with-its-attributes

def UTNx_make_node_df(G):
    nodes = {}
    for node, attribute in G.nodes(data=True):
        if not nodes.get('node'):
            nodes['node'] = [node]
        else:
            nodes['node'].append(node)

        for key, value in attribute.items():
            if not nodes.get(key):
                nodes[key] = [value]
            else:
                nodes[key].append(value)

    return pd.DataFrame(nodes)

def UTNx_make_edge_df(G):
    edges = {}
    for source, target, attribute in G.edges(data=True):

        if not edges.get('source'):
            edges['source'] = [source]
        else:
            edges['source'].append(source)

        if not edges.get('target'):
            edges['target'] = [target]
        else:
            edges['target'].append(target)

        for key, value in attribute.items():
            if not edges.get(key):
                edges[key] = [value]
            else:
                edges[key].append(value)
    return pd.DataFrame(edges)


def UTNx_node_df_to_ebunch(df, nodename='node'):

    attributes = [col for col in df.columns if not col==nodename]

    ebunch = []

    for ix, row in df.iterrows():
        ebunch.append((row[nodename], {attribute:row[attribute] for attribute in attributes}))

    return ebunch

#%%

def UTNx_GraphFromEdgesAndNodes(xedges,xnodes,xamplifier):
    graph = nx.from_pandas_edgelist(xedges, 'source', 'target',
                                        ['weight','color'],
                                        create_using=nx.DiGraph)
        
    for x in graph.nodes:
        graph.add_nodes_from([(x, {'node_color':xnodes.loc[x]['color'],
                                   'name':xnodes.loc[x]['name']})])
        
    new_sizes = dict(map(lambda node: (node[0],node[1]*xamplifier),
                         dict(graph.degree).items()))
    new_sizes
    nx.set_node_attributes(graph, new_sizes, 'node_size')
    
    return graph

#%% 

#%%

def UTNx_Adjust_nodes_size(xnxG,xminimumSize, xmaximumSize, xnodeSize,
                           xapplyToSizeZero=True, xadjustOnlyMinimum=False,
                           xnode_size_sufix='', xfixed_min_actual_size = None,
                           xfixed_max_actual_size = None):
    """
    Ajusta los tamaños de los nodos de un network para que queden dentro de
    un rango, más un mínimo, manteniendo las proprociones entre los tamaños

    Parameters
    ----------
    xnxG : networkx graph.
    xminimumSize : int, minimo nuevo tamaño.
    xmaximumSize : int, máximo nuevo tamaño.
    xnodeSize : str, nombre del atributo que tiene el tamaño del nodo.
    xapplyToSizeZero: bool, True: quiere decir que el cero se ajusta, 
                            False: quiere decir que no se ajusta.
                                    Esto es útil para el gráfico de barras 
                                    horizontal construido con networkx, para 
                                    que el inicio de cada línea no se vea.
    xadjustOnlyMinimum: bool, True: quiere decir que si el valor es menor
                                    que el mínimo, se ajusta al mínimo. De lo
                                    contrario no se ajusta.
    xnode_size_sufix: lo que se le quiere agregar al nombre del attributo
                      de tamaño para no cambiar el original. Normalmente
                      '_size'. Esto es útil cuando se crea el campo de
                      tamaño antes de llamar a la creación del plot, cuando
                      va a haber cabio dinamico de tamaños.
    xfixed_min(max)_actual_size: tiene valor cuando no quiere que se tomen
                                 los mínimos(máximos) del attributo de 
                                 tamaño, sino que vengan como parámetro.
                                 Se usa cuando se quiere mantener una 
                                 relación visual de tamaño del nodo cuando
                                 se cambia dinámicamente.
    Returns
    -------
    graph con atributo de tamaño actualizado.
    """
    
    # print('entré a UTNx_Adjust_nodes_size')
    
    def adjust_node_size(xactualSize):
        
        if (xactualSize == 0) and (xapplyToSizeZero == False):
            adjusted_node_size = 0
        else:
            if rango_actual == 0:
                adjusted_node_size = xminimumSize + (rango_ajustado / 2 )
            else:
                if xadjustOnlyMinimum == True:
                    adjusted_node_size=max(xminimumSize,xactualSize)
                else:
                    relación_rangos = rango_ajustado / rango_actual
                    # print('relación_rangos')
                    # print(relación_rangos)    
                    actualSizeMinusMin = xactualSize - min_actual_size
                    actualSizeMinusMinAdj = actualSizeMinusMin * relación_rangos
                    adjusted_node_size = actualSizeMinusMinAdj + xminimumSize
        
        return adjusted_node_size

    node_size_items = nx.get_node_attributes(xnxG, xnodeSize).items()
    # print('node_size_items')
    # print(node_size_items)
    node_size_items_DF = \
        pd.DataFrame(node_size_items, columns=['name', xnodeSize])
    # node_size_items_DF.sort_values(xnodeSize,inplace=True)
    # print('node_size_items_DF')
    # print(node_size_items_DF)
    if xfixed_min_actual_size:
        min_actual_size = xfixed_min_actual_size        
    else:
        min_actual_size = node_size_items_DF[xnodeSize].min() #[xnodeSize][0]
    if xfixed_max_actual_size:
        max_actual_size = xfixed_max_actual_size        
    else:
        max_actual_size = node_size_items_DF[xnodeSize].max() #[xnodeSize][0]
        
    # print('min_actual_size')
    # print(min_actual_size)
    # max_actual_size=node_size_items_DF[xnodeSize].max() #[node_size_items_DF.shape[0]-1]
    # print('max_actual_size')
    # print(max_actual_size)
    rango_actual = max_actual_size - min_actual_size
    # print('rango_actual')
    # print(rango_actual)
    rango_ajustado = xmaximumSize - xminimumSize
    # print('rango_ajustado')
    # print(rango_ajustado)
    
    node_size_items_DF[xnodeSize] = \
        node_size_items_DF[xnodeSize].apply(lambda x: adjust_node_size(x))
        
    node_size_items_Dict = node_size_items_DF.set_index('name').to_dict()
    # print('node_size_items_Dict')
    # print(node_size_items_Dict)
    
    nx.set_node_attributes(xnxG, node_size_items_Dict.get(xnodeSize), 
                           xnodeSize + xnode_size_sufix)
    return xnxG 

def UTNx_Adjust_edge_width(xnxG,xminimumWidth, xmaximumWidth,
                           xedgeWidthAttribute):
    """
    Ajusta el grosor (width) de las conexiones de un network para que queden 
    dentro de un rango, más un mínimo, manteniendo las proprociones entre 
    los tamaños.

    Parameters
    ----------
    xnxG : networkx graph.
    xminimumSize : int, minimo nuevo tamaño.
    xmaximumSize : int, máximo nuevo tamaño.
    xnodeSize : str, nombre del atributo que tiene el tamaño del nodo.
    xapplyToSizeZero: bool, True: quiere decir que el cero se ajusta, 
                            False: quiere decir que no se ajusta.
                                    Esto es útil para el gráfico de barras 
                                    horizontal construido con networkx, para 
                                    que el inicio de cada línea no se vea.
    xadjustOnlyMinimum: bool, True: quiere decir que si el valor es menor
                                    que el mínimo, se ajusta al mínimo. De lo
                                    contrario no se ajusta.
    Returns
    -------
    graph con atributo de tamaño actualizado.
    """
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTNx_Adjust_edge_width')
    # print('>>>>>>>>>>>>>>>>>> edge_width_items (UTNx_Adjust_edge_width)')
    # print(xedgeWidthAttribute)
    # print('>>>>>>>>>>>>>>>>>> xnxG.edges(data=True) (UTNx_Adjust_edge_width)')
    # print(xnxG.edges(data=True))
    
    def adjust_edge_width(xactual_width):
        
        if (xactual_width == 0):
            adjusted_edge_width = 0
        else:
            if rango_actual == 0:
                adjusted_edge_width = xminimumWidth + (rango_ajustado / 2 )
            else:
                relación_rangos = rango_ajustado / rango_actual
                # print('relación_rangos')
                # print(relación_rangos)    
                actual_width_minus_min = xactual_width - min_actual_width
                actual_width_minus_min_adj = \
                    actual_width_minus_min * relación_rangos
                adjusted_edge_width = \
                    actual_width_minus_min_adj + xminimumWidth
        
        return adjusted_edge_width

    edge_width_items = nx.get_edge_attributes(xnxG,xedgeWidthAttribute).items()
    # print('>>>>>>>>>>>>>>>>>> edge_width_items (UTNx_Adjust_edge_width)')
    # print(edge_width_items)
    
    edge_width_items_DF = \
        pd.DataFrame(edge_width_items, columns=['name', xedgeWidthAttribute])
    # print('>>>>>>>>>>>> edge_width_items_DF (UTNx_Adjust_edge_width)')
    # print(edge_width_items_DF)
    min_actual_width = edge_width_items_DF[xedgeWidthAttribute].min() #[xnodeSize][0]
    # print('>>>>>>>>>>>>>>>>>> min_actual_width')
    # print(min_actual_width)
    max_actual_width = \
        edge_width_items_DF[xedgeWidthAttribute].max() #[node_size_items_DF.shape[0]-1]
    # print('>>>>>>>>>>>>>>>>>> min_actual_width')
    # print(min_actual_width)
    rango_actual = max_actual_width - min_actual_width
    # print('rango_actual')
    # print(rango_actual)
    rango_ajustado = xmaximumWidth - xminimumWidth
    # print('rango_ajustado')
    # print(rango_ajustado)
    
    edge_width_items_DF[xedgeWidthAttribute] = \
        edge_width_items_DF[xedgeWidthAttribute].\
            apply(lambda x: adjust_edge_width(x))
        
    edge_width_items_Dict = edge_width_items_DF.set_index('name').to_dict()
    # print('node_size_items_Dict')
    # print(node_size_items_Dict)
    
    nx.set_edge_attributes(xnxG, 
                           edge_width_items_Dict.get(xedgeWidthAttribute),
                           xedgeWidthAttribute)
    # return xnxG 

#%%
def UTNx_adjacency_matrix_to_df(xG, xname_label, xadditional_attribute = '',
                              xadditional_attribute_display_label = '',
                              xdict_employee = {}):
    """
    Extrae la matriz de adyacencia y la convierte a un data frame con fines
    de desliegue

    Parameters
    ----------
    xG : grafo
    xname_label : nombre que se le quiere dar al identificador del nodo
    xadditional_attribute : Nombre de atributo adicional opcional que se 
    quiera incluir en el data frame. '': (default) es ninguno.
    xadditional_attribute_display_label : Título de la columna para el
    atributo adicional. '': (default) use el nombre del atributo.
    xdict_employee (optional): if not empty it is used to rename the nodes.
                                 This is needed because the nodes can be
                                 numeric codes.
    
    Returns adjacency_matrix_df_display, data frame para despliegue.
    """
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UTNx_adjacency_matrix_to_df')
    # print('>>>>>>>>>>>>>>> len(xdict_employee) (UTNx_adjacency_matrix_to_df)')
    # print(len(xdict_employee))
    # print('>>>>>>>>>>>>>>> xadditional_attribute (UTNx_adjacency_matrix_to_df)')
    # print(xadditional_attribute)
    # print('>>>>>>xadditional_attribute_display_label (UTNx_adjacency_matrix_to_df)')
    # print(xadditional_attribute_display_label)
    
    dict_employee_redmine = {k:v[1] for k,v in xdict_employee.items()}
    
    if len(xdict_employee) > 0:
        _G = nx.relabel_nodes(xG, dict_employee_redmine)
    else:
        _G = copy.deepcopy(xG)
    
    adjacency_matrix = nx.adjacency_matrix(_G)
    adjacency_matrix_df = pd.DataFrame(adjacency_matrix.toarray())
    # print('>>>>>>>>>>>>>>> adjacency_matrix_df (UTNx_adjacency_matrix_to_df)')
    # print(adjacency_matrix_df.shape)
    # print('adjacency_matrix_df.columns')
    # print(adjacency_matrix_df.columns)
    # print('adjacency_matrix_df')
    # print(adjacency_matrix_df)
    
    nodes_list = [n for n in _G.nodes()]
    # print('>>>>>>>>>>>>>>> nodes_list (UTNx_adjacency_matrix_to_df)')
    # print(nodes_list)
    adjacency_matrix_df.columns = nodes_list
    nodes_list_sorted =[n for n in _G.nodes()]
    nodes_list_sorted.sort()
    adjacency_matrix_df = adjacency_matrix_df[nodes_list_sorted]
    # print('>>>>>>>>>>>>> adjacency_matrix_df 2 (UTNx_adjacency_matrix_to_df)')
    # print(adjacency_matrix_df.shape)
    # print('adjacency_matrix_df.columns 2')
    # print(adjacency_matrix_df.columns)
    # print('adjacency_matrix_df 2')
    # print(adjacency_matrix_df)
    
    if xadditional_attribute != '':
        node_fields_tuple = \
            [(n,p.get(xadditional_attribute)) for n,p in _G.nodes(data=True)]
        if xadditional_attribute_display_label == '':
            additional_attribute_display_label = xadditional_attribute            
        else:
            additional_attribute_display_label = \
                xadditional_attribute_display_label
        column_labels = [xname_label, additional_attribute_display_label]
        
    else:
        node_fields_tuple = \
            [n for n in _G.nodes()]
        column_labels = [xname_label]
    # print('>>>>>>>>>>>>> column_labels (UTNx_adjacency_matrix_to_df)')
    # print(column_labels)
    
    node_fields_tuple_df = \
        pd.DataFrame(node_fields_tuple, columns = column_labels)
    # print('>>>>>>>>>>>>> node_fields_tuple_df (UTNx_adjacency_matrix_to_df)')
    # print(node_fields_tuple_df.shape)
    # print(node_fields_tuple_df.columns)
    # print(node_fields_tuple_df)
    
    adjacency_matrix_df_display = \
        pd.concat([node_fields_tuple_df, adjacency_matrix_df], axis=1)
    adjacency_matrix_df_display = \
        adjacency_matrix_df_display.sort_values(by=[xname_label], ascending=True)
    
    return adjacency_matrix_df_display

#%%

def UTNx_create_node_color_by(xgraph, xcolor_by):
    
    """
    Creates dictionary of node color for attribute xcolor_by
    
    """
        
    color_by_attribute_dict = nx.get_node_attributes(xgraph, xcolor_by)
    
    color_by_attribute_series = pd.Series(color_by_attribute_dict, 
                                          name=xcolor_by)
    
    color_by_attribute_series.index.name = 'Node'

    color_by_attribute_series = color_by_attribute_series.reset_index()
    
    node_color_dict, _ = \
        UT_CreateColorAttributeFromKeyComponent\
            (list(color_by_attribute_series[xcolor_by]),
             list(color_by_attribute_series['Node']))
            
    # print('att c d')
    # print(attribute_color_dict)
            
    # print('node c d')
    # print(node_color_dict)
            
    return node_color_dict

def UTNx_add_node_color_by(xgraph, xcolor_by):
    
    """
    Adds node color for attribute xcolor_by
    """
    # print('.-.-.-.-.-.-.-.-.-.-.-. UTNx_add_node_color_by')
    # print('>>>>>>>>>>>>>>>>>>> xcolor_by (UTNx_add_node_color_by)')
    # print(xcolor_by)
    
    _node_color_dict = UTNx_create_node_color_by(xgraph, xcolor_by)
    # print('.-.-.-.-.-.-.-.-.-.-.-. UTNx_add_node_color_by')
    # print('>>>>>>>>>>>>>>>>>>> _node_color_dict (UTNx_add_node_color_by)')
    # print(_node_color_dict)
    
    
    nx.set_node_attributes(xgraph, _node_color_dict, 
                           xcolor_by+'_color')

#%%

def UTNx_Ordered_circular_communities(xG, xcommunity_attribute):

    communities = set([v[xcommunity_attribute]
                      for n, v in xG.nodes(data=True)])

    G_ordered = nx.DiGraph()

    for c in communities:
        for n, v in xG.nodes(data=True):
            if v[xcommunity_attribute] == c:
                G_ordered.add_node(n)

    dict_node_attributes = \
        pd.DataFrame.from_dict(xG.nodes, orient='index').to_dict('index')
    nx.set_node_attributes(G_ordered, dict_node_attributes,
                           )

    G_ordered.add_edges_from([(u, v) for u, v in xG.edges])

    dict_edge_attributes =\
        pd.DataFrame.from_dict(xG.edges, orient='index').to_dict('index')
    nx.set_edge_attributes(G_ordered, dict_edge_attributes)

    return G_ordered

#%%
def UTNx_Create_graph_from_dataframe(xgraph_data_df, xedges_columns, 
                                   xedges_attributes = [],
                                   xnodes_attributes_columns = []):
    """
    Creates unimodal graph from DataFrame
    
    Parameters
    ----------
    xgraph_data_df : dataframe with graph data. Each row of the dataframe
                    is an edge
    xedges_columns : columns of the dataframe with edges. Two columns.
                    origin, target
    xedges_attributes : TYPE, optional
        DESCRIPTION. Columns with edege attributes. The default is [].
    xnodes_attributes_columns : TYPE, optional
        DESCRIPTION. Columns with node attributes. The default is [].

    Returns
    -------
    TYPE Networkx DiGraph.
        DESCRIPTION.  

    """    
    G = nx.DiGraph()
        
    edges = list(xgraph_data_df[xedges_columns].itertuples(index=False, 
                                                       name=None))
    
    if xedges_attributes == []:
        edges_attributes = []
    else:
        edges_attributes = \
            list(xgraph_data_df[xedges_attributes].itertuples(index=False, 
                                                       name=None))
            
    edges_complete_list = zip(edges, edges_attributes)
    
    def attributes_dict(xattributes):
        ad = {xedges_attributes[i]:xattributes[i] 
              for i in range(len(xedges_attributes))}
        return ad        
    
    edges_attributes_dict = \
        {x:attributes_dict(y) for x,y in edges_complete_list} 
        
    G.add_edges_from(edges)
    nx.set_edge_attributes(G, edges_attributes_dict)
    
    def create_node_attributes_dict(xnode_complete):
        ad = {xnodes_attributes_columns[i]:xnode_complete[i+1] 
              for i in range(len(xnodes_attributes_columns))}
        return ad
    
    if len(xnodes_attributes_columns) > 0:
        
        origin_nodes_complete_list = \
            list(xgraph_data_df[[xedges_columns[0]]+xnodes_attributes_columns].\
                 itertuples(index=False, name=None))
        origin_node_attributes_dict = \
            {node_complete[0]:create_node_attributes_dict(node_complete) 
             for node_complete in origin_nodes_complete_list}
        
        target_nodes_attributes_columns =\
            ['t_'+attribute for attribute in xnodes_attributes_columns]
        target_nodes_complete_list = \
            list(xgraph_data_df[[xedges_columns[1]] + \
                                target_nodes_attributes_columns].\
                 itertuples(index=False, name=None))
        target_node_attributes_dict = \
            {node_complete[0]:create_node_attributes_dict(node_complete) 
             for node_complete in target_nodes_complete_list}
            
        nx.set_node_attributes\
            (G, origin_node_attributes_dict | target_node_attributes_dict)
        
    return G


def UTNx_Dataframe_from_graph_nodes(xG, xindexName, xincluded_attributes = []):
    
    """
    Creates dataframe from graph nodes
    Input:  - graph
            - index label
    Output: dataframe with column for graph index and a columna for each
            node attribute
    """
    
    graph_nodes_df = \
        pd.DataFrame.from_dict(dict(xG.nodes(data=True)), orient='index')
        
    graph_nodes_df.reset_index(inplace=True)
    graph_nodes_df.rename(columns = {'index':xindexName}, inplace=True)
    
    if xincluded_attributes != []:
        
        selected_columns = [xindexName] + xincluded_attributes
        graph_nodes_df = graph_nodes_df[selected_columns]
    
    return graph_nodes_df


