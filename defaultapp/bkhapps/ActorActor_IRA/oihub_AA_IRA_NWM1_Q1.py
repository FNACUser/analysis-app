# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 23:16:50 2022

@author: luis.caro
"""

from bokeh.io import curdoc
from bokeh.models import Tabs, Div
from bokeh.layouts import row, column

from defaultapp.bkhapps.common.neo4j_learn_ONA import conn, insert_data
# from defaultapp.bkhapps.common.neo4j_connection_sandbox import conn, insert_data

from .oihub_AA_IRA_Main import FD_AA_IRA_Main

from .oihub_AA_IRA_QCommon import FD_network_parameters_dict

from .oihub_AA_IRA_Questions_dict import FD_global_questions_dict

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph



#%%


def FD_Main():
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_Main')
    
    company = 'Domecq'
    # company = 'Alcaparros'
    # company = 'Finac'
    # company = 'AYJ'
    
    language = 1
    
    if company == 'Alcaparros':
        id_question = 1
        network_mode = 3
    elif company == 'Finac':
        id_question = 1
        network_mode = 1
    elif company == 'AYJ':
        id_question = 5
        network_mode = 1
    else:
        #domecq
        id_question = 5
        network_mode = 1
    # network = 'aa_1'
    # active_selected_possible_responses = [0, 1]
    # reverse_edges = True
    # node_size_attribute = 'out_degree'
    # filter_group_active = 1
    # filter_group_enabled = False
    # preguntas_text_cut = 128
    # responder_direction = 'in'
    
    global_questions_dict = FD_global_questions_dict(company)
    print('>>>>>>>>>>>>>>>>>>>>>> global_questions_dict (FD_Main)')
    print(global_questions_dict)
    
    # gqd.get((3,1)).get('network')
    
    # network_parameters_dict, network_parameters_data_table = \
    # network_parameters_dict = \
    #     FD_network_parameters_dict(company, id_question, network_mode, network, \
    #                                active_selected_possible_responses,
    #                                language, reverse_edges, 
    #                                node_size_attribute, filter_group_active, 
    #                                filter_group_enabled,
    #                                responder_direction,
    #                                xpreguntas_text_cut = preguntas_text_cut)
    # network_parameters_dict = \
    #     FD_network_parameters_dict(company, id_question, network_mode,
    #                                language,
    #                                global_questions_dict)
    network_parameters_dict = {}
    # print('dict')
    # print(network_parameters_dict)
    FD_network_parameters_dict(conn, id_question, network_mode,
                               global_questions_dict, 
                               network_parameters_dict,
                               xcompany = company,
                               xlanguage = language)
    # print('dict')
    # print(network_parameters_dict)
    
    # print('dt')
    
    # print(network_parameters_data_table.source.data)
    
    # print('preguntaCorta')
    # print(network_parameters_data_table.source.data['preguntaCorta'])
    
    
    tabMayorRed, tabMayorNode, tabQuestionsMenu, selected_question = \
        FD_AA_IRA_Main(conn, global_questions_dict, network_parameters_dict)
    # ,
    #                                            network_parameters_data_table)
    
    # pregunta = network_parameters_data_table.source.data['pregunta'][0]
    pregunta = network_parameters_dict.get('pregunta')
    # network_mode_theme = \
    #     network_parameters_data_table.source.data['network_mode_theme'][0]
    network_mode_theme = network_parameters_dict.get('network_mode_theme')
    network_mode_theme = '<u><b>' + network_mode_theme + '</b></u>'
    
    preguntaEncabezado = Div(text=pregunta, width=500, height=25)
    network_mode_theme_encabezado = Div(text=network_mode_theme, width=500, 
                                        height=25)
    
    layout = column(UTBo_EmptyParagraph(50,5),
                         row(selected_question),
                         UTBo_EmptyParagraph(50,5),
                         Tabs(tabs=[tabQuestionsMenu, tabMayorRed, 
                                    tabMayorNode]))
    
    return layout
        
def AA_IRA_launch(doc):
    layout = FD_Main()
    doc.add_root(layout)

