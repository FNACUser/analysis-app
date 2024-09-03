# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 18:20:28 2023

@author: luis.caro
"""

import pandas as pd

# from neo4j_learn_ONA import conn

# from bokeh.models import (Tabs, Panel, CheckboxGroup, RadioButtonGroup)
from bokeh.layouts import row, column

from .oihub_AA_IRA_Utilities import FD_Unimodal_network

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph



#%%

# from Utilities import UT_CountOcurrences

# query =  """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-
# (e:Employee)<-[OF_EMPLOYEE]-(aif:Adjacency_input_form)-[OF_CYCLE]->
# (cy:Cycle{id_cycle:2})
# MATCH (aif)-[OF_NETWORK_MODE]->(nwm:Network_mode)-[IS_OF_THEME]->
# (nwmt:Network_mode_theme{network_mode_theme:'Trabajo'})
# RETURN e.employee, e.redmine_login, e.organization_area
# """
# result = conn.query(query) #, parameters=params)

# actors_data = pd.DataFrame([dict(_) for _ in result])
# actors_data.rename(columns={'e.employee': 'actor',
#                             'e.redmine_login': 'usuarioRedmine',
#                             'e.organization_area': 'area'}, inplace=True)
# print('>>>>>>>>>>>>>>>>> actors_data (FD_Unimodal_Network_Framework)')
# print(actors_data)
# print(actors_data.columns)

# UT_CountOcurrences(actors_data, 'area')

# groups = actors_data.groupby('area')['actor'].apply(list)
# groups



def FD_Unimodal_Network_Framework(xconn,xglobal_questions_dict, 
                                  xnetwork_parameters_dict, 
                                  # xnetwork_parameters_data_table,
                                  xdirMutabisFinac, xbimodalAmplifier, 
                                  _xamplifier):
    
    print('.-.-.finacGDB_AA_IRA_UnimodalFramework/FD_Unimodal_Network_Framework')
    # xedges_dict, xactors_data = FD_Edges_to_dictionary() 
    cycle = xnetwork_parameters_dict['cycle']
    # cycle = xnetwork_parameters_data_table.source.data['cycle'][0]
    # print('>>>>>>>>>>>>>>>>> cycle (FD_Unimodal_Network_Framework)')
    # print(cycle)
    network_mode_theme = xnetwork_parameters_dict['network_mode_theme']
    # network_mode_theme = \
    #     xnetwork_parameters_data_table.source.data['network_mode_theme'][0]
    # print('>>>>>>>>>>>>>>>>> network_mode_theme (FD_Unimodal_Network_Framework)')
    # print(network_mode_theme)
    
    
    #.-.-.-.-.-.-.-.-.-.-.-.- Neo4j
    #.-.-.-.-.-.-.-.-.-.-.-.- Neo4j
    #.-.-.-.-.-.-.-.-.-.-.-.- Neo4j
    #.-.-.-.-.-.-.-.-.-.-.-.- Neo4j
    # query =  """MATCH (e:Employee)
    #             WHERE NOT e.redmine_user = 'daniela.bonilla'
    #             AND NOT e.redmine_user = 'lorena.sarmiento' 
    #             AND NOT e.redmine_user = 'luisa.maldonado'
    #             AND NOT e.redmine_user = 'manuel.pachon'
    #             AND NOT e.redmine_user = 'ross.saenz' 
    #             AND NOT e.redmine_user = 'william.gutierrez'
    #             RETURN e.employee, e.redmine_user, e.organization_area
    # """
    query0 =  """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-
    (e:Employee)<-[OF_EMPLOYEE]-(aif:Adjacency_input_form)-[OF_CYCLE]->
    (cy:Cycle{id_cycle:"""
    query1 = str(cycle)
    query2="""})
    MATCH (aif)-[OF_NETWORK_MODE]->(nwm:Network_mode)-[IS_OF_THEME]->
    (nwmt:Network_mode_theme{network_mode_theme:'""" 
    query3 =  network_mode_theme
    query4="""'})
    RETURN e.employee, e.redmine_login, e.organization_area
    UNION
    MATCH (aif)<-[OF_FORM]-(r:Response)-[RELATED_TO]->(e:Employee)
    RETURN e.employee, e.redmine_login, e.organization_area
    ORDER BY e.redmine_login ASC
    """
    
    query = query0 + query1 + query2 + query3 + query4
    # query =  """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-
    # (e:Employee) RETURN e.employee, e.redmine_login, e.organization_area
    # """
    result = xconn.query(query) #, parameters=params)
    # print('>>>>>>>>>>>>>>>>> query (FD_Unimodal_Network_Framework)')
    # print(query)
    
    actors_data = pd.DataFrame([dict(_) for _ in result])
    actors_data.rename(columns={'e.employee': 'actor',
                                'e.redmine_login': 'usuarioRedmine',
                                'e.organization_area': 'area'}, inplace=True)
    # print('>>>>>>>>>>>>>>>>> actors_data (FD_Unimodal_Network_Framework)')
    # print(actors_data)
    # print(actors_data.columns)
    actors_data['usuarioRedmine'] = actors_data['usuarioRedmine'].str.lower()
    actors_data.sort_values(['usuarioRedmine'], ascending=[True],inplace=True)
    # print('>>>>>>>>>>>>>>>>> actors_data (FD_Unimodal_Network_Framework)')
    # print(actors_data)
    # print(actors_data.columns)
    
    XXXXedges_dict = 'aaaa'
    
    # frequencyCorte = 1 #0
    
    # # frequencyResponseMinimum = \
    # #     FD_Translate_Active_To_Code_AAFrequency(xfrequencyCorte)
    # frequencyResponseAccumulation = True
    
    # edges_AA_1 = edges_dict[('aa_1',frequencyCorte,frequencyResponseAccumulation)]
    # edges_AA_2 = edges_dict[('aa_2',frequencyCorte,frequencyResponseAccumulation)]
    # edges_AA_3 = edges_dict[('aa_3',frequencyCorte,frequencyResponseAccumulation)]
    # edges_AA_4 = edges_dict[('aa_4',frequencyCorte,frequencyResponseAccumulation)]
    
    # print(edges_AA_1.shape)
    # print(edges_AA_2.shape)
    # print(edges_AA_3.shape)
    # print(edges_AA_4.shape)
    
    # print(actors_data)
    
    
    #.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- AA pregunta 1
    
    # pregunta="""<u><b>¿Qué tan frecuente recibo información directamente de esta persona?</b></u>"""
    # preguntaCorta="AA1 ¿De quién recibo información?"
    # definiciónTablaInteracción = 'Filas: quien indicó que le proveo información, Columna: de quién recibo información'
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-empieza AA1 UMF')
    
    tabNetworkAA, mainAInDegreePlot_AA_1, mainAOutDegreePlot_AA_1,\
        mainAEigenvectorPlot_AA_1, mainABetweennessPlot_AA_1, \
            data_table_nodeDF, questions_menu, selected_question  = \
                FD_Unimodal_network(xconn,xglobal_questions_dict, 
                                    xnetwork_parameters_dict, 
                                    # xnetwork_parameters_data_table,
                                            XXXXedges_dict, actors_data,
                                          xbimodalAmplifier,
                                         xamplifier = _xamplifier,
                                         xgravityLevel=1)
    
    # tabAA_1, x_xdensityCAA_1, x_xdensityFAA_1, x_xfilasAA_1, x_xcolumnasAA_1,\
    # x_xlinksAA_1, \
    #     x_xcentralizationAA_1, \
    #         x_xplot1_AA_1, x_xmulti_select_AA_1, x_xplot2_AA_1, x_xplot3_AA_1, \
    #             x_xtabTablaInteracción_AA_1, x_xtabTabla3_AA_1, \
    #                 x_xtabTabla4_AA_1, \
    #                 x_xtabTablaDelta_AA_1, x_xgraph1_AA_1, \
    #                     x_xsourceInteracción_AA_1,_,_, \
    #                 mainAInDegreePlot_AA_1, mainAOutDegreePlot_AA_1,\
    #                     mainAEigenvectorPlot_AA_1, \
    #                         mainABetweennessPlot_AA_1, data_table_nodeDF,\
    #                             x_xnon_connected_list_AA_1, x_xplotH_AA_1  = \
    #                     FD_Unimodal_network(xnetwork_parameters_dict, 
    #                                         XXXXedges_dict, actors_data,
    #                                       xbimodalAmplifier,
    #                                      xamplifier = _xamplifier,
    #                                      xgravityLevel=1)
                        
    
    # tabAA_encabezado, densityG1, densityG2, filas, columnas, links, \
    #     centralization,\
    #     plot1, multi_select, plot2, plot3, tabTablaInteracción, tabModelo_completo, \
    #     tabModelo_filtrado, tabTablaDelta, graph1, data_table_interacción, \
    #         dirección,número_conexiones_componentes_eliminados, \
    #                 mainAInDegreeGraph, mainAOutDegreeGraph,\
    #                     mainAEigenvectorGraph, mainABetweennessGraph,\
    #                         data_table_nodeDF, non_connected_list, plotH
    
    node_degree_dashboard = column(UTBo_EmptyParagraph(50, 5),
                                row(mainAInDegreePlot_AA_1,
                                    mainAOutDegreePlot_AA_1,
                                    mainABetweennessPlot_AA_1,
                                    mainAEigenvectorPlot_AA_1),
                                data_table_nodeDF)

    
    #Con todo lo que devolvía
    # return densityCAA_1,densityFAA_1,filasAA_1,columnasAA_1,linksAA_1, \
    #     centralizationAA_1, node_degree_dashboard, tabAA_1
    return node_degree_dashboard, tabNetworkAA, questions_menu, selected_question
        
        # , node_degree_dashboard
    
# , checkbox_group, corte_button_group
