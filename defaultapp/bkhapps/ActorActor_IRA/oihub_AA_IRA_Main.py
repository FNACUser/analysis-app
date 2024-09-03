# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 16:57:28 2023

@author: luis.caro
"""

from bokeh.models import Tabs, TabPanel

from .oihub_AA_IRA_UnimodalFramework import FD_Unimodal_Network_Framework  

from defaultapp.bkhapps.common.Utilities import UT_bring_legend


#%%

# def FD_AA_IRA_Main(xnetwork_parameters_dict, xnetwork_parameters_data_table):
def FD_AA_IRA_Main(xconn, xglobal_questions_dict, xnetwork_parameters_dict):
    
    print(".-.--.-.-.-.-.-.-.-.-.-.-.-.-.-.- FD_AA_IRA_Main - entrada")
    
    dirAppFiles="E:/One Drive/OneDrive - FINAC S.A.S/ApplicationFiles"
    dirMutabisFinac=dirAppFiles+"/Consultoría Analítica/Productivity/Mutabis/Finac"
    
    legends_dict = xnetwork_parameters_dict['legends_dict']
    language = xnetwork_parameters_dict['language']
    # language = xnetwork_parameters_data_table.source.data['language'][0]
            
    amplifier = 40
    bimodalAmplifier = 40
   
        
    node_degree_dashboard, tabNetworkAA, questions_menu, selected_question = \
        FD_Unimodal_Network_Framework(xconn, xglobal_questions_dict,
                                      xnetwork_parameters_dict,
                                      # xnetwork_parameters_data_table,
                                      dirMutabisFinac, bimodalAmplifier,
                                      amplifier)
        
    # 'l-021':['Grados nodos','Nodes degrees']
    tabNodeDegree_title = UT_bring_legend('l-021', language, legends_dict)
    
    tabNodeDegree = \
        TabPanel(child= node_degree_dashboard, title = tabNodeDegree_title)
        
    tabsNodes = Tabs(tabs=[tabNodeDegree])
    
    # 'l-010':['Nivel nodo','Node level']
    tabMayorNode_title = UT_bring_legend('l-010', language, legends_dict)
    
    tabMayorNode = TabPanel(child= tabsNodes, title = tabMayorNode_title)
    
    # 'l-011':['Nivel red','Network level']
    tabMayorRed_title = UT_bring_legend('l-011', language, legends_dict)
    
    tabMayorRed = TabPanel(child = tabNetworkAA, title = tabMayorRed_title)
    
    # 'l-029':['Preguntas', 'Questions']
    tabQuestionsMenu_title = UT_bring_legend('l-029', language, legends_dict)
    
    tabQuestionsMenu = TabPanel(child= questions_menu,
                                title = tabQuestionsMenu_title)
    
    
    return tabMayorRed, tabMayorNode, tabQuestionsMenu, selected_question
