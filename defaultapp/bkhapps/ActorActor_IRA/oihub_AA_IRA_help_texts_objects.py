# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 11:54:12 2023

@author: luis.caro
"""

from bokeh.layouts import row, column, layout

from bokeh.models import Div, Button, Tabs, TabPanel

from bokeh.io import curdoc

from .oihub_AA_IRA_help_texts import FD_user_help_dict

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph



def FD_build_help_html(xquestion_help_texts_dict, xtext_head_and_style, 
                       xtitle, xtext_key = None):
    
    print('.-.-.-.-.-.-.-.- oihub_AA_IRA_help_texts_objects/FD_build_help_html')
    # print('>>>>>>>>>>>>>>>>>> xquestion_help_texts_dict (FD_build_help_html)')
    # print(xquestion_help_texts_dict)
    # print('>>>>>>>>>>>>>>>>>> xtext_key (FD_build_help_html)')
    # print(xtext_key)
    
    if xtext_key is None:
        
        text = xtitle
        
    else:
    
        text = xquestion_help_texts_dict[xtext_key]    

    body_head = """<body>
        	<center>
        		<h1>"""
                
    body_div_head = """</h1>
                        <div class="scroll">"""
                        
    body_tail = """</div>
                    	</center>
                    </body>"""
                    
    html_script = xtext_head_and_style + body_head + xtitle + body_div_head + \
        text + body_tail
        
    return html_script
    
def FD_build_help_texts_layout(xhelp_texts_tuple):
    
    help_text_introduction, help_text_edges, help_text_centralities,\
        help_text_filtered_employee, help_text_communities,\
            help_text_nivel_nodo = xhelp_texts_tuple
    
    tab_introduction = TabPanel(child = column(help_text_introduction), 
                           title = 'Introducción')        
    
    tab_edges = TabPanel(child = column(help_text_edges), title = 'conexiones')
    
    tab_centralities = TabPanel(child = column(help_text_centralities), 
                                 title = 'Centralidades')
    
    tab_filtered_employee=  TabPanel(child = column(help_text_filtered_employee), 
                                         title = 'Funcionario filtrado')
    
    tab_nivel_nodo =  TabPanel(child = column(help_text_nivel_nodo), 
                                              title = 'Nivel_nodo')
    
    tab_communities =  TabPanel(child = column(help_text_communities), 
                                title = 'Comunidades')
    
    tabs_toda_la_red = Tabs(tabs=[tab_edges, tab_centralities])
    tab_toda_la_red = TabPanel(child = tabs_toda_la_red, title = 'Toda la red')
    
    tabs_nivel_red = Tabs(tabs=[tab_toda_la_red, tab_filtered_employee,
                                tab_communities])
    tab_nivel_red = TabPanel(child = tabs_nivel_red, title = 'Nivel_red')
    
    help_tabs_global = Tabs(tabs=[tab_introduction, 
                                  tab_nivel_red, tab_nivel_nodo])
    
    return help_tabs_global
    
def FD_fetch_help_texts_objects(xnetwork_parameters_dict):
    
    print('.-.-.-.- oihub_AA_IRA_help_texts_objects/FD_fetch_help_texts_objects')
    
    question_help_texts_dict = \
        xnetwork_parameters_dict['question_help_texts_dict']
    
    # print('>>>>>>>>>>>>>>>>>> question_help_texts_dict (FD_build_help_html)')
    # print(question_help_texts_dict.keys())
    
    text_head_and_style = """<head>
    	<style>
    		h1 {
    			color: Green;
    		}
    
    		div.scroll {
    			margin: 4px, 4px;
    			padding: 4px;
    			background-color: white;
    			width: 384px;
                height: 350px;
    			overflow-x: hidden;
    			overflow-y: auto;
    			text-align: justify;
    		}
    	</style>
    </head>"""
    
    
    text_introduction = FD_build_help_html(question_help_texts_dict, 
                                           text_head_and_style,
                                           'Introducción', 
                                           xtext_key = 'introduction')
    
    text_edges = FD_build_help_html(question_help_texts_dict, text_head_and_style,
                                    'Conexiones', xtext_key ='edges')
    
    text_centralities = FD_build_help_html(question_help_texts_dict,
                                           text_head_and_style,
                                           'Centralidades', 
                                           xtext_key = 'centralities')
    
    text_communities = FD_build_help_html(question_help_texts_dict, 
                                          text_head_and_style,
                                           'Comunidades', 
                                           xtext_key = 'communities')
    
    text_filtered_employee = FD_build_help_html(question_help_texts_dict, 
                                                text_head_and_style,
                                                'Funcionario filtrado',
                                                xtext_key = 'filtered_employee')
    
    
    text_nodes = FD_build_help_html(question_help_texts_dict,
                                    text_head_and_style, 'Nodos',
                                    xtext_key = 'nodes')
    # print('>>>>>>>>>>>>>>>>>>>>>>> text_nodes (FD_fetch_help_texts_objects)')
    # print(text_nodes)
       
    
    help_text_introduction = Div(text = text_introduction)
            
    help_text_edges = Div(text = text_edges)
    # tab_edges = TabPanel(child = column(help_text_edges), title = 'conexiones')
            
    help_text_centralities = Div(text = text_centralities)
    # tab_centralities = TabPanel(child = column(help_text_centralities), 
    #                              title = 'Centralidades')
            
    help_text_filtered_employee =  Div(text = text_filtered_employee)
    # tab_filtered_employee=  TabPanel(child = column(help_text_filtered_employee), 
    #                                      title = 'Funcionario filtrado')
    
    help_text_communities =  Div(text = text_communities)
    # tab_communities =  TabPanel(child = column(help_text_communities), 
    #                             title = 'Comunidades')
        
    help_text_node_level =  Div(text = text_nodes)
    # tab_nivel_nodo =  TabPanel(child = definición_nivel_nodo, title = 'Nivel_nodo')
    
    # tabs_toda_la_red = Tabs(tabs=[tab_edges, tab_centralities])
    # tab_toda_la_red = TabPanel(child = tabs_toda_la_red, title = 'Toda la red')
    
    # tabs_nivel_red = Tabs(tabs=[tab_toda_la_red, tab_filtered_employee,
    #                             tab_communities])
    # tab_nivel_red = TabPanel(child = tabs_nivel_red, title = 'Nivel_red')
    
    # tab_introduction = TabPanel(child = column(help_text_introduction), 
    #                        title = 'Introducción')        
    
    # help_tabs_global = Tabs(tabs=[tab_introduction, tab_nivel_red, tab_nivel_nodo])
    
    help_texts_tuple = (help_text_introduction, help_text_edges,
                        help_text_centralities, help_text_filtered_employee,
                        help_text_communities, help_text_node_level)
    
    return help_texts_tuple

def FD_build_question_help(xnetwork_parameters_dict):
    
    """
    Builds help text for question
    """
    
    help_texts_tuple = FD_fetch_help_texts_objects(xnetwork_parameters_dict)
    
    help_tabs_global = FD_build_help_texts_layout(help_texts_tuple)
    
    return help_tabs_global, help_texts_tuple