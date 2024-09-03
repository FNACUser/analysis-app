# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 19:25:33 2023

@author: luis.caro
"""

import networkx as nx
import pandas as pd
import itertools

from math import pi

from bokeh.layouts import column
# from bokeh.models import Tabs, Div, Panel, Select, TapTool
from bokeh.plotting import figure

from bokeh.models.widgets import DataTable
# from bokeh.events import Tap

from bokeh.models import ColumnDataSource, TableColumn, Tabs, TabPanel

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import (UTBo_BokehGraphToNetworkxGraph,
                            UTBo_Network_PlotType2)

from defaultapp.bkhapps.common.oihub_UtilitiesNetworkx import UTNx_Ordered_circular_communities

from defaultapp.bkhapps.common.Utilities import UT_is_number

#Se puso esa t para verificar que no se necesita
#Se quitó para el modelo de 
# from oihub_mod_01 import oahubIniTest




#%%

def FD_Community_selector(xcommunities_for_community_color_selector, 
                          xtítulo_seleccione,
                          xinter_community_flag):
    
    # print('.-.-.-.-.-.-.-.-.-.-.- FD_Community_selector')
    # print('xnon_inter_communities (FD_Community_selector)')
    # print(xnon_inter_communities)
    # print('xinter_community_flag (FD_Community_selector)')
    # print(xinter_community_flag)
    
    # _xvalues=[str(community) for community,_ in sorted(xcommunitiesColor) \
    #           if community != xinter_community_flag]
    _xvalues = [community for community,
                _ in xcommunities_for_community_color_selector]
    # print('_xvalues (FD_Community_selector)')
    # print(_xvalues)    
        
    # _colors=[color for community,color in sorted(xcommunitiesColor)\
    #           if community != xinter_community_flag]
    _colors=[color for _, color in xcommunities_for_community_color_selector]

    
    # _xvalues=[str(community) for community,_ in xcommunitiesColor ]
    
    # _colors=[color for community,color in xcommunitiesColor]

    _yvalues=['Red oculta']
    
    _xs=list(itertools.chain.from_iterable(itertools.repeat(x, len(_yvalues)) \
                                           for x in _xvalues))
    # print('_xs (FD_Community_selector)')
    # print(_xs)
    
    _ys = _yvalues*len(_xvalues)    
    
    _community_color_selector = figure(title='Seleccione '+xtítulo_seleccione, 
                                       tools="tap", toolbar_location=None, 
                                       x_range = _xvalues, y_range = _yvalues,
                                       height=200,width=800)

    _community_color_selector.rect(_xs, _ys, color = _colors, 
                                   width=0.5, height=0.5, fill_alpha=0.5) 
    
    _community_color_selector.xaxis.major_label_orientation = pi/10
    # _community_color_selector.xaxis.major_label_orientation = 'vertical'
    
    # print('>.>.>.>.>.>.>.>.>.>.>.>.>.> _community_color_selector.x_range')
    # print(_community_color_selector.x_range.factors)
    
    # community_source = _community_color_selector.renderers[0].data_source
    
    # taptool = _community_color_selector.select(type=TapTool)
    
    # _multi_actor_communities = [str(community) for community, _ in xcommunitiesColor\
    #                             if str(community) != str(xinter_community_flag)]
    # print('FD_Community_selector - _multi_actor_communities')
    # print(_multi_actor_communities)
    # _multi_actor_communities = [str(community) for community in xcommunities\
    #                             if str(community) in _multi_actor_communities]
    # print('FD_Community_selector - _multi_actor_communities')
    # print(_multi_actor_communities)
    
    # def callback(event):
    #     selected = community_source.selected.indices
    #     print('callback - selected')
    #     print(selected)
    #     print('callback - _multi_actor_communities')
    #     print(_multi_actor_communities)
        
    #     if len(selected) == 1:
    #         _df, _temp_actors_table = \
    #             FD_Community_participants(_multi_actor_communities[selected[0]], 
    #                                       xplotCommunities, xcommunity_attribute)
    #         _data_table_community_participants.source.data = _df
    
    # _community_color_selector.on_event(Tap, callback)
    
    
    
    # source = _hm.renderers[0].data_source
    
    # taptool = _hm.select(type=TapTool)
    
    # def callback(event):
    #     selected = source.selected.indices
    #     print(selected)
    
    # _hm.on_event(Tap, callback)
    
    
    # def my_tap_handler(attr, old, new):
    #     index = new[0]
    #     print(index)

    # source.selected.on_change("indices", my_tap_handler)
    
    
    
    return _community_color_selector, _xvalues, _colors, _xs

def FD_community_selector_on_change(xselectedCommunity):
    
    # print(xselectedCommunity)
    
    return 0


def FD_Community_participants(xselectedCommunity, xcomplete_nx_graph,
                              xcommunity_attribute,
                              xwidth = 800, xheight = 350):
    
    print('.-.-.-.-.-.-. oihub_AA_IRA_Communities/FD_Community_participants')
    
    """
    Returns actors in a community as a DataFrame and as a DataTable.
    
    Input:  - selected community
            - complete nx graph
            - community attribute
    Output: - actors DataFrame
            - actors DataTable
    """
    # print('.-.-.-.-.-.-.-.-.-.-.- FD_Community_participants')
    # print('>>>>>>>>>>>>> xcommunity_attribute (FD_Community_participants)')
    # print(xcommunity_attribute)
    # print('>>>>>>>>>>>>> xselectedCommunity (FD_Community_participants)')
    # print(xselectedCommunity)
    
    # _graph = UTBo_BokehGraphToNetworkxGraph(xplotCommunities,xDiGraph=True)
    _graph = xcomplete_nx_graph
    print('>>>>>>>>>>>> _graph.nodes() (FD_Community_participants)')
    print(_graph.nodes(data=True))
    
    # for n,d in _graph.nodes(data=True):
    #     print(n,d['informal_network'])
    
    def compare_community(xattribute,xselectedCommunity):
        # print(xattribute)
        # print(xselectedCommunity)
        if UT_is_number(xselectedCommunity):
            # print('is int float')
            return xattribute == int(xselectedCommunity)
        else:
            # print('is NOT int float')
            return xattribute == xselectedCommunity
    
    # nodesCommunity = \
    #     [(x,y) for x,y in _graph.nodes(data=True) \
    #      if y[xcommunity_attribute]==int(xselectedCommunity)]
    
    nodesCommunity = \
        [(x,y) for x,y in _graph.nodes(data=True) \
         if compare_community(y[xcommunity_attribute], xselectedCommunity)]
            
    print('>>>>>>>>>>>>>>>>>>>>> nodesCommunity (FD_Community_participants)')
    print(nodesCommunity)
    
    
    actors, attributes = zip(*nodesCommunity)
    actorsDF = pd.DataFrame({'Actor':actors})
    attributesDF = pd.DataFrame(attributes)
    print('>>>>>>>>>>>>>>>>>>>>> attributesDF (FD_Community_participants)')
    print(attributesDF.to_dict('records'))
    
    attributesDF=attributesDF[['redmine_login','organization_area',
                               'out_degree_centrality', 
                               'total_degree_centrality',
                               'betweenness_centrality',
                               'eigenvector_centrality', 
                               'in_degree_centrality']]
    
    communityActors = pd.concat([actorsDF.reset_index(drop=True), 
                                 attributesDF], axis=1)
    
    print('>>>>>>>>>>>>>>>>>>>>> communityActors (FD_Community_participants)')
    print(communityActors.to_dict('records'))
    
    # a=5/0
    
    communityActorsCDF = ColumnDataSource(communityActors)
    
    columnsCA = \
        [TableColumn(field=Ci, title=Ci) for Ci in communityActors.columns]

    data_table_community_participants = \
        DataTable(source = communityActorsCDF, columns = columnsCA, 
                  width = xwidth, height = xheight)
        
    return communityActors, data_table_community_participants

    
#OOJJOO
# def FD_Communities_analyzer(xvvvplotCommunities, xcommunity_attribute,
#                             xcomplete_nx_graph):
def FD_Communities_analyzer(xcommunity_attribute, xcomplete_nx_graph):

    """
    Recibe: - atributo de la red (area o informal_network)
            - grafo nx completo
    Los pasos son:  - genera una lista de coumunidades (communities)
                    - genera una lista de tripletas con los colores
                      de las conexiones entre nodos. Son los colores de las
                      comunidades más un color adicional para la
                      comunidad 0, que no existe, pero que se refiere
                      al caso en que dos nodos de comunidades diferentes
                      se comunican (comunidad, color, intracomunidad (T/F)) 
                      (communties_connectors_colors)
                    - determina si hay conexiones entre nodos de 
                      comunidades diferentes: inter_community_flag = True
                      Esto solo sucede con informal_networks, no con area.
                    - elimina el valor intracomunidad de 
                      communties_connectors_colors
                    
    Devuelve:                   
    """
    print('.-.-.-.-.-.-.-.-oihub_AA_IRA_Communities/FD_Community_analyzer')
    # print('xcommunity_attribute (FD_Community_analyzer)')
    # print(xcommunity_attribute)
    
    # graph = UTBo_BokehGraphToNetworkxGraph(xplotCommunities,xDiGraph=True)
    
    # print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_Community_analyzer')
    # print('>>>>>>>>>>>>>>>>> xcommunity_attribute - FD_Communities_analyzer')
    # print(xcommunity_attribute)
    # print('>>>>>xcomplete_nx_graph.nodes(data=True) (FD_Community_analyzer)')
    # print(xcomplete_nx_graph.nodes(data=True))
    # print('>>>>>>>>>>>>>>>>>>>>>graph.edges(data=True) (FD_Community_analyzer)')
    # print(graph.edges(data=True))
    
    communities = \
        list(set([str(v[xcommunity_attribute]) \
                  for n,v in xcomplete_nx_graph.nodes(data=True)]))
    # print('>>>>>>>>>>>>>>>>> communities - FD_Communities_analyzer')
    # print(communities)
        
    if xcommunity_attribute == 'organization_area':
        communities_connectors_colors = \
            list(set([(v['organization_area'], v['organization_area_color'], False) \
                      for n,v in xcomplete_nx_graph.nodes(data=True)]))    
    else:
        communities_connectors_colors = \
            list(set([(w[xcommunity_attribute],w[xcommunity_attribute+'_color'],
                       xcomplete_nx_graph.nodes[n][xcommunity_attribute] != \
                           xcomplete_nx_graph.nodes[v][xcommunity_attribute]) \
                      for n,v,w in xcomplete_nx_graph.edges(data=True)]))
    # print('>>>>>>>>>> communities_connectors_colors (FD_Communities_analyzer)')
    # print(communities_connectors_colors)
    
    # intra_communities = \
    #     list(set(communities) - \
    #          set([community for community, _, intra in \
    #               communities_connectors_colors\
    #               if intra == False]))
    # print('>>>>>>>>>>>>>>>>> intra_communities - FD_Communities_analyzer')
    # print(intra_communities)
    
    # aaactors_in_single_actor_communities = \
    #     [(n,u.get(xcommunity_attribute)) for n,u in graph.nodes(data=True)\
    #       if u.get(xcommunity_attribute) in intra_communities]
    # print('>>>>> actors_in_single_actor_communities - FD_Communities_analyzer')
    # print(aaactors_in_single_actor_communities)
    
    
    inter_community_flag_list = \
        [community for community, _,inter_community in \
         communities_connectors_colors \
         if inter_community == True]
    if len(inter_community_flag_list) == 0:
        inter_community_flag = None
    else:
        inter_community_flag = inter_community_flag_list[0]
    # print('>>>>>>>>>>>>>>>>> inter_community_flag - FD_Communities_analyzer')
    # print(inter_community_flag)
    communities_connectors_colors = [(community,community_color) \
                        for community,community_color,_ in \
                            communities_connectors_colors]        
    # print('>>>>>>>>>>>>>>>>> communitiesColor - FD_Communities_analyzer')
    # print(communities_connectors_colors)
    
    communities.sort()
    # print('>>>>>>>>>>>>>>>>> communities (after sort) (FD_Communities_analyzer)')
    # print(communities)
       
    #OOJJO
    # return communities, communities_connectors_colors, xcomplete_nx_graph, \
    #     inter_community_flag
    return communities, communities_connectors_colors, inter_community_flag


def FD_create_informal_network_plot(xgraph, 
                                    xcommunity_color_selector_communities,
                                    xcommunity_attribute, 
                                    xselected_community_index,
                                    xnode_color_attribute):
    
    print('.-.-.-. finacDB_AA_IRA_Communities/FD_create_informal_network_plot')
    # print('>>>>>>>>> xcommunity_color_selector_communities (FD_create_informal_network_plot)')
    # print(xcommunity_color_selector_communities)
    print('>>>>>>>> xgraph.nodes(data=True) (FD_create_informal_network_plot)')
    print(xgraph.nodes(data=True))
    # print('>>>>>>>>> xcommunity_attribute (FD_create_informal_network_plot)')
    # print(xcommunity_attribute)
    # print('>>>>>>>>> xselected_community_index (FD_create_informal_network_plot)')
    # print(xselected_community_index)
    # print('>>>>>>>>> xnode_color_attribute (FD_create_informal_network_plot)')
    # print(xnode_color_attribute)
    
    # selected_community, _ = \
    selected_community = \
        xcommunity_color_selector_communities[xselected_community_index]
    # print('>>>>>>>> graph (FD_Communities_info)')
    # print(graph.nodes(data=True))
    informal_network_subgraph = \
        xgraph.subgraph([node for node, attr in xgraph.nodes(data=True)\
                    if str(attr.get(xcommunity_attribute)) == \
                        selected_community])
                    # if attr.get('informal_network')==1])
    print('>>>>>>>> informal_network_subgraph.nodes(data=True) (FD_create_informal_network_plot)')
    print(informal_network_subgraph.nodes(data=True))
    # print('>>>>>>>> informal_network_subgraph.edges(data=True) (FD_create_informal_network_plot)')
    # print(informal_network_subgraph.edges(data=True))
    # print(informal_network_subgraph.get_edge_data('alfredo.castellanos', 
    #                                         'paola.florez', default=0))
    
    informal_network_completed_graph_tool_tips = [('employee','@employee'),
                                            ('cvf_cluster','@cvf_cluster'),
                                            ('area','@organization_area'),
                                            ('community', '@informal_network')]
    
    # colors_by = ['organization_area', 'cvf_cluster']
    colors_by = []
    
    # _, informal_network_completed_graph, \
    #     informal_network_completed_graph_tool_tips, \
    #         informal_network_completed_graph_pos, \
    #             centralitiesTable, density, _, _  = \
    #         oahubIniTest(informal_network_subgraph, colors_by,
    #                      xidentify_communities=False,
    #                      xtool_tips = \
    #                          informal_network_completed_graph_tool_tips,
    #                      xonly_connected_nodes = False)
    # print('>>>>>>>> informal_network_completed_graph.edges(data=True) (FD_create_informal_network_plot)')
    # print(informal_network_completed_graph.edges(data=True))
    # print('>>>>>>>> informal_network_completed_graph.nodes (FD_Communities_info)')
    # print(informal_network_completed_graph.nodes(data=True))
    # print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
    # print('>>>>>>>> informal_network_completed_graph.edges (FD_Communities_info)')
    # print(informal_network_completed_graph.edges(data=True))
    # print('>>>>> len-informal_network_completed_graph (FD_create_informal_network_plot)')
    # print(len(informal_network_completed_graph.nodes()))
    
    if xnode_color_attribute != 'organization_area_color':
        edge_color_attribute = 'informal_network_color'
        edge_width_attribute = 'informal_network_width'
        colorLegendTitle = 'Community'
        keyColorAttribute ='informal_network'
    else:
        edge_color_attribute = 'id_organization_area_color'
        edge_width_attribute = 'id_organization_area_width'
        colorLegendTitle = 'Area'
        keyColorAttribute ='organization_area'
        
    #Así estaba
    # ordered_graph = \
    #     UTNx_Ordered_circular_communities(informal_network_completed_graph,
    #                                       xnode_color_attribute)
    ordered_graph = \
        UTNx_Ordered_circular_communities(informal_network_subgraph,
                                          xnode_color_attribute)
    
    print('>>>> ordered_graph.nodes(data=True) (FD_create_informal_network_plot)')
    print(ordered_graph.nodes(data=True))
    # print('>>>> ordered_graph.edges(data=True) (FD_create_informal_network_plot)')
    # print(ordered_graph.edges(data=True))
    
    # a=5/0
        
    # print('>>>>>>>>>>>>>>>> se fue por ordered_graph')
    sub_plot_informal_network, _ = \
        UTBo_Network_PlotType2(ordered_graph, 
                               informal_network_completed_graph_tool_tips, \
                               'Detalle kkk'+edge_color_attribute,
                                nx.circular_layout, nx.circular_layout, False,
                                350, 550,
                                xnodeSize='node_size',
                                xnodeColorAttribute=xnode_color_attribute,
                                xadjustNodeSize=True,
                              xedgeColorAttribute = edge_color_attribute,
                              xedgeWidthAttribute = edge_width_attribute,
                              xkeyColorAttribute=keyColorAttribute,
                              xColorLegendTitle=[colorLegendTitle],
                              xk=1.5,
                              xleft_margin = 1.5,
                              xlegend_text_font_size = '12px')
            
            # xpos = informal_network_completed_graph_pos,
            
    return sub_plot_informal_network

#OOJJOO
# def FD_Communities_info(xxxxplot_communities_renderer_0, xplotQuotient, 
def FD_Communities_info(xcommunity_attribute,
                        xtítulo_seleccione, xnode_color_attribute,
                        xcomplete_nx_graph):
    
    """
    output: - community_color_selector
            - _data_table_community_participants
            - xplotQuotient
            - sub_plot_informal_network
            - non_inter_communities
    """
    
    print('.--.-.-.-.-.-.-.-. oihub_AA_IRA_Communities/FD_Communities_info')
    # print('>>>>>>>>>>>> xcommunity_attribute (FD_Communities_info')
    # print(xcommunity_attribute)
    # print('>>>>>>>>>>>> xcomplete_nx_graph.nodes(data=True) 1 (FD_Communities_info')
    # print(xcomplete_nx_graph.nodes(data=True))
    
    #OOJJOO
    # _communities, _communitiesColor, graph, _inter_community_flag = \
        # FD_Communities_analyzer(xplot_communities_renderer_0, 
        #                         xcommunity_attribute, xcomplete_nx_graph)
    _communities, _communitiesColor, _inter_community_flag = \
        FD_Communities_analyzer(xcommunity_attribute, xcomplete_nx_graph)
    # print('>>>>>>>>>>>> graph.edges(data=True)[0] (FD_Communities_info')
    # print(graph.get_edge_data('alfredo.castellanos', 
    #                                        'paola.florez', default=0))
    # print('>>>>>>>>>>>>> FD_Communities_info - _communities')
    # print(_communities)
    # print('>>>>>>>>>>>>>>>>> FD_Communities_info - _communitiesColor')
    # print(_communitiesColor)
    # print('>>>>>>>>>>>>>>>> _inter_community_flag (FD_Communities_info)')
    # print(_inter_community_flag)
    # print('>>>>>>>>>>>> xcomplete_nx_graph.nodes(data=True) 2 (FD_Communities_info')
    # print(xcomplete_nx_graph.nodes(data=True))
    
    
     
    communities_for_community_color_selector = \
        [(str(community), color) \
         for community, color in sorted(_communitiesColor) \
              if community != _inter_community_flag]
    # print('>>>>>>>>>>>>>>>>> communities_for_community_color_selector (FD_Communities_info)')
    # print(communities_for_community_color_selector)
    
    community_color_selector, _, _, _ = \
        FD_Community_selector(communities_for_community_color_selector,
                                                     xtítulo_seleccione,
                                                     _inter_community_flag)
    
    # community_source = community_color_selector.renderers[0].data_source
    
    # taptool = community_color_selector.select(type=TapTool)
    
    _multi_actor_communities = [str(community) for community, _ in _communitiesColor\
                                if str(community) != str(_inter_community_flag)]
    # print('FD_Communities_info_layout - _multi_actor_communities')
    # print(_multi_actor_communities)
    _multi_actor_communities = [str(community) for community in _communities\
                                if str(community) in _multi_actor_communities]
    # print('FD_Communities_info_layout - _multi_actor_communities')
    # print(_multi_actor_communities)
    
    # print('>>>>>>>>>>>>>>>>> _communities (FD_Communities_info)')
    # print(_communities)    
    # print('>>>>>>>>>>>>>>>>> _communities[0] (FD_Communities_info)')
    # print(_communities[0])
    
    # print('>>>>>>>> graph (FD_Communities_info)')
    # print(graph.nodes(data=True))
    
    #nuevo
    community_color_selector_communities = \
        community_color_selector.x_range.factors
    first_selected_community = community_color_selector_communities[0]
    
    #OOJJOO
    # sub_plot_informal_network = \
    #     FD_create_informal_network_plot(graph, 
    sub_plot_informal_network = \
        FD_create_informal_network_plot(xcomplete_nx_graph, 
                                        community_color_selector_communities,
                                        xcommunity_attribute, 0,
                                        xnode_color_attribute)
    # print('>>>>>>>>>>>> xcomplete_nx_graph.nodes(data=True) 3 (FD_Communities_info')
    # print(xcomplete_nx_graph.nodes(data=True))
    
    # informal_network_subgraph = \
    #     graph.subgraph([node for node, attr in graph.nodes(data=True)\
    #                 if str(attr.get(xcommunity_attribute)) == \
    #                     first_selected_community])
    #                 # if attr.get('informal_network')==1])
    # # print('>>>>>>>> informal_network_subgraph (FD_Communities_info)')
    # # print(informal_network_subgraph.nodes(data=True))
    
    # informal_network_completed_graph_tool_tips = [('employee','@employee'),
    #                                         ('cvf_cluster','@cvf_cluster'),
    #                                         ('area','@area')]
    # _, informal_network_completed_graph, \
    #     informal_network_completed_graph_tool_tips, \
    #         informal_network_completed_graph_pos, \
    #             centralitiesTable, density, _, _  = \
    #         oahubIniTest(informal_network_subgraph,
    #                      xidentify_communities=False,
    #                      xtool_tips = informal_network_completed_graph_tool_tips,
    #                      xonly_connected_nodes = False)
    # # print('>>>>>>>> informal_network_completed_graph (FD_Communities_info)')
    # # print(informal_network_completed_graph.nodes(data=True))
    
    
    # def xcallback(selected):
    #     # selected = community_source.selected.indices
    #     # selected = new[0]
    #     print('.-.-.-.-.-.-.-.- FD_Communities_info_layout-callback')
    #     print('>>>>>>>>>>>> selected (FD_Communities_info_layout-callbak)')
    #     print(selected)
    #     # print('>>>>>>>>>>>> old (FD_Communities_info_layout-callbak)')
    #     # print(old)
    #     # print('callback - _multi_actor_communities')
    #     # print(_multi_actor_communities)
    #     # print('callback - _community_color_selector.x_range')
    #     # print(community_color_selector.x_range.factors)
    #     _m_actor_c = community_color_selector.x_range.factors
    #     print('>>>>>>>>>>>> _m_actor_c (FD_Communities_info_layout-callbak)')
    #     print(_m_actor_c)
        
    #     # if len(selected) == 1:
    #     _df, _temp_actors_table = \
    #         FD_Community_participants(_m_actor_c[selected], 
    #                                   xplotCommunities, xcommunity_attribute)
    #     print('>>>>>>>>>>>> _df (FD_Communities_info_layout-callbak)')
    #     print(_df)
    #     _data_table_community_participants.source.data = _df
        
    #     _sub_plot_informal_network = \
    #         FD_create_informal_network_plot(graph, non_inter_communities,
    #                                         xcommunity_attribute, 
    #                                         selected,
    #                                         xnode_color_attribute)
            
    #     xg1=sub_plot_informal_network.renderers[0]
    #     dsnrp1 = _sub_plot_informal_network.renderers[0].\
    #         node_renderer.data_source
    #     xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    #     dsnrp1g = _sub_plot_informal_network.renderers[0].\
    #         node_renderer.glyph
    #     xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
        
    #     dshrp1 = _sub_plot_informal_network.renderers[0].\
    #         edge_renderer.data_source
    #     xg1.edge_renderer.data_source.data = dict(dshrp1.data)
    #     dshrp1g = _sub_plot_informal_network.renderers[0].\
    #         edge_renderer.glyph
    #     xg1.edge_renderer.glyph.line_color = dshrp1g.line_color
        
    #     title_color_legend=sub_plot_informal_network.renderers[1]
    #     new_title_color_legend=_sub_plot_informal_network.\
    #         renderers[1].data_source
    #     title_color_legend.data_source.data = \
    #         dict(new_title_color_legend.data)
        
    #     rectangles_color_legend=sub_plot_informal_network.renderers[2]
    #     new_rectangles_color_legend = \
    #         _sub_plot_informal_network.renderers[2].data_source
    #     rectangles_color_legend.data_source.data = \
    #         dict(new_rectangles_color_legend.data)
        
    #     names_color_legend=sub_plot_informal_network.renderers[3]
    #     new_names_color_legend = \
    #         _sub_plot_informal_network.renderers[3].data_source
    #     names_color_legend.data_source.data = dict(new_names_color_legend.data)
        
        
        
    #     layout_graph=xg1.layout_provider
        
    #     layout_graph.graph_layout = \
    #         dict(_sub_plot_informal_network.renderers[0].\
    #              layout_provider.graph_layout)
            
    
    # community_color_selector_source = \
    #     community_color_selector.renderers[0].data_source
    
    # community_color_selector_source.\
    #     selected.on_change('indices', lambda attr, old, new: \
    #                        xcallback(community_color_selector_source.\
    #                            selected))
    
    
    # _, _data_table_community_participants = \
    #     FD_Community_participants(first_selected_community, xplotCommunities, 
    #                               xcommunity_attribute)
    # print('>>>>>>>>>>>> xcomplete_nx_graph.nodes(data=True) (FD_Communities_info')
    # print(xcomplete_nx_graph.nodes(data=True))
    
    # a=5/0
    _, _data_table_community_participants = \
        FD_Community_participants(first_selected_community, 
                                  xcomplete_nx_graph, 
                                  xcommunity_attribute)
        
    # return community_color_selector, _data_table_community_participants, \
    #     graph, sub_plot_informal_network
    return community_color_selector, _data_table_community_participants, \
        sub_plot_informal_network
        
# def FD_Communities_info_layout(xplotCommunities, xplotQuotient, 
#                                xcommunity_attribute,
#                                xtítulo_seleccione, xnode_color_attribute,
#                                xcomplete_nx_graph):
def FD_Communities_info_layout(xcommunity_color_selector, 
                               x_data_table_community_participants,
                               xplotQuotient, xsub_plot_informal_network):
    
    # print('.-.-.-.-.-.-.-.-.-.-.- FD_communities_info_layout')
    
    # community_color_selector, _data_table_community_participants, graph,\
    #     sub_plot_informal_network = \
    #         FD_Communities_info(xplotCommunities, xplotQuotient, 
    #                             xcommunity_attribute, xtítulo_seleccione,
    #                             xnode_color_attribute,
    #                             xcomplete_nx_graph)
    
    # xxxselected_community_participants = \
    #     _data_table_community_participants.source.data['Actor']
    # print('>>>> selected_community_participants (FD_communities_info_layout)')
    # print(selected_community_participants)
    
    
    panel_detail = TabPanel(child=xsub_plot_informal_network,
                            title="Detalle")
    #:_:_:_:_:_:_:_:_:_ fin ensayo gráfico
         
    panel_community = TabPanel(child=x_data_table_community_participants,
                               title="Actores")
    panel_quotient = TabPanel(child=xplotQuotient, title="Intercomunidades")
    # tabActoresComunidad = Tabs(tabs=[panel_community,panel_quotient])
    tabActoresComunidad = Tabs(tabs=[panel_community,panel_quotient,
                                      panel_detail])
    
    communities_info_layout = column(xcommunity_color_selector, 
                                     tabActoresComunidad)
    
    # return community_color_selector, _data_table_community_participants, \
    #     communities_info_layout
    return communities_info_layout
        


