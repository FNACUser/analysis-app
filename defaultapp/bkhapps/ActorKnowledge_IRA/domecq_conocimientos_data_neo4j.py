# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 21:59:11 2024

@author: luis.caro
"""

import pandas as pd


def get_data_from_db(xconn):
    query = """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-(e:Employee)<-
                [OF_EMPLOYEE]-(aif:Adjacency_input_form)<-
                [RESPONSE_OF_FORM]-(r:Response)-[FOR_QUESTION]->
                (q:Question)-[QUESTION_FOR]->(nwm:Network_mode)
                WHERE nwm.id_network_mode IN [4,5,6]
                MATCH (ns:Node_segment)<-[ES_DE_SEGMENTO]-(n:Node)<-[ABOUT]-
                (r)-[IS_ITEM]->(rpi:Response_pattern_item)
                RETURN q.id_question as id_question,
                        q.question as Question_es,
                        n.id_node as id_node,
                        n.node as node_es,
                        rpi.item_value as valor,
                        rpi.item_meaning as texto,
                        e.id_employee as id_employee,
                        e.employee as username,
                        oa.id_organization_area as id_organization_area,
                        oa.organization_area as Organization_area_es,
                        nwm.id_network_mode as id_network,
                        nwm.network_mode as name_es,
                        ns.id_segment as id_node_segment,
                        ns.segment as node_segment"""
                        
    response_final = xconn.query(query) #, parameters=params)
    
    response_final_df = pd.DataFrame([dict(_) for _ in response_final])
    
    users_df =\
        response_final_df[['id_employee', 'username', 'id_organization_area',
                            'Organization_area_es']].copy(deep=True)
    
    users_df = users_df.drop_duplicates()
            
    return response_final_df, users_df