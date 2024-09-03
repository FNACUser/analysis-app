# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 21:55:53 2023

@author: luis.caro
"""

from bokeh.layouts import row, column
from bokeh.io import curdoc
from bokeh.models import Div, Tabs, TabPanel

from defaultapp.bkhapps.common.neo4j_learn_ONA import conn, insert_data
# from defaultapp.bkhapps.common.neo4j_connection_sandbox import conn, insert_data

from .oihub_CVF_Actor_item_ranking import FD_Main_actor_item_ranking

from .oihub_CVF_Analysis import FD_Main_analysis

from .oihub_CVF_Clusters import FD_CVF_Clusters_Main

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph




def FD_Main():
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.oihub_CVF_Model/FD_Main')
    
    company = 'bacanos'
    if company == 'bacanos':
        ids_employees_to_exclude_from_average = [7]
    else:
        ids_employees_to_exclude_from_average = []
    
    cvf_plot1, cvf_plot2, cvf_plot3, cvf_plot4, cvf_plot5, cvf_plot6,  \
        selector_cycle, selector_employee, selector_organization_area,\
            cvf_plot_average, ira_employees_areas =\
                FD_Main_analysis(conn, ids_employees_to_exclude_from_average)
    
    segment_plots = column(row(cvf_plot1, UTBo_EmptyParagraph(10,5), 
                               cvf_plot2, UTBo_EmptyParagraph(10,5),cvf_plot3),
                           UTBo_EmptyParagraph(95,10),
                           row(cvf_plot4, UTBo_EmptyParagraph(10,5), cvf_plot5,
                               UTBo_EmptyParagraph(10,5), cvf_plot6))
            
    child_analysis = column(row(selector_cycle, selector_employee, 
                                 selector_organization_area),
                             row(segment_plots, UTBo_EmptyParagraph(10,5),
                                 cvf_plot_average))
    
    tab_analysis = TabPanel(child = child_analysis, 
                            title = "Análisis individual")
    
    preferred_actual_radio_group, top_bottom_radio_group, culture_theme_select, \
        plots, box_plots = FD_Main_actor_item_ranking(conn, 
                                                      ira_employees_areas) 
    
    child_actor_item_ranking = column(row(UTBo_EmptyParagraph(20,5),
                                          preferred_actual_radio_group,
                                          UTBo_EmptyParagraph(20,5),
                                          top_bottom_radio_group,
                                  UTBo_EmptyParagraph(20,5),
                                  culture_theme_select),
                              row(column(plots[0][0],UTBo_EmptyParagraph(20,5),
                                        box_plots[0]),
                                  UTBo_EmptyParagraph(1,5),
                                  column(plots[1][0],UTBo_EmptyParagraph(20,5),
                                        box_plots[1]),
                                  UTBo_EmptyParagraph(1,5),
                                  column(plots[2][0],UTBo_EmptyParagraph(20,5),
                                        box_plots[2]),
                                  UTBo_EmptyParagraph(1,5),
                                  column(plots[3][0],UTBo_EmptyParagraph(20,5),
                                        box_plots[3])))
    
    tab_actor_item_ranking = TabPanel(child = child_actor_item_ranking, 
                                      title = "Orden items cultura")
    
    
    if ira_employees_areas.shape[0] > 0:
        clusters_dashboard, cluster_detail_dashboard, clusters_list = \
            FD_CVF_Clusters_Main(conn, 0, 
                                 xira_employees_areas = ira_employees_areas)
    
        tab_comparativo_clusters = \
            TabPanel(child = clusters_dashboard, title = "Comparativo clusters")
    
        tab_detalle_cluster = \
            TabPanel(child = cluster_detail_dashboard, title = "Detalle cluster")
        
        child_cluster = Tabs(tabs=[tab_comparativo_clusters, tab_detalle_cluster]) 
        
        tab_cluster = TabPanel(child = child_cluster, title = "Análisis clusters")
        
        layout = Tabs(tabs=[tab_analysis, tab_cluster, tab_actor_item_ranking])
        
    else:
        
        layout = Tabs(tabs=[tab_analysis, tab_actor_item_ranking])
        
    return layout
        
    
    # return tab_analysis, tab_cluster, tab_actor_item_ranking
    # return tab_analysis, tab_actor_item_ranking

# tab_analysis, tab_cluster, tab_actor_item_ranking = FD_Main(conn)

def CVF_launch(doc):
    layout = FD_Main()
    doc.add_root(layout)



