# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 16:31:14 2023

@author: luis.caro
"""

import pandas as pd

# from neo4j_learn_ONA import conn, insert_data


from .oihub_AA_IRA_queries import FD_query_possible_responses

from .oihub_CVF_Clusters import FD_CVF_Clusters_df
# FD_CVF_Clusters_Main, 

from .oihub_AA_IRA_Actors_and_areas_dicts import FD_Actors_and_areas_dicts

from .oihub_IRA_legends import FD_legends_dict

from .oihub_AA_IRA_help_texts import FD_question_help_text_dict

# from oihub_AA_IRA_help_texts import FD_user_help_dict

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_DataFrame_to_DataTable


#%%

# def FD_legends_dict():
    
#     legends_dict = {'l-001':['Comparativo Clusters','Clusters Comparative'],
#                     'l-002':['Detalle Clusters','Clusters Detail'],
#                     'l-003':['Cultura','Culture'],
#                     'l-004':['Color nodo','Node color'],
#                     'l-005':['Departamento','Department'],
#                     'l-006':['Grupo cultura','Culture cluster'],
#                     'l-007':['Color del nodo: Departamento','Node color: Department'],
#                     'l-008':['Color del nodo: Grupo cultura',
#                              'Node color: Culture cluster'],
#                     'l-009':['Gravedad','Gravity'],
#                     'l-010':['Nivel nodo','Node level'],
#                     'l-011':['Nivel red','Network level'],
#                     'l-012':['Todos los funcionarios','All employees'],
#                     'l-013':['Funcionario filtrado','Filtered employee'],
#                     'l-014':['Red informal','Informal network'],
#                     'l-015':['Area','Area'],
#                     'l-016':['Redes informales','Informal networks'],
#                     'l-017':['Areas','Areas'],
#                     'l-018':['Centro','Core'],
#                     'l-019':['Comunidades','Communities'],
#                     'l-020':['Funcionario','Employee'],
#                     'l-021':['Grados nodos','Nodes degrees'],
#                     'l-022':['Todos','All'],
#                     'l-023':['Cualquiera','Any'],
#                     'l-024':['Filtro:','Filter'],
#                     'l-025':['Conexiones indicadas por respondedor:',
#                              'Connections indicated by responder'],
#                     'l-026':['Conexiones indicadas por otros:',
#                              'Connections indicated by others'],
#                     'l-027':['Gráfico:', 'Plot'],
#                     'l-028':['Tabla:', 'Table'],
#                     'l-029':['Preguntas', 'Questions']}

#     return legends_dict

# def FD_global_questions_dict(xcompany): 
    
#     #Uso de reverse_edges y responder direction
#     #El estándar es que el respondedor apunta a los que selecciona como
#     #relaciones. Así siempre:
#     #       - el out_degree corresponde a lo marcado por el respondedor
#     #       - el in-degree corresponde a lo marcado por otras personas
#     #       que seleccionaron al respondedor
#     #Este estándar se mantiene poniendo:
#     #       - reverse_edges = False (la dirección de los edges se deja tal
#     #       cual viene del grafo de neo4j)
#     #       - responder_direction = 'out' 
#     #
#     #Las opciones de estas variables (reverse_edges y responder direction)
#     #se hicieron para dar sentido al contenido de la pregunta. 
#     #Por ejemplo, la dirección del flujo de información cambia de sentido 
#     #si la pregunta es "de quién recibo" vs "a quién entrego". 
#     #Si es "de quien recibo" se podría pensar que aunque
#     #son personas seleccionadas por el responder, de ellas emana la 
#     #información, por lo tanto la dirección de los eges podria ser hacia
#     #el repondedor y el in_degree sería calculado sobre la base de la
#     #información que recibe. En este caso se marcaría reverse_edges = True y
#     #responder_direction = 1.
#     #
#     #Sin embargo, teniendo en cuenta que para algunas preguntas como "con 
#     #quien trabaja en equipo" no es clara la dirección, finalmente se optó 
#     #por dejar siempre el caso estándar, que siempre debe leerse como:
#     #       - el sentido de los edges es desde el seleccionador (responder)
#     #       a los seleccionados (en el cuadro filtrado izquierdo)
#     #       - el out_degree refleja las selecciones de los respondedores (o
#     #       sea entre más personas seleccione el respondedor, más alto su 
#     #       out_degree)
#     #       - el in_degree refleja las veces que otras personas seleccionan
#     #       al respondedor (o sea entre más personas seleccionen al 
#     #       respondedor, más alto su in_degree)
#     #Así se evitan confusiones.
#     #
#     #Las combinaciones reverse_edges=True con responder_direction='out', o
#     #reverse_edges=False con responder_direction='in', podrían servir para
#     #casos especiales, que por ahora no se consideran.
    
    
    
#     if xcompany == 'Alcaparros':
    
#         dict_2_1 = {'language': 1,
#                     'network': 'aa_1',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_2_2 = {'language': 1,
#                     'network': 'aa_2',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_2_3 = {'language': 1,
#                     'network': 'aa_3',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_2_4 = {'language': 1,
#                     'network': 'aa_4',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_3_1 = {'language': 1,
#                     'network': 'aa_5',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_3_2 = {'language': 1,
#                     'network': 'aa_6',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_3_3 = {'language': 1,
#                     'network': 'aa_7',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_3_4 = {'language': 1,
#                     'network': 'aa_8',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_4_5 = {'language': 1,
#                     'network': 'aa_7',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_4_6 = {'language': 1,
#                     'network': 'aa_8',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_5_1 = {'language': 1,
#                     'network': 'aa_8',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_5_2 = {'language': 1,
#                     'network': 'aa_7',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_5_5 = {'language': 1,
#                     'network': 'aa_8',
#                     'active_selected_possible_responses': [0, 1, 2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         questions_dict = {(2,1): dict_2_1,
#                           (2,2): dict_2_2,
#                           (2,3): dict_2_3,
#                           (2,4): dict_2_4,
#                           (3,1): dict_3_1,
#                           (3,2): dict_3_2,
#                           (3,3): dict_3_3,
#                           (3,4): dict_3_4,
#                           (4,5): dict_4_5,
#                           (4,6): dict_4_6,
#                           (5,1): dict_5_1,
#                           (5,2): dict_5_2,
#                           (5,5): dict_5_5}
        
#         get_cvf_clusters = False
        
#         global_questions_dict = {'questions_dict': questions_dict,
#                                  'get_cvf_clusters': get_cvf_clusters}
    
#     else:
    
#         #se cambió a 1 1
#         dict_1_1 = {'language': 1,
#                     'network': 'aa_1',
#                     'active_selected_possible_responses': [1,2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         #no se ha cambiado
#         dict_1_2 = {'language': 1,
#                     'network': 'aa_2',
#                     'active_selected_possible_responses': [1,2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'out_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_1_3 = {'language': 1,
#                     'network': 'aa_3',
#                     'active_selected_possible_responses': [1,2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         #no se ha cambiado
#         dict_1_4 = {'language': 1,
#                     'network': 'aa_4',
#                     'active_selected_possible_responses': [1,2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'out_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': False,
#                     'preguntas_text_cut': 128,
#                     'responder_direction': 'out'}
        
#         dict_2_5 = {'language': 1,
#                     'network': 'aa_5',
#                     'active_selected_possible_responses': [0,1,2],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': True,
#                     'preguntas_text_cut': 0,
#                     'responder_direction': 'out'}
    
#         dict_2_6 = {'language': 1,
#                     'network': 'aa_6',
#                     'active_selected_possible_responses': [0, 1],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': True,
#                     'preguntas_text_cut': 0,
#                     'responder_direction': 'out'}
    
#         dict_2_7 = {'language': 1,
#                     'network': 'aa_7',
#                     'active_selected_possible_responses': [0, 1],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': True,
#                     'preguntas_text_cut': 0,
#                     'responder_direction': 'out'}
    
#         dict_3_8 = {'language': 1,
#                     'network': 'aa_6',
#                     'active_selected_possible_responses': [0, 1],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': True,
#                     'preguntas_text_cut': 0,
#                     'responder_direction': 'out'}
    
#         dict_3_9 = {'language': 1,
#                     'network': 'aa_7',
#                     'active_selected_possible_responses': [0, 1],
#                     'reverse_edges': False,
#                     'node_size_attribute': 'in_degree',
#                     'filter_group_active': 1,
#                     'filter_group_enabled': True,
#                     'preguntas_text_cut': 0,
#                     'responder_direction': 'out'}
    
#         questions_dict = {(1,1): dict_1_1,
#                                 (1,2): dict_1_2,
#                                 (1,3): dict_1_1,
#                                 (1,4): dict_1_2,
#                                 (2,5): dict_2_5,
#                                 (2,6): dict_2_6,
#                                 (2,7): dict_2_7,
#                                 (3,8): dict_3_8,
#                                 (3,9): dict_3_9}
        
#         get_cvf_clusters = True
        
#         global_questions_dict = {'questions_dict': questions_dict,
#                                  'get_cvf_clusters': get_cvf_clusters}
    
#     return global_questions_dict
    


def FD_common_question_ini(xconn, xcompany, xid_question, xid_network_mode,
                           xget_cvf_clusters, xeliminate_option_zero, 
                           xpreguntas_text_cut = 0):
    
    print('.-.-.-.-.-.-.-.-. oahubGDB_AA_IRA_QCommon/FD_common_question_ini')
    # print('>>>>>>>>>>>>>>> xid_network_mode (FD_common_question_ini)')
    # print(xid_network_mode)
    
    legends_dict = FD_legends_dict()
    
    if xcompany == 'Finac':
        #.-.-.---.-.-.-.-.-FINAC
        # id_network_mode = 4
        cycle = 1
    else:
        #.-.-.---.-.-.-.-.-Alcaparros
        # id_network_mode = 3
        cycle = 1
        
    query0="""MATCH (nwm:Network_mode{id_network_mode:"""
    query1 = str(xid_network_mode)
    query2="""}) 
                -[IS_OF_THEME]-> (nwmt:Network_mode_theme) 
            RETURN nwmt.network_mode_theme"""
    query = query0 + query1 + query2
    
    # print('>>>>>>>>>>>>>>>>>>>>>>> query (FD_common_question_ini)')
    # print(query)
    
    network_mode_theme = xconn.query(query)
    
    # print('>>>>>>>>>>>>>>> network_mode_theme (FD_common_question_ini)')
    # print(network_mode_theme)
    xx = pd.DataFrame([dict(_) for _ in network_mode_theme])
    # print('>>>>>>>>>>>>>>> xx (FD_common_question_ini)')
    # print(xx)
    
    network_mode_theme = \
        list(pd.DataFrame([dict(_) for _ in network_mode_theme])\
             ['nwmt.network_mode_theme'])[0]
    
    # print('>>>>>>>>>>>> network_mode_theme oahubGDB_AA_IRA_QCommon/FD_common_question_ini')
    # print(network_mode_theme)
    
    query0="""MATCH (q:Question{id_question:"""
    query1=str(xid_question)
    query2="""}) RETURN q.question"""
    query = query0 + query1 + query2
    pregunta = xconn.query(query)
    pregunta = \
        list(pd.DataFrame([dict(_) for _ in pregunta])['q.question'])[0]
    pregunta

    if xpreguntas_text_cut == 0:
        pregunta = '<u><b>' + pregunta + '</b></u>'
    else:
        pregunta = '<u><b>' + pregunta[:xpreguntas_text_cut] + '</b></u>'
        
    #Esto se quitó pero vale la pena pensarlo bien.
    #Es para hacer mejor claridad en los dashboards
    # est_preguntas = pd.read_excel('Descripcion_informacion_alcaparros.xlsx', 
    #                               sheet_name='Est_preguntas')
    # print('>>>>>>>>>>>>>>>>>>>> est_preguntas (FD_common_question_ini)')
    # print(est_preguntas.to_dict('records'))
    # print(est_preguntas.columns)
    # est_preguntas_dict = \
    #     {k: list(v.values()) \
    #       for k, v in est_preguntas.set_index('id').to_dict('index').items()}
    # est_preguntas_dict
    # print('>>>>>>>>>>>>>>>>>>>> est_preguntas_dict (FD_common_question_ini)')
    # print(est_preguntas_dict)
    # preguntaCorta = est_preguntas_dict.get(1)[1]
    # print('>>>>>>>>>>>>>>>>>>>> preguntaCorta (FD_common_question_ini)')
    # print(preguntaCorta)
   
    # definiciónTablaInteracción = est_preguntas_dict.get(1)[2]
    # print('>>>>>>>>>>>>>>>>>>>> definiciónTablaInteracción (FD_common_question_ini)')
    # print(definiciónTablaInteracción)
    
    #por ahora no se usa pregutna corta. Esto hay que pensarlo por la misma
    #razón de arriba
    preguntaCorta = "xxxxxxxxxxx"
    
    definiciónTablaInteracción =\
        "Filas: quien contesta (origen), Columna: sobre quién contesta (destino)"
    
    
    
    possible_responses_components, possible_responses_dict = \
        FD_query_possible_responses(xconn, xid_question, 
                                    xeliminate_option_zero = xeliminate_option_zero)
        
    # print('>>>>>>>>>> possible_responses_components (FD_common_question_ini)')
    # print(possible_responses_components)
    # print('>>>>>>>>>> possible_responses_dict (FD_common_question_ini)')
    # print(possible_responses_dict)
    
    if xget_cvf_clusters == True:
        # _, _, cvf_clusters_df = \
        #     FD_CVF_Clusters_Main(xconn, 0)
        cvf_clusters_df = FD_CVF_Clusters_df(xconn, 0)
    else:
        cvf_clusters_df = pd.DataFrame(columns=['id_employee', 'cluster', 
                                                'id_user', 'employee', 
                                                'id_organization_area',
                                                'organization_area', 
                                                'cluster_str'])
        
    # print('>>>>>>>>>> cvf_clusters_df (FD_common_question_ini)')
    # print(cvf_clusters_df.shape)
    # print(cvf_clusters_df.columns)
    # print(list(cvf_clusters_df['employee']))
    # print(list(cvf_clusters_df['cluster_str']))
    # print(cvf_clusters_df.to_dict('records'))
    
    
    fields_table_filtered_employee = ['employee',
                                  'organization_area', 'cvf_cluster',
                                  'eigenvector_centrality',
                                  'betweenness_centrality',
                                  'unscaled_total_degree_centrality', 
                                  'unscaled_in_degree_centrality',
                                  'unscaled_out_degree_centrality', 
                                  'informal_network']
    
    
    return legends_dict, cycle, network_mode_theme, pregunta, preguntaCorta,\
        definiciónTablaInteracción, possible_responses_components, \
            possible_responses_dict, cvf_clusters_df, \
                fields_table_filtered_employee
            
# xcompany = 'Finac'
# xid_question = 1
# xid_network_mode = 1 
# FD_common_question_ini(xcompany, xid_question, xid_network_mode, 
#                            xpreguntas_text_cut = 0)



# def FD_network_parameters_dict(xcompany, xid_question, xid_network_mode,
#                                xnetwork, xactive_selected_possible_responses,
#                                xlanguage, xreverse_edges, 
#                                xnode_size_attribute, xfilter_group_active, 
#                                xfilter_group_enabled, xresponder_direction,
#                                xpreguntas_text_cut = 0):
def FD_network_parameters_dict(xconn, xid_question, xid_network_mode,
                               xglobal_questions_dict,
                               xnetwork_parameters_dict,
                               xcompany = '',
                               xlanguage = '',
                               xselection_label=''):
    
    """
    Input:  - xcompany
            - xid_question
            - xid_network_mode
            - xnetwork
            - xactive_selected_possible_responses
            - xlanguage
            - xreverse_edges
            - xnode_size_attribute
            - xfilter_group_active
            - xfilter_group_enabled
            - responder direction
            - xpreguntas_text_cut
    Output: Dictionary with the following fields:
        - 'network': xnetwork
        - 'pregunta': pregunta,
        - 'preguntaCorta': preguntaCorta,
        - 'definiciónTablaInteracción':
        - 'cycle': 
        - 'id_question': 
        - 'network_mode_theme': 
        - 'possible_responses_components': 
        - 'active_selected_possible_responses':
        - 'possible_responses_dict': 
        - 'cvf_clusters_df':
        - 'legends_dict': 
        - 'language': 
        - 'reverse_edges': in the graph database the source is the responder
                and the targets are the persons selected by the responder.
                When the question implies reception by the source (example:
                'Who porvides me information'), the edges must be reversed
                (reversed_edges = True) for display purposes and for in/out 
                degree calculations. Otherwise, reverse_edges = False.
        - 'node_size_attribute': 
        - 'filter_group_active': 
        - 'filter_group_enabled': 
        - responder_direction
        - fields_table_filtered_plot: fields to display in DataTable of
            filtered employee's egos plots
        - dict_employee: key: id_employee, content: employee, redmine_login,
                         id_organization_area, organization_area
        - dict_employee_reverse: key: redmine_login, content: id_employee, 
                                employee, id_organization_area, 
                                organization_area
        - dict_employee_by_name: key: employee, content: id_employee, 
                                redmine_login, id_organization_area, 
                                organization_area
        - dict_organization_area: key: id_organization_area, 
                                    content: organization_area
        - dict_organization_area_reverse: key: organization_area,
                                                content: id_organization_area
        - selection_label: label to describe question's default selections
    """
    
    print('.-.-.-.-.-.-.-.-. oihub_AA_IRA_QCommon/FD_network_parameters_dict')
    # print('>>>>>>>>>>>>>>> xid_question (FD_network_parameters_dict)')
    # print(xid_question)
    # print('>>>>>>>>>>>>>>> xid_network_mode (FD_network_parameters_dict)')
    # print(xid_network_mode)
    
    # global_question_dict = xglobal_questions_dict.get((xid_network_mode,
    #                                                    xid_question))
    # questions_dict = \
    #     xglobal_questions_dict.get('questions_dict')
    questions_dict = \
        xglobal_questions_dict['questions_dict']
    # print('>>>>>>>>>>>>>>> questions_dict (FD_network_parameters_dict)')
    # print(questions_dict)
    
    if xselection_label == '':
        # question_dict = questions_dict.get((xid_network_mode, xid_question))
        question_dict = questions_dict[(xid_network_mode, xid_question)]
        selection_display_order = 0
    else:
        # question_dict = questions_dict.get((xid_network_mode, xid_question,
        #                                     xselection_label))
        question_dict = questions_dict[(xid_network_mode, xid_question,
                                            xselection_label)]
        selection_display_order = question_dict.get('selection_display_order')
    # print('>>>>>>>>>>>>>>> question_dict (FD_network_parameters_dict)')
    # print(question_dict)
    
    language = question_dict['language']
    network = question_dict['network']
    active_selected_possible_responses = \
        question_dict['active_selected_possible_responses']
    reverse_edges = question_dict['reverse_edges']
    node_size_attribute = question_dict['node_size_attribute']
    filter_group_active_initial = question_dict['filter_group_active_initial']
    filter_group_enabled = question_dict['filter_group_enabled']
    preguntas_text_cut = question_dict['preguntas_text_cut']
    responder_direction = question_dict['responder_direction']
    selection_label = question_dict['selection_label']
    question_type_dict = question_dict['question_type_dict']
    inverse_question = question_dict['inverse_question']
    associated_questions = question_dict['associated_questions']
    eliminate_option_zero = question_dict['eliminate_option_zero']
    # print('>>>>>>>>>>>>>>> question_type (FD_network_parameters_dict)')
    # print(question_type_dict)
    
    question_help_texts_dict = FD_question_help_text_dict(question_type_dict)
    # print('>>>>>>>>>>> question_help_texts_dict (FD_network_parameters_dict)')
    # print(question_help_texts_dict)
    
    get_cvf_clusters = xglobal_questions_dict['get_cvf_clusters']
    
    #
    #xcompany = '' when a new question is selected. In this case company
    #           is already in the dictionary
    #xcompany comes with a value the dirst time the dictionary is created.
    if xcompany == '':
        company = xnetwork_parameters_dict['company']
    else:
        company = xcompany
        
    legends_dict, cycle, network_mode_theme, pregunta, preguntaCorta,\
        definiciónTablaInteracción, possible_responses_components, \
            possible_responses_dict, cvf_clusters_df,\
                fields_table_filtered_employee = \
                FD_common_question_ini(xconn, company, xid_question,
                                       xid_network_mode,
                                       get_cvf_clusters,
                                       eliminate_option_zero,
                                       xpreguntas_text_cut = \
                                           preguntas_text_cut)
    # print('>>>>>>>>>>> possible_responses_dict (FD_network_parameters_dict)')
    # print(possible_responses_dict)
                    
    # print('>>>>>>>>>>>>>>> pregunta (FD_network_parameters_dict)')
    # print(pregunta)
    
    # a=5/0
                    
    dict_employee, dict_employee_reverse, dict_organization_area, \
        dict_organization_area_reverse, dict_employee_by_name =\
            FD_Actors_and_areas_dicts(xconn)
        
    graph_query_tuples = [(cycle, network_mode_theme, xid_question,
                     active_selected_possible_responses)]
                        
    xnetwork_parameters_dict.update({'company': company,
                                     'network': network,
                                'pregunta': pregunta,
                                #'preguntaCorta': preguntaCorta,
                                'definiciónTablaInteracción': \
                                    definiciónTablaInteracción,
                                'cycle': cycle,
                                'id_question': xid_question,
                                'id_network_mode': xid_network_mode,
                                'network_mode_theme': network_mode_theme,
                                'possible_responses_components': \
                                    possible_responses_components,
                                'active_selected_possible_responses':
                                    active_selected_possible_responses,
                                'possible_responses_dict': \
                                    possible_responses_dict,
                                'cvf_clusters_df': 
                                    cvf_clusters_df,
                                'legends_dict': legends_dict,
                                'reverse_edges': reverse_edges,
                                'node_size_attribute': node_size_attribute,
                                'filter_group_active_initial': 
                                    filter_group_active_initial,
                                'filter_group_enabled': filter_group_enabled,
                                'responder_direction': responder_direction,
                                'fields_table_filtered_employee': 
                                    fields_table_filtered_employee,
                                'dict_employee':dict_employee, 
                                'dict_employee_reverse':dict_employee_reverse,
                                'dict_employee_by_name': dict_employee_by_name,
                                'dict_organization_area':\
                                    dict_organization_area,
                                'dict_organization_area_reverse':\
                                    dict_organization_area_reverse,
                                'graph_query_tuples': graph_query_tuples,
                                'selection_label' : selection_label,
                                'selection_display_order' : 
                                    selection_display_order,
                                'question_help_texts_dict':
                                    question_help_texts_dict,
                                'inverse_question': inverse_question,
                                'associated_questions': associated_questions})
        # ,
        #                         'get_cvf_clusters': get_cvf_clusters})
        
    if xcompany != '':
        xnetwork_parameters_dict.update({'company':xcompany})
    if xlanguage != '':
        xnetwork_parameters_dict.update({'language':xlanguage})
        
    # network_parameters_dict = {'network': network,
    #                             'pregunta': pregunta,
    #                             'preguntaCorta': preguntaCorta,
    #                             'definiciónTablaInteracción': \
    #                                 definiciónTablaInteracción,
    #                             'cycle': cycle,
    #                             'id_question': xid_question,
    #                             'network_mode_theme': network_mode_theme,
    #                             'possible_responses_components': \
    #                                 possible_responses_components,
    #                             'active_selected_possible_responses':
    #                                 active_selected_possible_responses,
    #                             'possible_responses_dict': \
    #                                 possible_responses_dict,
    #                             'cvf_clusters_df': 
    #                                 cvf_clusters_df,
    #                             'legends_dict': legends_dict,
    #                             'language': xlanguage,
    #                             'reverse_edges': reverse_edges,
    #                             'node_size_attribute': node_size_attribute,
    #                             'filter_group_active': filter_group_active,
    #                             'filter_group_enabled': filter_group_enabled,
    #                             'responder_direction': responder_direction,
    #                             'fields_table_filtered_employee': 
    #                                 fields_table_filtered_employee}
        
    # network_parameters_dict = {'possible_responses_components': \
    #                                possible_responses_components,
    #                            'active_selected_possible_responses':
    #                                xactive_selected_possible_responses,
    #                            'possible_responses_dict': \
    #                                possible_responses_dict,
    #                            'cvf_clusters_df': 
    #                                cvf_clusters_df,
    #                            'legends_dict': legends_dict,
    #                            'fields_table_filtered_employee': 
    #                                fields_table_filtered_employee}
        
    # network_parameters_df_dict = {'network': xnetwork,
    #                               'pregunta': pregunta,
    #                               'preguntaCorta': preguntaCorta,
    #                               'definiciónTablaInteracción': \
    #                                   definiciónTablaInteracción,
    #                               'cycle': cycle,
    #                               'id_question': xid_question,
    #                               'network_mode_theme': network_mode_theme,
    #                                'language': xlanguage,
    #                                'reverse_edges': xreverse_edges,
    #                                'node_size_attribute': xnode_size_attribute,
    #                                'filter_group_active': xfilter_group_active,
    #                                'filter_group_enabled': \
    #                                    xfilter_group_enabled,
    #                                'responder_direction': xresponder_direction}
        
    # network_parameters_df = pd.DataFrame(network_parameters_df_dict,
    #                                                index=[0])
    
    # network_parameters_data_table = \
    #     UTBo_DataFrame_to_DataTable(network_parameters_df)
        
    # return xnetwork_parameters_dict
    # return network_parameters_dict, network_parameters_data_table
    
# def FD_update_network_parameters_dict(xnetwork_parameters_dict,
#                                       xall_any_filter_group_active):
    
#     print('.-.-.-.-.-. oihub_AA_IRA_QCommon/FD_update_network_parameters_dict')
#     print('>>>>>>>all_any_filter_group_active (FD_update_network_parameters_dict)')
#     print(xall_any_filter_group_active)
    
#     xnetwork_parameters_dict.update({'filter_group_active': 
#                                      xall_any_filter_group_active})


    