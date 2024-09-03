# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:08:58 2023

@author: luis.caro
"""

from bokeh.plotting import figure, output_file, show

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import random

import sklearn
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score


# from neo4j_learn_ONA import conn, insert_data


# from bokeh.models.widgets.inputs import NumericInput 
from bokeh.io import curdoc

from bokeh.layouts import column, row

from bokeh.models import Div, Select, ColumnDataSource, TableColumn
from bokeh.models.widgets import DataTable


# from bokeh.plotting import figure

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph

from defaultapp.bkhapps.common.Utilities import UT_CountOcurrences

from .oihub_CVF_Functions import (FD_fetch_employee_culture_GDB, 
                           FD_employee_list_score,
                           FD_plot_weights_position,
                           FD_CVF_plot_single,
                           FD_horizontal_box_plot,
                           FD_fetch_valid_employees_areas)

#%% Temporal para tomar válidos - hay que arreglar GDB
# from sqlalchemy_pure_connection_cloud import session_scope

# from new_db_schema import CVF_Culture_input_form
#%%


#%%

def udpate_theme_box_plot(_xtheme_box_plot_actual, x_theme_box_plot_actual):
    
    # print('.-.-.-.-.-.-.-.-.-.- udpate_theme_box_plot')
    
    for i in range(0,8):
        # print(i)
        datasource = x_theme_box_plot_actual.renderers[i].data_source
        # if i == 6:
        # print('>>>>>>>>>>>>> dict(datasource.data) (udpate_theme_box_plot)')
        # print(i)
        # print(dict(datasource.data))
        _xtheme_box_plot_actual.renderers[i].data_source.data = \
            dict(datasource.data)
            

def udpate_cvf_plot(_xcvf_plot, x_cvf_plot):
    datasource = x_cvf_plot.renderers[2].data_source
    _xcvf_plot.renderers[2].data_source.data = dict(datasource.data)
    datasource3 = x_cvf_plot.renderers[3].data_source
    _xcvf_plot.renderers[3].data_source.data = dict(datasource3.data)
    datasource4 = x_cvf_plot.renderers[4].data_source
    _xcvf_plot.renderers[4].data_source.data = dict(datasource4.data)
    
    
def udpate_cvf_table(_xcvf_table, x_cvf_table):
    datasource = x_cvf_table.source.data
    _xcvf_table.source.data = dict(datasource)
    
# data_table.source.data = new_data


def udpate_cluster_plot_table(_xcvf_plot, x_cvf_plot):
    udpate_cvf_plot(_xcvf_plot[0], x_cvf_plot[0])
    udpate_cvf_table(_xcvf_plot[1], x_cvf_plot[1])   
     

def update_clusters_measure(xconn, xselector_measure, xira_employees_areas,
                            xthemes_dict, xn_clusters,
                            xcVF_clusters_plots_and_employees,
                            xbox_plot_actual_0, xbox_plot_preferido_0,
                            xbox_plot_actual_1, xbox_plot_preferido_1,
                            xbox_plot_actual_2, xbox_plot_preferido_2,
                            xbox_plot_actual_3, xbox_plot_preferido_3,
                            xselector_cluster,
                            xcvf_plot_1, xtheme_box_plot_actual_1, 
                            xtheme_box_plot_preferido_1,
                            xcvf_plot_2, xtheme_box_plot_actual_2, 
                            xtheme_box_plot_preferido_2, 
                            xcvf_plot_3, xtheme_box_plot_actual_3, 
                            xtheme_box_plot_preferido_3, 
                            xcvf_plot_4, xtheme_box_plot_actual_4, 
                            xtheme_box_plot_preferido_4, 
                            xcvf_plot_5, xtheme_box_plot_actual_5, 
                            xtheme_box_plot_preferido_5, 
                            xcvf_plot_6, xtheme_box_plot_actual_6, 
                            xtheme_box_plot_preferido_6):
    
    # print('.-.-.-.-.-.-.-.-.-.-.- update_clusters_measure')
    # print('>>>>>>>>>>>>> xselector_cluster.value (update_clusters_measure)')
    # print(xselector_cluster.value)
    
    if xselector_measure.value == 'Preferido':
        measure = 'Preferred'
    else:
        measure = xselector_measure.value

    
    _n_clusters, _clusters, _employees_clusters_df = \
        FD_CVF_build_clusters(xconn, xira_employees_areas, measure,
                              xn_clusters = xn_clusters)
        
    _employee_clusters_culture_list = \
        FD_build_employee_clusters_culture_list(xconn, 
                                                _clusters, 
                                                _employees_clusters_df)
        
    _cVF_clusters_plots_and_employees = \
        [FD_CVF_Cluster_plot(cluster, _employee_clusters_culture_list,
                             _employees_clusters_df, xira_employees_areas) \
         for cluster in range(1, 1 + _n_clusters)] 
    
    # print('>>>>>>>>> len(_cVF_clusters_plots_and_employees) (update_clusters_measure)')
    # print(len(_cVF_clusters_plots_and_employees))
    
    # cvf_plots_list=[(xcVF_clusters_plots_and_employees[cluster][0],
    #                  _cVF_clusters_plots_and_employees[cluster][0]) \
    #                 for cluster in range(_n_clusters)]
    
    cvf_plots_tables_list = [(xcVF_clusters_plots_and_employees[cluster],
                              _cVF_clusters_plots_and_employees[cluster]) \
                             for cluster in range(_n_clusters)]
    
    #VIEJO
    # def udpate_cvf_plot(_xcvf_plot, x_cvf_plot):
    #     datasource = x_cvf_plot.renderers[2].data_source
    #     _xcvf_plot.renderers[2].data_source.data = dict(datasource.data)
            
    # [udpate_cvf_plot(xcvf_plot, _cvf_plt) \
    #   for xcvf_plot, _cvf_plt in cvf_plots_list]
        
    
    [udpate_cluster_plot_table(xcvf_plot_table, _cvf_plot_table) \
      for xcvf_plot_table, _cvf_plot_table in cvf_plots_tables_list]
    
    
    #:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_

    _box_plot_actual_0, _box_plot_preferido_0 = \
        CVF_box_plots(xconn, 1, _employees_clusters_df, xwidth=280, xheight=150)
    _box_plot_actual_1, _box_plot_preferido_1 = \
        CVF_box_plots(xconn, 2, _employees_clusters_df, xwidth=280, xheight=150)
    _box_plot_actual_2 = None
    _box_plot_actual_3 = None
    _box_plot_preferido_2 = None
    _box_plot_preferido_3 = None
    if _n_clusters > 2:
        _box_plot_actual_2, _box_plot_preferido_2 = \
            CVF_box_plots(xconn, 3, _employees_clusters_df, xwidth=280, 
                          xheight=150)
        if _n_clusters > 3:
            _box_plot_actual_3, _box_plot_preferido_3 = \
                CVF_box_plots(xconn, 4, _employees_clusters_df, xwidth=280, 
                              xheight=150)
                
    xbox_plot_actual_list=[xbox_plot_actual_0, xbox_plot_actual_1, 
                           xbox_plot_actual_2, xbox_plot_actual_3]
    
    _box_plot_actual_list=[_box_plot_actual_0, _box_plot_actual_1, 
                           _box_plot_actual_2, _box_plot_actual_3]
    
    xbox_plot_preferido_list=[xbox_plot_preferido_0, xbox_plot_preferido_1,
                              xbox_plot_preferido_2, xbox_plot_preferido_3]
    
    _box_plot_preferido_list=[_box_plot_preferido_0, _box_plot_preferido_1,
                              _box_plot_preferido_2, _box_plot_preferido_3]
    
    [udpate_theme_box_plot(xbox_plot_actual_list[i],
                           _box_plot_actual_list[i]) for i in range(_n_clusters)]
    
    [udpate_theme_box_plot(xbox_plot_preferido_list[i],
                           _box_plot_preferido_list[i]) \
     for i in range(_n_clusters)]
        
        
    if xselector_cluster.value == "1":
        
        print('>->->->->->->->-> actualizar con xselector_cluster.value == "0"')
        
        update_cluster(xconn, xselector_cluster, _clusters, 
                       _employees_clusters_df,
                       _employee_clusters_culture_list, xthemes_dict, xcvf_plot_1, 
                       xtheme_box_plot_actual_1, xtheme_box_plot_preferido_1, 
                       xcvf_plot_2, 
                       xtheme_box_plot_actual_2, xtheme_box_plot_preferido_2, 
                       xcvf_plot_3,
                       xtheme_box_plot_actual_3, xtheme_box_plot_preferido_3, 
                       xcvf_plot_4, 
                       xtheme_box_plot_actual_4, xtheme_box_plot_preferido_4, 
                       xcvf_plot_5, 
                       xtheme_box_plot_actual_5, xtheme_box_plot_preferido_5, 
                       xcvf_plot_6, 
                       xtheme_box_plot_actual_6, xtheme_box_plot_preferido_6)
        
    else:
        
        print('>->->->->->->->-> actualizar con xselector_cluster.value != "0"')        
        
        xselector_cluster.value = "1"
        
    # column0 = column(cVF_clusters_plots_and_employees[0][0],
    #                  UTBo_EmptyParagraph(20,10), título_peso_actual,
    #                  box_plot_actual_0, UTBo_EmptyParagraph(20,10),
    #                  título_peso_preferido, box_plot_preferido_0,
    #                  UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
    #                  cVF_clusters_plots_and_employees[0][1])
    # column1 = column(cVF_clusters_plots_and_employees[1][0], 
    #                  UTBo_EmptyParagraph(20,10), título_peso_actual,
    #                  box_plot_actual_1, UTBo_EmptyParagraph(20,10),
    #                  título_peso_preferido, box_plot_preferido_1,
    #                  UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
    #                  cVF_clusters_plots_and_employees[1][1])
    # column2 = column()
    # column3 = column()
    # if n_clusters > 2:
    #     box_plot_actual_2, box_plot_preferido_2 = CVF_box_plots(2, xwidth=280, 
    #                                                             xheight=150)
    #     column2 = column(cVF_clusters_plots_and_employees[2][0], 
    #                      UTBo_EmptyParagraph(20,10), título_peso_actual,
    #                      box_plot_actual_2, UTBo_EmptyParagraph(20,10),
    #                      título_peso_preferido, box_plot_preferido_2,
    #                      UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
    #                      cVF_clusters_plots_and_employees[2][1])
    #     if n_clusters > 3:
    #         box_plot_actual_3, box_plot_preferido_3 = CVF_box_plots(3, xwidth=280, 
    #                                                                 xheight=150)
    #         column3 = column(cVF_clusters_plots_and_employees[3][0],
    #                          UTBo_EmptyParagraph(20,10), título_peso_actual,
    #                          box_plot_actual_3, UTBo_EmptyParagraph(20,10),
    #                          título_peso_preferido, box_plot_preferido_3,
    #                          UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
    #                          cVF_clusters_plots_and_employees[3][1])

        


    return 0


def update_cluster(xconn, xselector_cluster, xclusters, xemployees_clusters_df,
                   xemployee_clusters_culture_list, xthemes_dict, xcvf_plot_1, 
                   xtheme_box_plot_actual_1, xtheme_box_plot_preferido_1, 
                   xcvf_plot_2, 
                   xtheme_box_plot_actual_2, xtheme_box_plot_preferido_2, 
                   xcvf_plot_3,
                   xtheme_box_plot_actual_3, xtheme_box_plot_preferido_3, 
                   xcvf_plot_4, 
                   xtheme_box_plot_actual_4, xtheme_box_plot_preferido_4, 
                   xcvf_plot_5, 
                   xtheme_box_plot_actual_5, xtheme_box_plot_preferido_5, 
                   xcvf_plot_6, 
                   xtheme_box_plot_actual_6, xtheme_box_plot_preferido_6):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- update_cluster')
    # print('>>>>>>>>>>>>>>>>>>>>>> xselector_cluster.value (update_cluster)')
    # print(xselector_cluster.value)
    
    _cvf_plot_1, _theme_box_plot_actual_1, _theme_box_plot_preferido_1,\
        _cvf_plot_2, _theme_box_plot_actual_2, _theme_box_plot_preferido_2,\
            _cvf_plot_3, _theme_box_plot_actual_3, _theme_box_plot_preferido_3,\
                _cvf_plot_4, _theme_box_plot_actual_4, \
                    _theme_box_plot_preferido_4, _cvf_plot_5, \
                        _theme_box_plot_actual_5, _theme_box_plot_preferido_5, \
                             _cvf_plot_6, _theme_box_plot_actual_6, \
                                 _theme_box_plot_preferido_6\
                            = FD_build_cluster_detail_plots\
                                (xconn, int(xselector_cluster.value), 
                                 xclusters, xemployees_clusters_df,
                                 xemployee_clusters_culture_list, xthemes_dict)
       
    cvf_plots_list=[(xcvf_plot_1, _cvf_plot_1), (xcvf_plot_2, _cvf_plot_2), 
                    (xcvf_plot_3, _cvf_plot_3), (xcvf_plot_4, _cvf_plot_4),
                    (xcvf_plot_5, _cvf_plot_5), (xcvf_plot_6, _cvf_plot_6)]    
    
    # def udpate_cvf_plot(_xcvf_plot, x_cvf_plot):
    #     datasource = x_cvf_plot.renderers[2].data_source
    #     _xcvf_plot.renderers[2].data_source.data = dict(datasource.data)
            
    [udpate_cvf_plot(xcvf_plot, _cvf_plt) \
      for xcvf_plot, _cvf_plt in cvf_plots_list]
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- inicio update box (update_cluster)')
    
    actual_box_plots_list=[(xtheme_box_plot_actual_1, _theme_box_plot_actual_1),
                           (xtheme_box_plot_actual_2, _theme_box_plot_actual_2),
                           (xtheme_box_plot_actual_3, _theme_box_plot_actual_3),
                           (xtheme_box_plot_actual_4, _theme_box_plot_actual_4),
                           (xtheme_box_plot_actual_5, _theme_box_plot_actual_5),
                           (xtheme_box_plot_actual_6, _theme_box_plot_actual_6)]    
        
    # def udpate_theme_box_plot(_xtheme_box_plot_actual, x_theme_box_plot_actual):
        
    #     for i in range(0,6):
    #         # print('i')
    #         # print(i)
    #         datasource = x_theme_box_plot_actual.renderers[i].data_source
    #         _xtheme_box_plot_actual.renderers[i].data_source.data = \
    #             dict(datasource.data)            
            
    [udpate_theme_box_plot(xtheme_box_plot_actual, _theme_box_plot_actual) \
      for xtheme_box_plot_actual, _theme_box_plot_actual in \
          actual_box_plots_list]
    
    preferido_box_plots_list = \
        [(xtheme_box_plot_preferido_1, _theme_box_plot_preferido_1),
         (xtheme_box_plot_preferido_2, _theme_box_plot_preferido_2),
         (xtheme_box_plot_preferido_3, _theme_box_plot_preferido_3),
         (xtheme_box_plot_preferido_4, _theme_box_plot_preferido_4),
         (xtheme_box_plot_preferido_5, _theme_box_plot_preferido_5),
         (xtheme_box_plot_preferido_6, _theme_box_plot_preferido_6)]    
        
    [udpate_theme_box_plot(xtheme_box_plot_preferido, _theme_box_plot_preferido) \
      for xtheme_box_plot_preferido, _theme_box_plot_preferido in \
          preferido_box_plots_list]
        
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- fin update box (update_cluster)')
    
    
def FD_employee_cluster_culture(xconn, xemployees_clusters_df, xcluster):
    
    print('.-.-.-.-.-.-.-.-.-. FD_employee_cluster_culture')
    # print('>>>>>>>>>>>>>>>>>>>>>> xcluster (FD_employee_cluster_culture)')
    # print(xcluster)
    # print('>>>>>>>>>>>>> xemployees_clusters_df (FD_employee_cluster_culture)')
    # print(xemployees_clusters_df)
    
    cluster_employees = \
        xemployees_clusters_df.loc[xemployees_clusters_df.cluster == xcluster]
    
    # print('>>>>>>>>>>>>>>>> cluster employees (FD_employee_cluster_culture)')
    # print(cluster_employees)
    
    employee_cluster_culture = \
        FD_employee_list_score(xconn, list(cluster_employees['id_employee']))
    
    # print('>>>>>>>>>> employee_cluster_culture (FD_employee_cluster_culture)')
    # print(employee_cluster_culture)
        
    return employee_cluster_culture


def CVF_box_plots(xconn, _xcluster, xemployees_clusters_df, 
                  _xculture_mode_theme = -1, 
                  xheight = 200, 
                  xwidth = 225):
    
    # print('-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. CVF_box_plots')
    # print('.-.-.-.-.-.-.-._xcluster (CVF_box_plots)')
    # print(_xcluster)

    employees_in_cluster = \
        list(xemployees_clusters_df.loc[xemployees_clusters_df.cluster==_xcluster]\
             ['id_employee'])
    # print('.-.-.-.-.-.-.-.employees_in_cluster (CVF_box_plots)')
    # print(employees_in_cluster)

    cluster_detail_actual_df = pd.DataFrame()
    cluster_detail_preferred_df = pd.DataFrame()
    
    for employee_id in employees_in_cluster:
        
        questions_responses_df = FD_fetch_employee_culture_GDB(xconn, 
                                                               employee_id)
        if _xculture_mode_theme != -1:
            questions_responses_df = \
                questions_responses_df.loc\
                    [questions_responses_df.id_culture_mode_theme==_xculture_mode_theme]
        # cluster_detail_actual_df = \
        #     cluster_detail_actual_df.append(questions_responses_df,
        #                                     ignore_index = True)\
        #         [["culture_quadrant", "Actual"]]
        cluster_detail_actual_df = \
            pd.concat([cluster_detail_actual_df, questions_responses_df], 
                      ignore_index=True)\
                [["culture_quadrant", "Actual"]]
        # cluster_detail_preferred_df = \
        #     cluster_detail_preferred_df.append(questions_responses_df,
        #                                     ignore_index = True)\
        #         [["culture_quadrant", "Preferred"]]
        cluster_detail_preferred_df = \
            pd.concat([cluster_detail_preferred_df, questions_responses_df], 
                      ignore_index=True)\
                [["culture_quadrant", "Preferred"]]
                
    box_plot_actual = FD_horizontal_box_plot(cluster_detail_actual_df, 
                                             'culture_quadrant', 'Actual',
                                             _xheight = xheight, _xwidth = xwidth)
    box_plot_preferido = FD_horizontal_box_plot(cluster_detail_preferred_df, 
                                                'culture_quadrant', 'Preferred',
                                                _xheight = xheight, _xwidth = xwidth)

    return box_plot_actual, box_plot_preferido

def FD_plots_culture_mode_theme(xconn, xcluster, xculture_mode_theme, 
                                xthemes_dict,
                                xemployee_clusters_culture_list,
                                xemployees_clusters_df,
                                xwidth=225, xheight=200,
                                xbox_height=225, xbox_width=200):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.- FD_plots_culture_mode_theme')
    # print('>>>>>>>>>>>>>>>>>>>>>> xcluster (FD_plots_culture_mode_theme)')
    # print(xcluster)
    # print('>>>>> xemployee_clusters_culture_list (FD_plots_culture_mode_theme)')
    # print(xemployee_clusters_culture_list)
    
    # se va a hacer una prueba de un plot
    #coordenadas del plot
    #se usa cluster-1 por que los npumeros de los clusters comienzan en 1
    actual_coordinates = \
        FD_plot_weights_position(xemployee_clusters_culture_list\
                                 [xcluster-1][0][xculture_mode_theme-1])
    preferred_coordinates = \
        FD_plot_weights_position(xemployee_clusters_culture_list\
                                 [xcluster-1][1][xculture_mode_theme-1])
    
    title1, title2 = xthemes_dict.get(xculture_mode_theme).split(" ",1)
    
    # print('>>>>>>>>> actual_coordinates (FD_plots_culture_mode_theme)')
    # print(actual_coordinates)

    CVF_plot = FD_CVF_plot_single(actual_coordinates, preferred_coordinates,
                            _xwidth = xwidth, _xheight = xheight,
                            xtitle_font_size = '10pt')
    
    box_plot_actual, box_plot_preferido = \
        CVF_box_plots(xconn, xcluster, xemployees_clusters_df, 
                      _xculture_mode_theme = xculture_mode_theme,
                      xwidth = xbox_width, xheight = xbox_height)    
    
    return CVF_plot, box_plot_actual, box_plot_preferido 


def FD_CVF_Cluster_plot(xcluster, xemployee_clusters_culture_list, 
                        xemployees_clusters_df, xira_employees_areas,
                        xwidth=280, xheight=250):
    
    print('.-.-.-.-.-.-.-.-.- oihub_CVF_Clusters/FD_CVF_Cluster_plot')
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_CVF_Cluster_plot')
    # print('>>>>>>>>> xcluster (FD_CVF_Cluster_plot)')
    # print(xcluster)
    # print('>>>>>>>>> xemployee_clusters_culture_list (FD_CVF_Cluster_plot)')
    # print(xemployee_clusters_culture_list)
    # print('>>>>>>>>> xemployees_clusters_df (FD_CVF_Cluster_plot)')
    # print(xemployees_clusters_df)
    # print('>>>>>>>>> xira_employees_areas (FD_CVF_Cluster_plot)')
    # print(xira_employees_areas)
    
    #se pone cluster-1 porque los clusters empiezan en 1
    actual_weights = \
        (xemployee_clusters_culture_list[xcluster-1][0].sum(axis=0))/6
    preferred_weights = \
        (xemployee_clusters_culture_list[xcluster-1][1].sum(axis=0))/6
    # print('>>>>>>>>> actual_weights (FD_CVF_Cluster_plot)')
    # print(actual_weights)
    # print('>>>>>>>>> preferred_weights (FD_CVF_Cluster_plot)')
    # print(preferred_weights)
    
    
    
    actual_coordinates = \
        FD_plot_weights_position(actual_weights)
    preferred_coordinates = \
        FD_plot_weights_position(preferred_weights)
        
    # print('>>>>>>>>> actual_coordinates (FD_CVF_Cluster_plot)')
    # print(actual_coordinates)
    
    title = "Cluster: "+str(xcluster)
    
    CVF_plot = FD_CVF_plot_single(actual_coordinates, preferred_coordinates,
                            xtitle1 = title, _xwidth = xwidth, _xheight = xheight)
    
    cluster_employees_df = \
        xemployees_clusters_df.loc[xemployees_clusters_df.cluster==xcluster]
    # print('>>>>>>>>> cluster_employees_df (FD_CVF_Cluster_plot)')
    # print(cluster_employees_df)
    cluster_employees_df = \
        cluster_employees_df.merge(xira_employees_areas,left_on='id_employee',
                                   right_on='id_employee', how='left')  
    
    source = ColumnDataSource(data=cluster_employees_df[['id_employee','employee',
                                                         'organization_area']])

    tbl_columns = [
        TableColumn(field="id_employee", title="ID", width=20),
        TableColumn(field="employee", title="Funcionario", width=130),
        TableColumn(field="organization_area", title="Area", width=130)
    ]

    employees_in_cluster_table = DataTable(source=source, columns=tbl_columns,
                                           editable=False,
                                           index_position=None,
                                           fit_columns=False,
                                           width = xwidth, height = xheight)
    
    # def cluster_to_string(xcluster):
    #     return 'Cluster'+str(xcluster)
    cluster_employees_df['cluster_str'] = \
        cluster_employees_df.apply(lambda row: 'Cluster-'+str(row.cluster), 
                                   axis = 1)

    
    return CVF_plot, employees_in_cluster_table, cluster_employees_df
    



# a=FD_fetch_employee_culture_GDB(93)
# a.to_dict('records')

# def FD_GDB_fetch_ira_employees_areas(xvalid_employees):
    
#     print('.-.-.-.-.-.-.-.-.-.- FD_GDB_fetch_ira_employees_areas')

#     query = """MATCH (e:Employee)-[FUNCIONARIO_DE]->(a:Organization_area) 
#                 WHERE e.is_active = True AND e.id_employee IS NOT NULL
#                 RETURN e.id_employee AS id_employee, e.redmine_login AS id_user, 
#                 e.employee AS employee,
#                 a.id_organization_area AS id_organization_area, 
#                 a.organization_area AS organization_area
#             """
            
#     result = conn.query(query) #, parameters=params)
    
#     _ira_employees_areas = pd.DataFrame([dict(_) for _ in result])
    
#     print('>>>>>>>>> _ira_employees_areas (FD_GDB_fetch_ira_employees_areas)')
#     print(_ira_employees_areas)

#     #.-.-.-.-.-.-.- Temporal
#     # with session_scope() as session:
#     #     culture_input_forms = session.query(CVF_Culture_input_form).all()

#     # culture_input_forms

#     # culture_input_forms_tuples = [(cif.id, cif.id_employee, cif.id_cycle,
#     #                                 cif.id_culture_mode, cif.Is_concluded) \
#     #                                     for cif in culture_input_forms]
#     # culture_input_forms_df = \
#     #     pd.DataFrame.from_records(culture_input_forms_tuples, 
#     #                               columns=['id', 'id_employee',
#     #                                         'id_cycle', 'id_culture_mode',
#     #                                         'Is_concluded'])

#     # valid_employees = list(culture_input_forms_df.loc\
#     #                         [culture_input_forms_df.Is_concluded == True]\
#     #                             ['id_employee'])
#     # print('>>>>>>>>> valid_employees (FD_GDB_fetch_ira_employees_areas)')
#     # print(valid_employees)
        
#     # non_clustered_employees = list(culture_input_forms_df.loc\
#     #                         [culture_input_forms_df.Is_concluded == False]\
#     #                             ['id_employee'])
    
#     _ira_employees_areas = \
#         _ira_employees_areas.loc[_ira_employees_areas['id_employee'].\
#                                 isin(xvalid_employees)]
#     #:_:_:_:_:_:_:_:_:_:_ fin temporal

#     #%%

#     # print('>>>>>>>>> _ira_employees_areas (FD_GDB_fetch_ira_employees_areas)')
#     # print(_ira_employees_areas)
#     # print('>>>>>>>>>non_clustered_employees (FD_GDB_fetch_ira_employees_areas)')
#     # print(non_clustered_employees)


#     return _ira_employees_areas
# , non_clustered_employees



def FD_fetch_themes_dictionary(xconn):
    query = """match(t:Tema) RETURN t.id_tema, t.tema"""
    
    themes = xconn.query(query)
    themes_df = pd.DataFrame([dict(_) for _ in themes])
    themes_df
    _themes_dict = dict(zip(themes_df['t.id_tema'], themes_df['t.tema']))
    return _themes_dict


#%% Clustering

def FD_calculate_silhouette(xn_clusters, xdata):
    clusterer = KMeans(n_clusters=xn_clusters, max_iter=10000,
                          random_state=3425, n_init=10)
    preds = clusterer.fit_predict(xdata)
    centers = clusterer.cluster_centers_

    score = silhouette_score(xdata, preds)
    
    return score
    

def FD_CVF_build_clusters(xconn, xira_employees_areas, xmeasure, 
                          xn_clusters = 0):
    
    print('.-.-.-.-.-.-.-.-.-.- oihub_CVF_Clusters/FD_CVF_build_clusters')
    
    # print('>>>>>>>>>>>>>>>>>>>> xmeasure FD_CVF_build_clusters')
    # print(xmeasure)
    # print('>>>>>>>>>>>>>>> xira_employees_areas (FD_CVF_build_clusters)')
    # print(xira_employees_areas)
    
    if xmeasure == 'Preferido':
        xmeasure = 'Preferred'

    responses_df = pd.DataFrame()

    for id_employee in list(xira_employees_areas['id_employee']):
        
        employee_responses = FD_fetch_employee_culture_GDB(xconn, id_employee)
        # print('>>>>>>>>>>>>>>> employee_responses.shape (FD_CVF_build_clusters)')
        # print(employee_responses.shape)
        
        employee_responses['id_employee'] = id_employee
        
        # responses_df = responses_df.append(employee_responses, ignore_index = True)
        responses_df = pd.concat([responses_df, employee_responses], 
                                 ignore_index=True)
    # responses_df = 
    responses_df.sort_values(['id_employee', 'id_culture_mode_theme_question'], 
                             ascending=[True, True], inplace=True)       
    
    print('>>>>>>>>>>>>>>>>>>>>>>>> responses_df (FD_CVF_build_clusters)')
    print(responses_df.loc[responses_df.id_employee==1].to_dict('records'))
    print(responses_df.loc[responses_df.id_employee==1].shape)
    
    UT_CountOcurrences(responses_df, ['id_culture_mode_theme_question']) 
    
    responses_pivot_df = \
        responses_df.pivot_table(index=['id_employee'], 
                                 columns='id_culture_mode_theme_question',
                                 values = xmeasure).reset_index()
                                 # values='Preferred').reset_index()
        
    fetched_employee_id = list(responses_pivot_df['id_employee'])
    
    print('>>>>>>>>>>>>>>>>>>>>>>>> responses_pivot_df (FD_CVF_build_clusters)')
    print(responses_pivot_df.to_dict('records'))
    
    # a=5/0
    
    responses_pivot_df.drop(columns=['id_employee'],inplace=True)
    
    
    responses_pivot_array = responses_pivot_df.to_numpy()
    
    if xn_clusters == 0:
    
        silhouettes_list= [FD_calculate_silhouette(n_clusters, responses_pivot_array) \
                         for n_clusters in range(2,5)]
        # print('>>>>>>>>>>>>>>>>  silhouettes_list (FD_CVF_build_clusters)')
        # print(silhouettes_list)
        
        max_silhouette = max(silhouettes_list)
        # print('>>>>>>>>>>>>>>>>  max_silhouette (FD_CVF_build_clusters)')
        # print(max_silhouette)
        max_silhouette_index = int(silhouettes_list.index(max_silhouette))
        # print('>>>>>>>>>>>>>>>>  max_silhouette_index (FD_CVF_build_clusters)')
        # print(max_silhouette_index)
        n_clusters = max_silhouette_index + 2
        
    else:
        
        n_clusters = xn_clusters

    
    kmeans_model = KMeans(n_clusters = n_clusters, max_iter=10000,
                          random_state=3425, n_init=10).\
        fit(responses_pivot_array)
    
    _clusters = 1 + kmeans_model.labels_
    # print('.-.-.-.-.-.-.- _clusters (FD_CVF_build_clusters)')   
    # print(_clusters)   
    
    _employees_clusters_df = \
        pd.DataFrame({'id_employee':fetched_employee_id, 'cluster':_clusters})
    # print('.-.-.-.-.-.-.- employees_clusters_df (FD_CVF_build_clusters)')   
    # print(_employees_clusters_df) 
    
    return n_clusters, _clusters, _employees_clusters_df


def FD_build_employee_clusters_culture_list(xconn, xclusters, 
                                            xemployees_clusters_df):
    """
    Devuelve una lista de n posiciones, donde n es el número de clusters.
    - Cada elemento es una lista de 2 posiciones.
      - Cada posición son 6 vectores, cada uno con los pesos promedio del
        cluster (4) de cada tema
        - el orden es: - caracteríticas dominantes
                       - liderazgo organizacional
                       - manejo de empleados
                       - cohesión organizacional
                       - énfasis estratégico
                       - criterios de éxito
      - La primera posición son valores 'Actual' y la segunda 'Preferido'
    """
    
    _employee_clusters_culture_list = \
        [FD_employee_cluster_culture(xconn, xemployees_clusters_df, 
                                     cluster_number) \
         for cluster_number in range(1, 1+len(set(xclusters)))]
            
    # _employee_clusters_culture_list[0][0][0]
    # _employee_clusters_culture_list[0][1][0]
    # a=_employee_clusters_culture_list[0][0]
    # _employee_clusters_culture_list
    
    # len(_employee_clusters_culture_list)
    # len(_employee_clusters_culture_list[0])
    # len(_employee_clusters_culture_list[0][0])
    # len(_employee_clusters_culture_list[0][0][0])
    
    return _employee_clusters_culture_list


def FD_build_cluster_detail_plots(xconn, xcluster, xclusters, 
                                  xemployees_clusters_df,
                                  xemployee_clusters_culture_list, 
                                  xthemes_dict):
    
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> FD_build_cluster_detail_plots')
    # print('.-.-.-.-.-.-.-.-.-.-. xcluster (FD_build_cluster_detail_plots)')
    # print(xcluster)

    FD_employee_list_score(xconn, [12])
    FD_employee_list_score(xconn, [93])
    FD_employee_list_score(xconn, [12,93])
    # a=FD_fetch_employee_culture_GDB(93)
    #devuelve dos arrays de 6x4 con los promedios de las repuestas.
    #El primer array es Actual, el segundo es Preferred 
    
    
        
    #una lista de 4 posiciones (una por cluster)
    #cada posición tiene 2 arrays con los promedios de Actual y Preferred
    #cada array tiene 6 filas, una por tema, y 4 columnas, 1 por cuadrante
    
    detail_width = 200
    detail_height = 200
    box_width = 200
    box_height = 150
    
    # xcluster, xculture_mode_theme, xthemes_dict,
    #                                 xemployee_clusters_culture_list,
    
    _CVF_plot_1, _theme_box_plot_actual_1, _theme_box_plot_preferido_1 = \
        FD_plots_culture_mode_theme(xconn, xcluster,1, xthemes_dict, 
                                    xemployee_clusters_culture_list,
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
    _CVF_plot_2, _theme_box_plot_actual_2, _theme_box_plot_preferido_2 = \
        FD_plots_culture_mode_theme(xconn, xcluster,2, xthemes_dict, 
                                    xemployee_clusters_culture_list, 
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
    _CVF_plot_3, _theme_box_plot_actual_3, _theme_box_plot_preferido_3 = \
        FD_plots_culture_mode_theme(xconn, xcluster,3, xthemes_dict, 
                                    xemployee_clusters_culture_list,
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
    _CVF_plot_4, _theme_box_plot_actual_4, _theme_box_plot_preferido_4 = \
        FD_plots_culture_mode_theme(xconn, xcluster,4, xthemes_dict, 
                                    xemployee_clusters_culture_list,
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
    _CVF_plot_5, _theme_box_plot_actual_5, _theme_box_plot_preferido_5 = \
        FD_plots_culture_mode_theme(xconn, xcluster,5, xthemes_dict, 
                                    xemployee_clusters_culture_list,
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
    _CVF_plot_6, _theme_box_plot_actual_6, _theme_box_plot_preferido_6 = \
        FD_plots_culture_mode_theme(xconn, xcluster,6, xthemes_dict, 
                                    xemployee_clusters_culture_list,
                                    xemployees_clusters_df,
                                    xwidth=detail_width, 
                                    xheight=detail_height,
                                    xbox_height=box_height, 
                                    xbox_width=box_width)
        
    return _CVF_plot_1, _theme_box_plot_actual_1, _theme_box_plot_preferido_1,\
        _CVF_plot_2, _theme_box_plot_actual_2, _theme_box_plot_preferido_2,\
            _CVF_plot_3, _theme_box_plot_actual_3, _theme_box_plot_preferido_3,\
                _CVF_plot_4, _theme_box_plot_actual_4, \
                    _theme_box_plot_preferido_4, _CVF_plot_5, \
                        _theme_box_plot_actual_5, _theme_box_plot_preferido_5, \
                            _CVF_plot_6, _theme_box_plot_actual_6, \
                                _theme_box_plot_preferido_6 
    

#%% Main


def FD_CVF_Clusters_Main(xconn, xmeasurement_option_index, 
                         xira_employees_areas = pd.DataFrame()):
    print('.-.-.-.-.-.-.-..-.-.-.-.-.-.- oihub_CVF_Clusters/FD_CVF_Clusters_Main')
    
    if xira_employees_areas.shape == (0,0):    
        xira_employees_areas = FD_fetch_valid_employees_areas(xconn)
    # ira_employees_areas = \
    #     FD_GDB_fetch_ira_employees_areas(xvalid_employees)
    # print('>>>>>>>>>>>>>>>>>>>>>>> xira_employees_areas FD_CVF_Clusters_Main')
    # print(xira_employees_areas)
    
    themes_dict = FD_fetch_themes_dictionary(xconn)
    
    measurement_options = ['Actual', 'Preferido']
    start_measurement_option = measurement_options[xmeasurement_option_index]
    
    n_clusters, clusters, employees_clusters_df = \
        FD_CVF_build_clusters(xconn, xira_employees_areas, 
                              start_measurement_option)
    
    clusters_options = [str(n) for n in range(1, 1 + n_clusters)]
    
    selector_cluster = Select(title="Seleccione Cluster", value="1",
                            options = clusters_options, width=200)
    
    selector_cluster.\
        on_change('value', lambda attr, old, new: \
                  update_cluster(xconn, selector_cluster, clusters, 
                                 employees_clusters_df,
                                  employee_clusters_culture_list, themes_dict, 
                                  cvf_plot_1, theme_box_plot_actual_1, 
                                  theme_box_plot_preferido_1,
                                  cvf_plot_2, theme_box_plot_actual_2, 
                                  theme_box_plot_preferido_2, 
                                  cvf_plot_3, theme_box_plot_actual_3, 
                                  theme_box_plot_preferido_3, 
                                  cvf_plot_4, theme_box_plot_actual_4, 
                                  theme_box_plot_preferido_4, 
                                  cvf_plot_5, theme_box_plot_actual_5, 
                                  theme_box_plot_preferido_5, 
                                  cvf_plot_6, theme_box_plot_actual_6, 
                                  theme_box_plot_preferido_6))
    
    selector_measure = Select(title="Seleccione medida", 
                              value = start_measurement_option,
                              options = measurement_options, width=200)
    
    selector_measure.\
        on_change('value', lambda attr, old, new: \
                  update_clusters_measure(xconn, selector_measure, 
                                          xira_employees_areas,
                                          themes_dict, n_clusters,
                                          cVF_clusters_plots_and_employees,
                                          box_plot_actual_0, box_plot_preferido_0,
                                          box_plot_actual_1, box_plot_preferido_1,
                                          box_plot_actual_2, box_plot_preferido_2,
                                          box_plot_actual_3, box_plot_preferido_3,
                                          selector_cluster,
                                          cvf_plot_1, theme_box_plot_actual_1, 
                                          theme_box_plot_preferido_1,
                                          cvf_plot_2, theme_box_plot_actual_2, 
                                          theme_box_plot_preferido_2, 
                                          cvf_plot_3, theme_box_plot_actual_3, 
                                          theme_box_plot_preferido_3, 
                                          cvf_plot_4, theme_box_plot_actual_4, 
                                          theme_box_plot_preferido_4, 
                                          cvf_plot_5, theme_box_plot_actual_5, 
                                          theme_box_plot_preferido_5, 
                                          cvf_plot_6, theme_box_plot_actual_6, 
                                          theme_box_plot_preferido_6))
    
    
    
    employee_clusters_culture_list = \
        FD_build_employee_clusters_culture_list(xconn, clusters, 
                                                employees_clusters_df)
        
    # print('>>>>>>>>>>>>>>>>>>>>> employee_clusters_culture_list (FD_CVF_Clusters_Main)')
    # print(employee_clusters_culture_list)
    # len(employee_clusters_culture_list)
    # len(employee_clusters_culture_list[0])
    # employee_clusters_culture_list[1]
    # len(employee_clusters_culture_list[1])
    # employee_clusters_culture_list[0][0]
    # employee_clusters_culture_list[0][0][0]
    # employee_clusters_culture_list[0][1]
    # employee_clusters_culture_list[0][1][0]
    # a=employee_clusters_culture_list[0][0]
    # employee_clusters_culture_list
    
    # len(employee_clusters_culture_list)
    # len(employee_clusters_culture_list[0])
    # len(employee_clusters_culture_list[0][0])
    # len(employee_clusters_culture_list[0][0][0])
        
    cvf_plot_1, theme_box_plot_actual_1, theme_box_plot_preferido_1,\
        cvf_plot_2, theme_box_plot_actual_2, theme_box_plot_preferido_2,\
            cvf_plot_3, theme_box_plot_actual_3, theme_box_plot_preferido_3,\
                cvf_plot_4, theme_box_plot_actual_4, theme_box_plot_preferido_4,\
                    cvf_plot_5, theme_box_plot_actual_5, theme_box_plot_preferido_5, \
                        cvf_plot_6, theme_box_plot_actual_6, theme_box_plot_preferido_6\
                            = FD_build_cluster_detail_plots\
                                (xconn, clusters[0], clusters, employees_clusters_df,
                                  employee_clusters_culture_list, themes_dict)
    
    
    
    
    #%%
    
    título_lista_funcionarios = Div(text="<b>Funcionarios en cluster</b>",visible=True,
                   styles={'font-size': '130%', 'color': 'black',
                          'text-align': 'center'})
    título_peso_actual = Div(text="<b>Peso actual</b>",visible=True,
                   styles={'font-size': '130%', 'color': 'black',
                          'text-align': 'center'})
    título_peso_preferido = Div(text="<b>Peso preferido</b>",visible=True,
                   styles={'font-size': '130%', 'color': 'black',
                          'text-align': 'center'})
    
    def FD_armar_título(xtexto, xfont_size):
        título = Div(text="<b>"+xtexto+"</b>", visible=True,
                       styles={'font-size': xfont_size, 'color': 'black',
                              'text-align': 'center'})
        return título
        
        
    título_características_dominantes = \
        FD_armar_título(themes_dict.get(1), '130%')
    título_características_dominantes = \
        FD_armar_título(themes_dict.get(2), '130%')
    
    
    _cluster_detail_dashboard = column(row(selector_cluster),
                                      row(column(FD_armar_título(themes_dict.get(1), 
                                                                  '130%'),
                                                  cvf_plot_1, 
                                                  título_peso_actual,
                                                  theme_box_plot_actual_1,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_1),
                                          column(FD_armar_título(themes_dict.get(2), 
                                                                      '130%'),
                                                  cvf_plot_2, 
                                                  título_peso_actual,
                                                  theme_box_plot_actual_2,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_2),
                                          column(FD_armar_título(themes_dict.get(3), 
                                                                      '130%'),
                                                  cvf_plot_3, 
                                                  título_peso_actual,
                                                  theme_box_plot_actual_3,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_3),
                                          column(FD_armar_título(themes_dict.get(4), 
                                                                      '130%'),
                                                  cvf_plot_4,
                                                  título_peso_actual,
                                                  theme_box_plot_actual_4,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_4),
                                          column(FD_armar_título(themes_dict.get(5), 
                                                                      '130%'),
                                                  cvf_plot_5, 
                                                  título_peso_actual,
                                                  theme_box_plot_actual_5,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_5),
                                          column(FD_armar_título(themes_dict.get(6), 
                                                                      '130%'),
                                                  cvf_plot_6, 
                                                  título_peso_actual,
                                                  theme_box_plot_actual_6,
                                                  título_peso_preferido,
                                                  theme_box_plot_preferido_6)))
    
    
    
    cVF_clusters_plots_and_employees = \
        [FD_CVF_Cluster_plot(cluster, employee_clusters_culture_list,
                             employees_clusters_df, xira_employees_areas) \
         for cluster in range(1, 1+n_clusters)] 
    
    box_plot_actual_0, box_plot_preferido_0 = \
        CVF_box_plots(xconn, 1, employees_clusters_df, xwidth=280, xheight=150)
    box_plot_actual_1, box_plot_preferido_1 = \
        CVF_box_plots(xconn, 2, employees_clusters_df, xwidth=280, xheight=150)
    box_plot_actual_2 = None
    box_plot_actual_3 = None
    box_plot_preferido_2 = None
    box_plot_preferido_3 = None
    
    # clusters_df = cVF_clusters_plots_and_employees[0][2].\
    #     append(cVF_clusters_plots_and_employees[1][2])
    clusters_df = pd.concat([cVF_clusters_plots_and_employees[0][2],
                             cVF_clusters_plots_and_employees[1][2]], 
                            ignore_index=True)
    
    
    column0 = column(cVF_clusters_plots_and_employees[0][0],
                     UTBo_EmptyParagraph(20,10), título_peso_actual,
                     box_plot_actual_0, UTBo_EmptyParagraph(20,10),
                     título_peso_preferido, box_plot_preferido_0,
                     UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
                     cVF_clusters_plots_and_employees[0][1])
    column1 = column(cVF_clusters_plots_and_employees[1][0], 
                      UTBo_EmptyParagraph(20,10), título_peso_actual,
                      box_plot_actual_1, UTBo_EmptyParagraph(20,10),
                      título_peso_preferido, box_plot_preferido_1,
                      UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
                      cVF_clusters_plots_and_employees[1][1])
    # column1 = column()
    column2 = column()
    column3 = column()
    if n_clusters > 2:
        box_plot_actual_2, box_plot_preferido_2 = \
            CVF_box_plots(xconn, 3, employees_clusters_df, xwidth=280, xheight=150)
        column2 = column(cVF_clusters_plots_and_employees[2][0], 
                         UTBo_EmptyParagraph(20,10), título_peso_actual,
                         box_plot_actual_2, UTBo_EmptyParagraph(20,10),
                         título_peso_preferido, box_plot_preferido_2,
                         UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
                         cVF_clusters_plots_and_employees[2][1])
        # clusters_df = clusters_df.append(cVF_clusters_plots_and_employees[2][2])
        clusters_df = pd.concat([clusters_df,
                                 cVF_clusters_plots_and_employees[2][2]], 
                                ignore_index=True)
        if n_clusters > 3:
            box_plot_actual_3, box_plot_preferido_3 = \
                CVF_box_plots(xconn, 4, employees_clusters_df, xwidth=280, xheight=150)
            column3 = column(cVF_clusters_plots_and_employees[3][0],
                             UTBo_EmptyParagraph(20,10), título_peso_actual,
                             box_plot_actual_3, UTBo_EmptyParagraph(20,10),
                             título_peso_preferido, box_plot_preferido_3,
                             UTBo_EmptyParagraph(20,10), título_lista_funcionarios,
                             cVF_clusters_plots_and_employees[3][1])
            # clusters_df = \
            #     clusters_df.append(cVF_clusters_plots_and_employees[3][2])
            clusters_df = pd.concat([clusters_df,
                                     cVF_clusters_plots_and_employees[3][2]], 
                                    ignore_index=True)
            
    
    _clusters_dashboard = column(row(selector_measure),
                                row(column0,
                                    column(UTBo_EmptyParagraph(20,10)),
                                    column1,
                                    column(UTBo_EmptyParagraph(20,10)),
                                    column2,
                                    column(UTBo_EmptyParagraph(20,10)),
                                    column3))
    
    return _clusters_dashboard, _cluster_detail_dashboard, clusters_df


# def FD_CVF_Clusters_DF(xconn, xmeasurement_option_index, 
#                          xira_employees_areas = pd.DataFrame()):
def FD_CVF_Clusters_df(xconn, xmeasurement_option_index, 
                         xira_employees_areas = pd.DataFrame()):
    
    if xira_employees_areas.shape == (0,0):    
        xira_employees_areas = FD_fetch_valid_employees_areas(xconn)

    measurement_options = ['Actual', 'Preferido']
    start_measurement_option = measurement_options[xmeasurement_option_index]
    
    n_clusters, clusters, employees_clusters_df = \
        FD_CVF_build_clusters(xconn, xira_employees_areas, 
                              start_measurement_option)
    employee_clusters_culture_list = \
        FD_build_employee_clusters_culture_list(xconn, clusters, 
                                                employees_clusters_df)
    
    cVF_clusters_plots_and_employees = \
        [FD_CVF_Cluster_plot(cluster, employee_clusters_culture_list,
                             employees_clusters_df, xira_employees_areas) \
         for cluster in range(1, 1+n_clusters)] 
    
    clusters_df = pd.concat([cVF_clusters_plots_and_employees[0][2],
                             cVF_clusters_plots_and_employees[1][2]], 
                            ignore_index=True)
    
    if n_clusters > 2:
        # clusters_df = clusters_df.append(cVF_clusters_plots_and_employees[2][2])
        clusters_df = pd.concat([clusters_df,
                                 cVF_clusters_plots_and_employees[2][2]], 
                                ignore_index=True)
        if n_clusters > 3:
            # clusters_df = \
            #     clusters_df.append(cVF_clusters_plots_and_employees[3][2])
            clusters_df = pd.concat([clusters_df,
                                     cVF_clusters_plots_and_employees[3][2]], 
                                    ignore_index=True)
                

    return clusters_df
    
    
    