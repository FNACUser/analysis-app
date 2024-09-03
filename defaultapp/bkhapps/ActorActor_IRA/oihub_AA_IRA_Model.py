# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 21:20:09 2023

@author: luis.caro
"""

import pandas as pd
import numpy as np
import networkx as nx
import copy
import itertools

import networkx.algorithms.community as nxcom

# from neo4j_learn_ONA import conn, insert_data

from bokeh.models.widgets import DataTable, MultiSelect
from bokeh.models import ColumnDataSource, TableColumn, TabPanel, Scatter, Div
from bokeh.layouts import row, column, layout
from bokeh.plotting import from_networkx

from .oihub_AA_IRA_queries import FD_query_question_data

from defaultapp.bkhapps.common.Utilities import (UT_CreateColorAttributeFromKeyComponent,
                       UT_RoundDictionary, UT_bring_legend, FD_cut_name)

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import (UTBo_Network_PlotType2,
                            UTBo_Network_AddSelectedNodesGlyph,
                            UTBo_Network_AddSelectedNodesGraph,
                            # UTBo_Plot_HorizontalBarAndBubble,
                            UTBo_BokehGraphToNetworkxGraph,
                            UTBo_EmptyParagraph,
                            UTBo_Network_FlushSelectedNodesGlyph,
                            UTBo_NodePlot, UTBo_Create_mapped_palette,
                            UTBo_Create_mapped_palette,
                            UTBo_nx_nodes_to_DataTable,
                            UTBo_DataFrame_to_DataTable)

# from oihub_CVF_Actor_item_ranking import UTBo_NodePlot

from defaultapp.bkhapps.common.oihub_UtilitiesNetworkx import (UTNx_getCentralization, 
                                     UTNx_make_node_df,
                               UTNx_adjacency_matrix_to_df,
                               UTNx_Create_graph_from_dataframe,
                               UTNx_Dataframe_from_graph_nodes)


# %%
def FD_edges_count(xgraph, xnode, xto):
    if xto == True:
        return len([v for u, v in xgraph.edges() if v == xnode])
    else:
        return len([u for u, v in xgraph.edges() if u == xnode])


# %%
def FD_Add_Gravity(xg, xgravity):
    g_both = xg.to_undirected(reciprocal=True)

    for v, w in xg.edges:
        if ((v, w) in set(g_both.edges())) | ((w, v) in set(g_both.edges())):
            xg.edges[v, w]['weight'] = 1
            xg.edges[v, w]['color'] = 'green'
            xg.edges[v, w]['gravity'] = xgravity
        else:
            xg.edges[v, w]['weight'] = 1
            xg.edges[v, w]['color'] = 'red'
            xg.edges[v, w]['gravity'] = 1

    return xg


# %%
def FD_Set_node_community(xG, xcommunities, xcommunity_attribute):
    '''Add community to node attributes'''
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- FD_Set_node_community')
    # print('>>>>>>>>>>>>>>>>>> xcommunities (FD_Set_node_community)')
    # print(xcommunities)
    # print('>>>>>>>>>>>>>>>>>> xcommunity_attribute (FD_Set_node_community)')
    # print(xcommunity_attribute)
    for c, v_c in enumerate(xcommunities):
        for v in v_c:
            # Add 1 to save 0 for external edges
            xG.nodes[v][xcommunity_attribute] = c + 1


def FD_Set_edge_community(xG, xcommunity_attribute, xintra_network_value=None):
    '''Find internal edges and add their community to their attributes'''

    # print('>>>>>>>>>>>>>>>>>>>>>FD_Set_edge_community')
    # print(xG.nodes(data=True))

    for v, w, in xG.edges:
        if xG.nodes[v][xcommunity_attribute] == xG.nodes[w][xcommunity_attribute]:
            # Internal edge, mark with community
            xG.edges[v, w][xcommunity_attribute] = xG.nodes[v][xcommunity_attribute]
            xG.edges[v, w][xcommunity_attribute+'_base_weight'] = 2
            xG.edges[v, w][xcommunity_attribute+'_weight'] = 2
            xG.edges[v, w][xcommunity_attribute+'_width'] = 3
        else:
            # External edge, mark as 0
            if xintra_network_value == None:
                xG.edges[v, w][xcommunity_attribute] = 0
            else:
                xG.edges[v, w][xcommunity_attribute] = xintra_network_value
            xG.edges[v, w][xcommunity_attribute+'_base_weight'] = 1
            xG.edges[v, w][xcommunity_attribute+'_weight'] = 1
            xG.edges[v, w][xcommunity_attribute+'_width'] = .25


def FD_create_community_color_palette(xcommunities, xpaletteDict=None):

    if xpaletteDict == None:
        '''agrega color de comunidad al edge'''
        _palette = UTBo_Create_mapped_palette('Turbo', 256,
                                            0, len(xcommunities)+1)
        _paletteDict = {v: k for v, k in enumerate(_palette)}
    else:
        _palette = xpaletteDict
        _paletteDict = _palette

    # print('>>>>>>>>>>>>>> FD_Set_edge_community_color_palette')
    # print(xcommunity_attribute)
    # print(xG_in.edges(data=True))
    # print('_paletteDict')
    # print(_paletteDict)

    return _paletteDict

def FD_Set_edge_community_color(xG_in, xcommunities, xcommunity_attribute,
                                xpaletteDict=None):

    print('.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Model/FD_Set_edge_community_color')
    # print('>>>>>>>> xG_in.edges (oihub_AA_IRA_Model/FD_Set_edge_community_color)')
    # print(xG_in.edges(data=True))
    # print('>>>>>>>> xcommunities (oihub_AA_IRA_Model/FD_Set_edge_community_color)')
    # print(xcommunities)
    # print('>>>>>>>> xcommunity_attribute (oihub_AA_IRA_Model/FD_Set_edge_community_color)')
    # print(xcommunity_attribute)
    
    _paletteDict = \
        FD_create_community_color_palette(xcommunities, 
                                          xpaletteDict = xpaletteDict)

    # print(xcommunity_attribute)
    # print(xG_in.edges(data=True))
    # print('>>>>>>>> _paletteDict (oihub_AA_IRA_Model/FD_Set_edge_community_color)')
    # print(_paletteDict)
    
    for v, w in xG_in.edges:
        # print('v')
        # print(v)
        # print('w')
        # print(w)
        # print('xG_in.edges[v, w]')
        # print(xG_in.edges[v, w])
        xG_in.edges[v, w][xcommunity_attribute+'_color'] = \
            _paletteDict[xG_in.edges[v, w][xcommunity_attribute]]
            
    return _paletteDict

def FD_Set_node_community_color(xG_in, xnode_community_attribute,
                                xpaletteDict):

    # print('.--.-.-.-. finacGDB_AA_IRA_Model/FD_Set_node_community_color')
    
    node_community_color_dict =\
        {n: xpaletteDict.get(u.get(xnode_community_attribute)) \
         for n, u in xG_in.nodes(data=True)}
            
    nx.set_node_attributes(xG_in, node_community_color_dict,
                           xnode_community_attribute + '_color')


def FD_Community_net(G_in, xedgeCommunityColor=False):

    communities = sorted(nxcom.greedy_modularity_communities(G_in), key=len,
                         reverse=False)
    FD_Set_node_community(G_in, communities, 'informal_network')
    FD_Set_edge_community(G_in, 'informal_network')
    if xedgeCommunityColor == True:
        FD_Set_edge_community_color(G_in, communities, 'informal_network')

    return communities


def FD_Ordered_circular_communities(xG, xcommunity_attribute):

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


# %%

def FD_DeltaTable(xtablaModeloCompleto, xtablaModeloFiltradoDF):

    deltaTable = pd.merge(xtablaModeloCompleto, xtablaModeloFiltradoDF,
                          left_on='BusinessComponent',
                          right_on='BusinessComponent',
                          how='inner')
    deltaTable.rename(columns={'total_degree_centrality_x':
                               'total_degree_centrality_complete',
                               'total_degree_centrality_y':
                               'total_degree_centrality_filtered',
                               'unscaled_total_degree_centrality_x':
                               'unscaled_total_degree_centrality_complete',
                               'unscaled_total_degree_centrality_y':
                               'unscaled_total_degree_centrality_filtered'},
                      inplace=True)

    deltaTable['ScaledDifferenceFromComplete'] = \
        -1*((deltaTable['total_degree_centrality_complete'] /
             deltaTable['total_degree_centrality_filtered'])-1)
    deltaTable['UnscaledDifferenceFromComplete'] = \
        -1*((deltaTable['unscaled_total_degree_centrality_complete'] /
            deltaTable['unscaled_total_degree_centrality_filtered'])-1)
    deltaTable['ScaledDifferenceToFiltered'] = \
        (deltaTable['total_degree_centrality_complete'] -
         deltaTable['total_degree_centrality_filtered']) / \
        deltaTable['total_degree_centrality_complete']
    deltaTable['UnScaledDifferenceToFiltered'] = \
        (deltaTable['unscaled_total_degree_centrality_complete'] -
         deltaTable['unscaled_total_degree_centrality_filtered']) / \
        deltaTable['unscaled_total_degree_centrality_complete']

    return deltaTable


# %%

def FD_egoNodes(xnxGraph, xbusinessComponent, xcutoff, 
                xpredecesor_ego = True,
                xbidirected_ego = False):
    
    print('.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Model/FD_egoNodes')
    # print('>>>>>>>>>>>>>>>>>>> xbidirected_ego (FD_egoNodes)')
    # print(xbidirected_ego)
    # print('>>>>>>>>>>>>>>>>>>> xpredecesor_ego (FD_egoNodes)')
    # print(xpredecesor_ego)

    if xbidirected_ego == True:
        egoNodes_p = [node for node in xnxGraph.predecessors(xbusinessComponent)]
        # print('>>>>>>>>>>>>>>>>>>> egoNodes_p T (FD_egoNodes)')
        # print(egoNodes_p)
        egoNodes = [node for node in xnxGraph.successors(xbusinessComponent)]
        # print('>>>>>>>>>>>>>>>>>>> egoNodes T (FD_egoNodes')
        # print(egoNodes)
        # print(egoNodes+egoNodes_p)
        egoNodes=list(set(egoNodes+egoNodes_p))
        egoNodes.append(xbusinessComponent)
        # print(egoNodes)        
    elif xpredecesor_ego == True:
        egoNodes = [node for node in xnxGraph.predecessors(xbusinessComponent)]
        egoNodes.append(xbusinessComponent)
        # print('>>>>>>>>>>>>>>>>>>> egoNodes in (FD_egoNodes')
        # print(egoNodes)
    else:
        egoNodes = [node for node in xnxGraph.successors(xbusinessComponent)]
        egoNodes.append(xbusinessComponent)
        # print('>>>>>>>>>>>>>>>>>>> egoNodes else (FD_egoNodes')
        # print(egoNodes)
        
    return egoNodes


def FD_eliminatedNodesEgosNodes(xnxGraph, xbusinessComponentsToEliminate,
                                xcutoff,
                                xbusinessComponentsByIndex=False,
                                xbusinessComponents='',
                                xbidirected_ego = False):
    
    print('.-.-.-.-.-. finacGDB_AA_IRA_Model/FD_eliminatedNodesEgosNodes')
    # print('>>>>>>>>>>>>< xbidirected_ego (FD_eliminatedNodesEgosNodes)')
    # print(xbidirected_ego)

    if xbusinessComponentsByIndex == True:
        _businessComponentsToEliminate = \
            [xbusinessComponents[businessComponentIndex]
             for businessComponentIndex in xbusinessComponentsToEliminate]
    else:
        _businessComponentsToEliminate = xbusinessComponentsToEliminate
        
    # print('>>>> _businessComponentsToEliminate (FD_eliminatedNodesEgosNodes)')
    # print(_businessComponentsToEliminate)
    
    # print('FD_eliminatedNodesEgosNodes/edges jessica')
    # for u,v in xnxGraph.edges():
    #     if u == 47:
    #         print((u,v))
    # for u,v in xnxGraph.edges():
    #     if v == 47:
    #         print((u,v))
    

    eliminatedNodesPredecessorEgosNodesList = \
        [FD_egoNodes(xnxGraph, businessComponent, xcutoff, 
                     xpredecesor_ego = True,
                     xbidirected_ego = xbidirected_ego)
         for businessComponent in _businessComponentsToEliminate]

    
    eliminatedNodesPredecessorEgosNodesList = \
        list(itertools.chain.from_iterable\
             (eliminatedNodesPredecessorEgosNodesList))

    eliminatedNodesPredecessorEgosNodes = \
        set(eliminatedNodesPredecessorEgosNodesList)

    # print('>>>> eliminatedNodesPredecessorEgosNodes (FD_eliminatedNodesEgosNodes)')
    # print(eliminatedNodesPredecessorEgosNodes)
    
    eliminatedNodesSuccessorEgosNodesList = \
        [FD_egoNodes(xnxGraph, businessComponent, xcutoff, 
                     xpredecesor_ego = False,
                     xbidirected_ego = xbidirected_ego)
         for businessComponent in _businessComponentsToEliminate]

    
    eliminatedNodesSuccessorEgosNodesList = \
        list(itertools.chain.from_iterable\
             (eliminatedNodesSuccessorEgosNodesList))

    eliminatedNodesSuccessorEgosNodes = \
        set(eliminatedNodesSuccessorEgosNodesList)

    # print('>>>> eliminatedNodesSuccessorEgosNodes (FD_eliminatedNodesEgosNodes)')
    # print(eliminatedNodesSuccessorEgosNodes)
    
    return eliminatedNodesPredecessorEgosNodes, \
        eliminatedNodesSuccessorEgosNodes


# %%

def FD_IntermediateNode(xnodeFrom, xnodeTo, xpos, xpercentage, 
                        xencode_multiplier, xinverse=False):

    # print('.-.-.-.-.-.-.-.-.-.-.- finacGDB_AA_IRA_Model/FD_IntemediateNode')
    # print('>>>>>>>>>>> xnodeFrom (FD_IntemediateNode)')
    # print(xnodeFrom)
    # print('>>>>>>>>>>> xnodeTo (FD_IntemediateNode)')
    # print(xnodeTo)
    # print('>>>>>>>>>>> xpos (FD_IntemediateNode)')
    # print(xpos)
    # print(len(xpos))
    
    def encode(xa, xb):
        return (xencode_multiplier * xa) + xb
    
    x_from = xpos[xnodeFrom][0]
    y_from = xpos[xnodeFrom][1]
    x_to = xpos[xnodeTo][0]
    y_to = xpos[xnodeTo][1]

    xspan = x_to - x_from
    yspan = y_to - y_from

    if xspan == 0:
        slope = 1
    else:
        slope = yspan / xspan

    edgeLength = (xspan**2 + yspan**2)**(1/2)

    percentage = min(xpercentage, 0.025/edgeLength)

    if xinverse == True:
        percentageShift = percentage
    else:
        percentageShift = 1 - percentage

    xintermediateShift = percentageShift * xspan
    xintermediate = x_from + (percentageShift * xspan)
    yintermediate = y_from + (slope*xintermediateShift)

    #
    if xinverse == True:
        intermediateNode = encode(xnodeTo, xnodeFrom)
    else:
        intermediateNode = encode(xnodeFrom, xnodeTo)


    return intermediateNode, xintermediate, yintermediate


# %%
def FD_Arrows(xplot, xrendererToUpdate=0, xedge_attr=True):

    graph = UTBo_BokehGraphToNetworkxGraph(xplot.renderers[0], xDiGraph=True,
                                           _xedge_attr = xedge_attr)

    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- finacGDB_AA_IRA_Model/FD_Arrows')
    # print('>>>>>>>>>>>>>>>>> graph.nodes())(FD_Arrows)')
    # print(graph.nodes())
    # print('>>>>>>>>>>>>>>>>> len(graph.nodes()) (FD_Arrows)')
    # print(len(graph.nodes()))
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(graph.edges(data=True))
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(graph.nodes())
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
    # print(graph.edges())
    gc = graph.copy()
    
    # reciprocal creates edge only if edeges in both directions occur between 2 nodes
    g_both = graph.to_undirected(reciprocal=True)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>> g_both')
    # print(g_both.edges())
    
    g_either = graph.to_undirected()
    
    for v, w in g_either.edges:
        if (v, w) in set(g_both.edges()):
            g_either.edges[v, w]['weight'] = 1
            g_either.edges[v, w]['color'] = 'green'
            g_either.edges[v, w]['gravity'] = 20
        else:
            g_either.edges[v, w]['weight'] = 1
            g_either.edges[v, w]['color'] = 'red'
            g_either.edges[v, w]['gravity'] = 1

    for n in g_either.nodes:
        g_either.nodes[n]['node_color'] = 'red'
        g_either.nodes[n]['node_size'] = 5
        
    # encode_multiplier = 10 ** (1 + g_either.number_of_nodes())
    encode_multiplier = 10 ** 5


    # weighted_pos=nx.spring_layout(g_either,weight='gravity')
    weighted_pos = xplot.renderers[0].layout_provider.graph_layout
    # print('>>>>>>>>>>>>>>>>> weighted_pos)(FD_Arrows)')
    # print(weighted_pos)
    

    # collect all edges, lose positional information
    set_list_both = [set(a) for a in g_both.edges()]
    
    #reciporcal edges son las que son pareja (en ambos sentidos)
    reciprocalEdges = [(v, w)
                       for v, w in gc.edges() if set([v, w]) in set_list_both]
    gc.remove_edges_from(reciprocalEdges)

    unidirected_nodes_pos = \
        [FD_IntermediateNode(v, w, weighted_pos, 0.25, encode_multiplier) 
         for v, w in gc.edges()]

    bidirected_nodes_pos = \
        [FD_IntermediateNode(v, w, weighted_pos, 0.25, encode_multiplier)
         for v, w in g_both.edges()]

    bidirected_reverse_nodes_pos = \
        [FD_IntermediateNode(v, w, weighted_pos, 0.25, encode_multiplier, 
                             xinverse=True)
         for v, w in g_both.edges()]

    g_arrows = nx.Graph()
    arrows = dict()

    def addIntermediateNode(xnode, xnode_x, xnode_y):
        arrows[xnode] = np.array([xnode_x, xnode_y])
        g_arrows.add_node(xnode)
        g_arrows.nodes[xnode]['node_color'] = 'yellow'
        g_arrows.nodes[xnode]['node_size'] = 3

    [addIntermediateNode(node, node_x, node_y)
     for node, node_x, node_y in unidirected_nodes_pos]

    [addIntermediateNode(node, node_x, node_y)
     for node, node_x, node_y in bidirected_nodes_pos]

    [addIntermediateNode(node, node_x, node_y)
     for node, node_x, node_y in bidirected_reverse_nodes_pos]


    imposedBokehGraph = \
        from_networkx(g_arrows, nx.spring_layout, scale=1, center=(0, 0))

    imposedBokehGraph.node_renderer.glyph = \
        Scatter(marker='triangle', size='node_size')
        # ,
        #         fill_color='node')

    layout2 = imposedBokehGraph.layout_provider

    layout2.graph_layout = arrows

    if xrendererToUpdate == 0:
        xplot.renderers.append(imposedBokehGraph)
    else:
        xplot.renderers[xrendererToUpdate] = imposedBokehGraph
    
    return xplot


# %%

def FD_Build_tables2and3(xG):
    
    print('.-.-.-.-.-.-.--.-. oihub_AA_IRA_Model/FD_Build_tables2and3')
    # print('>>>>>>>>>>>>>>>>>>>>> xG.nodes(data=True) (FD_Build_tables2and3)')
    # print(xG.nodes(data=True))

    table = pd.DataFrame()

    def nodeToDF(xnode, xattr):
        nodeDF = pd.DataFrame([xattr])
        nodeDF['BusinessComponent'] = xnode
        return nodeDF

    for (node, att) in xG.nodes(data=True):
        table = pd.concat([table, nodeToDF(node, att)], ignore_index=True)

    # print('>>>>>>>>>>>>>>>>>>>>> table (FD_Build_tables2and3)')
    # print(table.to_dict('records'))

    selected_columns = ['total_degree_centrality',
                        'unscaled_total_degree_centrality', 
                        'in_degree_centrality',
                        'unscaled_in_degree_centrality', 
                        'out_degree_centrality', 
                        'unscaled_out_degree_centrality']

    table = table[['BusinessComponent', 'employee', 'total_degree_centrality',
                   'unscaled_total_degree_centrality', 'in_degree_centrality',
                  'unscaled_in_degree_centrality', 'out_degree_centrality',
                   'unscaled_out_degree_centrality','eigenvector_centrality',
                   'betweenness_centrality']]
    
    # print('>>>>>>>>>>>>>>>>>>>>> table (FD_Build_tables2and3)')
    # print(table.to_dict('records'))
    # print(table.columns)
    # print(table.shape)
    
    # tt = UTNx_Dataframe_from_graph_nodes(xG, 'BusinessComponent',
    #                                      xincluded_attributes = \
    #                                          selected_columns)
    
    # print('>>>>>>>>>>>>>>>>>>>>> tt (FD_Build_tables2and3)')
    # print(tt.to_dict('records'))
    # print(tt.columns)
    # print(tt.shape)
    
    return table


# %%

def FD_AddCentralities(xG, xamplifier, xnodeSizeAttribute):

    # print('.-.-.-.-.-.-.-.- finacGDB_AA_IRA_Model/FD_AddCentralities')
    # print('>>>>>>>>>>>>>>>>>>>>>>> xnodeSizeAttribute (FD_AddCentralities)')
    # print(xnodeSizeAttribute)
    

    
    non_directed_G = nx.compose(nx.Graph(), xG)

    numberOfNodes = xG.number_of_nodes()

    nx.set_node_attributes(xG,
                           UT_RoundDictionary(nx.in_degree_centrality(xG), 4),
                           'in_degree_centrality')
    nx.set_node_attributes(xG,
                           UT_RoundDictionary(nx.out_degree_centrality(xG), 4),
                           'out_degree_centrality')
    degree_centrality_dict =\
        {key: (value/(2*(numberOfNodes-1))) for (key, value) in xG.degree}

    nx.set_node_attributes(xG,
                           UT_RoundDictionary(degree_centrality_dict, 4),
                           'total_degree_centrality')

    try:
        nx.set_node_attributes(xG,
                               UT_RoundDictionary(
                                   nx.eigenvector_centrality(xG,
                                                             max_iter = 1000),
                                                             4),
                               'eigenvector_centrality')
    except:
        print('No se pudo calcular eigenvector_centrality (FD_AddCentralities)')
        for node in xG.nodes:
            xG.nodes[node]['eigenvector_centrality'] = 0
    
    nx.set_node_attributes(xG,
                           UT_RoundDictionary(
                               nx.betweenness_centrality(xG), 4),
                           'betweenness_centrality')

    unscaled_total_degree_centrality_dict =\
        {key: value for (key, value) in xG.degree}
    nx.set_node_attributes(xG, unscaled_total_degree_centrality_dict,
                           'unscaled_total_degree_centrality')
    
    unscaled_in_degree_centrality_dict =\
        {key: value for (key, value) in xG.in_degree}
    nx.set_node_attributes(xG, unscaled_in_degree_centrality_dict,
                           'unscaled_in_degree_centrality')
    
    unscaled_out_degree_centrality_dict =\
        {key: value for (key, value) in xG.out_degree}
    nx.set_node_attributes(xG, unscaled_out_degree_centrality_dict,
                           'unscaled_out_degree_centrality')

    # .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- node size
    if xnodeSizeAttribute == "in_degree":
        node_size_dict =\
            {key: (xamplifier*value/(2*(numberOfNodes-1)))
             for (key, value) in xG.in_degree}
        nx.set_node_attributes(xG, node_size_dict,
                               'node_size')
    else:
        node_size_dict =\
            {key: (xamplifier*value/(2*(numberOfNodes-1)))
             for (key, value) in xG.out_degree}
        nx.set_node_attributes(xG, node_size_dict,
                               'node_size')
    # print('node_size_dict')
    # print(pd.DataFrame([node_size_dict]))

    # print('>>>>>>>>>>>>>>>>>>> xG.nodes(data=True) (FD_AddCentralities')
    # print(xG.nodes(data=True))


def FD_CreateGraphAndMetricsII(xkeyComponents, xbusinessComponents,
                               xxedges, xnodesToDelete,
                               xamplifier, xnodeSizeAttribute,
                               xplot):

    # print('.-.-.-.-.-.-.-.- finacGB_AA_IRA_Model/FD_CreateGraphAndMetricsII')
    graph = UTBo_BokehGraphToNetworkxGraph(xplot.renderers[0])
    # print(".-.-.-.-.-.-.-.-.  len(graph.nodes()) (FD_CreateGraphAndMetricsII)")
    # print(len(graph.nodes()))

    # print(">>>>>>>>>>>>>>>>>>> xnodesToDelete (FD_CreateGraphAndMetricsII)")
    # print(xnodesToDelete)
    nodesToDeleteNames = [xbusinessComponents[nodeToDelete]
                          for nodeToDelete in xnodesToDelete]
    # print(">>>>>>>>>>>>>>> nodesToDeleteNames (FD_CreateGraphAndMetricsII)")
    # print(nodesToDeleteNames)

    remove = [node for node in graph.nodes() if node in nodesToDeleteNames]
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>. remove (FD_CreateGraphAndMetricsII)")
    # print(remove)

    graph.remove_nodes_from(remove)
    # print(".-.-.-.-.-.-.-.-. FD_CreateGraphAndMetricsII - graph removed")
    # print(graph.nodes())

    FD_AddCentralities(graph, xamplifier, xnodeSizeAttribute)


    centralitiesTable = FD_Build_tables2and3(graph)

    density = round(nx.density(graph), 4)

    return graph, centralitiesTable, density


def FD_active_responses_list(xactive_selected_possible_responses,
                             xpossible_responses_dict,
                             xquestions_data_df):
    
    """
    input:  - active_selected_possible_responses: respuestas que se usan
                                                como selección inicial
            - xpossible_responses_dict: diccionario de respuestas posibles
            - xfilter_group_active: ver definición en FD_CreateGraphAndMetrics.
    
    output: - lista de respuestas positivas (que se incluyen en el resultado)    
    """
    
    print('.-.-.-.-.-.-.-.- oihub_AA_IRA_Model/FD_active_responses_list')
    # print('>> xactive_selected_possible_responses (FD_active_responses_list)')
    # print(xactive_selected_possible_responses)
    # print('>> xpossible_responses_dict (FD_active_responses_list)')
    # print(xpossible_responses_dict)
    # print('>> xfilter_group_active (FD_active_responses_list)')
    # print(xfilter_group_active)
    
    questions_data_df_grouped = \
        xquestions_data_df.groupby(['id_employee', 't_id_employee'])['value'].\
            agg(set).reset_index()
    # print('>> questions_data_df_grouped (FD_active_responses_list)')
    # print(questions_data_df_grouped)
    # print(list(questions_data_df_grouped['value']))
    
    
    active_ids = set([1 + active_selected_possible_response\
                  for active_selected_possible_response in \
                      xactive_selected_possible_responses])
    # print('>> active_ids (FD_active_responses_list)')
    # print(active_ids)
    
    active_responses_list = \
        questions_data_df_grouped.\
            loc[questions_data_df_grouped['value'] == active_ids]
    # print('>>>>>>>>>>>>> active_responses_list (FD_active_responses_list)')
    # print(active_responses_list)
            
    return active_responses_list


def FD_CreateGraphAndMetrics(xconn, xnetwork_parameters_dict, 
                             # xnetwork_parameters_data_table, 
                             q_xXxkeyComponents, 
                             q_xXxbusinessComponents,
                             xbusinessComponentsToDelete,
                             xamplifier,
                             q_XxfrequencyCorte, 
                             q_XxfrequencyResponseAccumulation,
                             xactive_selected_possible_responses,
                             xall_any_filter_group_active):
    
    """
    input:  - network_parameters_dict: diccionario global de parámetros
            - q_xkeyComponents: organization areas
            - q_xbusinessComponents: personas
            - xbusinessComponentsToDelete: personas que se quieren excluir
            - xamplifier: multiplicador del tamaño de los nodos
            - q_xxfrequencyCorte, 
            - q_xxfrequencyResponseAccumulation: no se usan            
            - active_selected_possible_responses: respuestas que se usan
                                                como selección inicial
            - xfilter_group_active: se usa para preguntas que permiten
                                    escoger multiples respuestas. 
                                    0 - quiere decir que solo son positivas
                                        respuestas que tienen todas las
                                        opciones del filtro
                                    1 - quiere decir que son positivas
                                        respuestas que tienen alguna de
                                        las opciones del filtro
                                    Nótese que para preguntas que solo
                                    permiten una opción, es necesario
                                    que sea 1.
    
    output: - gneo4j: a nx graph loaded with node attributes. The graph
              is built with data from the neo4j database, corresponding to
              the question that wants to be illustrated
            - centralitiesTable: a dataframe with all the nodes metrics
            - density: density of the graph
            - _componentName_color_Dict: dictionary of node colors of
                                        organization area
    """

    print('.-.-.-.-.-.-.-. finacGDB_AA_IRA_Model/FD_CreateGraphAndMetrics')
    # print('>>>>>>>>>>>>>>> xbusinessComponentsToDelete (FD_CreateGraphAndMetrics)')
    # print(xbusinessComponentsToDelete)
    # print('>>>>>>>> xamplifier (FD_CreateGraphAndMetrics)')
    # print(xamplifier)
    # print('>>>>>>>> xnodeSizeAttribute (FD_CreateGraphAndMetrics)')
    # print(xnodeSizeAttribute)
    # print('>>>>>>>>>>>>>>> xall_any_filter_group_active (FD_CreateGraphAndMetrics)')
    # print(xall_any_filter_group_active)
    # print('>>>>>>>> xactive_selected_possible_responses (FD_CreateGraphAndMetrics)')
    # print(xactive_selected_possible_responses)

    
    # # print('>>>>>>>>>>>>>>> indexesToDelete (FD_CreateGraphAndMetrics)')
    # # print(businessComponentsToDeleteIndexes)
    
    # print('>>>>>>>>>>>>>>> len(businessComponentsFiltered) (FD_CreateGraphAndMetrics)')
    # print(len(businessComponentsFiltered))
    # print('>>>>>>>> len(keyComponentsFiltered) (FD_CreateGraphAndMetrics)')
    # print(len(keyComponentsFiltered))
   
    
    #
    #see xnetwork_parameters_dict fields definition in 
    # oahubGDB_AA_IRA_QCommon/FD_network_parameters_dict
    # id_question = \
    #     xnetwork_parameters_data_table.source.data['id_question'][0]
    id_question = xnetwork_parameters_dict['id_question']
    cycle = xnetwork_parameters_dict['cycle']
    network_mode_theme = xnetwork_parameters_dict['network_mode_theme'] 
    possible_responses_dict = \
        xnetwork_parameters_dict['possible_responses_dict']
    cvf_clusters_df = xnetwork_parameters_dict['cvf_clusters_df']
    reverse_edges = xnetwork_parameters_dict['reverse_edges']
    p_d_node_size_attribute = \
        xnetwork_parameters_dict['node_size_attribute']
    filter_group_enabled = xnetwork_parameters_dict['filter_group_enabled']
    # print('>>>>>>>>>>>>> id_question (FD_CreateGraphAndMetrics)')
    # print(id_question)
    # print('>>>>>>>>>>>>> cycle (FD_CreateGraphAndMetrics)')
    # print(cycle)
    # print('>>>>>>>>>>>>> network_mode_theme (FD_CreateGraphAndMetrics)')
    # print(network_mode_theme)
    # print('>>>>>>>>>>>>> cvf_clusters_df (FD_CreateGraphAndMetrics)')
    # print(cvf_clusters_df)
    # print('>>>>>>>>>>>>> possible_responses_dict (FD_CreateGraphAndMetrics)')
    # print(possible_responses_dict)
    # print('>>>>>>>>>>>>> network_mode_theme (FD_CreateGraphAndMetrics)')
    # print(network_mode_theme)
    # print('>>>>>>>>>>>>> filter_group_enabled (FD_CreateGraphAndMetrics)')
    # print(filter_group_enabled)
    
    """
    esto se hace porque hay respuestas posibles que no tiene values
    seguidos (por ejemplo: 2:"poco", 5:"mucho#)
    """
    possible_responses_dict_keys_list = list(possible_responses_dict.keys())
    # print('>>>>>>>>>>>>> possible_responses_dict_keys_list (FD_CreateGraphAndMetrics)')
    # print(possible_responses_dict_keys_list)
    
    """
    se cambio porque ahora necesitamos los values de las respuestas y no
    los meannig
    """
    selected_possible_responses = \
        [possible_responses_dict_keys_list[aspr]
         for aspr in xactive_selected_possible_responses]
    # print('>>>>>>>>selected_possible_responses (FD_CreateGraphAndMetrics)')
    # print(selected_possible_responses)
    
    exclude_list = xbusinessComponentsToDelete
     
    question_tuples = [(cycle, network_mode_theme, id_question,
                        selected_possible_responses)]
    # print('>>>>>>>>question_tuples (FD_CreateGraphAndMetrics)')
    # print(question_tuples)
    
    questions_data_df = pd.DataFrame()
    for question_tuple in question_tuples:
        question_data_df = FD_query_question_data(xconn, question_tuple)
        questions_data_df = pd.concat([questions_data_df, 
                                       question_data_df], ignore_index=True)
    # print('>>>>>>>>questions_data_df.shape (FD_CreateGraphAndMetrics)')
    # print(questions_data_df.shape)
        
    """
    filter_group_enabled = True quiere decir que puede haber respuestas
                            múltiples (más de una respuesta para la pregunta)
    all_any_filter_group_active = 0 quiere decir que se seleccionan las
                                    respuestas que seleccionarion todas
                                    las opciones que el usuario indicó en
                                    el filtro
    """
    if (filter_group_enabled == True) & (xall_any_filter_group_active == 0):
        active_responses_list = \
            FD_active_responses_list(xactive_selected_possible_responses,
                                     possible_responses_dict,
                                     questions_data_df)
        columns = ['id_employee', 'is_active', 'redmine_login', 'employee', 
                   't_id_employee', 't_employee', 't_is_active', 
                   't_redmine_login', 'id_organization_area',
                   'organization_area', 'value_x', 'meaning']
        questions_data_df = \
            questions_data_df.merge(active_responses_list, 
                                    left_on=['id_employee', 't_id_employee'],
                                    right_on=['id_employee', 't_id_employee'],
                                    how = 'right')[columns]
        questions_data_df.rename(columns={'value_x':'value'}, inplace = True)
        # print('>>>>>>>>questions_data_df selected (FD_CreateGraphAndMetrics)')
        # print(questions_data_df)
        # print(questions_data_df.shape)
        # print(questions_data_df.columns)
        


    
    # questions_data_df.groupby('continent')['country'].apply(list).reset_index(name='country_list')
    
    query2 = """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-(e:Employee)
                RETURN e.id_employee as t_id_employee,
                oa.id_organization_area as t_id_organization_area,
                oa.organization_area as t_organization_area"""
    result2 = xconn.query(query2)    
    result2_df = pd.DataFrame([dict(_) for _ in result2])
    # print('>>>>>>>>>>>>>>>>>>>>> result2_df (FD_CreateGraphAndMetrics)')
    # print(result2_df.columns)
    # print(result2_df.shape)    
    # print('>>>>>>>>>>>>>>>>>>>>> questions_data_df (FD_CreateGraphAndMetrics)')
    # print(questions_data_df.columns)
    # print(questions_data_df.shape)    
    
    # complete_result_df = pd.merge(result_df, result2_df, 
    complete_result_df = pd.merge(questions_data_df, result2_df, 
                                  left_on = 't_id_employee',
                                  right_on = 't_id_employee',
                                  how = 'left')
    # print('>>>>>>>>complete_result_df.shape (FD_CreateGraphAndMetrics)')
    # print(complete_result_df.shape)
    # print(complete_result_df.columns)
    
    complete_result_df['employee'] =\
        complete_result_df['employee'].apply(lambda x: FD_cut_name(x))
    complete_result_df['t_employee'] =\
        complete_result_df['t_employee'].apply(lambda x: FD_cut_name(x))
    
    
    """
    complete_result_df : dataframe with graph data. Each row of the dataframe
                    is an edge
    ['id_employee', 't_id_employee'] : edges origin and target
    ['meaning','value'] : edge attributes.
    ['id_employee', 'is_active', 'redmine_login', 'employee',
     'id_organization_area', 'organization_area'] : node attributes.
    """
    gneo4j = UTNx_Create_graph_from_dataframe(complete_result_df, 
                                              ['id_employee', 
                                               't_id_employee'],
                                      xedges_attributes = ['meaning','value'],
                                      xnodes_attributes_columns = \
                                           ['id_employee', 'is_active', 
                                            'redmine_login', 'employee',
                                            'id_organization_area',
                                            'organization_area'])
        
    # print('VERIFICACION VERIFICACION VERIFICACION ')
    # print(result_df.loc[complete_result_df.id_employee == 71].to_dict('records'))
    # print(gneo4j.nodes(data=True)[71])
    # print(len(list(gneo4j.nodes())))
    # print([e for e in gneo4j.edges(data=True) if (e[0] == 71) & (e[1] == 31)])
        
    # print('>>>>>>>>>>>>> gneo4j.nodes(data=True) (FD_CreateGraphAndMetrics)')
    # print(gneo4j.nodes(data = True))
    # print('>>>>>>>>>>>>> len(gneo4j.nodes()) (FD_CreateGraphAndMetrics)')
    # print(len(gneo4j.nodes()))
    # print('>>>>>>>>>>>>> gneo4j.edges(data=True) (FD_CreateGraphAndMetrics)')
    # print(gneo4j.edges(data = True))
    
    #
    actors_areas_tuples = \
        [(n, v.get('id_organization_area')) \
         for n,v in gneo4j.nodes(data = True)]
    actors_areas_tuples.sort(key=lambda tup: tup[0])
    _businessComponents = \
        [actor_area[0] for actor_area in actors_areas_tuples]
    _keyComponents = \
        [actor_area[1] for actor_area in actors_areas_tuples] 
    # print('>>>>>>>>>>> _businessComponents (FD_CreateGraphAndMetrics)')
    # print(_businessComponents)
    # print(len(_businessComponents))
    # print('>>>>>>>>>>> _keyComponents (FD_CreateGraphAndMetrics)')
    # print(_keyComponents)
    # print(len(_keyComponents))
    
    businessComponentsToDeleteIndexes = \
        [_businessComponents.index(componentToDelete) \
          for componentToDelete in xbusinessComponentsToDelete]
    # print('>>>>>>>>>>>>>>> indexesToDelete (FD_CreateGraphAndMetrics)')
    # print(businessComponentsToDeleteIndexes)
    
    businessComponentsFiltered = copy.deepcopy(_businessComponents)
    for index in businessComponentsToDeleteIndexes:
        del businessComponentsFiltered[index]
    # print('>>>>>>>>>>> businessComponentsFiltered (FD_CreateGraphAndMetrics)')
    # print(businessComponentsFiltered)
    

    keyComponentsFiltered = copy.deepcopy(_keyComponents)
    for index in businessComponentsToDeleteIndexes:
        del keyComponentsFiltered[index]
    # print('>>>>>>>>>>> keyComponentsFiltered (FD_CreateGraphAndMetrics)')
    # print(keyComponentsFiltered)
        

    """
    Esto se necesita cuando el sentido de la pregunta es al revés.
    Por ejempo: de quién recibo información
    Ver xreverse_edges en oahubGDB_AA_IRA_QCommon/FD_network_parameters_dict
    """
    if reverse_edges == True:
        gneo4j = gneo4j.reverse(copy=True)
    
    gneo4j.remove_nodes_from(exclude_list)
    
    """
    cvf_clusters_dict - key: node, value: cvf_cluster
    cvf is "competing values framework"
    """
    cvf_clusters_dict = \
        pd.Series(cvf_clusters_df.cluster.values,
                  index=cvf_clusters_df.id_employee).to_dict()
    # print('>>>>>>>>>>>>> cvf_clusters_dict (FD_CreateGraphAndMetrics)')
    # print(cvf_clusters_dict)
    # print(len(cvf_clusters_dict))
    # print(cvf_clusters_df.shape)
    
    """
    assign cluster to each node.
    Initially assigns 0 because there might be nodes that do not have an
    assigned cluster
    """
    nx.set_node_attributes(gneo4j, 0, 'cvf_cluster')
    nx.set_node_attributes(gneo4j, cvf_clusters_dict, 'cvf_cluster')
    
    # print('>>>>>>>>>>>>> gneo4j.nodes(data=True) (FD_CreateGraphAndMetrics)')
    # print(gneo4j.nodes(data=True))
   
    #adds centralities
    FD_AddCentralities(gneo4j, xamplifier, p_d_node_size_attribute)
    
    if len(keyComponentsFiltered) > 0:
        area_color_dict, _componentName_color_Dict = \
            UT_CreateColorAttributeFromKeyComponent(keyComponentsFiltered,
                                                    businessComponentsFiltered)
    else:
        area_color_dict = {}
        _componentName_color_Dict = {}
    # print('.-.-.-.-.-.-.- area_color_dict (FD_CreateGraphAndMetrics)')
    # print(area_color_dict)
    # print(len(area_color_dict))
    # print('.-.-.-.-.-.-.- _componentName_color_Dict (FD_CreateGraphAndMetrics)')
    # print(_componentName_color_Dict)
    # print(len(_componentName_color_Dict))
    
    nx.set_node_attributes(gneo4j, area_color_dict, "organization_area_color")
    # print('>>>>>>>>>>>>>>>> len gneo4j.nodes (FD_CreateGraphAndMetrics)')
    # print(gneo4j.nodes(data=True))
    # print(len(gneo4j.nodes()))
    
    employee_cluster_list = [(n,v.get('cvf_cluster')) 
                              for n,v in gneo4j.nodes(data=True)]
    ids_employees_list, clusters_list = map(list,zip(*employee_cluster_list))
    
    #
    cvf_cluster_color_dict, _cvf_cluster_componentName_color_dict = \
        UT_CreateColorAttributeFromKeyComponent(clusters_list,
                                                ids_employees_list)
    # print('.-.-.-.-.-.-.- cvf_cluster_color_dict (FD_CreateGraphAndMetrics)')
    # print(cvf_cluster_color_dict)
    # print(len(cvf_cluster_color_dict))
    # print('.- cvf_cluster_componentName_color_dict (FD_CreateGraphAndMetrics)')
    # print(_cvf_cluster_componentName_color_dict)
    # print(len(_cvf_cluster_componentName_color_dict))
    # print('.-.-.-.-.-.-.- n nodes gneo4j (FD_CreateGraphAndMetrics)')
    # print(len(gneo4j.nodes()))
    
   
    nx.set_node_attributes(gneo4j, cvf_cluster_color_dict, "cvf_cluster_color")
    
    # print('>>>>>>>>>>>>> gneo4j.nodes(data=True) (FD_CreateGraphAndMetrics)')
    # print(gneo4j.nodes(data=True))
   
    centralitiesTable = FD_Build_tables2and3(gneo4j)

    density = round(nx.density(gneo4j), 4)

    # print('>>>>>>>>>>> graph.nodes(data=True) (FD_CreateGraphAndMetrics)')
    # print(gneo4j.number_of_nodes())
    # print(gneo4j.edges(data=True))
    
    # print('<>_<>_<>_<>_<>_<>_<>_<>_<>_<> saliendo de createGraphAndMetrics')
    # print('<>_<>_<>_<>_<>_<>_<>_<>_<>_<> saliendo de createGraphAndMetrics')
    # print('<>_<>_<>_<>_<>_<>_<>_<>_<>_<> saliendo de createGraphAndMetrics')
    # print('<>_<>_<>_<>_<>_<>_<>_<>_<>_<> saliendo de createGraphAndMetrics')
    # print('<>_<>_<>_<>_<>_<>_<> centralitiesTable')
    # print(centralitiesTable)
    # print(centralitiesTable.columns)
    # print('<>_<>_<>_<>_<>_<>_<> density')
    # print(density)
    # print('<>_<>_<>_<>_<>_<>_<> _componentName_color_Dict')
    # print(_componentName_color_Dict)
    # print('<>_<>_<>_<>_<>_<>_<> _businessComponents')
    # print(_businessComponents)
    # print('<>_<>_<>_<>_<>_<>_<> _keyComponents')
    # print(_keyComponents)
    # i=0
    # for n,d in gneo4j.nodes(data=True):
    #     if i<2:
    #         print(n)
    #         print(d)
    #     i+=1
    
    return gneo4j, centralitiesTable, density, _componentName_color_Dict,\
        _businessComponents, _keyComponents



# %%

def FD_ego_graph(xego_nx_graph, xp_d_responder_direction, x_completeNxGraph,
              xbusinessComponentsToEliminate,
              xinverse_responder = False):
    #Solo se quieren los edges que conectan el nodo eliminado
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.- FD_ego_graph')
    
    def replace_in_edges():
        in_edges = x_completeNxGraph.in_edges(
            xbusinessComponentsToEliminate, data=True)
        xego_nx_graph.add_edges_from(in_edges)
        número_conexiones_componentes_eliminados = \
            str(len(x_completeNxGraph.in_edges\
                    (xbusinessComponentsToEliminate)))
        dirección = 'in'
        return número_conexiones_componentes_eliminados, dirección
    
    def replace_out_edges():
        out_edges = x_completeNxGraph.out_edges(
            xbusinessComponentsToEliminate, data=True)
        xego_nx_graph.add_edges_from(out_edges)
        número_conexiones_componentes_eliminados = \
            str(len(x_completeNxGraph.out_edges\
                    (xbusinessComponentsToEliminate)))
        dirección = 'out'
        return número_conexiones_componentes_eliminados, dirección
    
    xego_nx_graph.remove_edges_from\
        (dict(xego_nx_graph.edges))
    if ((xp_d_responder_direction == 'in') & (xinverse_responder == False)) |\
        ((xp_d_responder_direction == 'out') & (xinverse_responder == True)):
        número_conexiones_componentes_eliminados, dirección = \
            replace_in_edges()
        # print('>>>> dirección (FD_ego_graph)')
        # print(dirección)
    else:
        número_conexiones_componentes_eliminados, dirección = \
            replace_out_edges()
        # print('>>>> dirección (FD_ego_graph)')
        # print(dirección)
        
    return número_conexiones_componentes_eliminados, dirección



#%%
def FD_responder_and_inverse_graphs(xcompleteNxGraph, 
                                    xp_d_responder_direction,
                                    xbusinessComponentsToEliminate):
    
    print('.-.-.-.-. finacGDB_AA_IRA_Model/FD_responder_and_inverse_graphs')
    
    eliminatedNodesPredecessorEgosNodes, eliminatedNodesSuccessorEgosNodes = \
        FD_eliminatedNodesEgosNodes(xcompleteNxGraph, 
                                    xbusinessComponentsToEliminate, 1,
                                    xbusinessComponents = \
                                        xcompleteNxGraph.nodes())
    
    predecessor_egoNxGraphSubGraph = \
        xcompleteNxGraph.subgraph(eliminatedNodesPredecessorEgosNodes)
    predecessor_egoNxGraph = predecessor_egoNxGraphSubGraph.copy()
    
    successor_egoNxGraphSubGraph = \
        xcompleteNxGraph.subgraph(eliminatedNodesSuccessorEgosNodes)
    successor_egoNxGraph = successor_egoNxGraphSubGraph.copy()
    
    if xp_d_responder_direction == 'in':   
        responder_número_conexiones_componentes_eliminados, \
            responder_dirección = \
            FD_ego_graph(predecessor_egoNxGraph, xp_d_responder_direction,
                      xcompleteNxGraph, xbusinessComponentsToEliminate)
        responder_egoNxGraph = predecessor_egoNxGraph.copy()
        inverse_responder_número_conexiones_componentes_eliminados, \
            inverse_responder_dirección = \
            FD_ego_graph(successor_egoNxGraph, xp_d_responder_direction,
                      xcompleteNxGraph, xbusinessComponentsToEliminate,
                      xinverse_responder = True)
        inverse_responder_egoNxGraph = successor_egoNxGraph.copy()        
    else:
        responder_número_conexiones_componentes_eliminados, \
            responder_dirección = \
            FD_ego_graph(successor_egoNxGraph, xp_d_responder_direction,
                      xcompleteNxGraph, xbusinessComponentsToEliminate)
        responder_egoNxGraph = successor_egoNxGraph.copy()
        inverse_responder_número_conexiones_componentes_eliminados, \
            inverse_responder_dirección = \
            FD_ego_graph(predecessor_egoNxGraph, xp_d_responder_direction,
                      xcompleteNxGraph, xbusinessComponentsToEliminate,
                      xinverse_responder = True)
        inverse_responder_egoNxGraph = predecessor_egoNxGraph.copy()
        
    return responder_dirección, \
            responder_número_conexiones_componentes_eliminados, \
                responder_egoNxGraph, inverse_responder_dirección, \
                    inverse_responder_número_conexiones_componentes_eliminados, \
                        inverse_responder_egoNxGraph


#%%
def FD_businessComponentSelection(xexcluded_select, 
                                  xnetwork_parameters_dict,
                                  xparameters_for_business_component_selection_dict,
                                  xxcompleteNxGraph, xplot1, xplot2, xplot3, 
                                  xnodeSizeAttribute,
                                  xgraph1, xgraph2, xgraph3, 
                                  xselectedImposedBokehGraph, 
                                  xxlayout_graph1,
                                  xpd_responder_direction,
                                  xtable_inverse_responder_ego,
                                  xtable_responder_ego):

    print('.-.-.-.-.- finacGDB_AA_IRA_Model/FD_businessComponentSelection')
    
    p_d_dict_employee_by_name = \
        xnetwork_parameters_dict.get('dict_employee_by_name')
    # print(">>>>>>>>>> dict_employee_reverse (FD_businessComponentSelection)")
    # print(dict_employee_reverse)
    
    pd_tablaModeloCompleto = \
        xparameters_for_business_component_selection_dict.get\
            ('tablaModeloCompletoDF')
    pd_sourceModeloFiltrado = \
        xparameters_for_business_component_selection_dict.get\
            ('sourceModeloFiltrado')
    pd_sourceDelta = xparameters_for_business_component_selection_dict.get\
        ('sourceDelta')
    pd_keyComponents = xparameters_for_business_component_selection_dict.get\
        ('_keyComponentsConnected')
    pd_businessComponents = \
        xparameters_for_business_component_selection_dict.get\
            ('_businessComponentsConnected')
    pd_fields_table_filtered_employee = \
        xparameters_for_business_component_selection_dict.get\
            ('fields_table_filtered_employee')    
    
    _layout_graph1 = xgraph1.layout_provider
    
    updated_completeNxGraph = \
        UTBo_BokehGraphToNetworkxGraph(xplot1.renderers[0])
            
    # print(xexcluded_select.value)
    # print(">>>>>>>>>> len(xkeyComponents) (FD_businessComponentSelection)")
    # print(len(pd_keyComponents))
    # print(">>>>>>>>>> pd_businessComponents (FD_businessComponentSelection)")
    # print(pd_businessComponents)
    # print(">>>>> len(pd_businessComponents) (FD_businessComponentSelection)")
    # print(len(pd_businessComponents))
    # print(">>>>> xcompleteNxGraph.nodes() (FD_businessComponentSelection)")
    # print(xcompleteNxGraph.nodes())
    # print(">>> len(xcompleteNxGraph.nodes()) (FD_businessComponentSelection)")
    # print(len(xcompleteNxGraph.nodes()))
    
    excluded_select_values = xexcluded_select.value
    print(">>>>>>>>>> dict_employee_by_name (FD_businessComponentSelection)")
    print(p_d_dict_employee_by_name)
    print(">>>>>>>>>> excluded_select_value (FD_businessComponentSelection)")
    print(excluded_select_values)
    excluded_select_ids = \
        [p_d_dict_employee_by_name.get(excluded_select_value)[0] 
         for excluded_select_value in excluded_select_values]
        
    XXXedges = 'aa'

    xg1 = xplot1.renderers[0]
    dsnrp1 = xplot1.renderers[0].node_renderer.data_source
    # print(".-.-.-.-.-FD_businessComponentSelection - dsnrp1")
    # print(dict(dsnrp1.data))
    dshrp1 = xplot1.renderers[0].edge_renderer.data_source
    # print(".-.-.-.-.-FD_businessComponentSelection - dshrp1")
    # print(dict(dshrp1.data))

    xg11 = UTBo_BokehGraphToNetworkxGraph(xg1)
    # print(".-.-.-.-.- len(xg11.nodes) (FD_businessComponentSelection")
    # print(len(xg11.nodes()))
    # print(".-.-.-.-.-FD_businessComponentSelection - xg11 edges")
    # print(xg11.edges(data=True))

    _businessComponentsToEliminate = excluded_select_ids
    # print(">>>> _businessComponentsToEliminate (FD_businessComponentSelection)")
    # print(_businessComponentsToEliminate)
    
    businessComponentsToEliminateIndexes = \
        [pd_businessComponents.index(bctoe)
         for bctoe in _businessComponentsToEliminate]
    # print('>>>> businessComponentsToEliminateIndexes (FD_businessComponentSelection)')
    # print(businessComponentsToEliminateIndexes)

    # .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- refresca las tablas
    Gf, tablef, densityGf = \
        FD_CreateGraphAndMetricsII(pd_keyComponents, pd_businessComponents, 
                                   XXXedges,
                                   businessComponentsToEliminateIndexes,
                                   100, xnodeSizeAttribute, xplot1)
                                   # xamplifier, xnodeSizeAttribute, xplot1)

    pd_sourceModeloFiltrado.data = tablef

    deltaTablef = FD_DeltaTable(pd_tablaModeloCompleto, tablef)

    pd_sourceDelta.data = deltaTablef

    #
    # .-.-.-.-.-.-.-.-.-.-.-. refresca los nodos seleccionados en el plot
    UTBo_Network_FlushSelectedNodesGlyph(xselectedImposedBokehGraph)

    selectedNodesNxGraph = nx.Graph()

    for node in updated_completeNxGraph.nodes:
        if node in  excluded_select_ids:
            optional_attrs = updated_completeNxGraph.nodes[node]
            selectedNodesNxGraph.add_node(node, **optional_attrs)
            # print('>>> node added to selectedNodesNxGraph (FD_businessComponentSelection)')
            # print(node)

    UTBo_Network_AddSelectedNodesGlyph(xplot1, _layout_graph1,
                                       xselectedImposedBokehGraph,
                                       selectedNodesNxGraph, 8)

    #
    pvuplott, grapht = \
        UTBo_Network_PlotType2(Gf, [], 'xx',
                           nx.spring_layout,
                           _layout_graph1, False,
                           10, 10,
                           xnodeSize='node_size',
                           xadjustNodeSize=True)  
       
    dsnrp2 = grapht.node_renderer.data_source
    xgraph2.node_renderer.data_source.data = dict(dsnrp2.data)

    dshrp2 = grapht.edge_renderer.data_source
    xgraph2.edge_renderer.data_source.data = dict(dshrp2.data)

    layoutt = xgraph2.layout_provider

    layoutt.graph_layout = dict(_layout_graph1.graph_layout)

    xplot2 = FD_Arrows(xplot2, xrendererToUpdate=1)

    # .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- refrescar plot ego de los eliminados

    eliminatedNodesPredecessorEgosNodes, eliminatedNodesSuccessorEgosNodes = \
        FD_eliminatedNodesEgosNodes(updated_completeNxGraph,
                                    _businessComponentsToEliminate, 1)
    # print('>>>>> eliminatedNodesPredecessorEgosNodes (FD_businessComponentSelection)')
    # print(eliminatedNodesPredecessorEgosNodes)
    # print('>>>>> eliminatedNodesSuccessorEgosNodes (FD_businessComponentSelection)')
    # print(eliminatedNodesSuccessorEgosNodes)
    
    #>.<.<.<.<.<.<.<.<.<.<.<.<.
    responder_dirección, responder_número_conexiones_componentes_eliminados,\
        responder_egoNxGraph, inverse_responder_dirección, \
            inverse_responder_número_conexiones_componentes_eliminados, \
                inverse_responder_egoNxGraph = \
                    FD_responder_and_inverse_graphs\
                        (updated_completeNxGraph,
                          xpd_responder_direction, 
                          _businessComponentsToEliminate) 
    
    
    #
    successor_egoNxGraphSubGraph = \
        updated_completeNxGraph.subgraph(eliminatedNodesSuccessorEgosNodes)
    _egoNxGraph = successor_egoNxGraphSubGraph.copy()
    
    # print('>>>> _egoNxGraph.nodes(data=True) (FD_businessComponentSelection)')
    # print(_egoNxGraph.nodes(data=True))

    #    
    número_conexiones_componentes_eliminados, dirección = \
        FD_ego_graph(_egoNxGraph, 'out_degree',
                      updated_completeNxGraph, 
                      _businessComponentsToEliminate)

    # print('>>>> _egoNxGraph.nodes(data=True) (FD_businessComponentSelection)')
    # print(_egoNxGraph.nodes(data=True))
    
    #    
    inverse_pvuplottego, inverse_graphtego = \
            UTBo_Network_PlotType2(inverse_responder_egoNxGraph, [], 'xx',
                               nx.spring_layout,
                               _layout_graph1, True,
                               10, 10,
                               xnodeSize='node_size',
                               xadjustNodeSize=True)  
        
    _table_inverse_responder_ego = \
        UTBo_nx_nodes_to_DataTable(inverse_responder_egoNxGraph,
                             xattributes = pd_fields_table_filtered_employee,
                             xwidth = 550, xheight = 600)

    datasource = _table_inverse_responder_ego.source.data
    xtable_inverse_responder_ego.source.data = dict(datasource)

    _table_responder_ego = \
        UTBo_nx_nodes_to_DataTable(responder_egoNxGraph,
                             xattributes = pd_fields_table_filtered_employee,
                             xwidth = 550, xheight = 600)

    datasource = _table_responder_ego.source.data
    xtable_responder_ego.source.data = dict(datasource)



    dsnrp2 = inverse_graphtego.node_renderer.data_source
    xgraph2.node_renderer.data_source.data = dict(dsnrp2.data)
    
    # print('>>> dict(dsnrp3.data) (FD_businessComponentSelection)')
    # print(dict(dsnrp3.data))

    dshrp2 = inverse_graphtego.edge_renderer.data_source
    xgraph2.edge_renderer.data_source.data = dict(dshrp2.data)

    layout_graph2 = xgraph2.layout_provider
    layout_graph2.graph_layout = dict(_layout_graph1.graph_layout)

    xplot2 = FD_Arrows(xplot2, xrendererToUpdate=1)

    xplot2.title.text = \
        'Ego inverso - Conexiones['+inverse_responder_dirección\
            +']:' + \
        inverse_responder_número_conexiones_componentes_eliminados

    #
    pvuplottego, graphtego = \
            UTBo_Network_PlotType2(responder_egoNxGraph, [], 'xx',
                               nx.spring_layout,
                               _layout_graph1, True,
                               10, 10,
                               xnodeSize='node_size',
                               xadjustNodeSize=True)



    dsnrp3 = graphtego.node_renderer.data_source
    xgraph3.node_renderer.data_source.data = dict(dsnrp3.data)
    
    # print('>>> dict(dsnrp3.data) (FD_businessComponentSelection)')
    # print(dict(dsnrp3.data))

    dshrp3 = graphtego.edge_renderer.data_source
    xgraph3.edge_renderer.data_source.data = dict(dshrp3.data)

    layout_graph3 = xgraph3.layout_provider
    layout_graph3.graph_layout = dict(_layout_graph1.graph_layout)

    xplot3 = FD_Arrows(xplot3, xrendererToUpdate=1)

    #
    xplot3.title.text = \
        'Ego componentes eliminados - Conexiones['+responder_dirección\
            +']:' + \
        responder_número_conexiones_componentes_eliminados



#%%
def FD_filtered_nodes_ego_graph(xconn, xnetwork_parameters_dict,
                                # xnetwork_parameters_data_table,
                                xnodesToEliminate,
                                x_businessComponentsConnected,
                                x_keyComponentsConnected,
                                xamplifier,
                                xfrequencyCorte, 
                                xfrequencyResponseAccumulation,
                                xactive_selected_possible_responses,
                                xall_any_filter_group_active,
                                xcompleteNxGraph,
                                xtablaModeloCompletoDF
                                ):
    
    """
    Recieves an nx graph (xcompleteNxGraph) and a list of nodes to eliminate
    (xnodesToEliminate), and returns 3 nx graphs: 
        - the input graph without the eliminated nodes (filteredNxGraph)
        - an nx graph with the eliminated nodes and their predecessors
            (predecessor_egoNxGraph)
        - an nx graph with the eliminated nodes and their antecessors
            (antecessor_egoNxGraph)
    Note: the last 2 graphs only have edges that connect to elminated nodes.
    
    input:  - xnetwork_parameters_dict
            - xnodesToEliminate
            - x_businessComponentsConnected,
            - x_keyComponentsConnected
            - xamplifier
            - xfrequencyCorte
            - xfrequencyResponseAccumulation
            - xactive_selected_possible_responses
            - xfilter_group_active
            - xcompleteNxGraph
            - xtablaModeloCompletoDF
    
    output: - businessComponentsToEliminate, 
            - densityG2: filteredNxGraph's density'  
            - filteredNxGraph
            - tablaModeloFiltradoDF: centralities for each node in 
                                        filteredNxGraph
            - deltaTable: difference in centralities for each node between
                            filteredNxGraph and xcompleteNxGraph
            - dirección
            - número_conexiones_componentes_eliminados
            - predecessor_egoNxGraph
    """
    print('.-.-.-.-.- finacGDB_AA_IRA_Model/FD_filtered_nodes_ego_graph')
    # print('>>>>>> xnodesToEliminate (FD_filtered_nodes_ego_graph)')
    # print(xnodesToEliminate)
    # print('>>>>>> x_businessComponentsConnected (FD_filtered_nodes_ego_graph)')
    # print(x_businessComponentsConnected)
    
    # p_d_node_size_attribute = \
    #     xnetwork_parameters_dict.get('node_size_attribute')
    # print('>>>>>> p_d_node_size_attribute (FD_filtered_nodes_ego_graph)')
    # print(p_d_node_size_attribute)
    
    #
    p_d_responder_direction = \
        xnetwork_parameters_dict.get('responder_direction')
        
    #
    businessComponentsToEliminate = \
        [x_businessComponentsConnected[businessComponentIndex]
          for businessComponentIndex in xnodesToEliminate]

    # print('>>> businessComponentsToEliminate (FD_filtered_nodes_ego_graph)')
    # print(businessComponentsToEliminate)
    
    #
    #filteredNxGraph- nx.grafo sin nodesToEliminate. NOTA: los edges los 
    #                    extrae de 
    #                    neo4j con un query con los siguientes parámetros:
    #                    - cycle, 
    #                    - network_mode_theme
    #                    - id_question
    #tablaModeloFiltradoDF- df con todas las métricas 
    #densityG2- densidad 
    #componentName_color_Dict- diccionario de colores por área
    filteredNxGraph, tablaModeloFiltradoDF, densityG2, _, _, _ = \
        FD_CreateGraphAndMetrics(xconn, xnetwork_parameters_dict, 
                                 # xnetwork_parameters_data_table,
                                  -1, 
                                  -1,
                                  businessComponentsToEliminate, 
                                  xamplifier,
                                  xfrequencyCorte, 
                                  xfrequencyResponseAccumulation,
                                  xactive_selected_possible_responses,
                                  xall_any_filter_group_active)
    # print('>>>>>>>>>>>>>>> filteredNxGraph.nodes (FD_filtered_nodes_ego_graph)')
    # print(filteredNxGraph.nodes())
    # print(len(filteredNxGraph.nodes()))
    
    
    #
    #deltaTable-diferencias en centralidades
    deltaTable = FD_DeltaTable(xtablaModeloCompletoDF, tablaModeloFiltradoDF)
    # print('>>>>>>>>>>>>>>>>> deltaTable (FD_AA_model_main)')
    # print(deltaTable)
    
    #    
    responder_dirección, responder_número_conexiones_componentes_eliminados,\
        responder_egoNxGraph, inverse_responder_dirección, \
            inverse_responder_número_conexiones_componentes_eliminados, \
                inverse_responder_egoNxGraph = \
                    FD_responder_and_inverse_graphs\
                        (xcompleteNxGraph,
                         p_d_responder_direction, 
                         businessComponentsToEliminate)       
        
    return businessComponentsToEliminate, densityG2, filteredNxGraph,\
        tablaModeloFiltradoDF, deltaTable, responder_dirección, \
            responder_número_conexiones_componentes_eliminados, \
                responder_egoNxGraph, inverse_responder_dirección, \
                    inverse_responder_número_conexiones_componentes_eliminados, \
                        inverse_responder_egoNxGraph
    
    
# %%

def FD_AA_model_main(xconn, xnetwork_parameters_dict, 
                     # xnetwork_parameters_data_table, 
                     xxxactors_data, xxXedges, xamplifier,
                     xfrequencyCorte, xfrequencyResponseAccumulation,
                     xactive_selected_possible_responses,
                     xall_any_filter_group_active,
                     xgravityLevel=0,
                     xnode_color_attribute = 'organization_area_color'):
    
    """
    xdefiniciónTablaInteracción: texto explicación de como interpretar filas
                                 y columnas de matriz adyacente
    """
    
    print('.-.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Model/FD_AA_model_main')
    # print('>>>>>>>>>>>>>>>>> xnetwork_parameters_dict (FD_AA_model_main)')
    # print(xnetwork_parameters_dict)
    
    network = xnetwork_parameters_dict.get('network')
    definiciónTablaInteracción = \
        xnetwork_parameters_dict.get('definiciónTablaInteracción')
    legends_dict = xnetwork_parameters_dict.get('legends_dict')
    language = xnetwork_parameters_dict.get('language') 
    p_d_fields_table_filtered_employee = \
        xnetwork_parameters_dict.get('fields_table_filtered_employee')
    dict_employee = \
        xnetwork_parameters_dict.get('dict_employee')
    
    print('>>>>>>>>>>>> p_d_fields_table_filtered_employee (FD_AA_model_main)')
    print(p_d_fields_table_filtered_employee)
    print('>>>>>>>>>>>> xamplifier (FD_AA_model_main)')
    print(xamplifier)
    print('>>>>>>>>>>>> network (FD_AA_model_main)')
    print(network)
    print('>>>>>>>>>>>> xfrequencyCorte (FD_AA_model_main)')
    print(xfrequencyCorte)
    print('>>>>>>>>>>>> xfrequencyResponseAccumulation (FD_AA_model_main)')
    print(xfrequencyResponseAccumulation)
    print('>>>>>>>>>>>> xactive_selected_possible_responses (FD_AA_model_main)')
    print(xactive_selected_possible_responses)
    print('>>>>>>>>>>>> xgravityLevel (FD_AA_model_main)')
    print(xgravityLevel)
    print('>>>>>>>>>>>> xall_any_filter_group_active (FD_AA_model_main)')
    print(xall_any_filter_group_active)
    
    # a=5/0


    plotHeight_todos = 500
    plotWidth_todos = 800
    plotHeight_filtrado = 500
    plotWidth_filtrado = 600


    #
    #allCompleteNxGraph- nx.grafo completo NOTA: los edges los extrae de 
    #                    neo4j con un query con los siguientes parámetros:
    #                    - cycle, 
    #                    - network_mode_theme
    #                    - id_question
    #tablaModeloCompletoDF- df con todas las métricas 
    #densityG1- densidad 
    #componentName_color_Dict- diccionario de colores por área
    allCompleteNxGraph, tablaModeloCompletoDF, densityG1, \
        componentName_color_Dict, businessComponents, keyComponents = \
        FD_CreateGraphAndMetrics(xconn, xnetwork_parameters_dict, 
                                 # xnetwork_parameters_data_table,
                                 -1, -1,
                                 [], xamplifier,
                                 xfrequencyCorte,
                                 xfrequencyResponseAccumulation,
                                 xactive_selected_possible_responses,
                                 xall_any_filter_group_active)
        
    # print('>>>>>>>>>>>>>>>>> allCompleteNxGraph.nodes (FD_AA_model_main)')
    # print(allCompleteNxGraph.nodes(data=True))
    # print('$$$$$$$$$$$$$$$$$$$$$$')
    # print('>>>>>>>>>>>>>>>>>>> allCompleteNxGraph.edges(data=True) (FD_AA_model_main)')
    # print(allCompleteNxGraph.edges(data=True))
    # print(len(allCompleteNxGraph.nodes()))
    # print('>>>>>>>>>>>>>>>>> tablaModeloCompletoDF (FD_AA_model_main)')
    # print(tablaModeloCompletoDF)
    # print('>>>>>>>>>>>>>>>>> componentName_color_Dict (FD_AA_model_main)')
    # print(componentName_color_Dict)
    # print('>>>>>>>>>>>>>>> businessComponents (FD_AA_model_main)')
    # print(businessComponents)
    # print('>>>>>>>>>>>>>>> keyComponents)  (FD_AA_model_main)')
    # print(keyComponents)
    
    
    connected_nodes = \
        [n for n in allCompleteNxGraph.nodes
         if (allCompleteNxGraph.nodes[n]['in_degree_centrality'] > 0) |
         (allCompleteNxGraph.nodes[n]['out_degree_centrality'] > 0)]
    
    all_employees_ids_list = [k for k,v in dict_employee.items()]
    non_connected_nodes_ids = \
        list(set(all_employees_ids_list) - set(connected_nodes))
    non_connected_nodes = \
        [dict_employee.get(node_id)[0] for node_id in non_connected_nodes_ids]
    # print('>>>>>>>>>>>>>>> len(connected nodes)  (FD_AA_model_main)')
    # print(len(connected_nodes))
    # print('>>>>>>>>>>>>>>> non connected nodes  (FD_AA_model_main)')
    # print(non_connected_nodes)
    # print('>>>>>>>>>>>>>>> non_connected_nodes  (FD_AA_model_main)')
    # print(non_connected_nodes)
    # print(len(non_connected_nodes))
    
    #
    #unordered_completeNxGraph- subgrafo con solo nodos conectados
    #indexConnected- índices de los nodos conectados
    #_keyComponentsConnected- lista nodos (personas) conectados
    #_businessComponentsConnected- lista de áreas de los nodos conectados
    unordered_completeNxGraph = allCompleteNxGraph.subgraph(connected_nodes)
    indexConnected = [index for index in range(0, len(businessComponents))
                      if businessComponents[index] in connected_nodes]
    _keyComponentsConnected = [keyComponents[index]
                               for index in indexConnected]
    _businessComponentsConnected = \
        [businessComponents[index] for index in indexConnected]
    # print('>>>>>>>>>>>>>>>>>>>>>>>>> index connected (FD_AA_model_main)')
    # print(indexConnected)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>> _keyComponentsConnected (FD_AA_model_main)')
    # print(_keyComponentsConnected)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>> _businessComponentsConnected (FD_AA_model_main)')
    # print(_businessComponentsConnected)
    
    non_connected_list = MultiSelect(title="Agentes no conectados:",
                                     options=non_connected_nodes,
                                     height=150, width=200)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>> non_connected_list (FD_AA_model_main)')
    # print(non_connected_list)
    
    tooltips = [("id_employee", "@index"),
                ("employee", "@employee"),
                ("area", "@organization_area"),
                ('total_degree_centrality', '@total_degree_centrality'),
                ('unscaled_total_degree_centrality',
                '@unscaled_total_degree_centrality'),
                ('in_degree_centrality', '@in_degree_centrality'),
                ('unscaled_in_degree_centrality',
                 '@unscaled_in_degree_centrality'),
                ('out_degree_centrality', '@out_degree_centrality'),
                ('unscaled_out_degree_centrality',
                 '@unscaled_out_degree_centrality'),
                ('community', '@informal_network')]

    
    title1 = 'Modelo completo - Network density = '+str(densityG1)

    #    
    # agrega gravityLevel al edge cuando hay comunicación en ambos sentidos
    # el atributo es 'gravity'
    unordered_completeNxGraph = \
        FD_Add_Gravity(unordered_completeNxGraph, xgravityLevel)
    # unordered_completeNxGraph = FD_Add_Gravity(unordered_completeNxGraph, 0)

    #
    # informal_network_graph es el grafo con informal_networks
    # Tiene que ser undirected
    informal_network_attribute = 'informal_network'
    informal_network_graph = unordered_completeNxGraph.copy()
    informal_network_graph = nx.Graph(informal_network_graph)
    
    #
    # agrega el atributo 'community' al nodo
    # a los edges les agrega los siguiente atributos:
    # 'community'(0 si comunican nodos de comunidades diferentes)
    # 'base_weight'(2 si comunican nodos de la misma comunidad,1 si no)
    # 'weight'(2 si comunican nodos de la misma comunidad,1 si no)
    # 'width'(3 si comunican nodos de la misma comunidad,0.25 si no)
    # _communities es una lista inmutable de communities
    # print('>>>>>>>>>>>>>>>>>> iraUjwaryPaper1 llamado cuando se crean communities')
    _communities = \
        FD_Community_net(informal_network_graph, xedgeCommunityColor=True)
    
    
    
    # print('>>>>>>>>>>>>> informal_network_graph  (FD_AA_model_main)')
    # print(informal_network_graph.nodes(data=True))
    # print(informal_network_graph.edges(data=True))

    # print('>>>>>>>>>>>>> unordered_completeNxGraph antes  (FD_AA_model_main)')
    # print(unordered_completeNxGraph.nodes(data=True))
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(unordered_completeNxGraph.edges(data=True))

    """    
    node_informal_network_dictionary: diccionario de 'community' en los 
          nodos H
    """
    node_informal_network_dictionary = \
        {u: d[informal_network_attribute]
         for u, d in informal_network_graph.nodes(data=True)}

    nx.set_node_attributes(unordered_completeNxGraph,
                           node_informal_network_dictionary,
                           informal_network_attribute)

    """
    a los edges les agrega los siguiente atributos:
    'community'(0 si comunican nodos de comunidades diferentes)
    'base_weight'(2 si comunican nodos de la misma comunidad,1 si no)
    'weight'(2 si comunican nodos de la misma comunidad,1 si no)
    'width'(3 si comunican nodos de la misma comunidad,0.25 si no)
    """
    FD_Set_edge_community(unordered_completeNxGraph,
                          informal_network_attribute)
    
    
    """
    # pone 'community_color' a los edges
    # print('llamado 1 a FD_Set_edge_community_color')
    """
    _informal_network_palette_dict = \
        FD_Set_edge_community_color(unordered_completeNxGraph, _communities,
                                    informal_network_attribute)
    # print('>>>>>>>>>> _informal_network_palette_dict (FD_AA_model_main)')
    # print(_informal_network_palette_dict)
    
    FD_Set_node_community_color(unordered_completeNxGraph, 'informal_network', 
                                _informal_network_palette_dict)
    
    # print('>>>>>>>>>>>>> unordered_completeNxGraph después  (FD_AA_model_main)')
    # print(unordered_completeNxGraph.nodes(data=True))
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print(unordered_completeNxGraph.edges(data=True))
        
    
    """
    completeNxGraph- es todo el grafo con los atributos de communities, con
                     los nodos ordenados por community
    pos- posiciones de nodos con layout circular. Se usa como punto de
         para que cuando se genere el plot con spring layout, los nodos de
         una misma comunidad queden cerca.
    """
    completeNxGraph = FD_Ordered_circular_communities(unordered_completeNxGraph,
                                                      informal_network_attribute)
    pos = nx.circular_layout(completeNxGraph)
    # print('>>>>>>>>>>>>> completeNxGraph  (FD_AA_model_main)')
    # print(completeNxGraph.nodes(data=True))
    
    informal_networks = \
        list(set([v['informal_network']
             for n, v in completeNxGraph.nodes(data=True)]))
    # print('informal_networks - iraUjwary 1182')
    # print(informal_networks)

    nodes_by_community = \
        [[node for node, v in completeNxGraph.nodes(data=True)
          if v['informal_network'] == group]
         for group in informal_networks]
    # print('>>>>>>>>>>>>> nodes_by_community (finacGB_AA_IRA_Model)')
    # print(nodes_by_community)
    
       
    
    quotient_graph_informal_network = \
        nx.quotient_graph(completeNxGraph, nodes_by_community, relabel=True)
    
    informal_networks_DF = pd.DataFrame(informal_networks)
    # print('informal_networks_DF')
    # print(informal_networks_DF)
    informal_networks_Dict = informal_networks_DF.to_dict('index')
    # print('informal_networks_Dict')
    # print(informal_networks_Dict)

    degree_dict_quotient_graph_informal_network = \
        {k: v for k, v in \
         nx.degree_centrality(quotient_graph_informal_network).items()}
    
    for (n, d) in quotient_graph_informal_network.nodes(data=True):
        del d["graph"]
        d['node_size'] = d["nnodes"] * 10
        d['informal_network'] = n+1
        d['informal_network_color'] = \
            _informal_network_palette_dict[d['informal_network']]
        d['degree_centrality'] = \
            degree_dict_quotient_graph_informal_network[n]

    for u, v, d in quotient_graph_informal_network.edges(data=True):
        d['edge_width'] = d["weight"] * 2
        
    dict_organization_areas = \
        xnetwork_parameters_dict.get('dict_organization_area')
    # print('>>>>>>>>>>>>>>>>> dict_organization_areas (finacGB_AA_IRA_Model)')
    # print(dict_organization_areas)
    
    
    #
    organization_area_nodes_by_organization_area_all_tuples = \
        [(id_organization_area,
          [node for node, v in completeNxGraph.nodes(data=True)
          if v['id_organization_area'] == id_organization_area])
         for id_organization_area, _ in dict_organization_areas.items()]
    organization_area_nodes_by_organization_area_tuples = \
        [(id_organization_area, organization_area_nodes) 
          for id_organization_area, organization_area_nodes 
          in organization_area_nodes_by_organization_area_all_tuples
          if len(organization_area_nodes)>0]
    # print('>>>>>>>>>>>>> organization_area_nodes_by_organization_area_tuples (finacGB_AA_IRA_Model)')
    # print(organization_area_nodes_by_organization_area_tuples)
    
    organization_areas_ids_list, nodes_in_organzation_areas_lists_list = \
        map(list,zip(*organization_area_nodes_by_organization_area_tuples))
    # print('>>>>>>>>>>>>> organization_areas_ids_list (finacGB_AA_IRA_Model)')
    # print(organization_areas_ids_list)
    # print('>>>>>>>>>>>>> nodes_in_organzation_areas_lists_list (finacGB_AA_IRA_Model)')
    # print(nodes_in_organzation_areas_lists_list)
    
        
    #
    #BM2- grafo en el cual los nodos son las redes informales
    quotient_graph_organization_area = \
        nx.quotient_graph(completeNxGraph, 
                          nodes_in_organzation_areas_lists_list, 
                          relabel=True)
    # print('>>>>>>> quotient_graph_organization_area.nodes (finacGB_AA_IRA_Model)')
    # print(quotient_graph_organization_area.nodes(data=True))
    # print('>>>>>>> quotient_graph_organization_area.edges (finacGB_AA_IRA_Model)')
    # print(quotient_graph_organization_area.edges(data=True))
    
    #
    quotient_graph_organization_area_nodes_list = \
        [k for k,_ in quotient_graph_organization_area.nodes(data=True)]
    # print('>>>>>>> quotient_graph_organization_area_nodes_list (oihub_AA_IRA_Model)')
    # print(quotient_graph_organization_area_nodes_list)
    
    quotient_nodes_ids_vs_nodes_organization_areas_ids_dict = \
        {id_quotient_node:node_organization_area_id
         for id_quotient_node, node_organization_area_id
         in zip(quotient_graph_organization_area_nodes_list,
                organization_areas_ids_list)}
    # print('>>>>>>> quotient_nodes_ids_vs_nodes_organization_areas_ids_dict (oihub_AA_IRA_Model)')
    # print(quotient_nodes_ids_vs_nodes_organization_areas_ids_dict)
    
    #
    nx.relabel_nodes(quotient_graph_organization_area,
                     quotient_nodes_ids_vs_nodes_organization_areas_ids_dict, 
                     copy=False)
    # print('>>>>>>> quotient_graph_organization_area.nodes (finacGB_AA_IRA_Model)')
    # print(quotient_graph_organization_area.nodes(data=True))
        
    nx.set_node_attributes(quotient_graph_organization_area, 
                           dict_organization_areas,
                           'organization_area')
    # print('>>>>>>> quotient_graph_organization_area.nodes (finacGB_AA_IRA_Model)')
    # print(quotient_graph_organization_area.nodes(data=True))
    
    degree_dict_quotient_graph_organization_area = \
        {k: v for k, v in \
         nx.degree_centrality(quotient_graph_organization_area).items()}

    # print('>>>>>>>>>>>>> degree_dict_quotient_graph_organization_area (finacGB_AA_IRA_Model)')
    # print(degree_dict_quotient_graph_organization_area)
    
        
    for (n, d) in quotient_graph_organization_area.nodes(data=True):
        # print('>>>>>>>>>>>>> n in quotient_graph_organization_area (finacGB_AA_IRA_Model)')
        # print(n)
        # print('>>>>>>>>>>>>> d in quotient_graph_organization_area (finacGB_AA_IRA_Model)')
        # print(d)
        del d["graph"]
        d['node_size'] = d["nnodes"] * 10
        d['organization_area_color'] = \
            componentName_color_Dict[n]
        d['degree_centrality'] = \
            degree_dict_quotient_graph_organization_area[n]

    for u, v, d in quotient_graph_organization_area.edges(data=True):
        d['edge_width'] = d["weight"] * 2
    
    # print('>>>>>>> quotient_graph_organization_area.nodes (finacGB_AA_IRA_Model)')
    # print(quotient_graph_organization_area.nodes(data=True))
    
    
    #
    #plot_quotient- es el plot de las redes informales como nodos
    toolTips_quotient_graph_informal_network = \
        [("red informal", "@informal_network"),
         ('número actores', '@nnodes'),
         ('degree_centrality', '@degree_centrality')]
    plot_quotient_informal_network, plot_quotient_graph = \
        UTBo_Network_PlotType2(quotient_graph_informal_network, 
                               toolTips_quotient_graph_informal_network, 
                               title1,
                               nx.circular_layout, nx.circular_layout, False,
                               int(plotHeight_todos *
                                   0.8), int(plotHeight_todos*0.8),
                               xnodeSize='node_size',
                               xminimumNodeSize=8,
                               xmaximumNodeSize=24,
                               xnodeColorAttribute='informal_network_color',
                               xadjustNodeSize=True,
                               xedgeWidthAttribute='edge_width',
                               xadjustEdgeWidth = True)
        
    toolTips_quotient_graph_organization_area = \
        [("area", "@organization_area"),
         ('número actores', '@nnodes'),
         ('degree_centrality', '@degree_centrality')]
    
    plot_quotient_organization_area, plot_quotient_graph = \
        UTBo_Network_PlotType2(quotient_graph_organization_area, 
                               toolTips_quotient_graph_organization_area, 
                               title1,
                               nx.circular_layout, nx.circular_layout, False,
                               int(plotHeight_todos *
                                   0.8), int(plotHeight_todos*0.8),
                               xnodeSize='node_size',
                               xminimumNodeSize=8,
                               xmaximumNodeSize=24,
                               xnodeColorAttribute='area_color',
                               xadjustNodeSize=True,
                               xedgeWidthAttribute='edge_width',
                               xadjustEdgeWidth = True)

    
    
    #
    #plot_informal_network- es el plot completo con circular_layout
    plot_informal_network, plot_informal_graph = \
        UTBo_Network_PlotType2(completeNxGraph, tooltips, title1,
                               nx.circular_layout, nx.circular_layout, False,
                               plotHeight_todos, plotHeight_todos,
                               xnodeSize='node_size',
                               xnodeColorAttribute=xnode_color_attribute,
                               xedgeColorAttribute='informal_network_color',
                               xadjustNodeSize=True,
                               xedgeWidthAttribute='informal_network_width',
                               xColorLegendTitle=['Node color is area'])

    #
    #plot_area_network- similar a plot_informal_network, pero con
    area_network_attribute = 'id_organization_area'
    
    #
    completeNxGraph = \
        FD_Ordered_circular_communities(completeNxGraph,
                                        area_network_attribute)
    
    
    
    #
    FD_Set_edge_community(completeNxGraph, area_network_attribute)
    componentName_color_Dict[0] = 'black'
    
    # print('>>>>>>>>>>>>>>> componentName_color_Dict  (FD_AA_model_main)' )
    # print(componentName_color_Dict)
    FD_Set_edge_community_color(completeNxGraph, 'NA', 
                                area_network_attribute,
                                xpaletteDict=componentName_color_Dict)
    # print('>>>>>>> completeNxGraph.edges 2 (FD_AA_model_main)')
    # print(completeNxGraph.edges(data=True))
    # print(">>>>>>>>>>>>>>> completeNxGraph.edges(data=True)  (FD_AA_model_main)")
    # print(completeNxGraph.edges(data=True))
    
    
    plot_area_network, plot_area_graph = \
        UTBo_Network_PlotType2(completeNxGraph, tooltips, title1,
                               nx.circular_layout, nx.circular_layout, False,
                               plotHeight_todos, plotHeight_todos,
                               xnodeSize='node_size',
                               xnodeColorAttribute='informal_network_color',
                               xedgeColorAttribute='id_organization_area_color',
                               xadjustNodeSize=True,
                               xedgeWidthAttribute='id_organization_area_width',
                               xColorLegendTitle=['Node color is community'])

    core_layout = 0
    plot_core = 0
        
    # print('>>>>>>>>>>>>>>>>>> completeNxGraph.nodes(data=True) (FD_AA_model_main)')
    # print(completeNxGraph.nodes(data=True))
        
    if xnode_color_attribute == 'organization_area_color':
        colorLegendTitle = UT_bring_legend('l-005', language, legends_dict)
        keyColorAttribute='organization_area'
    else:
        colorLegendTitle = UT_bring_legend('l-006', language, legends_dict)
        keyColorAttribute='cvf_cluster'
    # print('>>>>>>>>>>>>>>>>>> colorLegendTitle (FD_AA_model_main)')
    # print(colorLegendTitle)
    
    
    # print('>>>>>>>>>>>>>>>>>> completeNxGraph antes de plot1 (FD_AA_model_main)')
    # print(completeNxGraph.nodes(data=True))
    # print(completeNxGraph.edges(data=True))
    # print([(u,v.get(keyColorAttribute),v.get(keyColorAttribute+'_color'))
    #       for u,v in completeNxGraph.nodes(data=True)])
    
    """
    #plot1- plot principal
    """
    plot1, graph1 = UTBo_Network_PlotType2(completeNxGraph, tooltips, title1,
                                           nx.spring_layout, nx.spring_layout, False,
                                           plotHeight_todos, plotWidth_todos,
                                           xnodeSize='node_size',
                                           xnodeColorAttribute = \
                                               xnode_color_attribute,
                                           xedgeColorAttribute='informal_network_color',
                                           xadjustNodeSize=True,
                                           xedgeWidthAttribute='informal_network_width',
                                           xpos=pos,
                                           xkeyColorAttribute=keyColorAttribute,
                                           xColorLegendTitle=[colorLegendTitle],
                                           xk=1.5,
                                           xleft_margin = 1.0,
                                           xlegend_text_font_size = '12px')

    # .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- campos para summary
    qu_filasG = completeNxGraph.number_of_nodes()
    qu_columnasG = completeNxGraph.number_of_nodes()
    qu_linksG = completeNxGraph.number_of_edges()
    qu_centralizationG = \
        UTNx_getCentralization(nx.degree_centrality(completeNxGraph), 'degree')
    nodeDF = UTNx_make_node_df(completeNxGraph)
    # print(">.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.> iraUjwaryPaper1")
    # print(">>>>>>>>>>>>>>>>>>>>>>>>>>>> iraUjwaryPaper1")
    # print('>>>>>>>>>>> nodeDF FD_AA_model_main')
    # print(nodeDF.columns)
    # print(nodeDF.to_dict('records'))
    
    nodeDF.drop(['node_size', 'organization_area_color'], axis=1, inplace=True)

    if network != '':
        nodeDF.to_csv('SURV_Centralities_'+ network +
                      '.csv', sep=',', encoding='utf-8')

    nodeDF_CDS = ColumnDataSource(nodeDF)
    columns_CDS = [TableColumn(field=Ci, title=Ci)
                   for Ci in nodeDF.columns]  # bokeh columns
    data_table_nodeDF = DataTable(source=nodeDF_CDS,
                                  columns=columns_CDS, width=1400,
                                  height=600)

    # mainAInDegreePlot, mainAInDegreeGraph = UTBo_NodePlot(
    #     nodeDF, 'in_degree_centrality', 15, label_column = 'employee')
    # mainAOutDegreePlot, mainAOutDegreeGraph = UTBo_NodePlot(
    #     nodeDF, 'out_degree_centrality', 15, label_column = 'employee')
    # mainAEigenvectorPlot, mainAEigenvectorGraph = UTBo_NodePlot(
    #     nodeDF, 'eigenvector_centrality', 15, label_column = 'employee')
    # mainABetweennessPlot, mainABetweennessGraph = UTBo_NodePlot(
    #     nodeDF, 'betweenness_centrality', 15, label_column = 'employee')
    mainAInDegreePlot, mainAInDegreeGraph = UTBo_NodePlot(
        nodeDF, 'in_degree_centrality', 15, xnode_name = 'employee')
    mainAOutDegreePlot, mainAOutDegreeGraph = UTBo_NodePlot(
        nodeDF, 'out_degree_centrality', 15, xnode_name = 'employee')
    mainAEigenvectorPlot, mainAEigenvectorGraph = UTBo_NodePlot(
        nodeDF, 'eigenvector_centrality', 15, xnode_name = 'employee')
    mainABetweennessPlot, mainABetweennessGraph = UTBo_NodePlot(
        nodeDF, 'betweenness_centrality', 15, xnode_name = 'employee')
    
       
    
    
    #plot1- se agrega glyph (estrella a node eliminado) y flechas
    layout_graph1 = graph1.layout_provider

    #
    #adds a graph to plot1, empty for now, but will be used to add the 
    #glyphs of the selected nodes
    selectedImposedBokehGraph = \
        UTBo_Network_AddSelectedNodesGraph(plot1, graph1, nx.Graph(), 8)


    nodesToEliminate = [0]
    businessComponentsToEliminate, densityG2, filteredNxGraph,\
        tablaModeloFiltradoDF, deltaTable, responder_dirección, \
            responder_número_conexiones_componentes_eliminados, \
                responder_egoNxGraph, inverse_responder_dirección, \
                    inverse_responder_número_conexiones_componentes_eliminados, \
                        inverse_responder_egoNxGraph = \
                    FD_filtered_nodes_ego_graph(xconn, xnetwork_parameters_dict,
                                                # xnetwork_parameters_data_table,
                                                nodesToEliminate,
                                                _businessComponentsConnected,
                                                _keyComponentsConnected,
                                                xamplifier,
                                                xfrequencyCorte,
                                                xfrequencyResponseAccumulation,
                                                xactive_selected_possible_responses,
                                                xall_any_filter_group_active,
                                                completeNxGraph,
                                                tablaModeloCompletoDF)
                    
    
    selectedNodesNxGraph = nx.Graph()

    for node in completeNxGraph.nodes:
        if node in businessComponentsToEliminate:
            optional_attrs = completeNxGraph.nodes[node]
            selectedNodesNxGraph.add_node(node, **optional_attrs)
            # print('>>>>> node added to selectedNodesNxGraph (finacGDB_AA_IRA_Model)')
            # print(node)
            
    UTBo_Network_AddSelectedNodesGlyph(plot1, layout_graph1,
                                       selectedImposedBokehGraph,
                                       selectedNodesNxGraph, 8)

    # print('>>>>>>>>>>>>> llamando FD_Arrows plot1 (finacGB_AA_IRA_Model)')
    plot1 = FD_Arrows(plot1)

    
    #
    #plot2- plot1 sin el nodo eliminado
    # title2 = 'Modelo filtrado (layout original) - Network density = ' + \
    #     str(densityG2)
    title2 = 'Ego inverso - Conexiones[' + \
        inverse_responder_dirección+']:' +\
        inverse_responder_número_conexiones_componentes_eliminados

    #
    plot_inverse_responder_ego, graph_inverse_responder_ego = \
        UTBo_Network_PlotType2(inverse_responder_egoNxGraph, tooltips, 
                               title2, nx.spring_layout, layout_graph1, True,
                               plotHeight_filtrado, plotWidth_filtrado,
                               xnodeSize='node_size',
                               xnodeColorAttribute=xnode_color_attribute,
                               xadjustNodeSize=True)

    # print('>>>>>>>>>>>>> llamando FD_Arrows plot2 (finacGB_AA_IRA_Model)')
    plot_inverse_responder_ego = FD_Arrows(plot_inverse_responder_ego)
    
    table_inverse_responder_ego = \
        UTBo_nx_nodes_to_DataTable(inverse_responder_egoNxGraph,
                             xattributes = p_d_fields_table_filtered_employee,
                             xwidth = 500, xheight = 450)    
    
    """
    egoNxGraph- grafo del ego del nodo eliminado
    """
    if len(businessComponentsToEliminate) == 0:
        layout = layout_graph1
        use_layout = True
    else:
        layout = nx.spring_layout
        use_layout = False

    """
    plot3- ego del nodo eliminado
    """
    title3 = 'Ego componentes eliminados - Conexiones[' + \
        responder_dirección+']:' +\
        responder_número_conexiones_componentes_eliminados

    """
    responder_egoNxGraph
    """
    plot_responder_ego, graph_responder_ego = \
        UTBo_Network_PlotType2(responder_egoNxGraph, tooltips, 
                               title3, nx.spring_layout, layout_graph1, True,
                               plotHeight_filtrado, plotWidth_filtrado,
                               xnodeSize='node_size',
                               xnodeColorAttribute=xnode_color_attribute,
                               xadjustNodeSize=True)

    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.')
    # print(nx.is_directed(egoNxGraph))
    # print(egoNxGraph.nodes())
    # print(egoNxGraph.edges())
    # print('>>>>>>>>>>>>> predecessor_egoNxGraph.nodes() (finacGB_AA_IRA_Model)')
    # print(predecessor_egoNxGraph.nodes())
    # print('>>>>>>>>>>>>> llamando FD_Arrows plot3 (finacGB_AA_IRA_Model)')
    plot_responder_ego = FD_Arrows(plot_responder_ego)

    table_responder_ego = \
        UTBo_nx_nodes_to_DataTable(responder_egoNxGraph,
                             xattributes = p_d_fields_table_filtered_employee,
                             xwidth = 500, xheight = 450)    
    
    """
    businessComponentsTable_neo4j- matriz de adyacencia
    """
    businessComponentsTable_neo4j = \
        UTNx_adjacency_matrix_to_df(completeNxGraph, 'Funcionario',
                                    xadditional_attribute='organization_area',
                                    xadditional_attribute_display_label= \
                                        'Area',
                                    xdict_employee = dict_employee)
    # print('>>>>>>>>>>>> businessComponentsTable_neo4j (FD_AA_model_main)')
    # print(businessComponentsTable_neo4j.columns)
    # print(businessComponentsTable_neo4j.shape)
    # print(businessComponentsTable_neo4j.to_dict('records'))

    
    """
    businessComponentsTable_neo4j- matriz de adyacencia
    """
    sourceInteracción = ColumnDataSource(businessComponentsTable_neo4j)

    columnsBCT = [TableColumn(field=Ci, title=Ci)
                  for Ci in businessComponentsTable_neo4j.columns]  # bokeh columns

    data_table_interacción = DataTable(source=sourceInteracción,
                                       columns=columnsBCT, width=1200,
                                       height=600)

    
    #
    #tabTablaInteracción- tabla con matriz de adyacencia
    #tabModelo_completo- centralidades modelo completo
    #tabModelo_filtrado- centralidades modelo filtrado
    #tabTablaDelta- diferencias de centralidades entre modelo completo y
    #               filtrado
    definiciónTablaInteracción = \
        column(UTBo_EmptyParagraph(25, 15),
               Div(text = definiciónTablaInteracción, width=400, height=25),
               UTBo_EmptyParagraph(25, 15))

    tabTablaInteracción = TabPanel(child=column(definiciónTablaInteracción,
                                                data_table_interacción),
                                   title="Interacción componentes")

    # print('>>>>>>>>>>>> tablaModeloCompletoDF (FD_AA_model_main)')
    # print(tablaModeloCompletoDF.columns)

    sourceModeloCompleto = ColumnDataSource(tablaModeloCompletoDF)

    columns = [TableColumn(field="employee"),
               TableColumn(field="total_degree_centrality"),
               TableColumn(field="unscaled_total_degree_centrality"),
               TableColumn(field="in_degree_centrality"),
               TableColumn(field="unscaled_in_degree_centrality"),
               TableColumn(field="out_degree_centrality"),
               TableColumn(field="unscaled_out_degree_centrality"),
               TableColumn(field="eigenvector_centrality"),
               TableColumn(field="betweenness_centrality")]

    data_table_ModeloCompleto = DataTable(source=sourceModeloCompleto, 
                                          columns=columns,
                                          width=1400, height=600)

    
    # tabModelo_completo = TabPanel(child=data_table_ModeloCompleto, 
    #                               title="Modelo completo")

    sourceModeloFiltrado = ColumnDataSource(tablaModeloFiltradoDF)

    data_table_ModeloFiltradoDF = DataTable(source=sourceModeloFiltrado, columns=columns,
                                            width=1400,
                                            height=600)

    tabModelo_filtrado = TabPanel(child=data_table_ModeloFiltradoDF, 
                                  title="Modelo filtrado")

    sourceDelta = ColumnDataSource(deltaTable)

    columnsDelta = [TableColumn(field="BusinessComponent"),
                    TableColumn(field="total_degree_centrality_complete"),
                    TableColumn(field="ScaledDifferenceToFiltered"),
                    TableColumn(
                        field="unscaled_total_degree_centrality_complete"),
                    TableColumn(field="UnScaledDifferenceToFiltered"),
                    TableColumn(field="total_degree_centrality_filtered"),
                    TableColumn(field="ScaledDifferenceFromComplete"),
                    TableColumn(
                        field="unscaled_total_degree_centrality_filtered"),
                    TableColumn(field="UnscaledDifferenceFromComplete")]

    data_table_delta = DataTable(source=sourceDelta, columns=columnsDelta,
                                 width=1400, height=600)

    tabTablaDelta = TabPanel(child=data_table_delta, 
                             title="Comparativo modelos")
    
    
    # print('>>>>>>>>>>>>>>>>>>>>>>> connected_nodes (oihub_AA_IRA_Model')
    # print(connected_nodes)
    
    
    parameters_for_business_component_selection_dict =\
        {'tablaModeloCompletoDF': tablaModeloCompletoDF,
         'sourceModeloFiltrado': sourceModeloFiltrado,
         'sourceDelta': sourceDelta,
         '_keyComponentsConnected': _keyComponentsConnected,
         '_businessComponentsConnected': _businessComponentsConnected,
         'connected_nodes': connected_nodes,
         'fields_table_filtered_employee': p_d_fields_table_filtered_employee
         }
        
    """
    Se pueden quitar densityG1, densityG2.
    """
    
    print('>>>>>>>>>>>>>>>>>>>>> completeNxGraph.edges(data=True) (FD_AA_model_main)')
    print(completeNxGraph.edges(data=True))
    
    
    return plot1, parameters_for_business_component_selection_dict, \
        plot_inverse_responder_ego, plot_responder_ego, tabTablaInteracción, \
            data_table_ModeloCompleto,\
        tabModelo_filtrado, tabTablaDelta, densityG1, densityG2, qu_filasG, qu_columnasG, \
            qu_linksG,\
        qu_centralizationG, graph1, sourceInteracción, \
        responder_dirección, \
            responder_número_conexiones_componentes_eliminados, \
        mainAInDegreePlot, mainAOutDegreePlot,\
        mainAEigenvectorPlot, mainABetweennessPlot,\
        data_table_nodeDF, \
        plot_informal_network, non_connected_list, \
        _communities, _informal_network_palette_dict, \
        plot_area_network, plot_quotient_informal_network, \
        plot_quotient_organization_area,\
        core_layout, plot_core, completeNxGraph,\
            graph_inverse_responder_ego, graph_responder_ego, \
                selectedImposedBokehGraph, layout_graph1,\
                table_inverse_responder_ego, table_responder_ego
             


