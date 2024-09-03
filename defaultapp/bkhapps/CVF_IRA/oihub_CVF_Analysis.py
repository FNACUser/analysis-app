# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 21:58:37 2023

@author: luis.caro
"""

from bokeh.plotting import figure, output_file, show

import pandas as pd
import numpy as np

# from neo4j_learn_ONA import conn, insert_data


# from bokeh.models.widgets.inputs import NumericInput 
from bokeh.io import curdoc

from bokeh.layouts import column, row

from bokeh.models import Div, Tabs, TabPanel, Select, Label 

# from bokeh.plotting import figure

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_EmptyParagraph

from defaultapp.bkhapps.common.Utilities import UT_CountOcurrences, FD_cut_name

from .oihub_CVF_Functions import (FD_actual_preferred_weights_arrays,
                           FD_plot_weights_position, FD_CVF_plot,
                           FD_fetch_employee_culture_GDB,
                           FD_employee_list_score, FD_selected_employees_score,
                           FD_fetch_valid_employees_areas)

#%% Temporal para tomar válidos - hay que arreglar GDB
# from sqlalchemy_pure_connection_cloud import session_scope
# from new_db_schema import CVF_Culture_input_form
#%%
# from finacIRANewSurveyApp import db

# from finacIRANewSurveyModels import (IRA_Employees, IRA_Cycles,
#                                       CVF_Culture_modes, 
#                                       CVF_Culture_modes_themes,
#                                       CVF_Culture_modes_themes_questions,
#                                       CVF_Culture_quadrants,
#                                       CVF_Culture_input_form,
#                                       CVF_Questions_responses,
#                                       CVF_Themes_responses)

# from finacIRAappSurveyQueryFunctions import IRA_general_queries

# from CVF_Utilities import (FD_fetch_employee_culture, UT_label_to_id,
# from CVF_Utilities import (UT_label_to_id, FD_questions_responses_to_DF)

#:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_

# def UT_label_to_id(xtable,xlabel_field,xid_field,xlabel_value):
#     """
#     devuelve el id de un registro de una tabla
#     """
#     # print(xtable)
#     # print(xlabel_field)
#     # print(xid_field)
#     # print(xlabel_value)
#     id_value = xtable[xtable[xlabel_field] == xlabel_value].iloc[0][xid_field]
#     # print(id_value)
#     return int(id_value)

# def FD_fetch_employee_culture_GDB(xid_employee):
#     query = """MATCH (e:Employee{id_employee:$employee_id})
#                         <-[CONTESTADA_POR]-(r:Respuesta)-
#                         [RESPUESTA_DE]->(p:Pregunta),
#                         (p:Pregunta)-[DE_TEMA]->(t:Tema),
#                         (p:Pregunta)-[DE_CUADRANTE]->(c:Cuadrante) 
#                         RETURN r.id_respuesta AS id_question_response,
#                         t.id_tema AS id_culture_mode_theme,
#                         t.tema AS culture_mode_theme,
#                         p.id_pregunta AS id_culture_mode_theme_question, 
#                         c.id_cuadrante AS id_culture_quadrant,
#                         c.cuadrante AS culture_quadrant,
#                         r.actual AS Actual, r.preferido AS Preferred
#             """

#     params = {'employee_id': xid_employee}

#     result = conn.query(query, parameters=params)

#     employee_culture = pd.DataFrame([dict(_) for _ in result])
    
#     return employee_culture

# a=FD_fetch_employee_culture_GDB(93)
# a.to_dict('records')

# def FD_fetch_complete_culture_input_forms():
#     query = """MATCH (r:Respuesta)-[OF_CULTURE_FORM]->(cif:Culture_input_form)
#                 -[OF_CYCLE]->(c:Cycle{id_cycle:1})
#                 RETURN cif.id_culture_input_form, r.id_respuesta
#             """
            
#     result = conn.query(query) #, parameters=params)
    
#     all_culture_input_forms_df = pd.DataFrame([dict(_) for _ in result])
    
#     grouped_culture_input_forms_df =\
#         all_culture_input_forms_df.groupby(['cif.id_culture_input_form']).\
#             size().reset_index(name='counts')
        
#     complete_culture_input_forms_df = \
#         grouped_culture_input_forms_df.\
#             loc[grouped_culture_input_forms_df.counts == 24]

#     complete_culture_input_forms = \
#         list(complete_culture_input_forms_df['cif.id_culture_input_form'])
        
#     return set(complete_culture_input_forms)


def FD_culture_modes_themes_questions_to_DF(xcVF_culture_modes_themes_questions):
    
    r= [(cmtq.id, cmtq.culture_mode_theme.id, 
         cmtq.culture_mode_theme.Culture_mode_theme, 
         cmtq.culture_quadrant.id, cmtq.culture_quadrant.Culture_quadrant)\
        for cmtq in xcVF_culture_modes_themes_questions]
        
    df = pd.DataFrame.from_records(r, columns=['id_culture_mode_theme_question', 
                                               'id_culture_mode_theme',
                                               'id_culture_mode',
                                               'id_culture_quadrant',
                                               'culture_quadrant'])
    return df


# a=cVF_Culture_modes_themes_questions =\
#     CVF_Culture_modes_themes_questions.query.all()
# FD_culture_modes_themes_questions_to_DF(a)

# def FD_questions_responses_to_DF(xcVF_questions_responses):
    
#     r= [(qr.id, qr.theme_responses.id,
#          qr.theme_responses.culture_mode_theme.id,
#          qr.theme_responses.culture_mode_theme.Culture_mode_theme,
#          qr.modes_themes_question.id,
#          qr.modes_themes_question.culture_quadrant.id,
#          qr.modes_themes_question.culture_quadrant.Culture_quadrant,
#          qr.Actual, qr.Preferred)\
#         for qr in xcVF_questions_responses]
        
#     df = pd.DataFrame.from_records(r, columns=['id_question_response', 
#                                                'id_themes_responses',
#                                                'id_culture_mode_theme',
#                                                'culture_mode_theme',
#                                                'id_culture_mode_theme_question',
#                                                'id_culture_quadrant',
#                                                'culture_quadrant',
#                                                'Actual','Preferred'])

#     return df

def FD_culture_modes_themes_to_dict(xconn):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- FD_culture_modes_themes_to_dict')
    
    # culture_modes_themes = CVF_Culture_modes_themes.query.all()
    
    # r=[(cmt.id, cmt.Culture_mode_theme) for cmt in culture_modes_themes]
    
    # culture_modes_themes_df = \
    #     pd.DataFrame.from_records(r, columns=['id_culture_mode_theme',
    #                                           'culture_mode_theme'])
        
    query = """MATCH (t:Tema) 
                RETURN t.id_tema AS id_culture_mode_theme,
                t.tema AS culture_mode_theme
            """

    result = xconn.query(query) #, parameters=params)

    culture_modes_themes_df = pd.DataFrame([dict(_) for _ in result])
    
    print('>>>>>>>>>> culture_modes_themes_df (FD_culture_modes_themes_to_dict)')
    print(culture_modes_themes_df)
    print('>>>>>>>>>> culture_modes_themes_df.columns (FD_culture_modes_themes_to_dict)')
    print(culture_modes_themes_df.columns)
    
    
    culture_modes_dict = \
        culture_modes_themes_df.set_index('id_culture_mode_theme')\
            ['culture_mode_theme'].to_dict()
    
    return culture_modes_dict

# query = """MATCH (t:Tema) 
#             RETURN t.id_tema AS id_culture_mode_theme,
#             t.tema AS culture_mode_theme
#         """

# result = conn.query(query) #, parameters=params)

# culture_modes_themes_df = pd.DataFrame([dict(_) for _ in result])

# culture_modes_dict = \
#     culture_modes_themes_df.set_index('id_culture_mode_theme')\
#         ['culture_mode_theme'].to_dict()
        
# culture_modes_dict

# FD_culture_modes_themes_to_dict()
#.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# employee = IRA_Employees.query.\
#     filter_by(id_employee= 3).first()
# employee
# IRA_Cycles.query.all()

# def FD_fetch_employee_culture(xid_employee):
#     cVF_Culture_input_form = CVF_Culture_input_form.query.\
#         filter(CVF_Culture_input_form.id_employee == xid_employee).first()
#     cVF_Culture_input_form.id
    
#     cVF_Themes_responses = CVF_Themes_responses.query.\
#         filter(CVF_Themes_responses.id_culture_input_form == \
#                cVF_Culture_input_form.id).all()
#     cVF_Themes_responses
    
#     cVF_questions_responses = [CVF_Questions_responses.query.\
#      filter(CVF_Questions_responses.id_theme_responses == theme_responses.id).all() \
#          for theme_responses in cVF_Themes_responses]
#     cVF_questions_responses
    
#     questions_responses_flat_list = \
#         [item for sublist in cVF_questions_responses for item in sublist]
    
    
#     questions_responses_df = \
#         FD_questions_responses_to_DF(questions_responses_flat_list)
#     questions_responses_df.to_dict('records')
    
#     questions_responses_df.shape
    
#     culture_modes_df = UT_CountOcurrences(questions_responses_df,
#                                           ['id_culture_mode_theme',
#                                            'culture_mode_theme'])
    
#     # culture_modes_dict = \
#     #     culture_modes_df.set_index('id_culture_mode_theme')['culture_mode_theme'].\
#     #         to_dict()
#     # culture_modes_dict
    
#     return questions_responses_df
# , culture_modes_dict

# questions_responses_df, culture_modes_dict = FD_fetch_employee_culture(1)
# questions_responses_df.to_dict('records')

def FD_average_weights(xactual_employee_weights, xpreferred_employee_weights,
                       xactual_area_weights, xpreferred_area_weights): 
    
    print('>>>>>>>>>>>>>>>>>>>>>> FD_average_weights')
    print('.-.-.-.-.-.-.-.-.- xactual_employee_weights (FD_average_weights)')
    print(xactual_employee_weights)
    
    # a=5/0
    
    _actual_employee_average_weights = [[0 for i in range(4)] for j in [0]]
    _preferred_employee_average_weights = [[0 for i in range(4)] for j in [0]]
    _actual_area_average_weights = [[0 for i in range(4)] for j in [0]]
    _preferred_area_average_weights = [[0 for i in range(4)] for j in [0]]
    
    print('.-.-.-.-.-.-.-.-.- _actual_employee_average_weights (FD_average_weights)')
    print(_actual_employee_average_weights)
    
    for i in range(6):
        _actual_employee_average_weights = \
            np.add(_actual_employee_average_weights, xactual_employee_weights[i])
        _preferred_employee_average_weights = \
            np.add(_preferred_employee_average_weights, xpreferred_employee_weights[i])
        _actual_area_average_weights = \
            np.add(_actual_area_average_weights, xactual_area_weights[i])
        _preferred_area_average_weights = \
            np.add(_preferred_area_average_weights, xpreferred_area_weights[i])
    
    print('.-.-.-.-.-.-.-.-.- _actual_employee_average_weights (FD_average_weights)')
    print(_actual_employee_average_weights)
            
    
    _actual_employee_average_weights = _actual_employee_average_weights/ 6
    _preferred_employee_average_weights = _preferred_employee_average_weights / 6
    _actual_area_average_weights = _actual_area_average_weights / 6
    _preferred_area_average_weights = _preferred_area_average_weights / 6
    
    return _actual_employee_average_weights, \
        _preferred_employee_average_weights, _actual_area_average_weights,\
            _preferred_area_average_weights


# def FD_actual_preferred_weights_arrays(xquestions_responses_df):
    
#     # print('>>>>>>>>>>>>>>>> FD_actual_preferred_weights_arrays')
#     # print('.-.-.-.-.-.-. xquestions_responses_df FD_actual_preferred_weights_arrays')
#     # print(xquestions_responses_df)
    
#     rows, cols = (6, 4)
#     arr_actual = [[0 for i in range(cols)] for j in range(rows)]
#     arr_preferred = [[0 for i in range(cols)] for j in range(rows)]
    
    
#     for index, df_row in xquestions_responses_df.iterrows():
        
#         # print('.-.-.-.-.-.-.-.-.-.-.-.')
#         # print(row)
#         # print(row['id_culture_mode_theme'])
#         # print(row['id_culture_quadrant'])
        
#         arr_actual[df_row['id_culture_mode_theme']-1]\
#             [df_row['id_culture_quadrant']-1] = df_row['Actual']
#         arr_preferred[df_row['id_culture_mode_theme']-1]\
#             [df_row['id_culture_quadrant']-1] = df_row['Preferred']
        
#         # print(arr_actual)
#         # print(arr_preferred)
        
#     return arr_actual, arr_preferred
    

# def FD_plot_weights_position(xweights):
    
#     # print('>>>>>>>>>>>>> FD_plot_weights_position')
#     # print('.-.-.-.-.-.-.-.- xweights - FD_plot_weights_position')
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
    
#     # print(x_coordinates_list)
#     # print(y_coordinates_list)
    
#     return x_coordinates_list, y_coordinates_list
    

# def FD_CVF_plot(xactual_employee_weights, xpreferred_employee_weights,
#                 xactual_area_weights, xpreferred_area_weights,
#                 xtitle = "", xwidth=250, xheight=250):
    
#     cvf_plot = figure(width = xwidth, height = xheight)

#     nan = float('nan')
#     cvf_plot.line([0, 10, nan, 10, 0], [0, 10, nan, 0,10], 
#                   line_width=2, line_dash='dashed', line_color='grey')
#     cvf_plot.line([0, 10, nan, 5, 5], [5, 5, nan, 0,10], 
#                   line_width=2, line_dash='solid', line_color='grey')

#     actual_employee_culture = FD_plot_weights_position(xactual_employee_weights)
#     preferred_employee_culture = FD_plot_weights_position(xpreferred_employee_weights)
    
#     actual_area_culture = FD_plot_weights_position(xactual_area_weights)
#     preferred_area_culture = FD_plot_weights_position(xpreferred_area_weights)

#     # cvf_plot.patches([actual_employee_culture[0], preferred_employee_culture[0]], 
#     #                  [actual_employee_culture[1], preferred_employee_culture[1]],
#     #           color=["firebrick", ""], alpha=[0.8, 0.3], line_width=2,
#     #           line_dash = ['solid', 'dashed'], 
#     #           line_color = ['firebrick', 'firebrick'])
    
#     print('.-.-.-.-.-.-.-.-.-.-.-.-.- FD_CVF_plot')
#     print('actual_employee_culture[0], actual_employee_culture[1]')
#     print(actual_employee_culture[0], actual_employee_culture[1])
#     print('preferred_employee_culture[0], preferred_employee_culture[1]')
#     print(preferred_employee_culture[0], preferred_employee_culture[1])
#     print('actual_area_culture[0], actual_area_culture[1]')
#     print(actual_area_culture[0], actual_area_culture[1])
#     print('preferred_area_culture[0], preferred_area_culture[1]')
#     print(preferred_area_culture[0], preferred_area_culture[1])
    
#     cvf_plot.patches([actual_employee_culture[0], preferred_employee_culture[0],
#                       actual_area_culture[0], preferred_area_culture[0]], 
#                       [actual_employee_culture[1], preferred_employee_culture[1],
#                       actual_area_culture[1], preferred_area_culture[1]],
#               color=["firebrick", "","navy", ""], alpha=[0.5, 0.5,0.5, 0.5], line_width=2,
#               line_dash = ['solid', 'dashed','solid', 'dashed'], 
#               line_color = ['firebrick', 'firebrick','navy', 'navy'])
    
#     # cvf_plot.patches([actual_employee_culture[0], preferred_employee_culture[0]], 
#     #                  [actual_employee_culture[1], preferred_employee_culture[1]],
#     #           color=["firebrick", ""], alpha=[0.5, 0.5], line_width=2,
#     #           line_dash = ['solid', 'dashed'], 
#     #           line_color = ['firebrick', 'firebrick'])
    
#     cvf_plot.xaxis.major_label_text_font_size = '0pt'  # turn off x-axis tick labels
#     cvf_plot.yaxis.major_label_text_font_size = '0pt'  # turn off y-axis tick labels
#     cvf_plot.xaxis.visible = False
#     cvf_plot.yaxis.visible = False
    
#     cvf_plot.title.text = xtitle
    
#     left_x = xwidth * .045
#     top_y = xheight * .75
#     bottom_y = xheight * .045
#     adhocracy_x = xwidth * .60
#     market_x =  xwidth * .70
#     # clan_annotation = Label(x=left_x, y=top_y, x_units='screen', y_units='screen',
#     clan_annotation = Label(x=0, y=9, x_units='data', y_units='data',
#                  text='Clan', render_mode='css',
#                  border_line_color='black', border_line_alpha=1.0,
#                  background_fill_color='white', background_fill_alpha=1.0)
#     # adhocracy_annotation = Label(x=adhocracy_x, y=top_y, x_units='screen', y_units='screen',
#     adhocracy_annotation = Label(x=6, y=9, x_units='data', y_units='data',
#                  text='Adhocracia', render_mode='css',
#                  border_line_color='black', border_line_alpha=1.0,
#                  background_fill_color='white', background_fill_alpha=1.0)
#     # hierarchy_annotation = Label(x=left_x, y=bottom_y, x_units='screen', y_units='screen',
#     hierarchy_annotation = Label(x=0, y=0, x_units='data', y_units='data',
#                  text='Jerarquía', render_mode='css',
#                  border_line_color='black', border_line_alpha=1.0,
#                  background_fill_color='white', background_fill_alpha=1.0)
#     market_annotation = Label(x=6.5, y=0, x_units='data', y_units='data',
#                  text='Mercado', render_mode='css',
#                  border_line_color='black', border_line_alpha=1.0,
#                  background_fill_color='white', background_fill_alpha=1.0)
#     cvf_plot.add_layout(clan_annotation)
#     cvf_plot.add_layout(adhocracy_annotation)
#     cvf_plot.add_layout(hierarchy_annotation)
#     cvf_plot.add_layout(market_annotation)
    
#     return cvf_plot


# def FD_employee_list_score(xemployee_list):
    
#     print('>>>>>>>>>> FD_employee_list_score')
#     print('.------- xemployee_list (FD_employee_list_score)')
#     print(xemployee_list)
    
#     rows, cols = (6, 4)
#     arr_actual_accumulated = [[0 for i in range(cols)] for j in range(rows)]
#     arr_preferred_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    
#     for employee_id in xemployee_list:
#         # print('employee_id')
#         # print(employee_id)
#         _questions_responses_df = FD_fetch_employee_culture_GDB(employee_id)
#         _arr_actual, _arr_preferred = \
#             FD_actual_preferred_weights_arrays(_questions_responses_df)
#         # print('_arr_actual, _arr_preferred')
#         # print(_arr_actual, _arr_preferred)
#         arr_actual_accumulated = np.add(arr_actual_accumulated,
#                                            _arr_actual)
#         arr_preferred_accumulated = np.add(arr_preferred_accumulated,
#                                            _arr_preferred)
#         # print('arr_actual_accumulated, arr_preferred_accumulated')
#         # print(arr_actual_accumulated, arr_preferred_accumulated)
        
#     arr_actual_accumulated = arr_actual_accumulated / len(xemployee_list)
#     # len_xemployee_list = len(xemployee_list)
#     # arr_actual_accumulated = \
#     #     [aaa/len_xemployee_list for aaa in arr_actual_accumulated]
#     arr_preferred_accumulated = arr_preferred_accumulated / len(xemployee_list)
#     # arr_preferred_accumulated = \
#     #     [aaa/len_xemployee_list for aaa in arr_preferred_accumulated]
        
#     return arr_actual_accumulated, arr_preferred_accumulated

# arr_actual_accumulated, arr_preferred_accumulated =\
#     FD_employee_list_score([1])
# arr_actual_accumulated

# a=FD_fetch_employee_culture(1)
# a.columns
# a.shape


# a=FD_fetch_employee_culture_GDB(1)
# a.columns
# a.shape



def FD_selected_areas_score(xconn, xarea_selector, xemployee_selector, 
                            xira_employees_areas, 
                            xids_employees_to_exclude_from_average):
    
    print('>>>>>>>>> oihub_CVF_Analysis/FD_selected_areas_score')
    
    
    
    
    if xarea_selector.value == '-Todas':
        employee_list =\
            [id_employee
             for id_employee in list(xira_employees_areas['id_employee'])
             if id_employee not in xids_employees_to_exclude_from_average]
    else:
        _xira_employees_areas = xira_employees_areas.\
             loc[xira_employees_areas.organization_area == \
                 xarea_selector.value]
        employee_list = \
            [id_employee
             for id_employee in list(xira_employees_areas['id_employee'])
             if id_employee not in xids_employees_to_exclude_from_average]
        
        selector_employee_list = list(_xira_employees_areas['employee'])
        print(selector_employee_list)
        selector_employee_list.append('-Todos')
        print(selector_employee_list)
        xemployee_selector.options = sorted(selector_employee_list) 
                
                
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


# def FD_selected_employees_score(xarea_selector, xemployee_selector, 
#                                 xira_employees_areas):
    
#     # rows, cols = (6, 4)
#     # arr_actual_accumulated = [[0 for i in range(cols)] for j in range(rows)]
#     # arr_preferred_accumulated = [[0 for i in range(cols)] for j in range(rows)]
    
#     print('>>>>>>>>>>> FD_selected_employees_score')
#     print(xarea_selector.value)
#     print(xemployee_selector.value)
    
    
#     #
#     #selecciona las filas de ira_employees_areas que corresponden a los
#     #empleados del área
#     if xarea_selector.value == '-Todas':
#         _xira_employees_areas = xira_employees_areas
#     else:
#         _xira_employees_areas = xira_employees_areas.\
#             loc[xira_employees_areas.organization_area == xarea_selector.value]
    
#     #
#     #selecciona los empleados a incluir (puede ser uno solo)
#     if xemployee_selector.value == '-Todos':
#         employee_list = list(_xira_employees_areas['id_employee'])
#     else:
#         employee_list = \
#             list(_xira_employees_areas.\
#                  loc[_xira_employees_areas.employee == \
#                      xemployee_selector.value]['id_employee'])
                
#     print(employee_list)
    
#     arr_actual_accumulated, arr_preferred_accumulated =\
#         FD_employee_list_score(employee_list)
    
#     # for employee_id in employee_list:
#     #     # print('employee_id')
#     #     # print(employee_id)
#     #     _questions_responses_df, _culture_modes_dict = \
#     #         FD_fetch_employee_culture(employee_id)
#     #     _arr_actual, _arr_preferred = \
#     #         FD_actual_preferred_weights_arrays(_questions_responses_df)
#     #     # print('_arr_actual, _arr_preferred')
#     #     # print(_arr_actual, _arr_preferred)
#     #     arr_actual_accumulated = np.add(arr_actual_accumulated,
#     #                                        _arr_actual)
#     #     arr_preferred_accumulated = np.add(arr_preferred_accumulated,
#     #                                        _arr_preferred)
#     #     # print('arr_actual_accumulated, arr_preferred_accumulated')
#     #     # print(arr_actual_accumulated, arr_preferred_accumulated)
        
#     # arr_actual_accumulated = arr_actual_accumulated / len(employee_list)
#     # arr_preferred_accumulated = arr_preferred_accumulated / len(employee_list)
        
#     return arr_actual_accumulated, arr_preferred_accumulated

       
#.-.-.-.-.-.-. datos básicos generales 

#reemplazado por GDB
# ira_cycles, _, ira_employees_areas, _, _, _ = IRA_general_queries()
# ira_employees_areas.columns
# ira_employees_areas.shape

#ira_cycles todavía noestá en el GDB



#.-.-.-.-.-.-. selectores
#.-.-.-.-.-.-. selectores

def update_employee(xconn, xselector_employee, xselector_area, xselector_cycle, 
                    xcvf_plot1, xcvf_plot2, 
                    xcvf_plot3, xcvf_plot4, xcvf_plot5, xcvf_plot6, 
                    xcvf_plot_average, xira_employees_areas, 
                    xids_employees_to_exclude_from_average):
    
    print('.-.-.-.-.-.-.-.- update_employee')
    print('.-.-.-.-.-.-.-.- update_employee')
    print('.-.-.-.-.-.-.-.- update_employee')
    print('.-.-.-.-.-.-.-.- update_employee')
    print(xselector_area.value)
    print(xselector_employee.value)
    
    # id_employee = UT_label_to_id(xira_employees_areas, 'employee',
    #                              'id_employee', 
    #                              selector_employee.value)    
    
    # _questions_responses_df = FD_fetch_employee_culture(id_employee)
    
    # _actual_employee_weights, _preferred_employee_weights = \
    #     FD_actual_preferred_weights_arrays(_questions_responses_df)
        
    # _actual_area_weights, _preferred_area_weights = \
    #     FD_selected_areas_score(xselector_area.value, xira_employees_areas)
        
    #.-.-.-.-.-.-
    
    _actual_employee_weights, _preferred_employee_weights = \
        FD_selected_employees_score(xconn, xselector_area, 
                                    xselector_employee, 
                                    xira_employees_areas)
    print('>>>>>>>>>>>>>>>>>>>>> _actual_employee_weights (update_employee)')
    print(_actual_employee_weights)
    print('>>>>>>>>>>>>>>>>>> _preferred_employee_weights (update_employee)')
    print(_preferred_employee_weights)
        
    _actual_area_weights, _preferred_area_weights = \
        FD_selected_areas_score(xconn, xselector_area, xselector_employee, 
                                xira_employees_areas, 
                                xids_employees_to_exclude_from_average)
    
    #:_:_:_:_:_

    _cvf_plot1 = FD_CVF_plot(_actual_employee_weights[0],
                             _preferred_employee_weights[0],
                             _actual_area_weights[0], _preferred_area_weights[0])
                             # _culture_modes_dict.get(1))
    _cvf_plot2 = FD_CVF_plot(_actual_employee_weights[1],
                             _preferred_employee_weights[1],
                             _actual_area_weights[1], _preferred_area_weights[1])
                             # _culture_modes_dict.get(2))
    _cvf_plot3 = FD_CVF_plot(_actual_employee_weights[2],
                             _preferred_employee_weights[2],
                             _actual_area_weights[2], _preferred_area_weights[2])
                             # _culture_modes_dict.get(3))
    _cvf_plot4 = FD_CVF_plot(_actual_employee_weights[3],
                             _preferred_employee_weights[3],
                             _actual_area_weights[3], _preferred_area_weights[3])
                             # _culture_modes_dict.get(4))
    _cvf_plot5 = FD_CVF_plot(_actual_employee_weights[4],
                             _preferred_employee_weights[4],
                             _actual_area_weights[4], _preferred_area_weights[4])
                             # _culture_modes_dict.get(5))
    _cvf_plot6 = FD_CVF_plot(_actual_employee_weights[5],
                             _preferred_employee_weights[5],
                             _actual_area_weights[5], _preferred_area_weights[5])
                             # _culture_modes_dict.get(6))
    
    _actual_employee_average_weights, _preferred_employee_average_weights, \
        _actual_area_average_weights, _preferred_area_average_weights = \
            FD_average_weights(_actual_employee_weights, 
                               _preferred_employee_weights,
                               _actual_area_weights, _preferred_area_weights)
    print('updated promedio')
    _cvf_plot_average = FD_CVF_plot(_actual_employee_average_weights[0],
                                    _preferred_employee_average_weights[0],
                                    _actual_area_average_weights[0],
                                    _preferred_area_average_weights[0])
 
        
    def update_plot(xplot, _plot):
        datasource = _plot.renderers[2].data_source
        xplot.renderers[2].data_source.data = dict(datasource.data)
        datasource3 = _plot.renderers[3].data_source
        xplot.renderers[3].data_source.data = dict(datasource3.data)
        datasource4 = _plot.renderers[4].data_source
        xplot.renderers[4].data_source.data = dict(datasource4.data)
        datasource5 = _plot.renderers[5].data_source
        xplot.renderers[5].data_source.data = dict(datasource5.data)
        datasource6 = _plot.renderers[6].data_source
        xplot.renderers[6].data_source.data = dict(datasource6.data)
        
    update_plot(xcvf_plot1, _cvf_plot1)
    update_plot(xcvf_plot2, _cvf_plot2)
    update_plot(xcvf_plot3, _cvf_plot3)
    update_plot(xcvf_plot4, _cvf_plot4)
    update_plot(xcvf_plot5, _cvf_plot5)
    update_plot(xcvf_plot6, _cvf_plot6)
    update_plot(xcvf_plot_average, _cvf_plot_average)
    
    # datasource1 = _cvf_plot1.renderers[2].data_source
    # xcvf_plot1.renderers[2].data_source.data = dict(datasource1.data)
    # datasource2 = _cvf_plot2.renderers[2].data_source
    # xcvf_plot2.renderers[2].data_source.data = dict(datasource2.data)
    # datasource3 = _cvf_plot3.renderers[2].data_source
    # xcvf_plot3.renderers[2].data_source.data = dict(datasource3.data)
    # datasource4 = _cvf_plot4.renderers[2].data_source
    # xcvf_plot4.renderers[2].data_source.data = dict(datasource4.data)
    # datasource5 = _cvf_plot5.renderers[2].data_source
    # xcvf_plot5.renderers[2].data_source.data = dict(datasource5.data)
    # datasource6 = _cvf_plot6.renderers[2].data_source
    # xcvf_plot6.renderers[2].data_source.data = dict(datasource6.data)
    # datasource_average = _cvf_plot_average.renderers[2].data_source
    # xcvf_plot_average.renderers[2].data_source.data = \
    #     dict(datasource_average.data)
    
    xselector_cycle.value = xselector_cycle.options[0]    

    print(':_:_:_:_:_:_:_:_:_:_:_:_:_: fin update_employee')
    print(':_:_:_:_:_:_:_:_:_:_:_:_:_: fin update_employee')
    print(':_:_:_:_:_:_:_:_:_:_:_:_:_: fin update_employee')
        
    
def update_organization_area(xconn, xselector_employee, xselector_area, 
                             xselector_cycle, xcvf_plot1, 
                             xcvf_plot2, xcvf_plot3, xcvf_plot4, xcvf_plot5, 
                             xcvf_plot6, xcvf_plot_average, 
                             xira_employees_areas, 
                             xids_employees_to_exclude_from_average):
    
    print('.-.-.-.-.-.-.-.- update_organization_area')
    print(xselector_area.value)
    print(xselector_employee.value)
    
    xselector_employee.value = '-Todos'
    
    update_employee(xconn, xselector_employee, xselector_area, xselector_cycle,
                    xcvf_plot1, xcvf_plot2, 
                        xcvf_plot3, xcvf_plot4, xcvf_plot5, xcvf_plot6, 
                        xcvf_plot_average, xira_employees_areas, 
                        xids_employees_to_exclude_from_average)
    
    xselector_cycle.value = xselector_cycle.options[0]      


def update_cycle():
    print('.-.-.-.-.-.-.-.- update_cycle')
    

def FD_Main_analysis(xconn, xids_employees_to_exclude_from_average):
    
    print('.-.-.-.-.-.-.-.-.-.-. oihub_CVF_Analysis/FD_Main_analysis')
    ira_cycles_tuples = [(1, 'mayo-2023', True)]
    ira_cycles = pd.DataFrame(ira_cycles_tuples, columns=['id_cycle','cycle',
                                                          'is_active'])
    
    # query = """MATCH (e:Employee)-[FUNCIONARIO_DE]->(a:Organization_area) 
    #             WHERE e.is_active = True AND e.id_employee IS NOT NULL
    #             RETURN e.id_employee AS id_employee, e.redmine_login AS id_user, 
    #             e.employee AS employee,
    #             a.id_organization_area AS id_organization_area, 
    #             a.organization_area AS organization_area
    #         """
            
    # result = conn.query(query) #, parameters=params)
    
    # ira_employees_areas = pd.DataFrame([dict(_) for _ in result])
    
    # print('>>>>>>>>>>>>>>>>> ira_employees_areas (oihub_CVF_Analysis/FD_Main_analysis)')
    # print(ira_employees_areas.to_dict('records'))
    
    # complete_culture_input_forms = \
    #     FD_fetch_complete_culture_input_forms()
    
    # query = """MATCH (e:Employee)<-[OF_EMPLOYEE]-(cif:Culture_input_form)-
    #             [OF_CYCLE]->(c:Cycle{id_cycle:1}) 
    #             RETURN cif.id_culture_input_form as id_culture_input_form, 
    #             e.id_employee as id_employee, c.id_cycle as id_cycle
    #         """
            
    # result = conn.query(query) #, parameters=params)
    
    # all_culture_input_forms_df = pd.DataFrame([dict(_) for _ in result])
    # all_culture_input_forms_df['id_culture_mode'] = 1
    # all_culture_input_forms_df['Is_concluded'] = True
    
    # culture_input_forms_df = \
    #     all_culture_input_forms_df\
    #         [all_culture_input_forms_df['id_culture_input_form'].isin\
    #          (complete_culture_input_forms)]
    
    # print('>>>>>>>>>>>>>>>>> culture_input_forms_df (oihub_CVF_Analysis/FD_Main_analysis)')
    # print(culture_input_forms_df.to_dict('records'))
    
    
    # #.-.-.-.-.-.-.-.- Temporal
    # with session_scope() as session:
    #     culture_input_forms = session.query(CVF_Culture_input_form).all()
    
    # culture_input_forms
    
    # culture_input_forms_tuples = [(cif.id, cif.id_employee, cif.id_cycle,
    #                                cif.id_culture_mode, cif.Is_concluded) \
    #                                    for cif in culture_input_forms]
    # culture_input_forms_df = \
    #     pd.DataFrame.from_records(culture_input_forms_tuples, 
    #                               columns=['id', 'id_employee',
    #                                        'id_cycle', 'id_culture_mode',
    #                                        'Is_concluded'])
    # print('>>>>>>>>>>>>>>>>> culture_input_forms_df (oihub/oihub_CVF_Analysis)')
    # print(culture_input_forms_df.to_dict('records'))
    
    # valid_employees = list(culture_input_forms_df.loc\
    #                        [culture_input_forms_df.Is_concluded == True]\
    #                            ['id_employee'])
    # valid_employees = list(culture_input_forms_df.loc\
    #                        [culture_input_forms_df.Is_concluded == True]\
    #                            ['id_employee'])
    # print('>>>>>>>>>>>>>>>>> valid_employees (oihub_CVF_Analysis/FD_Main_analysis)')
    # print(valid_employees)
    
    # ira_employees_areas = \
    #     ira_employees_areas.loc[ira_employees_areas['id_employee'].\
    #                             isin(valid_employees)]
    #:_:_:_:_:_:_:_:_:_:_ fin Temporal
    
    ira_employees_areas = FD_fetch_valid_employees_areas(xconn)
    print('>>>>>>>>>>>>>>>>> ira_employees_areas (FD_Main_analysis)')
    print(ira_employees_areas.to_dict('records'))
    
    #.-.-.-.-.-.-.-.-.-.-. solo por bacanos
    def change_name(xrow):
        if xrow['employee'] == 'Humberto Zuluaga':
            return 'Roberto Echeverría'
        else:
            return xrow['employee']
    def change_area(xrow):
        if xrow['employee'] == 'Roberto Echeverría':
            return 'Commodities'
        else:
            return xrow['organization_area']
    
    ira_employees_areas['employee'] =\
        ira_employees_areas.apply(lambda x: change_name(x), axis=1)
    ira_employees_areas['organization_area'] =\
        ira_employees_areas.apply(lambda x: change_area(x), axis=1)
    ira_employees_areas['employee'] =\
        ira_employees_areas['employee'].apply(lambda x: FD_cut_name(x))
    #:_:_:_:_:_:_:_:__:_: fin solo por bacanos 
    
    print('>>>>>>>>>>>>>>>>> ira_employees_areas (FD_Main_analysis)')
    print(ira_employees_areas.to_dict('records'))
    
    valid_employees = list(ira_employees_areas['id_employee'])
    
    
    #%%
    
    culture_modes_dict = FD_culture_modes_themes_to_dict(xconn)
    
    employees = ira_employees_areas['employee'].tolist()
    employees
    employees.append('-Todos')
    selector_employee = Select(title="Funcionario", value="-Todos", 
                         options = sorted(employees), 
                         width=200)
    
    organization_areas = \
        list(UT_CountOcurrences(ira_employees_areas,
                                ['organization_area'])['organization_area'])
    organization_areas.append('-Todas')
    selector_organization_area = Select(title="Area", value="-Todas", 
                                        options = sorted(organization_areas),
                                        width=200)
    
    selector_cycle = Select(title="Ciclo", value="",
                            options = [''] + ira_cycles['cycle'].tolist(), width=200)
    
    
    selector_employee.\
        on_change('value', lambda attr, old, new: \
                  update_employee(xconn, selector_employee, 
                                  selector_organization_area,
                                  selector_cycle,
                                  cvf_plot1, cvf_plot2, cvf_plot3, cvf_plot4, 
                                  cvf_plot5, cvf_plot6, cvf_plot_average, 
                                  ira_employees_areas,
                                  xids_employees_to_exclude_from_average))
    
    selector_organization_area.\
        on_change('value', lambda attr, old, new: \
                  update_organization_area(xconn, selector_employee, 
                                           selector_organization_area, 
                                           selector_cycle, cvf_plot1, 
                                           cvf_plot2, cvf_plot3, cvf_plot4,
                                           cvf_plot5, cvf_plot6, cvf_plot_average, 
                                           ira_employees_areas,
                                           xids_employees_to_exclude_from_average))
    
    selector_cycle.on_change('value', lambda attr, old, new: \
                             update_cycle())
    
    #:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_ fin Selectores
    #:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_:_ fin Selectores
    
    
            
    #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- Proceso
    #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- Proceso
    #-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- Proceso
    
    
    # questions_responses_df, culture_modes_dict = FD_fetch_employee_culture(1)
    # questions_responses_df.to_dict('records')
    
    
    # actual_employee_weights, preferred_employee_weights = \
    #     FD_actual_preferred_weights_arrays(questions_responses_df)
    
    # area="-Todas"
    # employee = "-Todos"
    
    actual_employee_weights, preferred_employee_weights = \
        FD_selected_employees_score(xconn, selector_organization_area, 
                                    selector_employee, ira_employees_areas)
    
    
    
    actual_area_weights, preferred_area_weights = \
        FD_selected_areas_score(xconn, selector_organization_area, selector_employee, 
                                ira_employees_areas, 
                                xids_employees_to_exclude_from_average)
    
    
    
    
    print('out employee-----actual_employee_weights, preferred_employee_weights')
    print(actual_employee_weights, preferred_employee_weights)
    print('out area-----actual_area_weights, preferred_area_weights')
    print(actual_area_weights, preferred_area_weights)
    print('out employee[0]-----actual_employee_weights[0], preferred_employee_weights[0]')
    print(actual_employee_weights[0], preferred_employee_weights[0])
    print('out area[0]-----actual_area_weights[0], preferred_area_weights[0]')
    print(actual_area_weights[0], preferred_area_weights[0])
    print('fin out :_:_:_:_:_:_:')
    
    
    cvf_plot1 = FD_CVF_plot(actual_employee_weights[0], preferred_employee_weights[0],
                            actual_area_weights[0], preferred_area_weights[0], 
                            xtitle = culture_modes_dict.get(1))
    cvf_plot2 = FD_CVF_plot(actual_employee_weights[1], preferred_employee_weights[1], 
                            actual_area_weights[1], preferred_area_weights[1], 
                            xtitle = culture_modes_dict.get(2))
    cvf_plot3 = FD_CVF_plot(actual_employee_weights[2], preferred_employee_weights[2], 
                            actual_area_weights[2], preferred_area_weights[2], 
                            xtitle = culture_modes_dict.get(3))
    cvf_plot4 = FD_CVF_plot(actual_employee_weights[3], preferred_employee_weights[3], 
                            actual_area_weights[3], preferred_area_weights[3], 
                            xtitle = culture_modes_dict.get(4))
    cvf_plot5 = FD_CVF_plot(actual_employee_weights[4], preferred_employee_weights[4], 
                            actual_area_weights[4], preferred_area_weights[4], 
                            xtitle = culture_modes_dict.get(5))
    cvf_plot6 = FD_CVF_plot(actual_employee_weights[5], preferred_employee_weights[5], 
                            actual_area_weights[5], preferred_area_weights[5], 
                            xtitle = culture_modes_dict.get(6))
    
    actual_employee_average_weights, preferred_employee_average_weights, \
        actual_area_average_weights, preferred_area_average_weights = \
            FD_average_weights(actual_employee_weights, preferred_employee_weights,
                               actual_area_weights, preferred_area_weights)
    
    cvf_plot_average = FD_CVF_plot(actual_employee_average_weights[0],
                                   preferred_employee_average_weights[0],
                                   actual_area_average_weights[0],
                                   preferred_area_average_weights[0],
                                   xtitle = 'Combinado', xwidth=500, xheight=500)
    
    
    # datasource1 = _cvf_plot1.renderers[1].data_source
    # xcvf_plot1.renderers[1].data_source.data = dict(datasource1.data)# cvf_plot1.renderers[0].data_source.data
    # cvf_plot1.renderers[1].data_source.data
    # cvf_plot1.renderers[2].data_source.data
    # cvf_plot1.renderers[0].data_source.data
    
    # datasource = _new_hm.renderers[0].data_source
    # xhm.renderers[0].data_source.data = dict(datasource.data)
    
    #.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-
    
    
    
    print(UT_CountOcurrences(ira_employees_areas,['organization_area']))

    return cvf_plot1, cvf_plot2, cvf_plot3, cvf_plot4, cvf_plot5, cvf_plot6,\
        selector_cycle, selector_employee, selector_organization_area,\
            cvf_plot_average, ira_employees_areas

# cvf_plot1, cvf_plot2, cvf_plot3, cvf_plot4, cvf_plot5, cvf_plot6,  \
#     selector_cycle, selector_employee, selector_organization_area,\
#         cvf_plot_average= FD_Main_analysis()

# segment_plots = column(row(cvf_plot1, UTBo_EmptyParagraph(10,5), 
#                             cvf_plot2, UTBo_EmptyParagraph(10,5),cvf_plot3),
#                         UTBo_EmptyParagraph(95,10),
#                         row(cvf_plot4, UTBo_EmptyParagraph(10,5), cvf_plot5,
#                             UTBo_EmptyParagraph(10,5), cvf_plot6))

# curdoc().add_root(column(row(selector_cycle, selector_employee, 
#                               selector_organization_area),
#                           row(segment_plots, UTBo_EmptyParagraph(10,5),
#                               cvf_plot_average)))
