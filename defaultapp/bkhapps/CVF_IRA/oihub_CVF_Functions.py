# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 17:57:43 2023

@author: luis.caro
"""

import pandas as pd
import numpy as np

from bokeh.plotting import figure

# from bokeh.models import Div, Tabs, Panel, Select, Label 
from bokeh.models import Label, Title

# from neo4j_learn_ONA import conn, insert_data


#%%
def FD_fetch_complete_culture_input_forms(xconn):
    query = """MATCH (r:Respuesta)-[OF_CULTURE_FORM]->(cif:Culture_input_form)
                -[OF_CYCLE]->(c:Cycle{id_cycle:1})
                RETURN cif.id_culture_input_form, r.id_respuesta
            """
            
    result = xconn.query(query) #, parameters=params)
    
    _all_culture_input_forms_df = pd.DataFrame([dict(_) for _ in result])
    
    grouped_culture_input_forms_df =\
        _all_culture_input_forms_df.groupby(['cif.id_culture_input_form']).\
            size().reset_index(name='counts')
        
    complete_culture_input_forms_df = \
        grouped_culture_input_forms_df.\
            loc[grouped_culture_input_forms_df.counts == 24]

    complete_culture_input_forms = \
        list(complete_culture_input_forms_df['cif.id_culture_input_form'])
        
    return set(complete_culture_input_forms)

def FD_GDB_fetch_ira_employees_areas(xconn):
    
    print('.-.-.-.-.-.- oihub_CVF_Functions/FD_GDB_fetch_ira_employees_areas')

    query = """MATCH (e:Employee)-[FUNCIONARIO_DE]->(a:Organization_area) 
                WHERE e.is_active = True AND e.id_employee IS NOT NULL
                RETURN e.id_employee AS id_employee, e.redmine_login AS id_user, 
                e.employee AS employee,
                a.id_organization_area AS id_organization_area, 
                a.organization_area AS organization_area
            """
            
    result = xconn.query(query) #, parameters=params)
    
    _ira_employees_areas = pd.DataFrame([dict(_) for _ in result])
    
    # print('>>>>>>>>> _ira_employees_areas (FD_GDB_fetch_ira_employees_areas)')
    # print(_ira_employees_areas)

    # _ira_employees_areas = \
    #     _ira_employees_areas.loc[_ira_employees_areas['id_employee'].\
    #                             isin(xvalid_employees)]
    #:_:_:_:_:_:_:_:_:_:_ fin temporal

    
    # print('>>>>>>>>> _ira_employees_areas (FD_GDB_fetch_ira_employees_areas)')
    # print(_ira_employees_areas)
    # print('>>>>>>>>>non_clustered_employees (FD_GDB_fetch_ira_employees_areas)')
    # print(non_clustered_employees)


    return _ira_employees_areas

def FD_fetch_valid_employees_areas(xconn):
    
    print('.-.-.-.-.-.-.-. oihub_CVF_Functions/FD_fetch_valid_employees_areas')

    complete_culture_input_forms = \
        FD_fetch_complete_culture_input_forms(xconn)
    print('>>>>>>>>>>>>>>>> complete_culture_input_forms (FD_fetch_valid_employees_areas)')
    print(complete_culture_input_forms) 
    
    query = """MATCH (e:Employee)<-[OF_EMPLOYEE]-(cif:Culture_input_form)-
                [OF_CYCLE]->(c:Cycle{id_cycle:1}) 
                RETURN cif.id_culture_input_form as id_culture_input_form, 
                e.id_employee as id_employee, c.id_cycle as id_cycle
            """
            
    result = xconn.query(query) #, parameters=params)
    
    all_culture_input_forms_df = pd.DataFrame([dict(_) for _ in result])
    print('>>>>>>>>>>>>>>>> all_culture_input_forms_df (FD_fetch_valid_employees_areas)')
    print(all_culture_input_forms_df) 
    print(all_culture_input_forms_df.shape) 
    print(all_culture_input_forms_df.columns) 
    
    all_culture_input_forms_df['id_culture_mode'] = 1
    all_culture_input_forms_df['Is_concluded'] = True
    
    culture_input_forms_df = \
        all_culture_input_forms_df\
            [all_culture_input_forms_df['id_culture_input_form'].isin\
             (complete_culture_input_forms)]
                
    valid_employees = list(culture_input_forms_df['id_employee'])
    # print('>>>>>>>>>>>>>>>>> valid_employees (oihub_CVF_Analysis/FD_Main_analysis)')
    # print(valid_employees)
    
    ira_employees_areas = FD_GDB_fetch_ira_employees_areas(xconn)
    
    ira_employees_areas = \
        ira_employees_areas.loc[ira_employees_areas['id_employee'].\
                                isin(valid_employees)]
    #:_:_:_:_:_:_:_:_:_:_ fin Temporal
    # print('>>>>>>>>>>>>>>>>> ira_employees_areas (oihub_CVF_Analysis/FD_Main_analysis)')
    # print(ira_employees_areas)
    
    return ira_employees_areas




#%%
def FD_actual_preferred_weights_arrays(xquestions_responses_df):
    
    # print('>>>>>>>>>>>>>>>> FD_actual_preferred_weights_arrays')
    # print('.-.-.-.-.-.-. xquestions_responses_df FD_actual_preferred_weights_arrays')
    # print(xquestions_responses_df)
    
    rows, cols = (6, 4)
    arr_actual = [[0 for i in range(cols)] for j in range(rows)]
    arr_preferred = [[0 for i in range(cols)] for j in range(rows)]
    
    
    for index, df_row in xquestions_responses_df.iterrows():
        
        # print('.-.-.-.-.-.-.-.-.-.-.-.')
        # print(row)
        # print(row['id_culture_mode_theme'])
        # print(row['id_culture_quadrant'])
        
        arr_actual[df_row['id_culture_mode_theme']-1]\
            [df_row['id_culture_quadrant']-1] = df_row['Actual']
        arr_preferred[df_row['id_culture_mode_theme']-1]\
            [df_row['id_culture_quadrant']-1] = df_row['Preferred']
        
        # print(arr_actual)
        # print(arr_preferred)
        
    return arr_actual, arr_preferred

    
def getSlope(x1, y1, x2, y2):
    
    """
    Slope -1 es que es vertical
    """
    
    if y2 == y1:
        slope = 0
    elif x2 != x1:
        slope = 1.0*(y2-y1)/(x2-x1)
    else:
        slope = -1
        
    return slope


def getIntercepts(x1, y1, x2, y2):
    
    """
    Si el slope (m) es cero, devuelve ceros
    """
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- getIntercepts')
    # print('>>>>>>>>>>>>> x1, y1, x2, y2 (getIntercepts)')
    # print(x1, y1, x2, y2)
    
    m = getSlope(x1, y1, x2, y2)
    # print('>>>>>>>>>>>>> m (getIntercepts)')
    # print(m)
    
    if m != 0:
        
        y_intercept = y1 - (m*x1)
        
        y_tendency = (m*5) + y_intercept
        
        x_intercept = (-1 * y_intercept) / m
        
        x_tendency = (5 - y_intercept) / m
        
    elif m == 0:
        
        y_tendency = y1
        
        x_tendency = -1
        
    else:
        
        x_tendency = x1
        
        y_tendency = -1
    
    return x_tendency, y_tendency


def FD_plot_weights_position(xweights,
                             xxy_plot_max = 10,
                             xmax_plotted_score = 6):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_CVF_Functions/FD_plot_weights_position')
    print('>>>>>>>>>>>>>>>>>> xweights - FD_plot_weights_position')
    print(xweights)
    # print('>>>>>>>>>>>>>>>>>> xxy_plot_max - FD_plot_weights_position')
    # print(xxy_plot_max)
    # print('>>>>>>>>>>>>>>>>>> xmax_plotted_score - FD_plot_weights_position')
    # print(xmax_plotted_score)
    
    def weights_effect(_xweights):
        _weights_effect = \
            min(mid_point,
                mid_point * (_xweights / 100) * \
                    ( xxy_plot_max / xmax_plotted_score ))
        return _weights_effect
    
    mid_point = xxy_plot_max / 2
    
    if xweights[0] != 0:
        weights_0_effect = weights_effect(xweights[0])
        p0_x = mid_point - weights_0_effect
        p0_y = mid_point + weights_0_effect
    else:
        p0_x = mid_point
        p0_y = mid_point
    
    if xweights[1] != 0:
        weights_1_effect = weights_effect(xweights[1])
        p1_x = mid_point + weights_1_effect
        p1_y = mid_point + weights_1_effect
    else:
        p1_x = mid_point
        p1_y = mid_point
    
    if xweights[2] != 0:
        weights_2_effect = weights_effect(xweights[2])
        p2_x = mid_point + weights_2_effect
        p2_y = mid_point - weights_2_effect
    else:
        p2_x = mid_point
        p2_y = mid_point
    
    if xweights[3] != 0:
        weights_3_effect = weights_effect(xweights[3])
        p3_x = mid_point - weights_3_effect
        p3_y = mid_point - weights_3_effect
    else:
        p3_x = mid_point
        p3_y = mid_point
    
    x_coordinates_list = [p0_x, p1_x, p2_x, p3_x]
    y_coordinates_list = [p0_y, p1_y, p2_y, p3_y]
    
    _, flexible_tendency = getIntercepts(p0_x, p0_y, p1_x, p1_y)
    outer_tendency, _ = getIntercepts(p1_x, p1_y, p2_x, p2_y)
    _, controlled_tendency = getIntercepts(p2_x, p2_y, p3_x, p3_y)
    inner_tendency, _ = getIntercepts(p3_x, p3_y, p0_x, p0_y)
    
    # print('>>>>>>>>>>>>>>>>>>> x_coordinates_list (FD_plot_weights_position)')
    # print(x_coordinates_list)
    # print(y_coordinates_list)
    # print('>>>>>>>>>>>>>>>>>>> flexible_tendency (FD_plot_weights_position)')
    # print(flexible_tendency)
    
    return x_coordinates_list, y_coordinates_list, flexible_tendency,\
        outer_tendency, controlled_tendency, inner_tendency

# FD_plot_weights_position([40,30,20,10])
# getIntercepts(3,7,6.5,6.5) 
# getIntercepts(6.5,6.5,6,4) 


def FD_CVF_plot(xactual_employee_weights, xpreferred_employee_weights,
                xactual_area_weights, xpreferred_area_weights,
                xtitle = "", xwidth=250, xheight=250):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-. oihub_CVF_Functions/FD_CVF_plot')
    
    def solve_tendencies(xcoordinates):
        _flexible_tendency = xcoordinates[2]
        _outer_tendency = xcoordinates[3] 
        _controlled_tendency = xcoordinates[4] 
        _inner_tendency = xcoordinates[5]
        # print('>>>>>>>>>>> actual_flexible_tendency (FD_CVF_plot_single)')
        # print(actual_flexible_tendency)
        # print('>>> actual_controlled_tendency (FD_CVF_plot_single)')
        # print(actual_controlled_tendency)  
        
        net_inner_outer_tendency = \
            (_outer_tendency + _inner_tendency) / 2
        net_flexible_controlled_tendency = \
            (_flexible_tendency + _controlled_tendency) / 2
            
        return net_inner_outer_tendency, net_flexible_controlled_tendency
    
    
    
    cvf_plot = figure(width = xwidth, height = xheight)

    nan = float('nan')
    cvf_plot.line([0, 10, nan, 10, 0], [0, 10, nan, 0,10], 
                  line_width=2, line_dash='dashed', line_color='grey')
    # cvf_plot.line([0, 7, nan, 7, 0], [0, 7, nan, 0,7], 
    #               line_width=2, line_dash='dashed', line_color='grey')
    cvf_plot.line([0, 10, nan, 5, 5], [5, 5, nan, 0,10], 
                  line_width=2, line_dash='solid', line_color='grey')
    # cvf_plot.line([0, 7, nan, 5, 5], [5, 5, nan, 0,7], 
    #               line_width=2, line_dash='solid', line_color='grey')

    actual_employee_culture = FD_plot_weights_position(xactual_employee_weights)
    preferred_employee_culture = FD_plot_weights_position(xpreferred_employee_weights)
    
    net_actual_employee_inner_outer_tendency, \
        net_actual_employee_flexible_controlled_tendency = \
            solve_tendencies(actual_employee_culture)
            
    net_preferred_employee_inner_outer_tendency, \
        net_preferred_employee_flexible_controlled_tendency = \
            solve_tendencies(preferred_employee_culture)
    
    actual_area_culture = FD_plot_weights_position(xactual_area_weights)
    preferred_area_culture = FD_plot_weights_position(xpreferred_area_weights)
    
    net_actual_area_inner_outer_tendency, \
        net_actual_area_flexible_controlled_tendency = \
            solve_tendencies(actual_area_culture)
            
    net_preferred_area_inner_outer_tendency, \
        net_preferred_area_flexible_controlled_tendency = \
            solve_tendencies(preferred_area_culture)
  

    print('>>>>>>>>>> actual_employee_culture 0 & 1CVF_Plot')
    print(actual_employee_culture[0], actual_employee_culture[1])
    print('>>>>>>>>>> preferred_employee_culture 0 & 1CVF_Plot')
    print(preferred_employee_culture[0], preferred_employee_culture[1])
    print('>>>>>>>>>> actual_area_culture 0 & 1 (CVF_Plot)')
    print(actual_area_culture[0], actual_area_culture[1])
    print('>>>>>>>>>> preferred_area_culture 0 & 1 (CVF_Plot)')
    print(preferred_area_culture[0], preferred_area_culture[1])
    
    cvf_plot.patches([actual_employee_culture[0], preferred_employee_culture[0],
                      actual_area_culture[0], preferred_area_culture[0]], 
                     [actual_employee_culture[1], preferred_employee_culture[1],
                      actual_area_culture[1], preferred_area_culture[1]],
              color=["firebrick", "","navy", ""], alpha=[0.5, 0.5,0.5, 0.5], line_width=2,
              line_dash = ['solid', 'dashed','solid', 'dashed'], 
              line_color = ['firebrick', 'firebrick','navy', 'navy'])
    
    cvf_plot.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    cvf_plot.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
    cvf_plot.xaxis.visible = False
    cvf_plot.yaxis.visible = False
    
    cvf_plot.title.text = xtitle
    
    cvf_plot.square([5, net_actual_employee_inner_outer_tendency], 
                    [net_actual_employee_flexible_controlled_tendency, 5], 
                    size=10, color=["firebrick","firebrick"], alpha=1)
    cvf_plot.star_dot([5, net_preferred_employee_inner_outer_tendency], 
                    [net_preferred_employee_flexible_controlled_tendency, 5], 
                    size=10, color=["orange","orange"], alpha=1)
    cvf_plot.square([5, net_actual_area_inner_outer_tendency], 
                    [net_actual_area_flexible_controlled_tendency, 5], 
                    size=10, color=["navy","navy"], alpha=1)
    cvf_plot.star_dot([5, net_preferred_area_inner_outer_tendency], 
                    [net_preferred_area_flexible_controlled_tendency, 5], 
                    size=10, color=["yellow","yellow"], alpha=1)
    
    left_x = xwidth * .045
    top_y = xheight * .75
    bottom_y = xheight * .045
    adhocracy_x = xwidth * .60
    market_x =  xwidth * .70
    # clan_annotation = Label(x=0, y=9, x_units='data', y_units='data',
    #             text='Clan', render_mode='css',
    #             border_line_color='black', border_line_alpha=1.0,
    #             background_fill_color='white', background_fill_alpha=1.0)
   
    # adhocracy_annotation = Label(x=6, y=9, x_units='data', y_units='data',
    #             text='Adhocracia', render_mode='css',
    #             border_line_color='black', border_line_alpha=1.0,
    #             background_fill_color='white', background_fill_alpha=1.0)
   
    # hierarchy_annotation = Label(x=0, y=0, x_units='data', y_units='data',
    #             text='Jerarquía', render_mode='css',
    #             border_line_color='black', border_line_alpha=1.0,
    #             background_fill_color='white', background_fill_alpha=1.0)
    # market_annotation = Label(x=6.5, y=0, x_units='data', y_units='data',
    #             text='Mercado', render_mode='css',
    #             border_line_color='black', border_line_alpha=1.0,
    #             background_fill_color='white', background_fill_alpha=1.0)
    
    clan_annotation = Label(x=0, y=9, x_units='data', y_units='data',
                 text='Clan',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
    
    adhocracy_annotation = Label(x=6, y=9, x_units='data', y_units='data',
                 text='Adhocracia',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
    
    hierarchy_annotation = Label(x=0, y=0, x_units='data', y_units='data',
                 text='Jerarquía',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
    market_annotation = Label(x=6.5, y=0, x_units='data', y_units='data',
                 text='Mercado',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0)
    
    cvf_plot.add_layout(clan_annotation)
    cvf_plot.add_layout(adhocracy_annotation)
    cvf_plot.add_layout(hierarchy_annotation)
    cvf_plot.add_layout(market_annotation)
    
    return cvf_plot


def FD_fetch_employee_culture_GDB(xconn, xid_employee):
    
    # print('.-.-.-.-.-.-.-.-.-. CVF_Functions/FD_fetch_employee_culture_GDB')
    # print('>>>>>>>>>>>> xid_employee (FD_fetch_employee_culture_GDB)')
    # print(xid_employee) 
    
    query = """MATCH (e:Employee{id_employee:$employee_id})<-[OF_EMPLOYEE]-
                (cif:Culture_input_form)<-[OF_CULTURE_FORM]-(r:Respuesta)-
                [RESPUESTA_DE]->(p:Pregunta)-[DE_TEMA]->(t:Tema)
                MATCH (p)-[DE_CUADRANTE]->(c:Cuadrante)
                RETURN r.id_respuesta AS id_question_response, 
                t.id_tema AS id_culture_mode_theme, 
                t.tema AS culture_mode_theme, 
                p.id_pregunta AS id_culture_mode_theme_question, 
                c.id_cuadrante AS id_culture_quadrant, 
                c.cuadrante AS culture_quadrant, 
                r.actual AS Actual, 
                r.preferido AS Preferred"""
    
    # query = """MATCH (e:Employee{id_employee:$employee_id})
    #                     <-[CONTESTADA_POR]-(r:Respuesta)-
    #                     [RESPUESTA_DE]->(p:Pregunta),
    #                     (p:Pregunta)-[DE_TEMA]->(t:Tema),
    #                     (p:Pregunta)-[DE_CUADRANTE]->(c:Cuadrante) 
    #                     RETURN r.id_respuesta AS id_question_response,
    #                     t.id_tema AS id_culture_mode_theme,
    #                     t.tema AS culture_mode_theme,
    #                     p.id_pregunta AS id_culture_mode_theme_question, 
    #                     c.id_cuadrante AS id_culture_quadrant,
    #                     c.cuadrante AS culture_quadrant,
    #                     r.actual AS Actual, r.preferido AS Preferred
    #         """

    params = {'employee_id': xid_employee}

    result = xconn.query(query, parameters=params)

    employee_culture_df = pd.DataFrame([dict(_) for _ in result])
    
    # print('>>>>>>>>>>>> employee_culture_df (FD_fetch_employee_culture_GDB)')
    # print(employee_culture_df)    
    
    return employee_culture_df

# a=FD_fetch_employee_culture_GDB(2)
# a

#%% esto va para FD_fecthc_total_culture_GDB
# 

# query = """MATCH (e:Employee)<-[OF_EMPLOYEE]-(cip:Culture_input_form)
#             <-[OF_CULTURE_FORM]-(r:Respuesta)-[RESPUESTA_DE]
#             ->(p:Pregunta)-[DE_CUADRANTE]->(c:Cuadrante) 
#             RETURN e.id_employee, r.actual, r.preferido, c.cuadrante"""
            
# result = conn.query(query)

# total_culture_df = pd.DataFrame([dict(_) for _ in result])

# totals = total_culture_df.groupby(['e.id_employee', 'c.cuadrante'], 
#                          as_index=False).mean()

# total_culture = \
#     (totals.pivot_table(index=['e.id_employee'],
#                                   columns='c.cuadrante',
#                                   values=['r.actual','r.preferido']).\
#      reset_index())
#%%:_:_:_:_:_:_:_:_:_:_:__:_            

def FD_fetch_ttotal_culture_GDB(xconn):
    query = """MATCH (e:Employee)-[p:PERCIBE_CULTURA_TOTAL]->(c:Cuadrante) 
                RETURN e.id_employee, p.actual, p.preferido, c.cuadrante
                            """
        
    result = xconn.query(query)

    total_culture_df = pd.DataFrame([dict(_) for _ in result])
    
    total_culture = \
        (total_culture_df.pivot_table(index=['e.id_employee'],
                                      columns='c.cuadrante',
                                      values=['p.actual','p.preferido']).\
         reset_index())
    
    return total_culture

# b=FD_fetch_total_culture_GDB()

def FD_employee_list_score(xconn, xemployee_list):
    
    print('.-.-.-.-.-.-.-.-.- oihub_CVF_Functions/FD_employee_list_score')
    print('>>>>>>>>>>>>>>>> xemployee_list (FD_employee_list_score)')
    print(xemployee_list)
    
    rows, cols = (6, 4)
    arr_actual_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    arr_preferred_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    # print('>>>>>>>>>>>>>>>> arr_actual_accumulated (oihub_CVF_Functions/FD_employee_list_score)')
    # print(arr_actual_accumulated)
    
    #OJO Devolver
    # for employee_id in [xemployee_list[0]]:
    for employee_id in xemployee_list:
        # print('>>>>>>>>>>>>>> employee_id (oihub_CVF_Functions/FD_employee_list_score)')
        # print(employee_id)
        _questions_responses_df = \
            FD_fetch_employee_culture_GDB(xconn, employee_id)
        # print('>>>>>>>>>>>>>> _questions_responses_df (oihub_CVF_Functions/FD_employee_list_score)')
        # print(_questions_responses_df.to_dict('records'))
        _arr_actual, _arr_preferred = \
            FD_actual_preferred_weights_arrays(_questions_responses_df)
        # print('_arr_actual, _arr_preferred')
        # print(_arr_actual, _arr_preferred)
        arr_actual_accumulated = np.add(arr_actual_accumulated,
                                           _arr_actual)
        arr_preferred_accumulated = np.add(arr_preferred_accumulated,
                                           _arr_preferred)
        # print('arr_actual_accumulated, arr_preferred_accumulated')
        # print(arr_actual_accumulated, arr_preferred_accumulated)
        
    print('>>>>>>>>>>>>>>>> arr_actual_accumulated (FD_employee_list_score)')
    print(arr_actual_accumulated)    
    print('>>>>>>>>>>>>>>>> arr_preferred_accumulated (FD_employee_list_score)')
    print(arr_preferred_accumulated)
    
    arr_actual_accumulated = arr_actual_accumulated / len(xemployee_list)
    # len_xemployee_list = len(xemployee_list)
    # arr_actual_accumulated = \
    #     [aaa/len_xemployee_list for aaa in arr_actual_accumulated]
    print('>>>>>>>>>>>>>>>> arr_actual_accumulated (FD_employee_list_score)')
    print(arr_actual_accumulated)    
    
    arr_preferred_accumulated = arr_preferred_accumulated / len(xemployee_list)
    # arr_preferred_accumulated = \
    #     [aaa/len_xemployee_list for aaa in arr_preferred_accumulated]
    print('>>>>>>>>>>>>>>>> arr_preferred_accumulated (FD_employee_list_score)')
    print(arr_preferred_accumulated)
    
    return arr_actual_accumulated, arr_preferred_accumulated

# arr_actual_accumulated, arr_preferred_accumulated =\
#     FD_employee_list_score([1])
# arr_actual_accumulated

# a=FD_fetch_employee_culture(1)
# a.columns
# a.shape


# a=FD_fetch_employee_culture_GDB(1)
# a.columns
# a.shape


# def FD_selected_employees_score(xarea_selector, xemployee_selector, 
#                                 xira_employees_areas):
def FD_selected_employees_score(xconn, xarea_selector, xemployee_selector, 
                                xira_employees_areas):
    
    # rows, cols = (6, 4)
    # arr_actual_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    # arr_preferred_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    
    print('.-.-.-.-.-.-.-.- oihub_CVF_Functions/FD_selected_employees_score')
    # print('>>>>>>>>>>>>>> xarea_selector.value (oihub_CVF_Functions/FD_selected_employees_score)')
    # print(xarea_selector.value)
    # print('>>>>>>>>>>>>>> xemployee_selector.value (oihub_CVF_Functions/FD_selected_employees_score)')
    # print(xemployee_selector.value)
    # print('>>>>>>>>>>>>>> xira_employees_areas (oihub_CVF_Functions/FD_selected_employees_score)')
    # print(xira_employees_areas)
    
    
    #
    #selecciona las filas de ira_employees_areas que corresponden a los
    #empleados del área
    if xarea_selector.value == '-Todas':
        _xira_employees_areas = xira_employees_areas
    else:
        _xira_employees_areas = xira_employees_areas.\
            loc[xira_employees_areas.organization_area == xarea_selector.value]
    # print('>>>>>>>>>>>>>> xira_employees_areas (oihub_CVF_Functions/FD_selected_employees_score)')
    # print(xira_employees_areas)
    
    #
    #selecciona los empleados a incluir (puede ser uno solo)
    if xemployee_selector.value == '-Todos':
        employee_list = list(_xira_employees_areas['id_employee'])
    else:
        employee_list = \
            list(_xira_employees_areas.\
                 loc[_xira_employees_areas.employee == \
                     xemployee_selector.value]['id_employee'])
    # print('>>>>>>>>>>>>>> employee_list (oihub_CVF_Functions/FD_selected_employees_score)')
    # print(employee_list)
    
    arr_actual_accumulated, arr_preferred_accumulated =\
        FD_employee_list_score(xconn, employee_list)
    
    # for employee_id in employee_list:
    #     # print('employee_id')
    #     # print(employee_id)
    #     _questions_responses_df, _culture_modes_dict = \
    #         FD_fetch_employee_culture(employee_id)
    #     _arr_actual, _arr_preferred = \
    #         FD_actual_preferred_weights_arrays(_questions_responses_df)
    #     # print('_arr_actual, _arr_preferred')
    #     # print(_arr_actual, _arr_preferred)
    #     arr_actual_accumulated = np.add(arr_actual_accumulated,
    #                                        _arr_actual)
    #     arr_preferred_accumulated = np.add(arr_preferred_accumulated,
    #                                        _arr_preferred)
    #     # print('arr_actual_accumulated, arr_preferred_accumulated')
    #     # print(arr_actual_accumulated, arr_preferred_accumulated)
        
    # arr_actual_accumulated = arr_actual_accumulated / len(employee_list)
    # arr_preferred_accumulated = arr_preferred_accumulated / len(employee_list)
        
    return arr_actual_accumulated, arr_preferred_accumulated


def FD_CVF_plot_single(xactual_coordinates, xpreferred_coordinates,
                        xtitle1 = "", xtitle2 = "", _xwidth=250, _xheight=250,
                        xtitle_font_size = '20pt',
                        xy_plot_max = 10):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_CVF_plot_single')
    
    # print('>>>>>>>>>>>>>>>>>>>> xactual_coordinates (FD_CVF_plot_single)')
    # print(xactual_coordinates)
    actual_flexible_tendency = xactual_coordinates[2]
    actual_outer_tendency = xactual_coordinates[3] 
    actual_controlled_tendency = xactual_coordinates[4] 
    actual_inner_tendency = xactual_coordinates[5]
    # print('>>>>>>>>>>> actual_flexible_tendency (FD_CVF_plot_single)')
    # print(actual_flexible_tendency)
    # print('>>> actual_controlled_tendency (FD_CVF_plot_single)')
    # print(actual_controlled_tendency)  
    
    net_actual_inner_outer_tendency = \
        (actual_outer_tendency + actual_inner_tendency) / 2
    net_actual_flexible_controlled_tendency = \
        (actual_flexible_tendency + actual_controlled_tendency) / 2
    # print('>>>>>>>>>>> net_actual_inner_outer_tendency (FD_CVF_plot_single)')
    # print(net_actual_inner_outer_tendency)
    # print('>>> net_actual_flexible_controlled_tendency (FD_CVF_plot_single)')
    # print(net_actual_flexible_controlled_tendency)  
    
    
    preferred_flexible_tendency = xpreferred_coordinates[2]
    preferred_outer_tendency = xpreferred_coordinates[3] 
    preferred_controlled_tendency = xpreferred_coordinates[4] 
    preferred_inner_tendency = xpreferred_coordinates[5]
    
    net_preferred_inner_outer_tendency = \
        (preferred_outer_tendency + preferred_inner_tendency) / 2
    net_preferred_flexible_controlled_tendency = \
        (preferred_flexible_tendency + preferred_controlled_tendency) / 2
    # print('>>>>>>>>>>> net_preferred_inner_outer_tendency (FD_CVF_plot_single)')
    # print(net_preferred_inner_outer_tendency)
    # print('>>> net_preferred_flexible_controlled_tendency (FD_CVF_plot_single)')
    # print(net_preferred_flexible_controlled_tendency)  
    
    cvf_plot = figure(width = _xwidth, height = _xheight)

    nan = float('nan')
    cvf_plot.line([0, xy_plot_max, nan, xy_plot_max, 0], 
                  [0, xy_plot_max, nan, 0, xy_plot_max], 
                  line_width=2, line_dash='dashed', line_color='grey')
    cvf_plot.line([0, xy_plot_max, nan, xy_plot_max/2, xy_plot_max/2], 
                  [xy_plot_max/2, xy_plot_max/2, nan, 0, xy_plot_max], 
                  line_width=2, line_dash='solid', line_color='grey')

    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.- FD_CVF_plot_single')
    # print('actual_coordinates[0], actual_coordinates[1]')
    # print(xactual_coordinates[0], xactual_coordinates[1])
    # print('preferred_coordinates[0], preferred_coordinates[1]')
    # print(xpreferred_coordinates[0], xpreferred_coordinates[1])
    
    cvf_plot.patches([xactual_coordinates[0], xpreferred_coordinates[0]], 
                     [xactual_coordinates[1], xpreferred_coordinates[1]],
              color=["firebrick", ""], alpha=[0.5, 0.5], line_width=2,
              line_dash = ['solid', 'dashed'], 
              line_color = ['firebrick', 'firebrick'])
    
    cvf_plot.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
    cvf_plot.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
    cvf_plot.xaxis.visible = False
    cvf_plot.yaxis.visible = False
    
    
    # left_x = _xwidth * .045
    # top_y = _xheight * .75
    # bottom_y = _xheight * .045
    # adhocracy_x = _xwidth * .60
    # market_x =  _xwidth * .70
    
    label_font_size="10px"
    # clan_annotation = Label(x=left_x, y=top_y, x_units='screen', y_units='screen',
    clan_annotation = Label(x = 0, y = .9 * xy_plot_max, x_units='data', 
                            y_units='data',
                 text='Clan',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0,
                 text_font_size=label_font_size)
    # adhocracy_annotation = Label(x=adhocracy_x, y=top_y, x_units='screen', y_units='screen',
    adhocracy_annotation = Label(x = .6 * xy_plot_max, y = .9 * xy_plot_max, 
                                 x_units='data', y_units='data',
                 text='Adhocracia',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0,
                 text_font_size=label_font_size)
    # hierarchy_annotation = Label(x=left_x, y=bottom_y, x_units='screen', y_units='screen',
    hierarchy_annotation = Label(x=0, y=0, x_units='data', y_units='data',
                 text='Jerarquía',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0,
                 text_font_size=label_font_size)
    market_annotation = Label(x = .65 * xy_plot_max, y=0, x_units='data', 
                              y_units='data',
                 text='Mercado',
                 border_line_color='black', border_line_alpha=1.0,
                 background_fill_color='white', background_fill_alpha=1.0,
                 text_font_size=label_font_size)
    cvf_plot.add_layout(clan_annotation)
    cvf_plot.add_layout(adhocracy_annotation)
    cvf_plot.add_layout(hierarchy_annotation)
    cvf_plot.add_layout(market_annotation)
    
    cvf_plot.toolbar.logo = None
    cvf_plot.toolbar_location = None
    
    if xtitle2 != "":
        cvf_plot.add_layout(Title(text=xtitle2, text_font_size=xtitle_font_size),
                            'above')
    if xtitle1 != "":
        cvf_plot.add_layout(Title(text=xtitle1, text_font_size=xtitle_font_size), 
                            'above')
    cvf_plot.title.text_font_size = xtitle_font_size
    
    # cvf_plot.square([5, actual_outer_tendency, 5, actual_inner_tendency], 
    #                 [actual_flexible_tendency, 5, actual_controlled_tendency, 5], 
    #                 size=5, color="olive", alpha=0.5)
    
    cvf_plot.square([5, net_actual_inner_outer_tendency], 
                    [net_actual_flexible_controlled_tendency, 5], 
                    size=10, color=["blue","green"], alpha=1)
    cvf_plot.star_dot([5, net_preferred_inner_outer_tendency], 
                    [net_preferred_flexible_controlled_tendency, 5], 
                    size=10, color=["yellow","orange"], alpha=1)
    
    return cvf_plot

# def FD_plot_weights_position(xweights):
    
#     print('.-.-.-.-.-.-.-.-.-.-.-. FD_plot_weights_position')
#     # print('>>>>>>>>>>>>>>>>>>>>>> xweights - FD_plot_weights_position')
#     # print(xweights)
    
#     if xweights[0] != 0:
#         p0_x = 5-5*(xweights[0]/100)
#         p0_y = 5+5*(xweights[0]/100)
#     else:
#         p0_x = 5
#         p0_y = 5
    
#     if xweights[1] != 0:
#         p1_x = 5+5*(xweights[1]/100)
#         p1_y = 5+5*(xweights[1]/100)
#     else:
#         p1_x = 5
#         p1_y = 5
    
#     if xweights[2] != 0:
#         p2_x = 5+5*(xweights[2]/100)
#         p2_y = 5-5*(xweights[2]/100)
#     else:
#         p2_x = 5
#         p2_y = 5
    
#     if xweights[3] != 0:
#         p3_x = 5-5*(xweights[3]/100)
#         p3_y = 5-5*(xweights[3]/100)
#     else:
#         p3_x = 5
#         p3_y = 5
    
#     x_coordinates_list = [p0_x, p1_x, p2_x, p3_x]
#     y_coordinates_list = [p0_y, p1_y, p2_y, p3_y]
    
#     # print('.-.-.-.-.-.-.-.- x_coordinates_list - FD_plot_weights_position')
#     # print(x_coordinates_list)
#     # print('.-.-.-.-.-.-.-.- y_coordinates_list - FD_plot_weights_position')
#     # print(y_coordinates_list)
    
#     return x_coordinates_list, y_coordinates_list


def FD_horizontal_box_plot(xdata_df, xgrouping_column,
                           xvalue_column, _x_range = (0,100), _xheight = 200,
                           _xwidth = 200, xtitle = ""):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- FD_horizontal_box_plot')
    # print('>>>>>>>>>>>>>>>>>>>>>> xdata_df (FD_horizontal_box_plot)')
    # print(xdata_df)
    # print('>>>>>>>>>>>>>>>>>>>>>> xgrouping_column (FD_horizontal_box_plot)')
    # print(xgrouping_column)
    # print('>>>>>>>>>>>>>>>>>>>>>> xvalue_column (FD_horizontal_box_plot)')
    # print(xvalue_column)
    
    # find the quartiles and IQR for each category
    groups = xdata_df.groupby(xgrouping_column)
    # print('>>>>>>>>>>>>>>>>>>>>>> groups (FD_horizontal_box_plot)')
    # print(groups)
    q1 = groups.quantile(q=0.25)
    # print('>>>>>>>>>>>>>>>>>>>>>> q1 (FD_horizontal_box_plot)')
    # print(q1)
    q2 = groups.quantile(q=0.5)
    # print('>>>>>>>>>>>>>>>>>>>>>> q2 (FD_horizontal_box_plot)')
    # print(q2)
    q3 = groups.quantile(q=0.75)
    # print('>>>>>>>>>>>>>>>>>>>>>> q3 (FD_horizontal_box_plot)')
    # print(q3)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr
    
    m = groups.mean()
    # print('>>>>>>>>>>>>>>>>>>>>>> m (FD_horizontal_box_plot)')
    # print(m)
    
    # print('.-.-.-.-.-.-.-.-. groups mean (FD_horizontal_box_plot)')
    # print(xdata_df.groupby(['culture_quadrant'])[xvalue_column].mean().reset_index())                                         

    categories = [n for n,_ in groups]
    # print('>>>>>>>>>>>>>>>>>>>>>> categories (FD_horizontal_box_plot)')
    # print(categories)
    
    # find the outliers for each category
    def outliers(group):
        cat = group.name
        return group[(group[xvalue_column] > upper.loc[cat][xvalue_column]) | \
                     (group[xvalue_column] < lower.loc[cat][xvalue_column])][xvalue_column]
    out = groups.apply(outliers).dropna()
    
    # prepare outlier data for plotting, we need coordinates for every outlier.
    if not out.empty:
        outx = list(out.index.get_level_values(0))
        outy = list(out.values)
    else:
        outx = []
        outy = []
    
    p = figure(tools="", background_fill_color="#efefef", y_range = categories, 
               x_range = _x_range, toolbar_location=None, height = _xheight, 
               width = _xwidth, title = xtitle)
    
    # if no outliers, shrink lengths of stems to be no longer than the minimums or maximums
    qmin = groups.quantile(q=0.00)
    qmax = groups.quantile(q=1.00)
    upper[xvalue_column] = \
        [min([x,y]) for (x,y) in zip(list(qmax.loc[:,xvalue_column]),
                                     upper[xvalue_column])]
    lower[xvalue_column] = \
        [max([x,y]) for (x,y) in zip(list(qmin.loc[:,xvalue_column]),
                                     lower[xvalue_column])]
    
    # stems
    p.segment(upper[xvalue_column], categories, q3[xvalue_column], 
              categories, line_color="black")
    p.segment(lower[xvalue_column], categories, q1[xvalue_column], 
              categories, line_color="black")
    
    # boxes
    p.hbar(categories, 0.35, q2[xvalue_column], q3[xvalue_column], 
           fill_color="#E08E79", line_color="black")
    p.hbar(categories, 0.35, q1[xvalue_column], q2[xvalue_column], 
           fill_color="#3B8686", line_color="black")
    
    # whiskers (almost-0 height rects simpler than segments)
    p.rect(lower[xvalue_column], categories, 0.01, 0.2, line_color="black")
    p.rect(upper[xvalue_column], categories, 0.01, 0.2, line_color="black")
    
    # outliers
    # if not out.empty:
    p.circle(outy, outx, size=6, color="#F38630", fill_alpha=0.6)
        
    #.-.-.-.-.-.-.-.-.-.-.-.-.-.- otra forma tomada de un ejemplo
    # actorMetricValue=list(actor_metrics[xmetric])
    # actorFrequencies = xfrequencies
    # sourceMetrics=ColumnDataSource(dict(x=actorFrequencies,
    #                                     actorMetricValue=actorMetricValue))
    
    # actorMetrics = Circle(x="x", y="actorMetricValue", size=6, line_color="black", 
    #                      fill_color="blue", line_width=2)
    # # glyph = Circle(x="x", y="y", size="sizes", line_color="#3288bd", fill_color="white", line_width=3)
    # p.add_glyph(sourceMetrics, actorMetrics)
    
    # _tooltips=[("actorMetricValue", "@actorMetricValue")]
    # p.add_tools(HoverTool(tooltips=_tooltips))
    #.-.-.-.-.-.-.-.-
    
    # print('>>>>>>>>>>>>>>>>>>>>>> m[xvalue_column] (FD_horizontal_box_plot)')
    # print(m[xvalue_column])
    
    colors=["yellow","yellow","yellow","yellow"]
    fill_color="yellow"
    color="#386CB0"
    # p.star_dot(list(m[xvalue_column]), categories, size=10, color=colors, alpha=1)
    p.star_dot(list(m[xvalue_column]), categories, size=10, color=fill_color, 
               alpha=1,fill_color=color)
    #:_:_:_:_:_:_:_:_:_:_:_:_:_:_:
    
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = "white"
    p.grid.grid_line_width = 2
    p.xaxis.major_label_text_font_size="8px"
    
    return p

def FD_average_cluster_weights(xactual_employee_weights, 
                               xpreferred_employee_weights):
# ,
#                                xactual_area_weights, 
#                                xpreferred_area_weights):    
    
    _actual_employee_average_weights = [[0 for i in range(4)] for j in [0]]
    _preferred_employee_average_weights = [[0 for i in range(4)] for j in [0]]
    # _actual_area_average_weights = [[0 for i in range(4)] for j in [0]]
    # _preferred_area_average_weights = [[0 for i in range(4)] for j in [0]]
    
    for i in range(6):
        _actual_employee_average_weights = \
            np.add(_actual_employee_average_weights, xactual_employee_weights[i])
        _preferred_employee_average_weights = \
            np.add(_preferred_employee_average_weights, xpreferred_employee_weights[i])
        # _actual_area_average_weights = \
        #     np.add(_actual_area_average_weights, xactual_area_weights[i])
        # _preferred_area_average_weights = \
        #     np.add(_preferred_area_average_weights, xpreferred_area_weights[i])
            
    _actual_employee_average_weights = _actual_employee_average_weights/ 6
    _preferred_employee_average_weights = _preferred_employee_average_weights / 6
    # _actual_area_average_weights = _actual_area_average_weights / 6
    # _preferred_area_average_weights = _preferred_area_average_weights / 6
    
    return _actual_employee_average_weights, _preferred_employee_average_weights
        
        # , _actual_area_average_weights,\
        #     _preferred_area_average_weights

