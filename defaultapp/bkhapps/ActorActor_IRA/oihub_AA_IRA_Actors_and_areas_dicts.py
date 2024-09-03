# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 15:23:52 2023

@author: luis.caro
"""

import pandas as pd

from defaultapp.bkhapps.common.Utilities import FD_cut_name

# from neo4j_learn_ONA import conn


#%%

def FD_Actors_and_areas_dicts(xconn):
    
    """
    Devuelve 4 cosas:
        - dict_employee: diccionario de todos los empleados que forman
                parte de alguna relación de algún formulario Actor-Actor. 
                Key: id_employee Value: employee, redmine_login,
                                        id_organization_area, organization_area
        - , dict_employee_reverse: similar a dict_employee con la diferencia
                que, en este caso, el Key es redmine_login
        - dict_organization_area: áreas de los funcionarios que forman
                parte de alguna relación de algún formulario Actor-Actor. 
                Key: id_organization_area, Value: organization_area
        - dict_organization_area_reverse: similar a dict_organization_area
                con la diferencia que el Key es organization_area y el
                Value es id_organization_area
    """
    
    print('-.-.-.- oihub_AA_IRA_Actors_and_areas_dicts/FD_Actors_and_areas_dicts')
    
    query2 = """MATCH (cy:Cycle{id_cycle:1})<-[OF_CYCLE]-
                (aif:Adjacency_input_form)
                -[OF_EMPLOYEE]->(e:Employee)-[FUNCIONARIO_DE]->
                (oa:Organization_area)
                MATCH (aif)<-[OF_FORM]-(r:Response)-[RELATED_TO]->(te:Employee)
                RETURN aif.id_adjacency_input_form, 
                e.id_employee as id_employee,
                e.employee as employee, e.redmine_login as redmine_login,
                oa.id_organization_area as id_organization_area,
                oa.organization_area as organization_area, 
                te.id_employee as t_id_employee,
                te.employee as t_employee, 
                te.redmine_login as t_redmine_login""" 
    result2 = xconn.query(query2)
    
    result2_df = pd.DataFrame([dict(_) for _ in result2])
    
    query3 = """MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-(e:Employee)
                RETURN e.id_employee as t_id_employee,
                oa.id_organization_area as t_id_organization_area,
                oa.organization_area as t_organization_area"""
    result3 = xconn.query(query3)    
    result3_df = pd.DataFrame([dict(_) for _ in result3])
    
    complete_result_df = pd.merge(result2_df, result3_df, 
                                  left_on = 't_id_employee',
                                  right_on = 't_id_employee',
                                  how = 'left')
    
    complete_result_df['employee'] =\
        complete_result_df['employee'].apply(lambda x: FD_cut_name(x))
    complete_result_df['t_employee'] =\
        complete_result_df['t_employee'].apply(lambda x: FD_cut_name(x))
    
    source_employee_list = \
        list(complete_result_df[['id_employee', 'employee', 'redmine_login',
                                 'id_organization_area','organization_area']]\
             .itertuples(index=False, name=None))
    target_employee_list = \
        list(complete_result_df[['t_id_employee', 't_employee', 
                                 't_redmine_login', 't_id_organization_area',
                                 't_organization_area']]\
             .itertuples(index=False, name=None))
            
    dict_employee = {id_employee:(employee, redmine_login, 
                                  id_organization_area, organization_area)
                     for id_employee, employee, redmine_login, 
                     id_organization_area, organization_area 
                     in list(set(source_employee_list + target_employee_list))}
    
    dict_employee_reverse = {redmine_login:(id_employee, employee, 
                                          id_organization_area, 
                                          organization_area)
                             for id_employee, employee, redmine_login,
                             id_organization_area, organization_area
                             in list(set(source_employee_list +\
                                         target_employee_list))}
    
    dict_employee_by_name = {employee:(id_employee, redmine_login, 
                                          id_organization_area, 
                                          organization_area)
                             for id_employee, employee, redmine_login,
                             id_organization_area, organization_area
                             in list(set(source_employee_list +\
                                         target_employee_list))}
    
    source_organization_area_list = \
        list(complete_result_df[['id_organization_area','organization_area']]\
             .itertuples(index=False, name=None))
    target_organization_area_list = \
        list(complete_result_df[['t_id_organization_area',
                                 't_organization_area']]\
             .itertuples(index=False, name=None))
            
    organization_area_list = \
        list(set(source_organization_area_list + \
                 target_organization_area_list))
    organization_area_list.sort()
            
    # print(organization_area_list)
            
    dict_organization_area = {id_organization_area:organization_area
                              for id_organization_area, organization_area
                              in organization_area_list}
    
    dict_organization_area_reverse = {organization_area:id_organization_area
                                      for id_organization_area, 
                                      organization_area
                                      in organization_area_list}
        
    # print([(k,v) for k,v in dict_organization_area.items()])
    
    return dict_employee, dict_employee_reverse, dict_organization_area, \
        dict_organization_area_reverse, dict_employee_by_name
