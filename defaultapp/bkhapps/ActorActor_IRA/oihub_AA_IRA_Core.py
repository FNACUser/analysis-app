# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 21:26:38 2023

@author: luis.caro
"""

import pandas as pd
import networkx as nx

from bokeh.models.widgets import DataTable, Select
from bokeh.layouts import row, column, layout
from bokeh.models import ColumnDataSource, TableColumn, Tabs, TabPanel


from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_Network_PlotType2

def FD_Core_lists(xG,xk):
    
    # print('>.>.>.>.>.>.>.>.>.>.>.>.>.> FD_Core_lists')
    # print('>>>>>>>>>>>>>> FD_Core_lists - xk')
    # print(xk)
    
    # coreList = list(nx.k_core(xG,k=xk).nodes())
    core_lists = \
        [(k,v.get('redmine_login')) 
         for k,v in nx.k_core(xG,k=xk).nodes(data=True)]
    if len(core_lists) == 0:
        core_list = [] 
        core_names_list = []
    else:
        core_list, core_names_list = map(list,zip(*core_lists)) 
    # print('>>>>>>>>>>>>>> FD_Core - coreList')
    # print(coreList)
    # shellList = list(nx.k_shell(xG,k=xk).nodes())
    shell_lists = \
        [(k,v.get('redmine_login')) 
         for k,v in nx.k_shell(xG,k=xk).nodes(data=True)]
    if len(shell_lists) == 0:
        shell_list = [] 
        shell_names_list = []
    else:
        shell_list, shell_names_list = map(list,zip(*shell_lists)) 
    
    
    # crustList= list(nx.k_crust(xG,k=xk-1).nodes())
    crust_lists = \
        [(k,v.get('redmine_login')) 
         for k,v in nx.k_crust(xG,k=xk-1).nodes(data=True)]
    if len(crust_lists) == 0:
        crust_list = [] 
        crust_names_list = []
    else:
        crust_list, crust_names_list = map(list,zip(*crust_lists)) 
    # print('>>>>>>>>>>>>>> FD_Core - crustList')
    # print(crustList)
    
    main_core_list = list(set(core_list) - set(shell_list))
    main_names_core_list = list(set(core_names_list) - set(shell_names_list))
    # print('>>>>>>>>>>>>>> FD_Core - main_coreList')
    # print(main_coreList)
    
    core_lists= [main_core_list, shell_list, crust_list]
    core_names_lists= [main_names_core_list, shell_names_list, 
                       crust_names_list]
    # print('>>>>>>>>>>>>>> FD_Core - coreLists')
    # print(coreLists)
    
    return core_lists, core_names_lists


def FD_Core(xG,xk=None):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Core/FD_Core')
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> xk (FD_Core)')
    # print(xk)
    
    xG.remove_edges_from(nx.selfloop_edges(xG))
    ndG = xG.to_undirected()
    # print('is directed')
    # print(nx.is_directed(xG))
    # print(nx.is_directed(ndG))
   
    if xk == None:
        Gk=nx.k_core(ndG)
        
        core_degree_centrality_dict = \
            {key: value for (key, value) in Gk.degree}
        # print('>>>>>>>>>>>>>>>>>>>>>> core_degree_centrality_dict (FD_Core)')
        # print(core_degree_centrality_dict)
        nx.set_node_attributes(Gk, core_degree_centrality_dict,
                                    'core_degree_centrality')
        # print('>>>>>>>>>>>>>>>>>>>>>> core_degree_centrality_dict (FD_Core)')
        # print(core_degree_centrality_dict)
        # print('>>>>>>>>>>>>>>>>>>>>>> Gk.nodes(data=True) (FD_Core)')
        # print(Gk.nodes(data=True))
        degrees_list_sorted = \
            [d['core_degree_centrality'] for n,d in Gk.nodes(data=True)]
        degrees_list_sorted.sort()
        # print('>>>>>>>>>>>>>>>>>>>>>> degrees_list_sorted (FD_Core)')
        # print(degrees_list_sorted)
        # print(degrees_list_sorted[len(degrees_list_sorted)-2])
        
        # coreDegree = min([d['core_degree_centrality'] 
        #                   for n,d in Gk.nodes(data=True)])
        coreDegree = degrees_list_sorted[len(degrees_list_sorted)-2]
    else:
        Gk=nx.k_core(ndG,k=xk)
        coreDegree = xk
    
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> xk (FD_Core)')
    # print(coreDegree)
    
    
    _core_lists, _core_names_lists = FD_Core_lists(xG,coreDegree)
    # _core_lists, _core_names_lists = FD_Core_lists(xG,1)
    # print('>>>>>>>>>>>>>> FD_Core')
    # print('>>>>>>>>>>>>>> FD_Core - Gk nodes')
    # print(Gk.nodes(data=True))
    # print('>>>>>>>>>>>>>> FD_Core - _coreLists')
    # print(_coreLists)
    
    tooltips=[("component", "@index"),
              ("nombre", "@redmine_login"),
              ("area", "@organization_area"),
              ("degree", "@core_degree_centrality")]
    
    plotCore, graphCore = UTBo_Network_PlotType2(xG,tooltips,
                                                 'Núcleo / Borde / Corteza',
                                                 nx.shell_layout,
                                                 nx.circular_layout,False,
                                                 500,500,xnodeSize='node_size',
                                                 xnodeColorAttribute = \
                                                     'organization_area_color',
                                                 xadjustNodeSize=True,
                                                 xnlist=_core_lists,
                                                 xcircle=[(3,'#c6dbef',None),
                                                          (2,'#deebf7','black'),
                                                          (1,'#f7fbff',None)])
    
    return plotCore, _core_lists, _core_names_lists, coreDegree, graphCore

def FD_Update_core_plot(xselected_core_degree, xG, xplotCore,
                        xnucleo_data_table, xborde_data_table,
                        xcorteza_data_table):
    
    selected_core_degree = int(xselected_core_degree)
    
    _, _core_lists, _core_names_lists, _coreDegree, _graphCore = \
        FD_Core(xG, xk = selected_core_degree)
    
    graphCore = xplotCore.renderers[3]
    
    # dsnrp3 = _graphCore.node_renderer.data_source
    # graphCore.node_renderer.data_source.data = dict(dsnrp3.data)
    
    # dshrp3 = graphtego.edge_renderer.data_source
    # xgraph3.edge_renderer.data_source.data = dict(dshrp3.data)
    
    graphCore_layout=graphCore.layout_provider
    _graphCore_layout=_graphCore.layout_provider
    graphCore_layout.graph_layout=dict(_graphCore_layout.graph_layout)
    
    xnucleo_data_table.source.data = \
        pd.DataFrame({'Actor':_core_names_lists[0]})
    xborde_data_table.source.data = \
        pd.DataFrame({'Actor':_core_names_lists[1]})
    xcorteza_data_table.source.data = \
        pd.DataFrame({'Actor':_core_names_lists[2]})
    
    
    # print(_coreLists)
    # print(_coreDegree)
    
    
def FD_List_to_data_table(xlist):
    
    listDT = pd.DataFrame({'Actor':xlist})
    
    columnDataSource = ColumnDataSource(listDT)
    
    columns = [TableColumn(field=Ci, title=Ci) for Ci in listDT.columns]

    data_table = \
        DataTable(source = columnDataSource, columns = columns, 
                  width = 800, height = 500)
        
    return data_table
    

def FD_Core_objects(xG):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Core/FD_Core_layout')
    # print('>>>>>>>>>>>>>>>>>>>>>>> xG.nodes(data=True) (FD_Core_layout)')
    # print(xG.nodes(data=True))
    
    _plotCore, _, _core_names_lists, _coreDegree, _ = FD_Core(xG)
    
    nucleo_data_table = FD_List_to_data_table(_core_names_lists[0])
    borde_data_table = FD_List_to_data_table(_core_names_lists[1])
    corteza_data_table = FD_List_to_data_table(_core_names_lists[2])
    
    return _plotCore, nucleo_data_table, borde_data_table,\
        corteza_data_table, _coreDegree
    
    # # print('>>>>>>>>>>>>>>>>>>>> _coreDegree (FD_Core_layout)')
    # # print(_coreDegree)
    
    # _options = [str(i) for i in range(1,_coreDegree+2)]
    # # print('>>>>>>>>>>>>>>>>>>>> _options (FD_Core_layout)')
    # # print(_options)
    
    # select_core_degree = Select(title="Grado núcleo:", 
    #                            value = str(_coreDegree), 
    #                            options=_options, 
    #                            height=50, width=200)
    
    # select_core_degree.on_change('value', 
    #                                 lambda attr, old, new: \
    #                                     FD_Update_core_plot(select_core_degree.value,
    #                                                         xG,
    #                                                         _plotCore,
    #                                                         nucleo_data_table,
    #                                                         borde_data_table,
    #                                                         corteza_data_table))
    
    
    # nucleo_panel = TabPanel(child=nucleo_data_table, title='Actores núcleo')
    # borde_panel = TabPanel(child=borde_data_table, title='Actores borde')
    # corteza_panel = TabPanel(child=corteza_data_table, title='Actores corteza')
    
    # nucleo_tabs =Tabs(tabs=[nucleo_panel, borde_panel, corteza_panel])
        
    # core_layout = row(_plotCore,column(select_core_degree,nucleo_tabs))
    
    # return core_layout, _plotCore, select_core_degree, _coreDegree


def FD_Core_layout(xG, xplotCore, xnucleo_data_table, xborde_data_table,
                   xcorteza_data_table, xcoreDegree):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Core/FD_Core_layout')
    # print('>>>>>>>>>>>>>>>>>>>>>>> xG.nodes(data=True) (FD_Core_layout)')
    # print(xG.nodes(data=True))
    
    # _plotCore, nucleo_data_table, borde_data_table,\
    #     corteza_data_table, _coreDegree = FD_Core_objects(xG)
    
    # print('>>>>>>>>>>>>>>>>>>>> _coreDegree (FD_Core_layout)')
    # print(_coreDegree)
    
    _options = [str(i) for i in range(1, xcoreDegree + 2)]
    # print('>>>>>>>>>>>>>>>>>>>> _options (FD_Core_layout)')
    # print(_options)
    
    select_core_degree = Select(title="Grado núcleo:", 
                               value = str(xcoreDegree), 
                               options = _options, 
                               height=50, width=200)
    
    select_core_degree.on_change('value', 
                                    lambda attr, old, new: \
                                        FD_Update_core_plot(select_core_degree.value,
                                                            xG,
                                                            xplotCore,
                                                            xnucleo_data_table,
                                                            xborde_data_table,
                                                            xcorteza_data_table))
    
    nucleo_panel = TabPanel(child = xnucleo_data_table, title='Actores núcleo')
    borde_panel = TabPanel(child = xborde_data_table, title='Actores borde')
    corteza_panel = TabPanel(child = xcorteza_data_table, title='Actores corteza')
    
    nucleo_tabs =Tabs(tabs=[nucleo_panel, borde_panel, corteza_panel])
        
    core_layout = row(xplotCore, column(select_core_degree, nucleo_tabs))
    
    return core_layout, select_core_degree