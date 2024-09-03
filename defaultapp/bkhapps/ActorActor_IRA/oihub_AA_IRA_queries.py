# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:21:16 2022

@author: luis.caro
"""

import pandas as pd

# from neo4j_learn_ONA import conn, insert_data
# from neo4j_connection_sandbox import conn, insert_data




def FD_query_possible_responses(xconn, xid_question, 
                                xeliminate_option_zero = True):
    
    print('.-.-..-.-. oihub_AA_IRA_queries/FD_query_possible_responses')
    # print('>>>>>>>>>> xeliminate_zero (FD_query_possible_responses)')
    # print(xeliminate_zero)

    query0="""MATCH (q:Question{id_question:"""

    query1 = """})-[HAS_PATTERN]->(rp:Response_pattern)<-
                [RESPONSE_ITEM_OF]-(rip:Response_pattern_item) 
                RETURN rip.item_meaning, rip.item_value, 
                    rip.id_response_pattern_item"""
            
    query = query0 + str(xid_question) + query1
    
    # print('>>>>>>>>>>>>>>>>> query (FD_query_possible_responses)')
    # print(query)
    
    result = xconn.query(query) #, parameters=params)
    
    result_df = pd.DataFrame([dict(_) for _ in result])
    
    possible_responses_df = \
        result_df.sort_values(by=['rip.item_value'], ascending=True)
        
    possible_responses_df.drop(columns=['rip.id_response_pattern_item'],
                               inplace = True)
    # print('>>>>>>>>>> possible_responses_df (FD_query_possible_responses)')
    # print(possible_responses_df)

    if xeliminate_option_zero == True:
        possible_responses_df = \
            possible_responses_df.\
                loc[possible_responses_df['rip.item_value'] != 0]
    
    possible_responses_dict = \
        possible_responses_df.set_index('rip.item_value').T.to_dict('list')    
    
    # print('>>>>>>>>>> possible_responses_dict (FD_query_possible_responses)')
    # print(possible_responses_dict)

    possible_responses_components = \
        [v[0] for k,v in possible_responses_dict.items() ]
        # \
        #  if len(k) == 1]
    
    # print('>>>>>>>>>> possible_responses_components (FD_query_possible_responses)')
    # print(possible_responses_components)

    
    return possible_responses_components, possible_responses_dict

# FD_query_possible_responses(conn, 1)

def FD_query_question_data(xconn, xquestion_tuple):
    
    """
    Devuelve data frame con las siguientes columnas:
        - id_adjacency_input_form, 
        - network_mode_theme,
        - id_employee, 
        - is_active,
        - redmine_login, 
        - employee,
        - id_response, 
        - t_id_employee,
        - t_is_active, 
        - t_redmine_login,
        - t_employee,
        - id_question, 
        - id_response_pattern_item,
        - item_value as value, 
        - item_meaning as meaning,
        - id_organization_area,
        - organization_area
    """
    
    print('.-.-.-.-.-.-.-.-.-. oihub_AA_IRA_queries/FD_query_question_data')
    # print('>>>>>>>>>>>> xquestion_tuple (FD_query_question_data)')
    # print(xquestion_tuple)


    cycle, network_mode_theme, question, selected_possible_responses = \
        xquestion_tuple
    
    query_parameters = \
         {'selected_possible_responses': selected_possible_responses,
          'cycle': cycle,
          'network_mode_theme': network_mode_theme,
          'question': question} 
    # print('>>>>>>>>>>>> query_parameters (FD_query_question_data)')
    # print(query_parameters)

        
     
    query = """WITH $cycle AS cycle, 
                $network_mode_theme AS network_mode_theme, 
                $question AS question,
                $selected_possible_responses AS selected_possible_responses
                
    
                MATCH (cy:Cycle)<-[OF_CYCLE]-(aif:Adjacency_input_form)
             -[OF_NETWORK_MODE]->(nwm:Network_mode)-[IS_OF_THEME]->
             (nwmt:Network_mode_theme)
             WHERE cy.id_cycle = cycle AND 
             nwmt.network_mode_theme = network_mode_theme
             
             MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-(e:Employee)<-
             [OF_EMPLOYEE]-(aif)
             
             MATCH (q:Question)<-[FOR_QUESTION]-(res:Response)-
             [OF_FORM]->(aif)
             WHERE q.id_question = question
             
             MATCH (rpi:Response_pattern_item)<-[IS_ITEM]-(res)-
             [rt:RELATED_TO]->(te:Employee)
             WHERE rpi.item_value IN selected_possible_responses
             
             MATCH (e)-[hr:HAS_RESPONSE]->(res)
             
             RETURN aif.id_adjacency_input_form, nwmt.network_mode_theme, 
             e.id_employee as id_employee, e.is_active as is_active, 
             e.redmine_login as redmine_login, e.employee as employee, 
             res.id_response, te.id_employee as t_id_employee, 
             te.is_active as t_is_active, te.redmine_login as t_redmine_login, 
             te.employee as t_employee, 
             q.id_question, rpi.id_response_pattern_item,
             rpi.item_value as value, rpi.item_meaning as meaning,
             oa.id_organization_area as id_organization_area,
             oa.organization_area as organization_area"""
         
    # WHERE rpi.item_value IN $selected_possible_responses
    
     
    result = xconn.query(query, parameters=query_parameters)
     
    result_df = pd.DataFrame([dict(_) for _ in result])
    # print('>>>>>>>>>>>>>>>>>>>>> result_df (FD_query_question_data)')
    # print(result_df.columns)
    # print(result_df.shape)
    
    return result_df

