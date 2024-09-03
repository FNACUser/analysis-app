# -*- coding: utf-8 -*-
"""
Created on Sat Jul  8 19:19:22 2023

@author: luis.caro
"""

import numpy as np
import pandas as pd
from functools import reduce
from math import pi
from bokeh.palettes import all_palettes


from bokeh.plotting import figure
from bokeh.models import TapTool, LabelSet, ColumnDataSource

# from neo4j_learn_ONA import conn, insert_data

from bokeh.io import show, curdoc
from bokeh.models import CustomJS, MultiSelect

from bokeh.layouts import row, column

from .oihub_AA_IRA_help_texts_objects import FD_build_question_help

# from oihub_UtilitiesBokeh import UTBo_Component_hmx
from defaultapp.bkhapps.common.oihub_UtilitiesBokeh_HeatMap import UTBoHM_Component_hm

from defaultapp.bkhapps.common.Utilities import UT_CountOcurrences


def FD_fetch_AA_questions(xconn):
    
    query = """MATCH (q:Question)-[QUESTION_FOR]->
                (nwm:Network_mode{network_mode:'Actor'})-[IS_OF_THEME]->
                (nwmt:Network_mode_theme) 
                RETURN q.id_question, q.question, nwmt.id_network_mode_theme,
                    nwmt.network_mode_theme, nwm.id_network_mode,
                        nwm.network_mode"""
                
    questions = xconn.query(query)

    questions_df = \
        pd.DataFrame([dict(_) for _ in questions])
        
    questions_df = questions_df.sort_values(['nwm.id_network_mode', 
                                             'q.id_question'],
                                            ascending=[True, True])
                                            # ascending=[False, False])
                                            
    questions_df.reset_index(drop=True, inplace=True)
    
    return questions_df

# FD_fetch_AA_questions()

def FD_fetch_AK_network_modes(xconn, xnetwork_modes_list):
    
    query_parameters = \
         {'network_modes': xnetwork_modes_list} 
         
         
    query = """WITH $network_modes AS network_modes
                MATCH (q:Question)-[QUESTION_FOR]->(nwm:Network_mode)
                WHERE nwm.id_network_mode IN network_modes
                RETURN nwm.id_network_mode, nwm.network_mode,
                q.id_question, q.question"""

    questions = xconn.query(query, parameters=query_parameters)

    questions_df = \
        pd.DataFrame([dict(_) for _ in questions])
        
    return questions_df


def findOccurrences(s, ch):
    return [i for i, letter in enumerate(s) if letter == ch]

def FD_unite_and_break_string(xprefix, xsufix, xlink_str, xline_length,
                              xmax_length):
    
    print('.-.-.-.-.-.-.-.-.-oihub_IRA_Questions/FD_unite_and_break_string')
    # print('>>>>>>>>>>>>>>>>> xprefix (FD_unite_and_break_string)')
    # print(xprefix)
    # print('>>>>>>>>>>>>>>>>> xsufix (FD_unite_and_break_string)')
    # print(xsufix)
    # print('>>>>>>>>>>>>>>>>> xline_length (FD_unite_and_break_string)')
    # print(xline_length)
    # print('>>>>>>>>>>>>>>>>> xmax_length (FD_unite_and_break_string)')
    # print(xmax_length)
    
    prefix = xprefix.strip()
    sufix = xsufix.strip()
    
    string = prefix + xlink_str + xsufix
    
    string = string.replace('\n', ' ').replace('\r', '')
    # print('>>>>>>>>>>>>>>>>> string (FD_unite_and_break_string)')
    # print(string)
    
    blanks_indexes = findOccurrences(string, ' ')
    # print('>>>>>>>>>>>>>>>>> blanks_indexes (FD_unite_and_break_string)')
    # print(blanks_indexes)
    
    parsed_length = xline_length
    line_feeds = []
    for blank_index in range(len(blanks_indexes)): 
        if blanks_indexes[blank_index] > parsed_length:
            line_feeds.append(blanks_indexes[blank_index-1])
            parsed_length += xline_length
    # print('>>>>>>>>>>>>>>>>> line_feeds (FD_unite_and_break_string)')
    # print(line_feeds)
            
    replaced_characters = 0
    for line_feed_index in range(len(line_feeds)):
        string = string[:line_feeds[line_feed_index]+replaced_characters] + \
                        '\n' + \
            string[line_feeds[line_feed_index]+replaced_characters+1:]
        # replaced_characters += 1
        
    string = string[:xmax_length]

    return string
    

# prefix = '   pppp   '
# sufix = '¿Acudo a esta persona para resolución de confl... Mi desarrollo profesional '    
# prefix    
# sufix
# link_str = ' / '
# line_length = 30
# max_length = 73

# string = FD_unite_and_break_string(prefix, sufix, link_str, line_length,
#                                    max_length)
# print(string)

# questions_df = FD_fetch_AA_questions()
# questions_df.columns

def questions_for_menu(xrow):
    
    # link_str = ' / '
    # line_length = 30
    # max_length = 73

    string = FD_unite_and_break_string(xrow['nwmt.network_mode_theme'], 
                                        xrow['q.question'], ' / ', 100, 250)

    return string
    
# questions_df['menu_question'] = questions_df.apply(questions_for_menu,
#                                                    axis = 1)

# [print(question_for_menu) \
#  for question_for_menu in list(questions_df['menu_question'])]
    
# questions_df

#%% .-.-.-.-.-.-.-.-.-.-.-.-.-.- desde aquí salió
#%% .-.-.-.-.-.-.-.-.-.-.-.-.-.- desde aquí salió
# def UTBo_Create_mapped_palette(xoriginPalette, xoriginPaletteLength,
#                              xstartColorIndex, xnumberOfIndexes,
#                              xreversed = True):
    
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-UTBo_Create_mapped_palette')
#     # print('>>>>>>>>>>>>>>>>>>> xnumberOfIndexes (UTBo_Create_mapped_palette)')
#     # print(xnumberOfIndexes)
    
#     if xreversed == True:
#         _palette = list(
#             reversed(list(all_palettes[xoriginPalette][xoriginPaletteLength])))
#     else:
#         _palette = list(all_palettes[xoriginPalette][xoriginPaletteLength])

#     _colorsToUse = xoriginPaletteLength - xstartColorIndex
#     # print('>>>>>>>>>>>>>>>>>>> _colorsToUse (UTBo_Create_mapped_palette)')
#     # print(_colorsToUse)
    
#     if xnumberOfIndexes == 1:
#         _palette = [_palette[int(xstartColorIndex+(_colorsToUse/2))]]
#     elif xnumberOfIndexes == 2:
#         _interval = int(_colorsToUse/4)
#         _colorIndexes = [xstartColorIndex+_interval,
#                          xstartColorIndex+(3*_interval)]
#         _palette = [_palette[colorIndex] for colorIndex in _colorIndexes]
#     else:

#         _interval = _colorsToUse // (xnumberOfIndexes - 1)
#         # print('>>>>>>>>>>>>>>>>>>> _interval (UTBo_Create_mapped_palette)')
#         # print(_interval)

#         _colorIndexes = [i*_interval for i in range(0, xnumberOfIndexes-2)]
#         # print('>>>>>>>>>>>>>>>>>>> _colorIndexes (UTBo_Create_mapped_palette)')
#         # print(_colorIndexes)

#         _lastInterval = _colorsToUse-max(_colorIndexes)
#         # print('>>>>>>>>>>>>>>>>>>> _lastInterval (UTBo_Create_mapped_palette)')
#         # print(_lastInterval)
        
#         _colorIndexes1 = \
#             _colorIndexes+[max(_colorIndexes) +
#                            (_lastInterval // 2), _colorsToUse-1]
#         # print('>>>>>>>>>>>>>>>>>>> _colorIndexes1 (UTBo_Create_mapped_palette)')
#         # print(_colorIndexes1)
        
#         _colorIndexes2 = [_colorIndexes1[colorIndex]
#                           for colorIndex in range(0, len(_colorIndexes1))]
#         # print('>>>>>>>>>>>>>>>>>>> _colorIndexes2 (UTBo_Create_mapped_palette)')
#         # print(_colorIndexes2)
        
#         _palette = [_palette[colorIndex] for colorIndex in _colorIndexes2]

#     return _palette

# def UTBo_Create_proportional_palette(xvalues_to_map, 
#                                      xoriginPalette, xoriginPaletteLength,
#                                      xstartColorIndex, xmax_value = None,
#                                      xreversed = True):
    
#     # print('.-.-.-.-.-.-.-.-.-. UTBo_Create_proportional_palette')
#     # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
#     # print(xmax_value)
#     # print('>>>>>>>>>>>>>>>> values_to_map (UTBo_Create_proportional_palette)')
#     # print(xvalues_to_map)
    
#     if xmax_value == None:
#         xmax_value = max(xvalues_to_map) + 1
#     #     print('none mv')
#     # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
#     # print(xmax_value)
    
#     _base_palette = UTBo_Create_mapped_palette(xoriginPalette, 
#                                                xoriginPaletteLength,
#                                                xstartColorIndex, 
#                                                xmax_value,
#                                                xreversed = xreversed)
#     # print('>>>>>>>>>>>>>>>> _base_palette (UTBo_Create_proportional_palette)')
#     # print(_base_palette)
    
#     _palette = [_base_palette[value_to_map] for value_to_map in xvalues_to_map]
    
#     # print('>>>>>>>>>>>>>>>>  _palette (UTBo_Create_proportional_palette)')
#     # print( _palette)
    
#     return _palette

# def string_array(xnrows,xncolumns):
    
    
#     columns = ['']*xncolumns
#     # array = [columns]*xnrows
#     array = [columns.copy() for i in range(xnrows)]
    
#     return array

# sa = string_array(6,4)

# sa[1][1]='b'
# sa[1][2]='c'

# def transpose_string_array(xarray):

#     nrows = len(xarray)
#     ncolumns = len(xarray[0])

#     transposed_array = string_array(ncolumns,nrows)

#     for i in range(nrows):
#         for j in range(ncolumns):
#             transposed_array[j][i] = xarray[i][j]
            
#     return transposed_array
    
# tsa = transpose_string_array(sa)        

# def flatten_string_array(xarray):
    
#     dim1_length = len(xarray)
#     dim2_length = len(xarray[0])
#     flattened_array = \
#         [xarray[i][j] for i in range(dim1_length) for j in range(dim2_length)]
#     return flattened_array


# def UTBo_component_contents(xcell_frequencies, 
#                                xdimension_x_length, xdimension_y_length, 
#                                xcontent_is_str = False,                               
#                                xtotal_cells = False, xstart_x_index = 0, 
#                                xstart_y_index = 0):
    
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_contents')
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_contents')
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_contents')
#     # print('>>>>>>>>> xdimension_x_length (UTBo_component_contents)')
#     # print(xdimension_x_length)
#     # print('>>>>>>>>> xdimension_y_length (UTBo_component_contents)')
#     # print(xdimension_y_length)
    
#     def add_content(xindex_x, xindex_y, xcontent):
#         # if (xindex_y == 4) | (xindex_y == 6) | (xindex_y == 7):
#         index_x = xindex_x - xstart_x_index
#         index_y = xindex_y - xstart_y_index
#         # print('>>>>>>>>> index_x (add_content)')
#         # print(index_x)
#         # print('>>>>>>>>> index_y (add_content)')
#         # print(index_y)
#         # print('>>>>>>>>> xcontent (add_content)')
#         # print(xcontent)
        
#         if xcontent_is_str == False:
#             if xtotal_cells == True:
#                 contents_array[index_y+1, index_x+1] = xcontent
#                 contents_array[0, index_x+1] = \
#                     contents_array[0, index_x+1] + xcontent
#                 contents_array[index_y+1, 0] = \
#                     contents_array[index_y+1, 0] + xcontent
#                 contents_array[0, 0] = \
#                     contents_array[0, 0] + xcontent
#             else:
#                 contents_array[index_y, index_x] = xcontent
#             # print(frequencies_array)
#         else:
#             contents_array[index_y][index_x] = xcontent
            
#         # print('>>>>>>>>> contents_array (add_content)')
#         # print(contents_array)    
        
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-. UTBo_component_contents')
#     # print('>>>>>>>>> xcell_frequencies.columns (UTBo_component_contents)')
#     # print(xcell_frequencies.columns)
#     # print('>>>>>>>>> xcell_frequencies.shape (UTBo_component_contents)')
#     # print(xcell_frequencies.shape)
#     # print('>>>>>>>>> xcell_frequencies (UTBo_component_contents)')
#     # print(xcell_frequencies.to_dict('records'))
    
#     content_tuples = \
#         [tuple(x) for x in xcell_frequencies.to_records(index=False)]
#     # print('>>>>>>>>> frequencies_tuples (UTBo_component_contents)')
#     # print(content_tuples)    
        
#     if xcontent_is_str == False:
#         if xtotal_cells == True:
#             contents_array = np.zeros((xdimension_y_length + 1, 
#                                           xdimension_x_length + 1))
#         else:
#             contents_array = np.zeros((xdimension_y_length, 
#                                        xdimension_x_length))
        
#         [add_content(int(index_x), int(index_y), frec) \
#          for  _, index_x, index_y, frec in content_tuples]
#         contents_array = np.transpose(contents_array)
#         contents_array_flattened = contents_array.flatten()
    
#     else:
#         contents_array = string_array(xdimension_y_length, 
#                                       xdimension_x_length)
#         [add_content(int(index_x), int(index_y), content) \
#          for  _, index_x, index_y, content in content_tuples]
#         contents_array = transpose_string_array(contents_array)
#         contents_array_flattened = flatten_string_array(contents_array)
    
        
#     # print('>>>>>>>>> contents_array (UTBo_component_contents)')
#     # print(contents_array)    
    
#     # print('>>>>>>>>> contents_array_flattened (UTBo_component_contents)')
#     # print(contents_array_flattened)    
        
#     return contents_array_flattened

# # a, b = FD_component_frequencies(academic_model_frequencies_count, 1)

# # a
# # b

# # possible_responses_9_dict,
# #                        possible_responses_10_dict, 
# #                        component_frequencies,
# #                        nodes_dict.get(component_id)

# # def UTBo_Component_hm(xnodes_list, xcomponent_id,
# #                     xcomponent_frequencies):
# def UTBo_Component_hm(xdimension_x_dict, xdimension_y_dict,
#                       xcell_contents, xtitle,
#                       xtotal_cells = False, xtotal_cells_label = '',
#                       xcontent_is_str = False,
#                       xstart_x_index = 0, xstart_y_index = 0,
#                       xlabel_x_axis = '', xlabel_y_axis = '',
#                       xwidth=400, xheight=400,
#                       xreverse_content = False,
#                       xsingle_color = 'lightblue'):
    
#     """
#     Returns a heatmap
    
#     Input:  - xdimension_x_dict: dictionary with x axis coordinates
#             - xdimension_y_dict: dictionary with y axis coordinates
#             - xcell_frequencies: DataFrame with 4 columns:
#                 - col1: irrevelant
#                 - col2: x index
#                 - col3: y index
#                 - col4: content to put in the cell
    
#     """
    
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
#     # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
#     # print('>>>>>>>>>>>>>>>>>> xtitle (UTBo_Component_hm)')
#     # print(xtitle)
#     # print('>>>>>>>>>>>>>>>>>> xdimension_x_dict (UTBo_Component_hm)')
#     # print(xdimension_x_dict)
#     # print('>>>>>>>>>>>>>>>>>> xdimension_y_dict (UTBo_Component_hm)')
#     # print(xdimension_y_dict)
#     # print('>>>>>>>>> xcell_contents (UTBo_Component_hm)')
#     # print(xcell_contents.to_dict('records'))
#     # print('>>>>>>>>> xtotal_cells (UTBo_Component_hm)')
#     # print(xtotal_cells)
#     dimension_x_list = [v for _,v in xdimension_x_dict.items()]
#     # print('>>>>>>>>>>>>>>>>>> dimension_x_list (UTBo_Component_hm)')
#     # print(dimension_x_list)
#     dimension_y_list = [v for _,v in xdimension_y_dict.items()]
#     # print('>>>>>>>>>>>>>>>>>> dimension_y_list (UTBo_Component_hm)')
#     # print(dimension_y_list)
#     dimension_x_length = len(dimension_x_list)
#     dimension_y_length = len(dimension_y_list)
    
#     if xtotal_cells == True:
#         x_lists = [[xtotal_cells_label]*(dimension_y_length + 1)] + \
#             [[dimension_x_list[i]]*(dimension_y_length + 1) \
#              for i in range(0,dimension_y_length)]
#         y_lists = [[xtotal_cells_label]+[dimension_y_list[i] \
#                                         for i in range(0,dimension_x_length)] \
#                for j in range(0,(dimension_x_length + 1))]
#     else:
#         x_lists = [[dimension_x_list[i]] * dimension_y_length \
#              for i in range(0,dimension_x_length)]
#         y_lists = [[dimension_y_list[i] \
#                                         for i in range(0,dimension_y_length)] \
#                for j in range(0,dimension_x_length)]
    
#     # print('>>>>>>>>>>>>>>>>>> x_lists (UTBo_Component_hm)')
#     # print(x_lists)
#     # print('>>>>>>>>>>>>>>>>>> y_lists (UTBo_Component_hm)')
#     # print(y_lists)
    
#     x = reduce(lambda a, b: a + b, x_lists)
#     y = reduce(lambda a, b: a + b, y_lists)
#     # print('>>>>>>>>>>>>>>>>>> x (UTBo_Component_hm)')
#     # print(x)
#     # print(len(x))
#     # print('>>>>>>>>>>>>>>>>>> y (UTBo_Component_hm)')
#     # print(y)
#     # print(len(y))
    
#     factors_x = [dimension_x_list[i] for i in range(0,dimension_x_length)]
#     factors_y = [dimension_y_list[i] for i in range(0,dimension_y_length)]
#     if xtotal_cells == True:
#         factors_x = [xtotal_cells_label] + factors_x
#         factors_y = [xtotal_cells_label] + factors_y
#     # print('>>>>>>>>>>>>>>>>>> factors_x (UTBo_Component_hm)')
#     # print(factors_x)
#     # print('>>>>>>>>>>>>>>>>>> factors_y (UTBo_Component_hm)')
#     # print(factors_y)
        
    
#     if xcontent_is_str == False:
#         contents = \
#             [int(frequency) for frequency in \
#              UTBo_component_contents(xcell_contents, 
#                                     dimension_x_length,
#                                     dimension_y_length,
#                                     xtotal_cells= xtotal_cells,
#                                     xcontent_is_str = xcontent_is_str,
#                                     xstart_x_index = xstart_x_index, 
#                                     xstart_y_index = xstart_y_index)]
#         colors = UTBo_Create_proportional_palette(contents, 'Greens', 256, 0)
#         contents_str = [str(content) if content > 0 else '' \
#                         for content in contents]
#     else:
#         contents = \
#              UTBo_component_contents(xcell_contents, 
#                                         dimension_x_length,
#                                         dimension_y_length,
#                                         xtotal_cells= xtotal_cells,
#                                         xcontent_is_str = xcontent_is_str,
#                                         xstart_x_index = xstart_x_index, 
#                                         xstart_y_index = xstart_y_index)
#         colors = [xsingle_color] * len(x)
#         contents_str = [content for content in contents]
    
#     # _tools=['hover','tap']
#     _tools=['tap']
    
    
#     # print('>>>>>>>>>>>>>>>>>> contents_str (UTBo_Component_hm)')
#     # print(contents_str)
    
#     source_dict = {'x': x,
#                    'y': y,
#                    'fill_colors': colors,
#                    'frequencies': contents_str}
#     # print('>>>>>>>>>>>>>>>>>> source_dict (UTBo_Component_hm)')
#     # print(source_dict)
#     source_df = pd.DataFrame.from_dict(source_dict)
#     # print('>>>>>>>>>>>>>>>>>> source_df (UTBo_Component_hm)')
#     # print(source_df)
    
#     source = ColumnDataSource(source_df)
    
#     hm = figure(title=xtitle, tools=_tools,
#                 toolbar_location=None,
#                 x_range=factors_x, y_range=factors_y, width = xwidth, 
#                 height = xheight,
#                 x_axis_label=xlabel_x_axis, 
#                 y_axis_label=xlabel_y_axis)
    
#     # hm.rect(x, y, color=colors, width=1, height=1)
#     hm.rect(
#         x="x",
#         y="y",
#         width=1,
#         height=1,
#         source=source,
#         fill_color={'field': 'fill_colors'},
#         line_color=None
#     )
    
#     hm.xaxis.major_label_orientation = pi/4
    
#     taptool = hm.select(type=TapTool)
    
    
#     # print('>>>>>>>>>>>>>>>>>> labels_dict (UTBo_Component_hm)')
#     # print(labels_dict)
    
#     # print('>>>>>>>>>>>>>>>>>> labels_df (UTBo_Component_hm)')
#     # print(labels_df)
    
    
    
#     labels = LabelSet(
#         x='x',
#         y='y',
#         text='frequencies',
#         level='glyph',
#         text_align='left',
#         x_offset=-400,
#         y_offset=-25,
#         source=source,
#         text_color = 'black'
#     )
    
# # render_mode='css',
# # y_offset=-7,

#     # labels = LabelSet(x, y, text=frequencies_str, level='glyph',
#     #                   text_align='center',  y_offset=-7, render_mode='canvas')
#     # labels = LabelSet(x=x, y=y, text=frequencies_str)
    
#     hm.add_layout(labels)
    
#     # print('hm.renderers[0].data_source.selected.indices')
#     # print(hm.renderers[0].data_source.selected.indices)
    
    
#     # hm_source = \
#     #     hm.renderers[0].data_source
        
#     # return hm_source, hm
#     return hm
#%%
#%% :_:_:_:_:_:_:_:_:_:_:_:_:_ hasta aquí salió


#.-.-.-.-.-.-. Números
# dimension_x_dict = {'0': 'Nada', '1': 'Muy poco', '2': 'Poco', 
#                     '3': 'Intermedio', '4': 'En buena medida', 
#                     '5': 'Totalmente'}
# dimension_y_dict = {1: 'Ambiente para el aprendizaje', 2: 'Evaluación', 
#                     3: 'Aprendizaje activo', 
#                     4: 'Preparación/selección contenidos', 
#                     5: 'Manejo de grupo', 6: 'Lenguaje apreciativo', 
#                     7: 'Understanding by design', 
#                     8: 'Metodología de proyectos'}

# cell_frequencies_dict = {'uno': [0, 0, 0, 0],
#                          'dos': [1, 2, 3, 4],
#                          'tres': [4, 3, 2, 1],
#                          'cuatro': [10,29,30,40]}

# #Preguntas.-.-.-.-.-.-.-.-.-
# dimension_x_dict = {'0': 'Nada'}
# dimension_y_dict = {1: 'Tema 1', 2: 'Tema 1', 
#                     3: 'Tema 1', 
#                     4: 'Tema 2', 
#                     5: 'Tema 2', 6: 'Tema 3', 
#                     7: 'Tema 4', 
#                     8: 'Tema 4'}
# # cell_frequencies_dict = {'uno': [0, 0, 0, 0],
# #                           'dos': [1, 2, 3, 4],
# #                           'tres': [4, 3, 2, 1],
# #                           'cuatro': ['p1','p2','p3','p4']}
# cell_frequencies_dict = {'uno': [0, 0, 0, 0],
#                           'dos': [0, 0, 0, 0],
#                           'tres': [4, 3, 2, 1],
#                           'cuatro': ['diez','veinte','treinta','cuarenta']}

#.-.-.-..-.-.-.-.-.-.-.-.-
def FD_single_question_hm(xquestion, xselected_question_title,
                          xwidth=900, xheight=140,
                          xx_offset = -400, xy_offset = -25):
    
    print('.-.-.-.-.-.-.-.-.-.-. oihub_IRA_Questions/FD_single_question_hm')
    
    dimension_x_dict = {'0': 'Nada'}

    dimension_y_dict = {'0': 'Nada'}
        
    cell_frequencies_dict = {'uno': [0],
                              'dos': [0],
                              'tres': [0],
                              'cuatro': [xquestion]}

    cell_frequencies = pd.DataFrame.from_dict(cell_frequencies_dict)

    hm2 = UTBoHM_Component_hm(dimension_x_dict, dimension_y_dict,
                           cell_frequencies, xselected_question_title,
                           xcontent_is_str = True,                       
                          xtotal_cells = False, xtotal_cells_label = '',
                          xstart_x_index = 0, xstart_y_index = 0,
                          xlabel_x_axis = '', xlabel_y_axis = '',
                          xwidth = xwidth, xheight = xheight,
                          xsingle_color='lightgreen')
                          # ,
                          # xx_offset = xx_offset, xy_offset = xy_offset)
    
    return hm2

def FD_tap_update(xhm, xhm2, xmenu_questions, xquestions_df):
    
    print ('.-.-.-.-.-.-.-.-.-.-.-.-. tap update')
    selected_indices = xhm.renderers[0].data_source.selected.indices
    print('>>>>>>>>>>>>>>>>> xcomponent_academic_model (FD_tap_update)')
    print(selected_indices)
    print('>>>>>>>>>>>>>>>>> menu_question (FD_tap_update)')
    print(xmenu_questions[selected_indices[0]])
    print('>>>>>>>>>>>>>>>>> question_df (FD_tap_update)')
    print(xquestions_df.iloc[xquestions_df.shape[0]-1-selected_indices[0]])
    
    
    _hm2 = FD_single_question_hm(xmenu_questions[selected_indices[0]])
    
    # xhm2_source = xhm2.renderers[0].data_source
    # print('>>>>>>>>>>dict(xhm_source.data)')
    # print(dict(xhm_source.data))
              
    _hm2_source = _hm2.renderers[0].data_source
    
       
    xhm2.renderers[0].data_source.data = dict(_hm2_source.data)
    

def FD_questions_main(xnetwork_parameters_dict,
                      xquestions_df, xquestions_title, 
                      xselected_question_title, xaa_questions = True,
                      xwidth = 900, xheight = 1000,
                      xx_offset = -400, xy_offset = -25,
                      xheight_single_question = 140):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.- oihub_IRA_Questions/FD_questions_menu')
    id_question = xnetwork_parameters_dict['id_question']
    # print('>>>>>>>>>>>>>>>>>>>>>>>> id_question (FD_questions_menu)')
    # print(id_question)
    
    if xaa_questions == True:
        xquestions_df['menu_question'] = \
            xquestions_df.apply(questions_for_menu, axis = 1)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> xquestions_df (FD_questions_menu)')
    # print(xquestions_df.to_dict('records'))
    menu_questions_list = list(xquestions_df['menu_question'])
    # print('menu_questions')
    # print(menu_questions)
    
    #
    #se reversa el orden de las preguntas porque hay que mandarlas al revés
    #al heatmap
    menu_questions_list.reverse()
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> menu_questions_list (FD_questions_menu)')
    # print(menu_questions_list)
    
    #
    #el question_index se usa para saber que pregunta desplegar como seleccionada
    question_index = list(xquestions_df['q.id_question']).index(id_question)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> question_index (FD_questions_menu)')
    # print(question_index)
    
    dimension_x_dict = {'0': 'Nada'}
    
    dimension_y_dict = {i:'p'+str(i) for i in range(xquestions_df.shape[0])}
        
    cell_frequencies_dict = {'uno': [0]*xquestions_df.shape[0],
                              'dos': [0]*xquestions_df.shape[0],
                              'tres': [i for i in range(xquestions_df.shape[0])],
                              'cuatro': menu_questions_list}   
    
    cell_frequencies = pd.DataFrame.from_dict(cell_frequencies_dict)
    
    hm = UTBoHM_Component_hm(dimension_x_dict, dimension_y_dict,
                           cell_frequencies, xquestions_title,
                           xcontent_is_str = True,                       
                          xtotal_cells = False, xtotal_cells_label = '',
                          xstart_x_index = 0, xstart_y_index = 0,
                          xlabel_x_axis = '', xlabel_y_axis = '',
                          xwidth = xwidth, xheight = xheight)
    
                          # ,
                          # xx_offset = xx_offset, xy_offset = xy_offset)
    
    hm.axis.visible = False
    
    
    #
    #la pregunta seleccionada se busca en menu_questions_list de atrás a
    #adelante porque a menu_questions_list se le aplicó reverse arriba
    hm2 = FD_single_question_hm\
        (menu_questions_list[len(menu_questions_list)-(question_index+1)],
         xselected_question_title, xwidth = xwidth, 
         xheight = xheight_single_question)
    
    hm2.axis.visible = False
    
    return hm, hm2, menu_questions_list, xquestions_df


def FD_questions_AA_main(xconn, xnetwork_parameters_dict, xquestions_title, 
                         xselected_question_title):
    
    questions_df = FD_fetch_AA_questions(xconn)
    
    questions_menu, selected_question, menu_questions_list, questions_df = \
        FD_questions_main(xnetwork_parameters_dict, 
                          questions_df, xquestions_title, 
                          xselected_question_title, 
                          xwidth = 900, xheight = 1000,
                          xx_offset = -400, xy_offset = -25,
                          xheight_single_question = 140)
        
    help_tabs_global, help_texts_tuple = \
        FD_build_question_help(xnetwork_parameters_dict)
        
    return questions_menu, selected_question, menu_questions_list, \
        questions_df, help_tabs_global, help_texts_tuple


def FD_questions_BM_main(xnetwork_parameters_dict,
                      xquestions_df, xquestions_title, 
                      xselected_question_title, xaa_questions = True,
                      xwidth = 900, xheight = 1000,
                      xx_offset = -400, xy_offset = -25,
                      xheight_single_question = 140):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.- oihub_IRA_Questions/FD_questions_menu')
    # id_question = xnetwork_parameters_dict['id_question']
    # print('>>>>>>>>>>>>>>>>>>>>>>>> id_question (FD_questions_menu)')
    # print(id_question)
    
    if xaa_questions == True:
        xquestions_df['menu_question'] = \
            xquestions_df.apply(questions_for_menu, axis = 1)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> xquestions_df (FD_questions_menu)')
    # print(xquestions_df.to_dict('records'))
    menu_questions_list = list(xquestions_df['menu_question'])
    # print('menu_questions')
    # print(menu_questions)
    
    #
    #se reversa el orden de las preguntas porque hay que mandarlas al revés
    #al heatmap
    menu_questions_list.reverse()
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> menu_questions_list (FD_questions_menu)')
    # print(menu_questions_list)
    
    #
    #el question_index se usa para saber que pregunta desplegar como seleccionada
    question_index = 0
    # = list(xquestions_df['q.id_question']).index(id_question)
    # print('>>>>>>>>>>>>>>>>>>>>>>>>>> question_index (FD_questions_menu)')
    # print(question_index)
    
    dimension_x_dict = {'0': 'Nada'}
    
    dimension_y_dict = {i:'p'+str(i) for i in range(xquestions_df.shape[0])}
        
    cell_frequencies_dict = {'uno': [0]*xquestions_df.shape[0],
                              'dos': [0]*xquestions_df.shape[0],
                              'tres': [i for i in range(xquestions_df.shape[0])],
                              'cuatro': menu_questions_list}   
    
    cell_frequencies = pd.DataFrame.from_dict(cell_frequencies_dict)
    
    hm = UTBoHM_Component_hm(dimension_x_dict, dimension_y_dict,
                           cell_frequencies, xquestions_title,
                           xcontent_is_str = True,                       
                          xtotal_cells = False, xtotal_cells_label = '',
                          xstart_x_index = 0, xstart_y_index = 0,
                          xlabel_x_axis = '', xlabel_y_axis = '',
                          xwidth = xwidth, xheight = xheight)
    
                          # ,
                          # xx_offset = xx_offset, xy_offset = xy_offset)
    
    hm.axis.visible = False
    
    
    #
    #la pregunta seleccionada se busca en menu_questions_list de atrás a
    #adelante porque a menu_questions_list se le aplicó reverse arriba
    hm2 = FD_single_question_hm\
        (menu_questions_list[len(menu_questions_list)-(question_index+1)],
         xselected_question_title, xwidth = xwidth, 
         xheight = xheight_single_question)
    
    hm2.axis.visible = False
    
    return hm, hm2, menu_questions_list, xquestions_df

def FD_questions_AK_main(xconn, xnetwork_parameters_dict,
                         xnetwork_modes_list,
                         xquestions_title, 
                         xselected_question_title):
    
    print('.-.-.-.-.-.-.-.-.-.-.- FD_K_questions_main')
    
    topics_menu_width = xnetwork_parameters_dict['topics_menu_width']
    topics_menu_height = xnetwork_parameters_dict['topics_menu_height'] 
    topics_menu_x_offset = xnetwork_parameters_dict['topics_menu_x_offset'] 
    topics_menu_y_offset = xnetwork_parameters_dict['topics_menu_y_offset'] 
    topics_single_topic_height = \
        xnetwork_parameters_dict['topics_single_topic_height'] 
        
    
    nwmq_df = FD_fetch_AK_network_modes(xconn, xnetwork_modes_list)
    
    questions_df = \
        UT_CountOcurrences(nwmq_df, 
                           ['nwm.id_network_mode','nwm.network_mode']) 
        
    questions_df.rename(columns={'nwm.network_mode':'menu_question'},
                        inplace = True)
    
    questions_menu, selected_question, menu_questions_list, questions_df = \
        FD_questions_BM_main(xnetwork_parameters_dict, 
                          questions_df, xquestions_title,
                          xselected_question_title, 
                          xaa_questions = False,
                          xwidth = topics_menu_width, 
                          xheight = topics_menu_height,
                          xx_offset = topics_menu_x_offset, 
                          xy_offset = topics_menu_y_offset,
                          xheight_single_question = topics_single_topic_height)
        
    
        
    return questions_menu, selected_question, menu_questions_list, questions_df
    



# def FD_questions_main(xconn):
#     questions_df = FD_fetch_AA_questions(xconn)
#     questions_df.columns
    
#     questions_df['menu_question'] = questions_df.apply(questions_for_menu,
#                                                        axis = 1)
#     # print('questions_df')
#     # print(questions_df[['nwmt.id_network_mode_theme','q.id_question']])
#     # print(questions_df)
#     menu_questions = list(questions_df['menu_question'])
#     # print('menu_questions')
#     # print(menu_questions)
#     menu_questions.reverse()
#     # print('menu_questions rev')
#     # print(menu_questions)
    
#     dimension_x_dict = {'0': 'Nada'}
    
#     dimension_y_dict = {i:'p'+str(i) for i in range(questions_df.shape[0])}
        
#     cell_frequencies_dict = {'uno': [0]*questions_df.shape[0],
#                               'dos': [0]*questions_df.shape[0],
#                               'tres': [i for i in range(questions_df.shape[0])],
#                               'cuatro': menu_questions}
    
    
    
#     cell_frequencies = pd.DataFrame.from_dict(cell_frequencies_dict)
    
#     hm = UTBo_Component_hm(dimension_x_dict, dimension_y_dict,
#                            cell_frequencies, 'Seleccione una pregunta:',
#                            xcontent_is_str = True,                       
#                           xtotal_cells = False, xtotal_cells_label = '',
#                           xstart_x_index = 0, xstart_y_index = 0,
#                           xlabel_x_axis = '', xlabel_y_axis = '',
#                           xwidth=900, xheight=1000)
    
#     hm.axis.visible = False
    
#     # hm_source = hm.renderers[0].data_source
    
        
#     # hm_source.selected.on_change('indices', lambda attr, old, new: \
#     #                         FD_tap_update(hm, hm2, menu_questions,
#     #                                       questions_df))
    
#     hm2 = FD_single_question_hm(menu_questions[len(menu_questions)-1])
#     hm2.axis.visible = False
    
#     return hm, hm2, menu_questions, questions_df
    
# hm, hm2, _ = FD_questions_main()
# # # # show(hm)
# curdoc().add_root(row(hm,hm2))


#%%
#.-.-.-.-.-.-.-.-.-
# def string_array(xnrows,xncolumns):
    
    
#     columns = ['']*xncolumns
#     # array = [columns]*xnrows
#     array = [columns.copy() for i in range(xnrows)]
    
#     return array

# sa = string_array(6,4)
# sa
# sa[1][1]='b'
# sa[1][2]='c'

# [sa[i][j] for i in range(6) for j in range(4)]

# def transpose_string_array(xarray):

#     nrows = len(xarray)
#     ncolumns = len(xarray[0])

#     transposed_array = string_array(ncolumns,nrows)

#     for i in range(nrows):
#         for j in range(ncolumns):
#             transposed_array[j][i] = xarray[i][j]
            
#     return transposed_array
    
# tsa = transpose_string_array(sa)        
    
# tsa    
# sa

# def flatten_string_array(xarray):
    
#     dim1_length = len(xarray)
#     dim2_length = len(xarray[0])
#     flattened_array = \
#         [xarray[i][j] for i in range(dim1_length) for j in range(dim2_length)]
#     return flattened_array
    
# flatten_string_array(tsa)


# OPTIONS = [("1", "foo \nfa"), ("2", "bar"), ("3", "baz"), ("4", "quux")]

# multi_select = MultiSelect(value=["1", "2"], options=OPTIONS)


# show(multi_select)


# from bokeh.models import CustomJS, RadioGroup

# LABELS = ["Option 1 \n ooooo", "Option 2", "Option 3"]

# radio_group = RadioGroup(labels=LABELS, active=0)
# radio_group.js_on_event('button_click', CustomJS(code="""
#     console.log('radio_group: active=' + this.origin.active, this.toString())
# """))

# show(radio_group)


# from bokeh.io import show
# from bokeh.models import (ColumnDataSource, DataCube, GroupingInfo,
#                           StringFormatter, SumAggregator, TableColumn)

# source = ColumnDataSource(data=dict(
#     d0=['AAAA\naaaajkjkjljllklklkñkljljlkhjhhghhffgfgfmmmmmmmmmmmmmmmmm\\nmmmmmmmmm', 
#         'E', 'E', 'E', 'J', 'L', 'M'],
#     d1=['B', 'D', 'D', 'H', 'K', 'L', 'N'],
#     d2=['C', 'F', 'G', 'H', 'K', 'L', 'O'],
#     px=[10, 20, 30, 40, 50, 60, 70],
# ))

# target = ColumnDataSource(data=dict(row_indices=[], labels=[]))

# formatter = StringFormatter(font_style='bold')

# columns = [
#     TableColumn(field='d2', title='Name', width=80, sortable=False, formatter=formatter),
#     TableColumn(field='px', title='Price', width=40, sortable=False),
# ]

# grouping = [
#     GroupingInfo(getter='d0', aggregators=[SumAggregator(field_='px')]),
#     GroupingInfo(getter='d1', aggregators=[SumAggregator(field_='px')]),
# ]

# cube = DataCube(source=source, columns=columns, grouping=grouping, target=target)

# show(cube)
