# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 19:08:37 2023

@author: luis.caro
"""

import pandas as pd
import numpy as np
import networkx as nx
# import itertools
import sqlite3


from bokeh.models import (ColumnDataSource, TableColumn, Slider, 
                          CheckboxButtonGroup, RadioGroup, Button,
                          CheckboxGroup)

from bokeh.models.widgets import DataTable, MultiSelect


from bokeh.layouts import row, column
from bokeh.models import Tabs, TabPanel 

from bokeh.io import curdoc

from .oihub_AA_IRA_Core import FD_Core_layout, FD_Core_objects

from .oihub_AA_IRA_Model import (FD_AA_model_main, FD_Arrows,
                                   FD_businessComponentSelection)


from .oihub_AA_IRA_Communities import (FD_Communities_info,
                                        FD_Communities_info_layout, 
                                        FD_Communities_analyzer,
                                        FD_Community_participants,
                                        FD_Community_selector,
                                        FD_create_informal_network_plot)

from .oihub_IRA_Questions import FD_questions_AA_main, FD_single_question_hm
# UTBo_Component_hmx

from .oihub_AA_IRA_QCommon import (FD_network_parameters_dict)

from .oihub_AA_IRA_help_texts_objects import FD_fetch_help_texts_objects

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import (UTBo_EmptyParagraph, 
                            UTBo_BokehGraphToNetworkxGraph,
                            UTBo_Network_PlotType2)

# from oihub_UtilitiesBokeh_HeatMap import UTBoHM_Component_hm

from .UtilitiesSQL import FD_Table_to_dataframe

from defaultapp.bkhapps.common.Utilities import UT_bring_legend


#%%

def FD_Edges_to_dictionary():
    
    connection = sqlite3.connect('finacHCAAedges.db')
    # cursor = connection.cursor()
    
    edges_dict={}
    
    networks = ['aa_1','aa_2','aa_3','aa_4']
    frequencies = [0,1,2]
    accumulations = [True,False]
    
    def add_network_edges_to_dictionary(xnetwork, xfrequency, xaccumulation):
        
        table=xnetwork+'_'+str(xfrequency)+'_'+str(xaccumulation)
        
        aa_edges = FD_Table_to_dataframe(connection,table).to_numpy()
        
        edges_dict[(xnetwork, xfrequency, xaccumulation)]=aa_edges[:,1:]
        
   
    [add_network_edges_to_dictionary(network, frequency, accumulation) 
     for network in networks \
         for frequency in frequencies \
             for accumulation in accumulations]
        
    actorsDF = FD_Table_to_dataframe(connection,'actors')
    actors_data = actorsDF.loc[actorsDF['incluido']==True].copy(deep=True) 
    
    
    return edges_dict, actors_data
    

#%%

# def FD_single_question_hm(xquestion):
    
#     dimension_x_dict = {'0': 'Nada'}

#     dimension_y_dict = {'0': 'Nada'}
        
#     cell_frequencies_dict = {'uno': [0],
#                               'dos': [0],
#                               'tres': [0],
#                               'cuatro': [xquestion]}

#     cell_frequencies = pd.DataFrame.from_dict(cell_frequencies_dict)

#     hm2 = UTBoHM_Component_hm(dimension_x_dict, dimension_y_dict,
#                            cell_frequencies, 'title',
#                            xcontent_is_str = True,                       
#                           xtotal_cells = False, xtotal_cells_label = '',
#                           xstart_x_index = 0, xstart_y_index = 0,
#                           xlabel_x_axis = '', xlabel_y_axis = '',
#                           xwidth=900, xheight=140,
#                           xsingle_color = "lightgreen")
    
#     return hm2


def FD_question_update(xconn, xhm, xhm2, xmenu_questions_list, xquestions_df,
                       xglobal_questions_dict,
                       xnetwork_parameters_dict,
                       xxfrequencyCorte, xxcheckedoptions, 
                       xresponses_button_group,
                       xnode_color_group, 
                       xall_any_filter_group,
                                            xamplifier, xbimodalAmplifier,
                                           xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
                                           xsourceInteracción_AA_x, xmulti_select_AA_x,
                                           xnon_connected_list_AA_x, xplot_informal_network,
                                           xplot_area_network_AA_x,
                                           xcommunity_attribute,
                                           xnetwork,xxedges_dict,
                                           xxactors_data,
                                           xgravity_slider,
                                           xxcomplete_nx_graph,
                                           xmainAInDegreePlot, 
                                           xmainAOutDegreePlot,
                                           xmainAEigenvectorPlot, 
                                           xmainABetweennessPlot,
                                           xdata_table_nodeDF,
                                           xparameters_for_business_component_selection_dict,
                                           xexcluded_select,
                                           xgraph2, xgraph3,
                                           xtable_inverse_responder_ego, 
                                           xtable_responder_ego,
                                           xcommunity_color_selector,
                                           xdata_table_community_participants,
                                           xplot_quotient_informal_network,
                                           xsub_plot_informal_network,
                                           xcommunity_color_selector2,
                                           xdata_table_community_participants2,
                                           xplot_quotient_organization_area,
                                           xsub_plot_informal_network2,
                                           xplot_core, xselect_core_degree,
                                           xhelp_texts_tuple,
                                           xdata_table_ModeloCompleto,
                                           xinverse_question_checkbox_group):
    
    print ('.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Utilities/FD_question_update')
    # print ('$$$$$$$$$$$$$$$$$$$$$$ oihub_AA_IRA_Utilities/FD_question_update')
    # print ('%%%%%%%%%%%%%%%%%%%%%% oihub_AA_IRA_Utilities/FD_question_update')
    # print ('.-.-.-.-.-.-.-.-.-.-.- oihub_AA_IRA_Utilities/FD_question_update')
    selected_indices = xhm.renderers[0].data_source.selected.indices
    # print('>>>>>>>>>>>>>>>>> xcomponent_academic_model (FD_tap_update)')
    # print(selected_indices)
    # print('>>>>>>>>>>>>>>>>> menu_question (FD_tap_update)')
    # print(xmenu_questions[selected_indices[0]])
    
    _hm2 = FD_single_question_hm(xmenu_questions_list[selected_indices[0]],
                                 xselected_question_title = '')
    
    xhm2_source = xhm2.renderers[0].data_source
    # print('>>>>>>>>>>dict(xhm_source.data)')
    # print(dict(xhm_source.data))
              
    _hm2_source = _hm2.renderers[0].data_source
    
       
    xhm2.renderers[0].data_source.data = dict(_hm2_source.data)
    
    #
    #help texts
    _help_text_introduction, _help_text_edges, _help_text_centralities, \
        _help_text_filtered_employee, _help_text_communities,\
            _help_text_node_level = xhelp_texts_tuple
            
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> _help_text_introduction (FD_question_update)')
    # print(_help_text_introduction.text)    
    
    # print('>>>>>>>>>>>>>>>>> question_df (FD_tap_update)')
    # print(xquestions_df.iloc[xquestions_df.shape[0]-1-selected_indices[0]])
    
    ids_df = xquestions_df.iloc[xquestions_df.shape[0]-1-selected_indices[0]]\
        [['q.id_question','nwm.id_network_mode']]
    id_question = ids_df['q.id_question']
    # print('id_question')
    # print(id_question)
    id_network_mode = ids_df['nwm.id_network_mode']
    # print('id_network_mode')
    # print(id_network_mode)
    
    # print('dict')
    # print(xnetwork_parameters_dict)
    FD_network_parameters_dict(xconn, id_question, id_network_mode,
                                xglobal_questions_dict, 
                                xnetwork_parameters_dict)
    # print('dict')
    # print(xnetwork_parameters_dict)
    
    """
    Despliega u oculta all_any_filter_group con base en la pregunta
    """
    filter_group_enabled = \
        xnetwork_parameters_dict['filter_group_enabled']
    
    if filter_group_enabled == True:
        xall_any_filter_group.visible = True
    else:
        xall_any_filter_group_visible = False
    
    
    ihelp_text_introduction, ihelp_text_edges, ihelp_text_centralities, \
        ihelp_text_filtered_employee, ihelp_text_communities,\
            ihelp_text_node_level = \
                FD_fetch_help_texts_objects(xnetwork_parameters_dict)
    
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> ihelp_text_introduction (FD_question_update)')
    # print(ihelp_text_introduction.text)  
    
    _help_text_introduction.text = ihelp_text_introduction.text
    _help_text_edges.text = ihelp_text_edges.text
    _help_text_centralities.text = ihelp_text_centralities.text
    _help_text_filtered_employee.text = ihelp_text_filtered_employee.text
    _help_text_communities = ihelp_text_communities
    _help_text_node_level.text = ihelp_text_node_level.text
    
    possible_responses_components = \
        xnetwork_parameters_dict.get('possible_responses_components')
    # print('possible_responses_components')
    # print(possible_responses_components)
    active_selected_possible_responses = \
        xnetwork_parameters_dict.get('active_selected_possible_responses')
    # print('active_selected_possible_responses')
    # print(active_selected_possible_responses)
    possible_responses_dict = \
        xnetwork_parameters_dict.get('possible_responses_dict')
    # print('possible_responses_dict')
    # print(possible_responses_dict)
    p_d_inverse_question = \
        xnetwork_parameters_dict.get('inverse_question')
        
    xresponses_button_group.labels = possible_responses_components
    xresponses_button_group.active = active_selected_possible_responses
    
    #.-.-.-.-.-.-.-.-.-.-.-. combine questions
    
    if p_d_inverse_question is None:
        xinverse_question_checkbox_group.visible = False
    else:
        xinverse_question_checkbox_group.visible = True
    
    #:_:_:_:_:_:_:_:_:_:_:_: combine questions
    
    FD_Cambio_corte2(xconn, xnetwork_parameters_dict,
                     # xnetwork_parameters_data_table,                              
                    "",
                    "",
                    xresponses_button_group.active,
                    xnode_color_group,
                    xall_any_filter_group.active,
                                         xamplifier, xbimodalAmplifier,
                                        xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
                                        xsourceInteracción_AA_x, xmulti_select_AA_x,
                                        xnon_connected_list_AA_x, xplot_informal_network,
                                        xplot_area_network_AA_x,
                                        xcommunity_attribute,
                                        xnetwork,xxedges_dict,
                                        xxactors_data,
                                        xgravity_slider,
                                        xxcomplete_nx_graph,
                                        xmainAInDegreePlot, 
                                        xmainAOutDegreePlot,
                                        xmainAEigenvectorPlot, 
                                        xmainABetweennessPlot,
                                        xdata_table_nodeDF,
                                        xparameters_for_business_component_selection_dict,
                                        xexcluded_select,
                                        xgraph2, xgraph3,
                                        xtable_inverse_responder_ego, 
                                        xtable_responder_ego,
                                        xcommunity_color_selector,
                                        xdata_table_community_participants,
                                        xplot_quotient_informal_network,
                                        xsub_plot_informal_network,
                                        xcommunity_color_selector2,
                                        xdata_table_community_participants2,
                                        xplot_quotient_organization_area,
                                        xsub_plot_informal_network2,
                                        xplot_core, xselect_core_degree,
                                        xdata_table_ModeloCompleto)

    
    
    

#%%

#aquí no se usa pero se importa en finacIRAUtilities
def FD_Adjust_gravity(xG,xgravity):
    
    # print('>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.> FD_Adjust_gravity')
    
    for u,w,v in xG.edges(data=True):
        if xG.nodes[u]['informal_network'] == xG.nodes[w]['informal_network']:
            v['informal_network_weight'] = \
                v['informal_network_base_weight'] * xgravity    



def FD_Cambio_gravity(slider_value,xplot1):
    
    # print('>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.> FD_Cambio_gravity')
    
    _plot1Graph=xplot1.renderers[0]
    
    _G=UTBo_BokehGraphToNetworkxGraph(_plot1Graph,xDiGraph=True)
    
    FD_Adjust_gravity(_G,slider_value)
    # print(_G.edges(data=True))
    
    _title=xplot1.title.text
    _height=xplot1.plot_height
    _width=xplot1.plot_width
    _tooltips=[("component", "@index")]
    
    _pos = nx.circular_layout(_G)
    
    
    _,_graphS = UTBo_Network_PlotType2(_G,_tooltips,_title,
                                        nx.spring_layout,nx.spring_layout,False,
                                        _height,_width,
                                        xnodeSize='node_size',
                                        xnodeColorAttribute='organization_area_color',
                                        xedgeColorAttribute='informal_network',
                                        xedgeWidthAttribute = 'informal_network_width',
                                        xadjustNodeSize=True,
                                        xpos=_pos,
                                        xgravityAttribute = 'informal_network_weight',
                                        xk=1.5)
    
        
    _nodes=_graphS.node_renderer.data_source
    _edges=_graphS.edge_renderer.data_source
    
    _plot1Graph.node_renderer.data_source.data = dict(_nodes.data)
    _plot1Graph.edge_renderer.data_source.data = dict(_edges.data)
    
    _layout_plot1Graph=_plot1Graph.layout_provider
    _layout_plot1Graph.graph_layout=dict(_graphS.layout_provider.graph_layout)
    
    _plot1SelectedNodeGraph=xplot1.renderers[4]
    _layout_plot1SelectedNodeGraph = _plot1SelectedNodeGraph.layout_provider
    _layout_plot1SelectedNodeGraph.graph_layout = dict(_graphS.layout_provider.graph_layout)
    
    FD_Arrows(xplot1,xrendererToUpdate=5)


#%%
def FD_update_main_AA_plot(xplot1_AA_x, xiplot1_AA_x):
    
    """
    Updates main_AA_plot (called plot1) every time the netwrok is
    recalculated
    """
    
    print('.-.-.-.-.-.-.-.- oihub_AA_IRA_Utilities/FD_update_main_AA_plot')
    
    xg1=xplot1_AA_x.renderers[0]
    dsnrp1 = xiplot1_AA_x.renderers[0].node_renderer.data_source
    xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    dsnrp1g = xiplot1_AA_x.renderers[0].node_renderer.glyph
    xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
    
    dshrp1 = xiplot1_AA_x.renderers[0].edge_renderer.data_source
    xg1.edge_renderer.data_source.data = dict(dshrp1.data)
    
    title_color_legend=xplot1_AA_x.renderers[1]
    new_title_color_legend = xiplot1_AA_x.renderers[1].data_source
    title_color_legend.data_source.data = dict(new_title_color_legend.data)
    
    rectangles_color_legend=xplot1_AA_x.renderers[2]
    new_rectangles_color_legend = xiplot1_AA_x.renderers[2].data_source
    rectangles_color_legend.data_source.data = dict(new_rectangles_color_legend.data)
    
    names_color_legend=xplot1_AA_x.renderers[3]
    new_names_color_legend = xiplot1_AA_x.renderers[3].data_source
    names_color_legend.data_source.data = dict(new_names_color_legend.data)
    
    #4 a 2
    xgSel=xplot1_AA_x.renderers[4]
    dsnrpSel = xiplot1_AA_x.renderers[4].node_renderer.data_source
    xgSel.node_renderer.data_source.data = dict(dsnrpSel.data)
    
    
    #5 a 3
    xgArrow=xplot1_AA_x.renderers[5]
    dsnrpArrow = xiplot1_AA_x.renderers[5].node_renderer.data_source
    xgArrow.node_renderer.data_source.data = dict(dsnrpArrow.data)
    
    layout_graph1_AA=xg1.layout_provider
    layout_graphSel_AA=xgSel.layout_provider
    layout_graphArrow_AA=xgArrow.layout_provider
    
    # print('>>>>>>dict(xplot1_AA_x.renderers[0].layout_provider.graph_layout) FD_update_main_AA_plot')
    # print(dict(xplot1_AA_x.renderers[0].layout_provider.graph_layout))
    layout_graph1_AA.graph_layout = \
        dict(xiplot1_AA_x.renderers[0].layout_provider.graph_layout)
    # print('>>>>>>dict(xiplot1_AA_x.renderers[0].layout_provider.graph_layout) FD_update_main_AA_plot')
    # print(dict(xiplot1_AA_x.renderers[0].layout_provider.graph_layout))
    
    # layout_graphSel_AA.graph_layout=dict(iplot1_AA_x.renderers[4].layout_provider.graph_layout)
    # layout_graphArrow_AA.graph_layout=dict(iplot1_AA_x.renderers[5].layout_provider.graph_layout)
    layout_graphSel_AA.graph_layout = \
        dict(xiplot1_AA_x.renderers[4].layout_provider.graph_layout)
    layout_graphArrow_AA.graph_layout = \
        dict(xiplot1_AA_x.renderers[5].layout_provider.graph_layout)
    
    
def FD_Update_AA_Network2(xconn, xnetwork_parameters_dict, 
                          xxedges_dict, xxxactors_data, xnetwork, xedges_AA_x,
                         xplot1_AA_x, xplot2_AA_x, xplot3_AA_x,
                         xsourceInteracción_AA_x, xxmulti_select_AA_x,
                         xnon_connected_list_AA_x,
                         xamplifier,
                         xxfrequencyCorte, xxfrequencyResponseAccumulation,
                         xactive_responses,
                         xnode_color_group,
                         xbimodalAmplifier, xplot_informal_network, 
                         xplot_area_network_AA_x,
                         xmainAInDegreePlot, 
                         xmainAOutDegreePlot,
                         xmainAEigenvectorPlot, 
                         xmainABetweennessPlot,
                         xdata_table_nodeDF,
                         xall_any_filter_group_active,
                         xparameters_for_business_component_selection_dict,
                         xgraph2, xgraph3,
                         xtable_inverse_responder_ego, 
                         xtable_responder_ego,
                         xcommunity_color_selector,
                         xdata_table_community_participants,
                         xplot_quotient_informal_network,
                         xsub_plot_informal_network,
                         xcommunity_color_selector2,
                         xdata_table_community_participants2,
                         xplot_quotient_organization_area,
                         xsub_plot_informal_network2,
                         xplot_core, xselect_core_degree,
                         xdata_table_ModeloCompleto):
    
    """
    This function is executed from FD_Cambio_corte_2. Since the execution
    of FD_Cambio_corte2 happens when the user changes the answers 
    included in the model (see FD_Cambio_corte2 to identify the cases in
    which this happens).
    
    The purpose of ths function is to execute the whole model running
    FD_AA_model_main, and updating all the dashboards' components.
    """ 
    
    print('.-.-.-.-.-.-.-.-.-.. oihub_AA_IRA_Utilities/FD_Update_AA_Network2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Update_AA_Network2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Update_AA_Network2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Update_AA_Network2')
    # print('>>>>>>>>>>>>> xfrequencyCorte (FD_Update_AA_Network2)')
    # print(xxfrequencyCorte)
    # print('>>>>>>>>>>>>> xfrequencyResponseAccumulation (FD_Update_AA_Network2)')
    # print(xxfrequencyResponseAccumulation)
    
    XXXXedges_dict = 'ghghg'
    
    
    if xnode_color_group.active == 0:
        node_color_attribute = 'organization_area_color'
    else:
        node_color_attribute = 'cvf_cluster_color'
                                    
    # print('Se va a ir a FD_AA_model_main (FD_Update_AA_Network2')
    
    #.-.-.-.-.-.-.-.-.
    iplot1_AA_x, parameters_for_business_component_selection_dict, \
        iplot2_AA_x, iplot3_AA_x, _, idata_table_ModeloCompleto, \
        _, _, idensityCAA_x, idensityFAA_x, _, _, \
            _, _, _, isourceInteracción_AA_x, \
                idirección, inúmero_conexiones_componentes_eliminados_x, \
                    imainAInDegreePlot, imainAOutDegreePlot,\
                    imainAEigenvectorPlot, imainABetweennessPlot,\
                    idata_table_nodeDF, iplot_informal_network, \
                            non_connected_list_AA_x, communities,\
                                community_palette, iplot_area_network_AA_x,\
                                    iplot_quotient_informal_network, \
                                        plot_quotient_organization_area, \
                                            x_core_layout, x_plot_core, \
                                        icomplete_nx_graph, _, _, _, _,\
                                        itable_inverse_responder_ego, \
                                            itable_responder_ego = \
                    FD_AA_model_main(xconn, xnetwork_parameters_dict, 
                                     -1, XXXXedges_dict, xamplifier,
                            "", 
                            "",
                            xactive_responses,
                            xall_any_filter_group_active,
                            xnode_color_attribute = node_color_attribute)
                    
    
    #Así estaba antes de crear core_objects los ii no se usan
    # iicore_layout, iplot_core, iiselect_core_degree, icore_degree = \
    #     FD_Core_objects(icomplete_nx_graph)
    iplot_core, iinucleo_data_table, iiborde_data_table, iicorteza_data_table,\
        icore_degree = FD_Core_objects(icomplete_nx_graph)
    
    xrenderer = xplot_core.renderers[3]
    irenderer = iplot_core.renderers[3].node_renderer.data_source
    xrenderer.node_renderer.data_source.data = dict(irenderer.data)
    irenderer_glyph = iplot_core.renderers[3].node_renderer.glyph
    xrenderer.node_renderer.glyph.fill_color = irenderer_glyph.fill_color
    
    irenderer_edge = iplot_core.renderers[3].edge_renderer.data_source
    xrenderer.edge_renderer.data_source.data = dict(irenderer_edge.data)
    
    ioptions = [str(i) for i in range(1, icore_degree+2)]
    
    xselect_core_degree.options = ioptions
    xselect_core_degree.value = str(icore_degree)    
    
    # xg2=xplot2_AA_x.renderers[0]
    # dsnrp2 = iplot2_AA_x.renderers[0].node_renderer.data_source
    # xg2.node_renderer.data_source.data = dict(dsnrp2.data)
    # dsnrp2g = iplot2_AA_x.renderers[0].node_renderer.glyph
    # xg2.node_renderer.glyph.fill_color = dsnrp2g.fill_color
    
    # dshrp2 = iplot2_AA_x.renderers[0].edge_renderer.data_source
    # xg2.edge_renderer.data_source.data = dict(dshrp2.data)
    
    
    # print('c')
    # yyy=iplot_core.renderers[0].glyph
    # yyy=iplot_core.renderers[1].glyph
    # yyy=iplot_core.renderers[2].glyph
    # for i in range(3,10):
    #     print(i)
    #     print('g')
    #     yyy=iplot_core.renderers[i].node_renderer.glyph
    #     print('er')
    #     zzz=iplot_core.renderers[i].edge_renderer.data_source
    #     print('nr')
    #     xxx=iplot_core.renderers[i].node_renderer.data_source
        
    
    # print('Va a update el diccionario (FD_Update_AA_Network2')
    icommunity_color_selector, idata_table_community_participants, \
        isub_plot_informal_network = \
            FD_Communities_info('informal_network', 'xx',
                                'organization_area_color', icomplete_nx_graph)
            
    icommunity_color_selector2, idata_table_community_participants2, \
        isub_plot_informal_network2 = \
            FD_Communities_info('organization_area', 'xx', 
                                'informal_network_color',
                                icomplete_nx_graph)
    

    
    xparameters_for_business_component_selection_dict.update\
        (parameters_for_business_component_selection_dict)
    
                    
    
    # print('Quedó updated el diccionario (FD_Update_AA_Network2')
    
                                    
    # print('FD_Update_AA_Network')
    # print(non_connected_list_AA_x.options)
    xnon_connected_list_AA_x.options = non_connected_list_AA_x.options
                                    
    FD_update_main_AA_plot(xplot1_AA_x, iplot1_AA_x)
    # xg1=xplot1_AA_x.renderers[0]
    # dsnrp1 = iplot1_AA_x.renderers[0].node_renderer.data_source
    # xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    # dsnrp1g = iplot1_AA_x.renderers[0].node_renderer.glyph
    # xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
    
    # dshrp1 = iplot1_AA_x.renderers[0].edge_renderer.data_source
    # xg1.edge_renderer.data_source.data = dict(dshrp1.data)
    
    # title_color_legend=xplot1_AA_x.renderers[1]
    # new_title_color_legend=iplot1_AA_x.renderers[1].data_source
    # title_color_legend.data_source.data = dict(new_title_color_legend.data)
    
    # rectangles_color_legend=xplot1_AA_x.renderers[2]
    # new_rectangles_color_legend=iplot1_AA_x.renderers[2].data_source
    # rectangles_color_legend.data_source.data = dict(new_rectangles_color_legend.data)
    
    # names_color_legend=xplot1_AA_x.renderers[3]
    # new_names_color_legend=iplot1_AA_x.renderers[3].data_source
    # names_color_legend.data_source.data = dict(new_names_color_legend.data)
    
    # #4 a 2
    # xgSel=xplot1_AA_x.renderers[4]
    # dsnrpSel = iplot1_AA_x.renderers[4].node_renderer.data_source
    # xgSel.node_renderer.data_source.data = dict(dsnrpSel.data)
    
    
    # #5 a 3
    # xgArrow=xplot1_AA_x.renderers[5]
    # dsnrpArrow = iplot1_AA_x.renderers[5].node_renderer.data_source
    # xgArrow.node_renderer.data_source.data = dict(dsnrpArrow.data)
    
    
    
    xg2=xplot2_AA_x.renderers[0]
    dsnrp2 = iplot2_AA_x.renderers[0].node_renderer.data_source
    xg2.node_renderer.data_source.data = dict(dsnrp2.data)
    dsnrp2g = iplot2_AA_x.renderers[0].node_renderer.glyph
    xg2.node_renderer.glyph.fill_color = dsnrp2g.fill_color
    
    dshrp2 = iplot2_AA_x.renderers[0].edge_renderer.data_source
    xg2.edge_renderer.data_source.data = dict(dshrp2.data)
    
    xg2Arrow=xplot2_AA_x.renderers[1]
    dsnrp2Arrow = iplot2_AA_x.renderers[1].node_renderer.data_source
    xg2Arrow.node_renderer.data_source.data = dict(dsnrp2Arrow.data)
    
    datasource = itable_inverse_responder_ego.source.data
    xtable_inverse_responder_ego.source.data = dict(datasource)

    
    xg3=xplot3_AA_x.renderers[0]
    dsnrp3 = iplot3_AA_x.renderers[0].node_renderer.data_source
    xg3.node_renderer.data_source.data = dict(dsnrp3.data)
    dsnrp3g = iplot3_AA_x.renderers[0].node_renderer.glyph
    xg3.node_renderer.glyph.fill_color = dsnrp3g.fill_color
    
    dshrp3 = iplot3_AA_x.renderers[0].edge_renderer.data_source
    xg3.edge_renderer.data_source.data = dict(dshrp3.data)
    
    xg3Arrow=xplot3_AA_x.renderers[1]
    dsnrp3Arrow = iplot3_AA_x.renderers[1].node_renderer.data_source
    xg3Arrow.node_renderer.data_source.data = dict(dsnrp3Arrow.data)
    
    datasource = itable_responder_ego.source.data
    xtable_responder_ego.source.data = dict(datasource)

    xgH=xplot_informal_network.renderers[0]
    dsnrpH = iplot_informal_network.renderers[0].node_renderer.data_source
    xgH.node_renderer.data_source.data = dict(dsnrpH.data)
    
    dshrpH = iplot_informal_network.renderers[0].edge_renderer.data_source
    xgH.edge_renderer.data_source.data = dict(dshrpH.data)
    
    xgAN=xplot_area_network_AA_x.renderers[0]
    dsnrpAN = iplot_area_network_AA_x.renderers[0].node_renderer.data_source
    xgAN.node_renderer.data_source.data = dict(dsnrpAN.data)
    
    dshrpAN = iplot_area_network_AA_x.renderers[0].edge_renderer.data_source
    xgAN.edge_renderer.data_source.data = dict(dshrpAN.data)
    
    # layout_graph1_AA=xg1.layout_provider
    # layout_graphSel_AA=xgSel.layout_provider
    # layout_graphArrow_AA=xgArrow.layout_provider
    layout_graph2_AA=xg2.layout_provider
    layout_graph2Arrow_AA=xg2Arrow.layout_provider
    layout_graph3_AA=xg3.layout_provider
    layout_graph3Arrow_AA=xg3Arrow.layout_provider
    layout_graphH_AA=xgH.layout_provider
    layout_graphAN_AA=xgAN.layout_provider
    
    # layout_graph1_AA.graph_layout = \
    #     dict(iplot1_AA_x.renderers[0].layout_provider.graph_layout)
    # layout_graphSel_AA.graph_layout = \
    #     dict(iplot1_AA_x.renderers[4].layout_provider.graph_layout)
    # layout_graphArrow_AA.graph_layout = \
    #     dict(iplot1_AA_x.renderers[5].layout_provider.graph_layout)
    layout_graph2_AA.graph_layout = \
        dict(iplot2_AA_x.renderers[0].layout_provider.graph_layout)
    layout_graph2Arrow_AA.graph_layout = \
        dict(iplot2_AA_x.renderers[1].layout_provider.graph_layout)
    layout_graph3_AA.graph_layout = \
        dict(iplot3_AA_x.renderers[0].layout_provider.graph_layout)
    layout_graph3Arrow_AA.graph_layout = \
        dict(iplot3_AA_x.renderers[1].layout_provider.graph_layout)
    layout_graphH_AA.graph_layout = \
        dict(iplot_informal_network.renderers[0].layout_provider.graph_layout)
    layout_graphAN_AA.graph_layout = \
        dict(iplot_area_network_AA_x.renderers[0].layout_provider.graph_layout)
    
    xplot1_AA_x.title.text = \
        'Modelo completo - Network density = '+ str(idensityCAA_x)
        
    xplot2_AA_x.title.text = \
        'Modelo filtrado (layout original) - Network density = '+ str(idensityFAA_x)
    
    xplot3_AA_x.title.text = \
        'Ego componentes eliminados - Conexiones['+ idirección + ']:'+ \
            inúmero_conexiones_componentes_eliminados_x
    
    xsourceInteracción_AA_x.data = dict(isourceInteracción_AA_x.data)
    
    #
    #update Modelo completo - centralities
    datasource_modelo_completo = idata_table_ModeloCompleto.source.data
    xdata_table_ModeloCompleto.source.data = dict(datasource_modelo_completo)
    
    
    #.-.-.-.-.- Degree plots
    def update_bubble_plot(xplot, _plot):
        xg1=xplot.renderers[0]
        dsnrp1 = _plot.renderers[0].node_renderer.data_source
        xg1.node_renderer.data_source.data = dict(dsnrp1.data)
        dsnrp1g = _plot.renderers[0].node_renderer.glyph
        xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
        
        dshrp1 = _plot.renderers[0].edge_renderer.data_source
        xg1.edge_renderer.data_source.data = dict(dshrp1.data)
        
        yaxis_overrides = _plot.yaxis.major_label_overrides
        xplot.yaxis.major_label_overrides = yaxis_overrides
        
        layout_graph1_AA=xg1.layout_provider
        
        layout_graph1_AA.graph_layout = \
            dict(_plot.renderers[0].layout_provider.graph_layout)
            
    update_bubble_plot(xmainAInDegreePlot, imainAInDegreePlot)
    update_bubble_plot(xmainAOutDegreePlot, imainAOutDegreePlot)
    update_bubble_plot(xmainAEigenvectorPlot, imainAEigenvectorPlot)
    update_bubble_plot(xmainABetweennessPlot, imainABetweennessPlot)
    
    datasource = idata_table_nodeDF.source.data
    xdata_table_nodeDF.source.data = dict(datasource)
    
    FD_update_communities_display_objects(xdata_table_community_participants,
                                          idata_table_community_participants,
                                          xsub_plot_informal_network,
                                          isub_plot_informal_network)
        
    FD_update_communities_display_objects(xdata_table_community_participants2,
                                          idata_table_community_participants2,
                                          xsub_plot_informal_network2,
                                          isub_plot_informal_network2)
    
    #:_:_:_:_:_:_ Degree plots
    # print('Sale de (FD_Update_AA_Network2')
    
    return icomplete_nx_graph


def FD_Cambio_corte2(xconn, xnetwork_parameters_dict,
                     xxfrequencyCorte, xxcheckedoptions, xactive_responses,
                     xnode_color_group, xall_any_filter_group_active,
                     xamplifier, xbimodalAmplifier,
                    xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
                    xsourceInteracción_AA_x, xmulti_select_AA_x,
                    xnon_connected_list_AA_x, xplot_informal_network,
                    xplot_area_network_AA_x,
                    xcommunity_attribute,
                    xnetwork,xxedges_dict,
                    xxactors_data,
                    xgravity_slider,
                    xxcomplete_nx_graph,
                    xmainAInDegreePlot, 
                    xmainAOutDegreePlot,
                    xmainAEigenvectorPlot, 
                    xmainABetweennessPlot,
                    xdata_table_nodeDF,
                    xparameters_for_business_component_selection_dict,
                    xexcluded_select,
                    xgraph2, xgraph3,
                    xtable_inverse_responder_ego, 
                    xtable_responder_ego,
                    xcommunity_color_selector,
                    xdata_table_community_participants,
                    xplot_quotient_informal_network,
                    xsub_plot_informal_network,
                    xcommunity_color_selector2,
                    xdata_table_community_participants2,
                    xplot_quotient_organization_area,
                    xsub_plot_informal_network2,
                    xplot_core, xselect_core_degree,
                    xdata_table_ModeloCompleto):
    
    """
    This function is executed in 3 cases:
        1- when the user selects new answers to
            include in the network in the responses_button_group,
            and presses the calculate_button.
        2 - when the user changes the selection in the node_color_group 
            (organization area vs informal network). This could have been 
            done in a simpler way, but for the time being it is solved 
            executing this function.
        3 - when the user cahnges the selection in the filter_group
            (all or any of the selections in the responses_button_group).
    """
    print('.-.-.-.-.-.-.-.-.-..-.- oihub_AA_IRA_Utilities/FD_Cambio_corte2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Cambio_corte2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Cambio_corte2')
    # print('.-.-.-.-.-.-.-.-.-..-.- FD_Cambio_corte2')
    print('>>>>>>>>>>>>>entrando xexcluded_select.value (FD_Cambio_corte2)')
    print(xexcluded_select.value)
    # print('>>>>>>>>>>>>> xcheckedoptions (FD_Cambio_corte2)')
    # print(xxcheckedoptions)
    # print('>>>>>>>>>>>>> xactive_responses (FD_Cambio_corte2)')
    # print(xactive_responses)
    
    # print('inicio len(complete_nx_graph.edges()) (FD_Cambio_corte2)')
    # print(len(xcomplete_nx_graph.edges()))
    
    
    
    # print('cambio corte xcheckedoptions:')
    # print(xcheckedoptions)
    
    # print('cambio corte positiveResponseMinimum:')
    # print(positiveResponseMinimum)
    
    # print('>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>.>>>> FD_Cambio_corte2')
    # print('FD_Cambio_corte2 - xnetwork')
    # print(xnetwork)
    # print('FD_Cambio_corte2 - xfrequencyCorte')
    # print(xfrequencyCorte)
    # print('FD_Cambio_corte2 - xcheckedoptions')
    # print(xcheckedoptions)
    
    xgravity_slider.value = 1
    
    
    XXXXiedges_AA = 'gggghg'
    XXXXedges_dict = 'gggghg'
    # print('FD_Cambio_corte2 - iedges_AA')
    # print(iedges_AA)
    
            
    _complete_nx_graph = FD_Update_AA_Network2(xconn, 
                                               xnetwork_parameters_dict, 
                          XXXXedges_dict, -1, xnetwork, 
                          XXXXiedges_AA,
                         xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
                         xsourceInteracción_AA_x,
                         xmulti_select_AA_x,
                         xnon_connected_list_AA_x,                         
                         xamplifier,
                         "", "",
                         xactive_responses,
                         xnode_color_group,
                         xbimodalAmplifier, xplot_informal_network,
                         xplot_area_network_AA_x,
                         xmainAInDegreePlot, 
                         xmainAOutDegreePlot,
                         xmainAEigenvectorPlot, 
                         xmainABetweennessPlot,
                         xdata_table_nodeDF,
                         xall_any_filter_group_active,
                         xparameters_for_business_component_selection_dict,
                         xgraph2, xgraph3,
                         xtable_inverse_responder_ego, 
                         xtable_responder_ego,
                         xcommunity_color_selector,
                         xdata_table_community_participants,
                         xplot_quotient_informal_network,
                         xsub_plot_informal_network,
                         xcommunity_color_selector2,
                         xdata_table_community_participants2,
                         xplot_quotient_organization_area,
                         xsub_plot_informal_network2,
                         xplot_core, xselect_core_degree,
                         xdata_table_ModeloCompleto)
    
    
    # print('Vuelve de FD_Update_AA_Network2 (FD_Cambio_corte2)')
    
    # print('recién len(_complete_nx_graph.edges()) (FD_Cambio_corte2)')
    # print(len(_complete_nx_graph.edges()))
    
    p_d_dict_employee = \
        xnetwork_parameters_dict.get('dict_employee')
    print('>>>>>>>>>>>>>p_d_dict_employee (FD_Cambio_corte2)')
    print(p_d_dict_employee)
    
    pd_connected_nodes_numeric = \
        xparameters_for_business_component_selection_dict.get\
            ('connected_nodes')
    pd_connected_nodes_numeric.sort()
    print('>>>>>>>>>>>>>pd_connected_nodes_numeric (FD_Cambio_corte2)')
    print(pd_connected_nodes_numeric)
    
    pd_connected_nodes = [p_d_dict_employee.get(node)[0] \
                          for node in pd_connected_nodes_numeric]
    print('>>>>>>>>>>>>>pd_connected_nodes (FD_Cambio_corte2)')
    print(pd_connected_nodes)
    
    # pd_connected_nodes = \
    #     xparameters_for_business_component_selection_dict.get\
    #         ('connected_nodes')
    
    # print('DDDDDDDDDDDespues')
    # print(len(xparameters_for_business_component_selection_dict.get\
    #     ('connected_nodes')))
    # print(len(pd_connected_nodes))
    
    # print('s antes')
    # print(len(xexcluded_select.options))
    
    # print('Va a cambiar a') 
    # print([pd_connected_nodes[0]])       
    
    #
    selected_filtered_node = pd_connected_nodes[0]
    pd_connected_nodes.sort()
    print('>>>>>>>>>>>>>pd_connected_nodes[pd_connected_nodes.index(selected_filtered_node)] (FD_Cambio_corte2)')
    print(pd_connected_nodes[pd_connected_nodes.index(selected_filtered_node)])
    xexcluded_select.value = \
        [pd_connected_nodes[pd_connected_nodes.index(selected_filtered_node)]]
    xexcluded_select.options = pd_connected_nodes
    
    
    # print('s despues')
    # print(xexcluded_select.value)
    # print(len(xexcluded_select.options))
    
    FD_update_community_selector(xcommunity_attribute, _complete_nx_graph,
                                     xdata_table_community_participants,
                                     xcommunity_color_selector)
    
    #OOJJOO
    # _communities, _communitiesColor, inter_community_flag = \
    #     FD_Communities_analyzer(xcommunity_attribute, _complete_nx_graph)
    # # print('>>>>>>>>>>>>> _communities (FD_Cambio_corte2)')
    # # print(_communities)
    # # print('>>>>>>>>>>>>> _communitiesColor (FD_Cambio_corte2)')
    # # print(_communitiesColor)
    # # print('>>>>>>>>>>>>> inter_community_flag (FD_Cambio_corte2)')
    # # print(inter_community_flag)
    
    # communities_for_community_color_selector = \
    #     [(str(community), color) \
    #      for community, color in sorted(_communitiesColor) \
    #           if community != inter_community_flag]    
    # # print('>>>>>>>>>>>>> non_inter_communities (FD_Cambio_corte2)')
    # # print(non_inter_communities)
    
    # _df, _temp_actors_table = \
    #     FD_Community_participants(_communities[0], _complete_nx_graph, 
    #                               xcommunity_attribute)
    # xdata_table_community_participants.source.data = _df
    # # print('>>>>>>>>>>>>> _df (FD_Cambio_corte2)')
    # # print(_df)    
    
    # #As'i' estaba
    # xcommunity_color_selector.x_range.factors = \
    #     [str(community) for community, _ in \
    #      sorted(communities_for_community_color_selector)]
        
        
    
    # _new_ccs, _, _, _ = \
    #     FD_Community_selector(communities_for_community_color_selector,
    #                           '',  inter_community_flag)
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg')
    # # print(_new_ccs)
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg')
    # # print(_new_ccs.renderers[0])
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_xvalues')
    # # print(_new_xvalues)
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_colors')
    # # print(_new_colors)
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_xs')
    # # print(_new_xs)
    
    # csr = xcommunity_color_selector.renderers[0]
    # _csr_ds = _new_ccs.renderers[0].data_source
    # csr.data_source.data = dict(_csr_ds.data)
    
    # xcommunity_color_selector.renderers[0].data_source.selected.indices = [0]
    
    # # print('wwwwwwwwwwwwwwwwwwggggggggggggggg')
    # # print(csr.x_range_name)
    
    #OOJJOO
    # xcomplete_nx_graph = _complete_nx_graph
    
    # print('fin len(xcomplete_nx_graph.edges()) (FD_Cambio_corte2)')
    # print(len(xcomplete_nx_graph.edges()))
    
#%%

# def FD_change_all_any_filter_group(xconn, xnetwork_parameters_dict,
#                      xxfrequencyCorte, xxcheckedoptions, xactive_responses,
#                      xnode_color_group, xall_any_filter_group_active,
#                      xamplifier, xbimodalAmplifier,
#                     xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
#                     xsourceInteracción_AA_x, xmulti_select_AA_x,
#                     xnon_connected_list_AA_x, xplot_informal_network,
#                     xplot_area_network_AA_x,
#                     xcommunity_attribute,
#                     xnetwork,xxedges_dict,
#                     xxactors_data,
#                     xgravity_slider,
#                     xxcomplete_nx_graph,
#                     xmainAInDegreePlot, 
#                     xmainAOutDegreePlot,
#                     xmainAEigenvectorPlot, 
#                     xmainABetweennessPlot,
#                     xdata_table_nodeDF,
#                     xparameters_for_business_component_selection_dict,
#                     xexcluded_select,
#                     xgraph2, xgraph3,
#                     xtable_inverse_responder_ego, 
#                     xtable_responder_ego,
#                     xcommunity_color_selector,
#                     xdata_table_community_participants,
#                     xplot_quotient_informal_network,
#                     xsub_plot_informal_network,
#                     xcommunity_color_selector2,
#                     xdata_table_community_participants2,
#                     xplot_quotient_organization_area,
#                     xsub_plot_informal_network2,
#                     xplot_core, xselect_core_degree):
    
#     FD_update_network_parameters_dict(xnetwork_parameters_dict,
#                                           xall_any_filter_group_active)
    
    
    
#     FD_Cambio_corte2\
#         (xconn,xnetwork_parameters_dict,
#          # xnetwork_parameters_data_table,
#           "",
#          "",
#          xactive_responses,
#          xnode_color_group,
#          xall_any_filter_group_active,
#          xamplifier,xbimodalAmplifier,                                                 
#          xplot1_AA_x,xplot2_AA_x,xplot3_AA_x,
#          xsourceInteracción_AA_x, xmulti_select_AA_x,
#          xnon_connected_list_AA_x, xplot_informal_network,
#          xplot_area_network_AA_x,
#          xcommunity_attribute,
#          xnetwork,xxedges_dict,
#          xxactors_data,
#          xgravity_slider,
#          xxcomplete_nx_graph,
#          xmainAInDegreePlot, 
#          xmainAOutDegreePlot,
#          xmainAEigenvectorPlot, 
#          xmainABetweennessPlot,
#          xdata_table_nodeDF,
#          xparameters_for_business_component_selection_dict,
#          xexcluded_select,
#          xgraph2, xgraph3,
#          xtable_inverse_responder_ego, 
#          xtable_responder_ego,
#          xcommunity_color_selector,
#          xdata_table_community_participants,
#          xplot_quotient_informal_network,
#          xsub_plot_informal_network,
#          xcommunity_color_selector2,
#          xdata_table_community_participants2,
#          xplot_quotient_organization_area,
#          xsub_plot_informal_network2,
#          xplot_core, xselect_core_degree)
    
    
    
#%%

def FD_internalExternalDF(xareas,xactors,xedges):

    def ieMetrics(xinternalExternalDF,xarea,xedges):
        filteredInternalExternalDF = \
            xinternalExternalDF.loc[xinternalExternalDF.Area==xarea]
        filteredInternalExternalDF.reset_index(level=0, inplace=True)
        filteredInternalExternalDF.rename(columns={'index':'funcionarioIndex'},
                                          inplace=True)
        rows=filteredInternalExternalDF['funcionarioIndex'].to_numpy()[:,None]
        columns=range(0,xedges.shape[1])
        
        inEdges=np.sum(xedges[rows,columns])
        outEdges=np.sum(np.transpose(xedges)[rows,columns])
        count=filteredInternalExternalDF.shape[0]
    
        return xarea,count, inEdges, outEdges
    
    internalExternalDF=pd.DataFrame({'Area':xareas,'Funcionario':xactors})
    
    areasList=list(set(xareas))
    
    
    ieEdges=[ieMetrics(internalExternalDF,area,xedges) for area in areasList]
    ieEdgesDF=pd.DataFrame(np.array(ieEdges))
    ieEdgesDF=pd.DataFrame(np.array(ieEdges),columns=['Area','Funcionarios','In',
                                                  'Out'])

    
    source_ieEdgesDF = ColumnDataSource(ieEdgesDF)
    
    columns_ie_EdgesDF = [TableColumn(field=Ci, title=Ci) \
                          for Ci in ieEdgesDF.columns]
    
    data_table_ieEdgesDF = DataTable(source = source_ieEdgesDF,
                                     columns = columns_ie_EdgesDF,
                                     width = 1400, height = 600)
    
    return data_table_ieEdgesDF


def FD_update_community_selector(xcommunity_attribute, x_complete_nx_graph,
                                 xdata_table_community_participants,
                                 xcommunity_color_selector):
    
    """
    Updates communities' selector after valid responses are updated
    """
    
    _communities, _communitiesColor, inter_community_flag = \
        FD_Communities_analyzer(xcommunity_attribute, x_complete_nx_graph)
    # print('>>>>>>>>>>>>> _communities (FD_update_community_selector)')
    # print(_communities)
    # print('>>>>>>>>>>>>> _communitiesColor (FD_update_community_selector)')
    # print(_communitiesColor)
    # print('>>>>>>>>>>>>> inter_community_flag (FD_update_community_selector)')
    # print(inter_community_flag)
    
    communities_for_community_color_selector = \
        [(str(community), color) \
         for community, color in sorted(_communitiesColor) \
              if community != inter_community_flag]    
    # print('>>>>>>>>>>>>> non_inter_communities (FD_update_community_selector)')
    # print(non_inter_communities)
    
    _df, _temp_actors_table = \
        FD_Community_participants(_communities[0], x_complete_nx_graph, 
                                  xcommunity_attribute)
    xdata_table_community_participants.source.data = _df
    # print('>>>>>>>>>>>>> _df (FD_update_community_selector)')
    # print(_df)    
    
    #As'i' estaba
    xcommunity_color_selector.x_range.factors = \
        [str(community) for community, _ in \
         sorted(communities_for_community_color_selector)]        
    
    _new_ccs, _, _, _ = \
        FD_Community_selector(communities_for_community_color_selector,
                              '',  inter_community_flag)
    # print('wwwwwwwwwwwwwwwwwwggggggggggggggg')
    # print(_new_ccs)
    # print('wwwwwwwwwwwwwwwwwwggggggggggggggg')
    # print(_new_ccs.renderers[0])
    # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_xvalues')
    # print(_new_xvalues)
    # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_colors')
    # print(_new_colors)
    # print('wwwwwwwwwwwwwwwwwwggggggggggggggg _new_xs')
    # print(_new_xs)
    
    csr = xcommunity_color_selector.renderers[0]
    _csr_ds = _new_ccs.renderers[0].data_source
    csr.data_source.data = dict(_csr_ds.data)
    
    xcommunity_color_selector.renderers[0].data_source.selected.indices = [0]
    

def FD_update_communities_display_objects(x_data_table_community_participants,
                                          xi_data_table_community_participants,
                                          xsub_plot_informal_network,
                                          _sub_plot_informal_network):
    
    """
    Updates communities' graphic components after filtering
    """
    print('.-.-.-.- finacGDB_AA_IRA_Utilities/FD_update_communities_display_objects')
    
    datasource = xi_data_table_community_participants.source.data
    x_data_table_community_participants.source.data = dict(datasource)
    # x_data_table_community_participants.source.data = \
    #     xi_data_table_community_participants
        
    xg1 = xsub_plot_informal_network.renderers[0]
    dsnrp1 = _sub_plot_informal_network.renderers[0].\
        node_renderer.data_source
    xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    dsnrp1g = _sub_plot_informal_network.renderers[0].\
        node_renderer.glyph
    xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
    
    # dshrpx = xsub_plot_informal_network.renderers[0].\
    #     edge_renderer.data_source
    # print('>>>>>>>>>>>>>>> dshrpx.data (FD_update_communities_display_objects)')
    # print(dshrpx.data)
    dshrp1 = _sub_plot_informal_network.renderers[0].\
        edge_renderer.data_source
    # print('>>>>>>>>>>>>>>> dshrp1.data (FD_update_communities_display_objects)')
    # print(dshrp1.data)
    xg1.edge_renderer.data_source.data = dict(dshrp1.data)
    #Parece que est sobra, según el ejemplo de abajo
    # dshrp1g = _sub_plot_informal_network.renderers[0].\
    #     edge_renderer.glyph
    # xg1.edge_renderer.glyph.line_color = dshrp1g.line_color
    
    #$$$$ ejemlo edges que sí funciona
    # dshrpH = iplot_informal_network.renderers[0].edge_renderer.data_source
    # xgH.edge_renderer.data_source.data = dict(dshrpH.data)
    
    # layout_graphH_AA=xgH.layout_provider
    # layout_graphH_AA.graph_layout = \
    #     dict(iplot_informal_network.renderers[0].layout_provider.graph_layout)
    #$$$$
    
    title_color_legend=xsub_plot_informal_network.renderers[1]
    new_title_color_legend=_sub_plot_informal_network.\
        renderers[1].data_source
    title_color_legend.data_source.data = \
        dict(new_title_color_legend.data)
    
    rectangles_color_legend = xsub_plot_informal_network.renderers[2]
    new_rectangles_color_legend = \
        _sub_plot_informal_network.renderers[2].data_source
    rectangles_color_legend.data_source.data = \
        dict(new_rectangles_color_legend.data)
    
    names_color_legend = xsub_plot_informal_network.renderers[3]
    new_names_color_legend = \
        _sub_plot_informal_network.renderers[3].data_source
    names_color_legend.data_source.data = dict(new_names_color_legend.data)
  
    
    layout_graph=xg1.layout_provider
    
    layout_graph.graph_layout = \
        dict(_sub_plot_informal_network.renderers[0].\
              layout_provider.graph_layout)

    

def FD_update_informal_subplot(selected,
                               xcommunity_color_selector,
                               xcommunity_attribute,
                               x_data_table_community_participants,
                               xmain_AA_plot, 
                               xnode_color_attribute,
                               xsub_plot_informal_network,
                               xcalculate_button):
    
    # xplot_communities,
    
    # return 0
    
    _main_AA_plot_graph = xmain_AA_plot.renderers[0]
    _complete_nx_graph = \
        UTBo_BokehGraphToNetworkxGraph(_main_AA_plot_graph,xDiGraph=True)
    
    
    """
    This function is executed when a different informal or area network
    is selected by the user(community_color_selector_source).
    
    input: - xnon_inter_communities - 
    """
    
    print('.-.-.-.-.-.-. finacGDB_AA_IRA_Utilities/FD_update_informal_subplot')
    # print('.-.-.-.-.-.-. finacGDB_AA_IRA_Utilities/FD_update_informal_subplot')
    # print('.-.-.-.-.-.-. finacGDB_AA_IRA_Utilities/FD_update_informal_subplot')
    # print('.-.-.-.-.-.-. finacGDB_AA_IRA_Utilities/FD_update_informal_subplot')
    # print('.-.-.-.-.-.-. finacGDB_AA_IRA_Utilities/FD_update_informal_subplot')
    
    if xcalculate_button.label == 'Calculando':
        # print ('No debo hacer nada')
        return 0
    else:
        print ('Ejecuto update')
    
    #OOJJOO
    # _complete_nx_graph = \
    #     UTBo_BokehGraphToNetworkxGraph(xplot_communities.renderers[0],
    #                                    xDiGraph=True)
    # print('>>>> xcomplete_nx_graph.edges(data=True) (FD_update_informal_subplot)')
    # print(xcomplete_nx_graph.get_edge_data('alfredo.castellanos', 
    #                                        'paola.florez', default=0))
    # print('>>>> xsub_plot_informal_network.edges(data=True) (FD_update_informal_subplot)')
    # print(xsub_plot_informal_network.get_edge_data('alfredo.castellanos', 
    #                                        'paola.florez', default=0))
    
    
    # print('inicio len(_complete_nx_graph.edges()) (FD_update_informal_subplot)')
    # print(len(_complete_nx_graph.edges()))
    
    # print('.-.-.-.-.-.-.-.- FD_update_informal_subplot')
    # print('>>>>>>>>>>>> old (FD_Communities_info_layout-callbak)')
    # print(old)
    # print('callback - _multi_actor_communities')
    # print(_multi_actor_communities)
    # print('_community_color_selector.x_range ((FD_update_informal_subplot)')
    # print(xcommunity_color_selector.x_range)
    community_color_selector_communities = \
        xcommunity_color_selector.x_range.factors
    # print('>>>>>>>>>>>> community_color_selector_communities (FD_update_informal_subplot)')
    # print(community_color_selector_communities)
    # print('_community_color_selector.renderers[0] ((FD_update_informal_subplot)')
    # print(xcommunity_color_selector.renderers[0])
    
    
    _new_community_participants_df, _temp_actors_table = \
        FD_Community_participants(community_color_selector_communities\
                                  [selected.indices[0]], 
                                  _complete_nx_graph, xcommunity_attribute)
    # print('>>>>>>>>>>>> _df (FD_Communities_info_layout-callbak)')
    # print(_df)
    
    #OOJJOO
    # x_data_table_community_participants.source.data = _df
    
    
    _sub_plot_informal_network = \
        FD_create_informal_network_plot(_complete_nx_graph, 
                                        community_color_selector_communities,
                                        xcommunity_attribute, 
                                        selected.indices[0],
                                        xnode_color_attribute)
        
    #OOJJOO
    # xg1 = xsub_plot_informal_network.renderers[0]
    # dsnrp1 = _sub_plot_informal_network.renderers[0].\
    #     node_renderer.data_source
    # xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    # dsnrp1g = _sub_plot_informal_network.renderers[0].\
    #     node_renderer.glyph
    # xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
    
    # dshrpx = xsub_plot_informal_network.renderers[0].\
    #     edge_renderer.data_source
    # print('>>>>>>>>>>>>>>> dshrpx.data (FD_update_informal_subplot)')
    # print(dshrpx.data)
    # dshrp1 = _sub_plot_informal_network.renderers[0].\
    #     edge_renderer.data_source
    # print('>>>>>>>>>>>>>>> dshrp1.data (FD_update_informal_subplot)')
    # print(dshrp1.data)
    # xg1.edge_renderer.data_source.data = dict(dshrp1.data)
    # #Parece que est sobra, según el ejemplo de abajo
    # # dshrp1g = _sub_plot_informal_network.renderers[0].\
    # #     edge_renderer.glyph
    # # xg1.edge_renderer.glyph.line_color = dshrp1g.line_color
    
    # #$$$$ ejemlo edges que sí funciona
    # # dshrpH = iplot_informal_network.renderers[0].edge_renderer.data_source
    # # xgH.edge_renderer.data_source.data = dict(dshrpH.data)
    
    # # layout_graphH_AA=xgH.layout_provider
    # # layout_graphH_AA.graph_layout = \
    # #     dict(iplot_informal_network.renderers[0].layout_provider.graph_layout)
    # #$$$$
    
    # title_color_legend=xsub_plot_informal_network.renderers[1]
    # new_title_color_legend=_sub_plot_informal_network.\
    #     renderers[1].data_source
    # title_color_legend.data_source.data = \
    #     dict(new_title_color_legend.data)
    
    # rectangles_color_legend = xsub_plot_informal_network.renderers[2]
    # new_rectangles_color_legend = \
    #     _sub_plot_informal_network.renderers[2].data_source
    # rectangles_color_legend.data_source.data = \
    #     dict(new_rectangles_color_legend.data)
    
    # names_color_legend = xsub_plot_informal_network.renderers[3]
    # new_names_color_legend = \
    #     _sub_plot_informal_network.renderers[3].data_source
    # names_color_legend.data_source.data = dict(new_names_color_legend.data)
  
    
    # layout_graph=xg1.layout_provider
    
    # layout_graph.graph_layout = \
    #     dict(_sub_plot_informal_network.renderers[0].\
    #           layout_provider.graph_layout)
    FD_update_communities_display_objects(x_data_table_community_participants,
                                              _temp_actors_table,
                                              xsub_plot_informal_network,
                                              _sub_plot_informal_network)
        

#%%
def FD_Unimodal_network(xconn, xglobal_questions_dict, 
                        xnetwork_parameters_dict, 
                        # xnetwork_parameters_data_table,
                        xxedges_dict, xxxxactors_data,
                        xbimodalAmplifier,
                        xamplifier = 40, 
                        xgravityLevel=1):
    
    
    """
    The main purposes of this function are:
        - creation of the following widgets:
            - gravity_slider (Slider): gravity intensity between nodes for 
                    display purposes. on_change executes: FD_Cambio_gravity
            - responses_button_group (CheckboxButtonGroup): selector for 
                        responses to include. 
                        on_change: visibilize_calculate_button            
            - calculate_button (Button): activates calculation.
                                        on_click: calculate_button_click
            - node_color_group (RadioGroup)
            - filter_group: all/any responses. on_change FD_Cambio_corte2
            - excluded_select (MultiSelect): select nodes to exclude.
                        on_change FD_businessComponentSelection
        - execution of FD_AA_model_main, that creates all the graphs 
            and tables displayed
    xdefiniciónTablaInteracción: texto explicación de como interpretar filas
                                 y columnas de matriz adyacente
    """
        
    print('.-.-.-.-.-.-.-.-. oihub_AA_IRA_Utilities/FD_Unimodal_network')
    print('>>>>>>>>>>>>>>>>>>>>>> xglobal_questions_dict.keys FD_Unimodal_network')
    print(xglobal_questions_dict.keys())
    print('>>>>>>>>>>>>>>>>>>>>>> xnetwork_parameters_dict.keys FD_Unimodal_network')
    print(xnetwork_parameters_dict.keys())
    # print('FD_Unimodal_network - xfrequencyResponseAccumulation')
    # print(xfrequencyResponseAccumulation)
    
    # pregunta = xnetwork_parameters_dict.get('pregunta')
    # preguntaCorta = xnetwork_parameters_dict.get('preguntaCorta')
    network = xnetwork_parameters_dict['network']
    # network = xnetwork_parameters_data_table.source.data['network'][0]
    language = xnetwork_parameters_dict['language']
    # language = xnetwork_parameters_data_table.source.data['language'][0]
    filter_group_active_initial = \
        xnetwork_parameters_dict['filter_group_active_initial']
    # filter_group_active = \
    #     xnetwork_parameters_data_table.source.data['filter_group_active'][0]
    filter_group_enabled = xnetwork_parameters_dict['filter_group_enabled']
    # print('>>>>>>>>>>>>>>>>>>>>>> filter_group_enabled (FD_Unimodal_network)')
    # print(filter_group_enabled)
    # filter_group_enabled = \
    #     xnetwork_parameters_data_table.source.data['filter_group_enabled'][0]
    p_d_node_size_attribute = \
        xnetwork_parameters_dict.get('node_size_attribute')
    # p_d_node_size_attribute = \
    #     xnetwork_parameters_data_table.source.data['node_size_attribute'][0]
    p_d_responder_direction = \
        xnetwork_parameters_dict.get('responder_direction')
    # p_d_responder_direction = \
    #     xnetwork_parameters_data_table.source.data['responder_direction'][0]
    
    possible_responses_components = \
        xnetwork_parameters_dict.get('possible_responses_components')
    frequencyCorte = xnetwork_parameters_dict.get('frecuenciaCorte')
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> frequencyCorte (FD_Unimodal_network)')
    # print(frequencyCorte)
    frequencyResponseAccumulation = \
        xnetwork_parameters_dict.get('frequencyResponseAccumulation') 
    # print('>>>>>>>>>>>>> frequencyResponseAccumulation (FD_Unimodal_network)')
    # print(frequencyResponseAccumulation)
    
    active_selected_possible_responses = \
        xnetwork_parameters_dict.get('active_selected_possible_responses')
    # selected_possible_responses = \
    #     xnetwork_parameters_dict.get('selected_possible_responses') 
    legends_dict = xnetwork_parameters_dict.get('legends_dict')
    # language = xnetwork_parameters_dict.get('language')
    # filter_group_active = xnetwork_parameters_dict.get('filter_group_active')
    # filter_group_enabled = \
    #     xnetwork_parameters_dict.get('filter_group_enabled')
    # p_d_node_size_attribute = \
    #     xnetwork_parameters_dict.get('node_size_attribute')
    # p_d_responder_direction = \
    #     xnetwork_parameters_dict.get('responder_direction')
        
    # print('>>>>>>>>> possible_responses_components (FD_Unimodal_network)')
    # print(possible_responses_components)
    # print('>>>>>>>>> active_selected_possible_responses (FD_Unimodal_network)')
    # print(active_selected_possible_responses)
        
    p_d_dict_employee = \
        xnetwork_parameters_dict.get('dict_employee')
    print('>>>>>>>>> p_d_dict_employee (FD_Unimodal_network)')
    print(p_d_dict_employee)
    
    p_d_inverse_question = xnetwork_parameters_dict['inverse_question']
    p_d_associated_questions = xnetwork_parameters_dict['associated_questions']
        
    
    # print('.-.-.-.-.-.-.-.-.-.- FD_Unimodal_Network')
    # print('>>>>>>>>>>>>> frequencyCorte (FD_Unimodal_Network)')
    # print(frequencyCorte)
    # print('>>>>>>>>>>>>> frequencyResponseAccumulation (FD_Unimodal_Network)')
    # print(frequencyResponseAccumulation)
    
    """
    gravity_slider
    """
    gravity_slider_title = UT_bring_legend('l-009', language, legends_dict)
    
    gravity_slider = Slider(start=1, end=10, value=1, step=1, 
                            title=gravity_slider_title)
    
    gravity_slider.on_change("value", lambda attr, old, new: \
                         FD_Cambio_gravity(gravity_slider.value,
                                           main_AA_plot))
    
    """
    responses_button_group
    """
    responses_button_group = \
        CheckboxButtonGroup(labels = possible_responses_components,
                            active=active_selected_possible_responses, 
                            width = 200)
        
    """
    calculate_button
    """
    calculate_button = Button(label="Presione para calcular", 
                              button_type="danger", width = 150,
                              visible = False)
    
    def reset_calculate_button_label():
        calculate_button.label = 'Inactivo'
        
    def launch_recalculate_network():
        if calculate_button.label == "Presione para calcular":
            calculate_button.label = 'Calculando'
            calculate_button.button_type="warning"
        curdoc().add_next_tick_callback(recalculate_network)
        curdoc().add_next_tick_callback(reset_calculate_button_label)
    
    def recalculate_network():
        if calculate_button.visible == True:
            calculate_button.visible = False
            FD_Cambio_corte2(xconn, xnetwork_parameters_dict,
                             # xnetwork_parameters_data_table,                              
                            "",
                            "",
                            responses_button_group.active,
                            node_color_group,
                            all_any_filter_group.active,
                            xamplifier,xbimodalAmplifier,                                                 
                            main_AA_plot,plot_inverse_responder_ego,
                            plot_responder_ego,
                            data_table_interacción,
                            excluded_select,
                            non_connected_list,
                            plot_informal_network, plot_area_network,
                            'informal_network',
                            network,XXXXedges_dict,
                            -1,
                            gravity_slider,
                            complete_nx_graph,
                            mainAInDegreePlot, 
                            mainAOutDegreePlot,
                            mainAEigenvectorPlot, 
                            mainABetweennessPlot,
                            data_table_nodeDF,
                            parameters_for_business_component_selection_dict,
                            excluded_select,
                            graph_inverse_responder_ego, 
                            graph_responder_ego,
                            table_inverse_responder_ego, 
                            table_responder_ego,
                            _community_color_selector,
                            _data_table_community_participants,
                            plot_quotient_informal_network,
                            _sub_plot_informal_network,
                            _community_color_selector2,
                            _data_table_community_participants2,
                            plot_quotient_organization_area,
                            _sub_plot_informal_network2,
                            plot_core, select_core_degree,
                            data_table_ModeloCompleto)
        
    # calculate_button.on_click(calculate_button_click)
    calculate_button.on_click(launch_recalculate_network)
    
    def visibilize_calculate_button(xcalculate_button):
        calculate_button.label = "Presione para calcular"
        calculate_button.button_type="danger"
        calculate_button.visible = True
        
    responses_button_group.on_change("active", lambda attr, old, new: \
                                     visibilize_calculate_button\
                                         (calculate_button)) 
    
        
    
    """
    node_color_group: selector para el color de los nodos
    """
    # 'l-007':['Color del nodo: Departamento','Node color: Department'],
    option1 = UT_bring_legend('l-007', language, legends_dict)
    # 'l-008':['Color del nodo: Grupo cultura', 'Node color: Culture cluster'],
    option2 = UT_bring_legend('l-008', language, legends_dict)
    LABELS = [option1, option2]
    
    # print('>>>>>>>>> LABELS (FD_Unimodal_network)')
    # print(LABELS)
    
    node_color_group = RadioGroup(labels=LABELS, active=0)
    
    node_color_group.on_change("active", lambda attr, old, new: \
                                 FD_Cambio_corte2\
                                     (xconn, xnetwork_parameters_dict,
                                      # xnetwork_parameters_data_table,
                                     "",
                                    "",
                                    responses_button_group.active,
                                    node_color_group,
                                    all_any_filter_group.active,
                                    xamplifier,xbimodalAmplifier,                                                 
                                    main_AA_plot,plot_inverse_responder_ego,
                                    plot_responder_ego,
                                    data_table_interacción,
                                    excluded_select,
                                    non_connected_list,
                                    plot_informal_network, plot_area_network,
                                    'informal_network',
                                    network,XXXXedges_dict,
                                    -1,
                                    gravity_slider,
                                    complete_nx_graph,
                                    mainAInDegreePlot, 
                                    mainAOutDegreePlot,
                                    mainAEigenvectorPlot, 
                                    mainABetweennessPlot,
                                    data_table_nodeDF,
                                    parameters_for_business_component_selection_dict,
                                    excluded_select,
                                    graph_inverse_responder_ego, 
                                    graph_responder_ego,
                                    table_inverse_responder_ego, 
                                    table_responder_ego,
                                    _community_color_selector,
                                    _data_table_community_participants,
                                    plot_quotient_informal_network,
                                    _sub_plot_informal_network,
                                    _community_color_selector2,
                                    _data_table_community_participants2,
                                    plot_quotient_organization_area,
                                    _sub_plot_informal_network2,
                                    plot_core, select_core_degree,
                                    data_table_ModeloCompleto))
    
    """
    all_any_filter_group: selector para todos / cualquiera
    #es útil para los que tienen posibles más de una respuesta
    """
    option1 = UT_bring_legend('l-022', language, legends_dict)
    option2 = UT_bring_legend('l-023', language, legends_dict)
    # _title = UT_bring_legend('l-024', language, legends_dict)
    LABELS = [option1, option2]
    all_any_filter_group = RadioGroup(labels=LABELS, 
                                      active = filter_group_active_initial)
    
    all_any_filter_group.on_change("active", lambda attr, old, new: \
                                 FD_Cambio_corte2\
                                     (xconn,xnetwork_parameters_dict,
                                      # xnetwork_parameters_data_table,
                                       "",
                                      "",
                                      responses_button_group.active,
                                      node_color_group,
                                      all_any_filter_group.active,
                                      xamplifier,xbimodalAmplifier,                                                 
                                      main_AA_plot,plot_inverse_responder_ego,
                                      plot_responder_ego,
                                      data_table_interacción,
                                      excluded_select,
                                      non_connected_list,
                                      plot_informal_network, plot_area_network,
                                      'informal_network',
                                      network,XXXXedges_dict,
                                      -1,
                                      gravity_slider,
                                      complete_nx_graph,
                                      mainAInDegreePlot, 
                                      mainAOutDegreePlot,
                                      mainAEigenvectorPlot, 
                                      mainABetweennessPlot,
                                      data_table_nodeDF,
                                      parameters_for_business_component_selection_dict,
                                      excluded_select,
                                      graph_inverse_responder_ego, 
                                      graph_responder_ego,
                                      table_inverse_responder_ego, 
                                      table_responder_ego,
                                      _community_color_selector,
                                      _data_table_community_participants,
                                      plot_quotient_informal_network,
                                      _sub_plot_informal_network,
                                      _community_color_selector2,
                                      _data_table_community_participants2,
                                      plot_quotient_organization_area,
                                      _sub_plot_informal_network2,
                                      plot_core, select_core_degree,
                                      data_table_ModeloCompleto))
    
                                    
    XXXXedges_AA = 'uuyu'
    XXXXedges_dict = 'hjhjhj'
    
    # print('>>>>>>>>>>>>>>>>>>>><  FD_Unimodal_Network')
    # print(xnetwork)
    # print(edges_AA)
    
    """
    dowwnload_centralities_button
    """
    download_centralities_button = Button(label="Presione para descargar", 
                                          button_type="danger", width = 150,
                              visible = True)
    
    
    """
    main_AA_plot
    parameters_for_business_component_selection_dict
    plot_inverse_responder_ego
    plot_responder_ego
    tabTablaInteracción
    data_table_ModeloCompleto
    tabModelo_filtrado
    tabTablaDelta
    main_AA_bokeh_graph
    data_table_interacción
    mainAInDegreePlot
    mainAOutDegreePlot
    mainAEigenvectorPlot
    mainABetweennessPlot
    data_table_nodeDF
    plot_informal_network
    non_connected_list
    plot_area_network
    plot_quotient_informal_network
    plot_quotient_organization_area
    complete_nx_graph
    graph_inverse_responder_ego
    graph_responder_ego
    selectedImposedBokehGraph
    layout_main_AA_bokeh_graph
    table_inverse_responder_ego
    table_responder_ego
    
    NO:
    x_densityG1
    x_densityG2
    x_filas
    x_columnas
    x_links
    x_centralization
    x_dirección
    x_número_conexiones_componentes_eliminados
    x_communities
    x_informal_network_palette_dict
    x_core_layout
    x_plot_core    
    """
    main_AA_plot, parameters_for_business_component_selection_dict, \
        plot_inverse_responder_ego, plot_responder_ego, \
            tabTablaInteracción, data_table_ModeloCompleto, \
        tabModelo_filtrado, tabTablaDelta, x_densityG1, x_densityG2, x_filas, x_columnas,\
            x_links, \
        x_centralization, main_AA_bokeh_graph, data_table_interacción, \
        x_dirección, x_número_conexiones_componentes_eliminados, \
        mainAInDegreePlot, mainAOutDegreePlot,\
            mainAEigenvectorPlot, mainABetweennessPlot, \
                data_table_nodeDF, plot_informal_network, \
                non_connected_list, x_communities,\
                    x_informal_network_palette_dict, \
                    plot_area_network,\
                    plot_quotient_informal_network, \
                    plot_quotient_organization_area, \
                        x_core_layout, x_plot_core,\
                    complete_nx_graph,\
                        graph_inverse_responder_ego, \
                            graph_responder_ego,\
                            selectedImposedBokehGraph,\
                                layout_main_AA_bokeh_graph, \
                                    table_inverse_responder_ego,\
                                        table_responder_ego = \
                    FD_AA_model_main(xconn,xnetwork_parameters_dict, 
                                     # xnetwork_parameters_data_table,
                                            -1, XXXXedges_AA, 
                                            xamplifier, frequencyCorte, 
                            frequencyResponseAccumulation,
                            active_selected_possible_responses,
                            all_any_filter_group.active,
                            xgravityLevel=xgravityLevel)
                    
    tabModelo_completo = TabPanel(child=data_table_ModeloCompleto, 
                                  title="Modelo completo")

    #tabla de centralidades por usuario
    centralities_DF = \
        pd.DataFrame.from_dict(data_table_ModeloCompleto.source.data)
    
    # print('EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('>>>>>>>>>>>>> complete_nx_graph_bokeh_object (FD_Unimodal_network)')
    # print(complete_nx_graph_bokeh_object)
    # print('>>>>>>>>>> complete_nx_graph_bokeh_object.source (FD_Unimodal_network)')
    # print(complete_nx_graph_bokeh_object.source)
    # print('>>>>>>>>>> complete_nx_graph_bokeh_object.source.data (FD_Unimodal_network)')
    # print(complete_nx_graph_bokeh_object.source.data)
    # print('>>>>>>>>>> dict(complete_nx_graph_bokeh_object.source.data) (FD_Unimodal_network)')
    # print(dict(complete_nx_graph_bokeh_object.source.data))
    
    # _plot1Graph=main_AA_plot.renderers[0]
    
    # _G=UTBo_BokehGraphToNetworkxGraph(_plot1Graph,xDiGraph=True)
    # print("$$$$$$$$$$$$$ _G.nodes")
    # print(_G.nodes(data=True))
    # print("$$$$$$$$$$$$$ _G.edges")
    # print(_G.edges(data=True))
    
    # print('fin EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('fin EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('fin EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('fin EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # print('fin EENNSSAAYYOO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    
    def launch_download_centralities():
        print('dlc')
        
        selected_centralities_DF = \
            centralities_DF[['employee','in_degree_centrality',
                             'out_degree_centrality', 'betweenness_centrality',
                             'eigenvector_centrality']].copy(deep=True)        
        
        selected_centralities_DF.rename(columns={'employee':'Individual',
                                        'in_degree_centrality':
                                            'In-degree centrality',
                                        'out_degree_centrality':
                                            'Out-degree centrality',
                                        'betweenness_centrality':
                                            'Betweenness centrality', 
                                        'eigenvector_centrality':
                                            'Eigenvector centrality'},
                              inplace=True)
        
        selected_centralities_DF.to_csv('oihub_centralities.csv', 
                                        sep=',', encoding='utf-8',
                                        index=False)
                    
    download_centralities_button.on_click(launch_download_centralities)
    
    # print('>>>>> p_d_dict_employee (FD_Unimodal_network)')
    # print(p_d_dict_employee)
    
    
    pd_connected_nodes_numeric = \
        parameters_for_business_component_selection_dict.get('connected_nodes')
    pd_connected_nodes_numeric.sort()
    # print('>>>>> pd_connected_nodes_numeric (FD_Unimodal_network)')
    # print(pd_connected_nodes_numeric)
    
    pd_connected_nodes = [p_d_dict_employee.get(node)[0] \
                          for node in pd_connected_nodes_numeric]
    selected_filtered_node = pd_connected_nodes[0]
    pd_connected_nodes.sort()
    # print('>>>>> pd_connected_nodes (oihub_AA_IRA_Utilities/FD_Unimodal_network)')
    # print(pd_connected_nodes)
    
    selected_filtered_node_index = \
        pd_connected_nodes.index(selected_filtered_node)
    # print('>>>>> selected_filtered_node_index (oihub_AA_IRA_Utilities/FD_Unimodal_network)')
    # print(selected_filtered_node_index)
    
    excluded_select = MultiSelect(title="Componentes a filtrar:",
                   value=[pd_connected_nodes[selected_filtered_node_index]],
                   options=pd_connected_nodes,
                   height=300, width=200)

    excluded_select.on_change("value", lambda attr, old, new:
                           FD_businessComponentSelection\
                               (excluded_select,
                                xnetwork_parameters_dict,
                                parameters_for_business_component_selection_dict,
                                complete_nx_graph, main_AA_plot, 
                                plot_inverse_responder_ego,
                                plot_responder_ego, 
                                p_d_node_size_attribute,
                                main_AA_bokeh_graph, graph_inverse_responder_ego,
                                graph_responder_ego, 
                                selectedImposedBokehGraph,
                                layout_main_AA_bokeh_graph,
                                p_d_responder_direction,
                                table_inverse_responder_ego,
                                table_responder_ego))

                    
    # print('>>>>>> complete_nx_graph.nodes(data=True) (FD_Unimodal_Network))')
    # print(complete_nx_graph.nodes(data=True))
    # print('>>>>>> complete_nx_graph.edges(data=True) (FD_Unimodal_Network))')
    # print(complete_nx_graph.edges(data=True))
                    

    #Esto se debe trasladar
    # métricas_area = FD_internalExternalDF(areas, actors, edges_AA)
    # tabAA_area = Panel(child=métricas_area, title='Area')
    
    # preguntaEncabezado = Div(text = pregunta, width=500, height=25)
    
    # encabezado = column(UTBo_EmptyParagraph(50,5),preguntaEncabezado,
    #                     UTBo_EmptyParagraph(50,5))
    
    #.-.-.-Este cambio se hizo para partir en dos tabs todos y funcionario filtrado
    
    # 'l-012':['Toda la red','Entire network'],
    legend_012 = UT_bring_legend('l-012', language, legends_dict)
    legend_013 = UT_bring_legend('l-013', language, legends_dict)
    legend_014 = UT_bring_legend('l-014', language, legends_dict)
    legend_015 = UT_bring_legend('l-015', language, legends_dict)
    # 'l-016':['Redes informales','Informal networks'],
    legend_016 = UT_bring_legend('l-016', language, legends_dict)
    # 'l-017':['Areas','Areas'],
    legend_017 = UT_bring_legend('l-017', language, legends_dict)
    # 'l-018':['Centro','Core'],
    legend_018 = UT_bring_legend('l-018', language, legends_dict)
    # 'l-019':['Comunidades','Communities'],
    legend_019 = UT_bring_legend('l-019', language, legends_dict)
    # 'l-020':['Funcionario','Employee']
    legend_020 = UT_bring_legend('l-020', language, legends_dict)
    legend_025 = UT_bring_legend('l-025', language, legends_dict)
    legend_026 = UT_bring_legend('l-026', language, legends_dict)
    legend_027 = UT_bring_legend('l-027', language, legends_dict)
    legend_028 = UT_bring_legend('l-028', language, legends_dict)
    
    #.-.-.-.-.-.-.-.-.-.-.- question menu
    questions_title = UT_bring_legend('l-030', language, legends_dict)
    selected_question_title = UT_bring_legend('l-031', language, legends_dict)
                
    questions_menu, selected_question, menu_questions_list, questions_df, \
        help_tabs_global, help_texts_tuple = \
        FD_questions_AA_main(xconn, xnetwork_parameters_dict, questions_title, 
                             selected_question_title)
        
    # print('>>>>>>>>>>>>>>>> help_texts_tuple (FD_Unimodal_network)')
    # print(help_texts_tuple)
    
    # 'l-012':['Toda la red','Entire network'],
    panel_todos = \
        TabPanel(child=row(main_AA_plot,
                           column(excluded_select,non_connected_list),
                           UTBo_EmptyParagraph(20,20),
                           help_tabs_global),
                 title=legend_012)
    
    plot_ego_responder = TabPanel(child=row(plot_responder_ego), 
                                  title=legend_027)
    table_ego = TabPanel(child=row(table_responder_ego),
                         title=legend_028)
    tab_plot_ego_responder = Tabs(tabs=[plot_ego_responder, table_ego])
    panel_ego_responder = TabPanel(child=tab_plot_ego_responder,
                                   title=legend_025)
    tab_ego_responder = Tabs(tabs=[panel_ego_responder])
    
    plot_ego_inverse = TabPanel(child=row(plot_inverse_responder_ego),
                                title=legend_027)
    table_ego_inverse = TabPanel(child=row(table_inverse_responder_ego),
                                 title=legend_028)
    tab_plot_ego_inverse = Tabs(tabs=[plot_ego_inverse, table_ego_inverse])
    panel_ego_inverse = TabPanel(child=tab_plot_ego_inverse, title=legend_026)
    tab_ego_inverse = Tabs(tabs=[panel_ego_inverse])
    
    plot_funcionario_filtrado=row(tab_ego_responder,tab_ego_inverse)
    # plot_funcionario_filtrado=row(plot2,plot3)
    panel_funcionario_filtrado = TabPanel(child=plot_funcionario_filtrado,
                                          title=legend_013)
    

            # FD_Communities_info(plot_area_network.renderers[0], 
    _community_color_selector, _data_table_community_participants, \
        _sub_plot_informal_network = \
            FD_Communities_info('informal_network', legend_014,
                                'organization_area_color', complete_nx_graph)
            
    community_color_selector_source = \
        _community_color_selector.renderers[0].data_source
    
    community_color_selector_source.\
        selected.on_change('indices', lambda attr, old, new: \
                            FD_update_informal_subplot\
                                (community_color_selector_source.selected,
                                  _community_color_selector,
                                  'informal_network',
                                  _data_table_community_participants,
                                  main_AA_plot, 
                                  'organization_area_color',
                                  _sub_plot_informal_network,
                                  calculate_button))
            
    # plot_informal_network,
        
    
    _communities_info_layout = \
        FD_Communities_info_layout(_community_color_selector,
                                   _data_table_community_participants,
                                   plot_quotient_informal_network, 
                                   _sub_plot_informal_network)
    

            # FD_Communities_info(plot_area_network.renderers[0], 
    _community_color_selector2, _data_table_community_participants2, \
        _sub_plot_informal_network2 = \
            FD_Communities_info('organization_area', legend_015, 
                                'informal_network_color',
                                complete_nx_graph)
            #plot_quotient_organization_area, 
            #_plotQuotient2, 
            
    community_color_selector_source2 = \
        _community_color_selector2.renderers[0].data_source
    
    community_color_selector_source2.\
        selected.on_change('indices', lambda attr, old, new: \
                            FD_update_informal_subplot\
                                (community_color_selector_source2.selected,
                                  _community_color_selector2,
                                  'organization_area',
                                  _data_table_community_participants2,
                                  main_AA_plot, 
                                  'informal_network_color',
                                  _sub_plot_informal_network2,
                                  calculate_button))
            
    # plot_area_network,
    # a=5/0
        
    _communities_info_layout2 = \
        FD_Communities_info_layout(_community_color_selector2,
                                   _data_table_community_participants2,
                                   plot_quotient_organization_area, 
                                   _sub_plot_informal_network2)
        
    """
    Core
    """
    plot_core, nucleo_data_table, borde_data_table, corteza_data_table,\
        coreDegree = FD_Core_objects(complete_nx_graph)
    core_layout, select_core_degree = \
        FD_Core_layout(complete_nx_graph, plot_core, nucleo_data_table, 
                       borde_data_table, corteza_data_table, coreDegree)
    
    
    # 'l-016':['Redes informales','Informal networks'],
    panel_redes_informales = TabPanel(child=row(plot_informal_network,
                                                _communities_info_layout),
                                      title=legend_016)
    # 'l-017':['Areas','Areas'],
    panel_areas = TabPanel(child=row(plot_area_network,
                                     _communities_info_layout2),
                           title=legend_017)
    # 'l-018':['Centro','Core'],
    panel_core = TabPanel(child=row(core_layout), title=legend_018)
    tabComunidades = Tabs(tabs=[panel_redes_informales, panel_areas,
                                panel_core])
    
    # 'l-019':['Comunidades','Communities'],
    panel_comunidades = TabPanel(child=tabComunidades,title=legend_019)
    tabFuncionarios = Tabs(tabs=[panel_todos, panel_funcionario_filtrado,
                                 panel_comunidades])
    
    tabAA_resultados_funcionario=\
        column(tabFuncionarios,
               download_centralities_button,
               Tabs(tabs=[tabTablaInteracción, tabModelo_completo,
                          tabModelo_filtrado, tabTablaDelta]))
    # 'l-020':['Funcionario','Employee']
    tabAA_funcionario = TabPanel(child=tabAA_resultados_funcionario,
                                 title=legend_020)
    
    
    if filter_group_enabled == True:
        all_any_filter_group.visible = True
    else:
        all_any_filter_group.visible = False
    radio_buttons_column = column(node_color_group,
                                      UTBo_EmptyParagraph(20,20),
                                      all_any_filter_group)
    
    #.-.-.-.-.-.-.-.- controles para pregunta inversa
    """
    all_any_filter_group: selector para todos / cualquiera
    #es útil para los que tienen posibles más de una respuesta
    """
    only_option = UT_bring_legend('l-035', language, legends_dict)
    inverse_question_label = [only_option]
    inverse_question_checkbox_group =\
        CheckboxGroup(labels = inverse_question_label, active=[])
    
    if p_d_inverse_question is None:
        inverse_question_checkbox_group.visible = False
    else:
        inverse_question_checkbox_group.visible = True
    #:_:_:_:_:_:_:_:_ fin controles para pregunta inversa  
        
    
        
    questions_menu_source = questions_menu.renderers[0].data_source
    
        
    questions_menu_source.selected.on_change('indices', lambda attr, old, new: \
                            FD_question_update(xconn, questions_menu, 
                                               selected_question,
                                               menu_questions_list, 
                                               questions_df,
                                               xglobal_questions_dict,
                                               xnetwork_parameters_dict,
                                                # xnetwork_parameters_data_table,
                                                 "",
                                                "",
                                                responses_button_group,
                                                node_color_group,
                                                all_any_filter_group,
                                                xamplifier,xbimodalAmplifier,                                                 
                                                main_AA_plot,plot_inverse_responder_ego,
                                                plot_responder_ego,
                                                data_table_interacción,
                                                excluded_select,
                                                non_connected_list,
                                                plot_informal_network, plot_area_network,
                                                'informal_network',
                                                network,XXXXedges_dict,
                                                -1,
                                                gravity_slider,
                                                complete_nx_graph,
                                                mainAInDegreePlot, 
                                                mainAOutDegreePlot,
                                                mainAEigenvectorPlot, 
                                                mainABetweennessPlot,
                                                data_table_nodeDF,
                                                parameters_for_business_component_selection_dict,
                                                excluded_select,
                                                graph_inverse_responder_ego, 
                                                graph_responder_ego,
                                                table_inverse_responder_ego, 
                                                table_responder_ego,
                                                _community_color_selector,
                                                _data_table_community_participants,
                                                plot_quotient_informal_network,
                                                _sub_plot_informal_network,
                                                _community_color_selector2,
                                                _data_table_community_participants2,
                                                plot_quotient_organization_area,
                                                _sub_plot_informal_network2,
                                                plot_core, select_core_degree,
                                                help_texts_tuple,
                                                data_table_ModeloCompleto,
                                                inverse_question_checkbox_group))
        
    # tabAA_encabezado=column(UTBo_EmptyParagraph(50,5),
    #                         selected_question,
    tabNetworkAA=column(UTBo_EmptyParagraph(50,5),
                            row(UTBo_EmptyParagraph(100,5),
                                gravity_slider,
                                UTBo_EmptyParagraph(100,5),
                                column(radio_buttons_column,
                                       inverse_question_checkbox_group)),
                            responses_button_group,
                            calculate_button,
                            UTBo_EmptyParagraph(50,5),
                            Tabs(tabs=[tabAA_funcionario]))
    
    return tabNetworkAA, mainAInDegreePlot, mainAOutDegreePlot,\
        mainAEigenvectorPlot, mainABetweennessPlot, \
            data_table_nodeDF, questions_menu, selected_question
            
    # return tabAA_encabezado, densityG1, densityG2, filas, columnas, links, \
    #     centralization,\
    #     main_AA_plot, excluded_select, plot_inverse_responder_ego, \
    #         plot_responder_ego, \
    #     tabTablaInteracción, \
    #         tabModelo_completo, \
    #     tabModelo_filtrado, tabTablaDelta, main_AA_bokeh_graph, \
    #         data_table_interacción, \
    #         dirección,número_conexiones_componentes_eliminados, \
    #                 mainAInDegreePlot, mainAOutDegreePlot,\
    #                     mainAEigenvectorPlot, mainABetweennessPlot,\
    #                         data_table_nodeDF, non_connected_list, \
    #                             plot_informal_network
