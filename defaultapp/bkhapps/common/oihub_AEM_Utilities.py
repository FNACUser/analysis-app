# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 21:13:00 2023

@author: luis.caro
"""

import pandas as pd
import numpy as np
from math import pi

from functools import reduce


from bokeh.palettes import all_palettes
from bokeh.plotting import figure
from bokeh.models import TapTool, LabelSet, ColumnDataSource


# from UtilitiesNeo4j import driver
# from neo4j_connection_sandbox import conn, insert_data
from defaultapp.bkhapps.common.neo4j_learn_ONA import conn, insert_data




#%%

def FD_Fetch_nodes(xnode_segment):
    
    query0='''MATCH (n:Node)-[ES_DE_SEGMENTO]->(ns:Node_segment{segment:"'''
    
    query1='''"}) RETURN n.id_node, n.node'''
    
    params = {}
    
    query = query0 + xnode_segment + query1
    
    # results = driver.session().run(query, parameters=params)
    results = conn.query(query)
    
    nodes_df = pd.DataFrame([dict(_) for _ in results])
    nodes_df.rename(columns={'n.id_node':'id_node',
                             'n.node':'node'}, inplace=True)
    
    nodes_df.sort_values(['id_node'], ascending=[True], inplace=True)
    
    return nodes_df

def FD_teachers_schools():
    
    query='''MATCH (oa:Organization_area) WHERE oa.id_organization_area IN 
        [1,2,3,4,6,8] RETURN oa.id_organization_area, oa.organization_area'''
     
    params = {}
    
    # results = driver.session().run(query, parameters=params)
    results = conn.query(query)
    
    
    nodes_df = pd.DataFrame([dict(_) for _ in results])
    nodes_df.rename(columns={'oa.id_organization_area':'id_organization_area',
                             'oa.organization_area':'organization_area'}, 
                    inplace=True)
    
    todos = pd.DataFrame({'id_organization_area': 0, 
                          'organization_area': '-todos'}, index=[0])
    # nodes_df = nodes_df.append(todos, ignore_index = True)
    nodes_df = pd.concat([nodes_df, todos], ignore_index=True)
    
    nodes_df.sort_values(['id_organization_area'], ascending=[True], 
                          inplace=True)
    
    return nodes_df

# FD_teachers_schools()


def UTBo_Create_mapped_palette(xoriginPalette, xoriginPaletteLength,
                             xstartColorIndex, xnumberOfIndexes,
                             xreversed = True):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-UTBo_Create_mapped_palette')
    # print('>>>>>>>>>>>>>>>>>>> xnumberOfIndexes (UTBo_Create_mapped_palette)')
    # print(xnumberOfIndexes)
    
    if xreversed == True:
        _palette = list(
            reversed(list(all_palettes[xoriginPalette][xoriginPaletteLength])))
    else:
        _palette = list(all_palettes[xoriginPalette][xoriginPaletteLength])

    _colorsToUse = xoriginPaletteLength - xstartColorIndex
    # print('>>>>>>>>>>>>>>>>>>> _colorsToUse (UTBo_Create_mapped_palette)')
    # print(_colorsToUse)
    
    if xnumberOfIndexes == 1:
        _palette = [_palette[int(xstartColorIndex+(_colorsToUse/2))]]
    elif xnumberOfIndexes == 2:
        _interval = int(_colorsToUse/4)
        _colorIndexes = [xstartColorIndex+_interval,
                         xstartColorIndex+(3*_interval)]
        _palette = [_palette[colorIndex] for colorIndex in _colorIndexes]
    else:

        _interval = _colorsToUse // (xnumberOfIndexes - 1)
        # print('>>>>>>>>>>>>>>>>>>> _interval (UTBo_Create_mapped_palette)')
        # print(_interval)

        _colorIndexes = [i*_interval for i in range(0, xnumberOfIndexes-2)]
        # print('>>>>>>>>>>>>>>>>>>> _colorIndexes (UTBo_Create_mapped_palette)')
        # print(_colorIndexes)

        _lastInterval = _colorsToUse-max(_colorIndexes)
        # print('>>>>>>>>>>>>>>>>>>> _lastInterval (UTBo_Create_mapped_palette)')
        # print(_lastInterval)
        
        _colorIndexes1 = \
            _colorIndexes+[max(_colorIndexes) +
                           (_lastInterval // 2), _colorsToUse-1]
        # print('>>>>>>>>>>>>>>>>>>> _colorIndexes1 (UTBo_Create_mapped_palette)')
        # print(_colorIndexes1)
        
        _colorIndexes2 = [_colorIndexes1[colorIndex]
                          for colorIndex in range(0, len(_colorIndexes1))]
        # print('>>>>>>>>>>>>>>>>>>> _colorIndexes2 (UTBo_Create_mapped_palette)')
        # print(_colorIndexes2)
        
        _palette = [_palette[colorIndex] for colorIndex in _colorIndexes2]

    return _palette

def UTBo_Create_proportional_palette(xvalues_to_map, 
                                     xoriginPalette, xoriginPaletteLength,
                                     xstartColorIndex, xmax_value = None,
                                     xreversed = True):
    
    # print('.-.-.-.-.-.-.-.-.-. UTBo_Create_proportional_palette')
    # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
    # print(xmax_value)
    # print('>>>>>>>>>>>>>>>> values_to_map (UTBo_Create_proportional_palette)')
    # print(xvalues_to_map)
    
    if xmax_value == None:
        xmax_value = max(xvalues_to_map) + 1
    #     print('none mv')
    # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
    # print(xmax_value)
    
    _base_palette = UTBo_Create_mapped_palette(xoriginPalette, 
                                               xoriginPaletteLength,
                                               xstartColorIndex, 
                                               xmax_value,
                                               xreversed = xreversed)
    # print('>>>>>>>>>>>>>>>> _base_palette (UTBo_Create_proportional_palette)')
    # print(_base_palette)
    
    _palette = [_base_palette[value_to_map] for value_to_map in xvalues_to_map]
    
    # print('>>>>>>>>>>>>>>>>  _palette (UTBo_Create_proportional_palette)')
    # print( _palette)
    
    return _palette

# UTBo_Create_proportional_palette([0,1,2,4,8,16,32,64,128], 
#                                  'Greys', 256, 0, 256, xreversed = False)
    

#%%


def FD_Fetch_possible_responses(xquestion):
    
    query0="""MATCH (pr:Possible_response)-[pro:POSSIBLE_RESPONSE_OF]->
                (q:Question{id_question:"""

    query1="""}) RETURN pr.value, pr.meaning"""
    
    query_parameters = {'question': xquestion}
    
    query="""WITH $question AS question
                MATCH (q:Question)-[HAS_PATTERN]->(rp:Response_pattern)<-
                [RESPONSE_ITEM_OF]-(rpi:Response_pattern_item)
                WHERE q.id_question = question
                RETURN rpi.item_value, rpi.item_meaning"""
    
    results = conn.query(query, query_parameters)
    
    
    possible_responses_df = pd.DataFrame([dict(_) for _ in results])
    possible_responses_df.rename(columns={'rpi.item_value':'value',
                                          'rpi.item_meaning':'meaning'}, 
                                 inplace=True)
    
    possible_responses_df['meaning'] = \
        possible_responses_df['meaning'].str.strip()
    
    possible_responses_df.sort_values(['value'], ascending=[True], 
                                      inplace=True)
    
    
    possible_responses_dict = dict(zip(possible_responses_df.value, 
                                       possible_responses_df.meaning))
    
    return possible_responses_dict

# a=FD_Fetch_possible_responses(10)
# a
# len(a)
# [(k,v) for k,v in a.items()]


def FD_Fetch_nodes(xnode_segment):
    
    query0='''MATCH (n:Node)-[ES_DE_SEGMENTO]->(ns:Node_segment{segment:"'''
    
    query1='''"}) RETURN n.id_node, n.node'''
    
    params = {}
    
    query = query0 + xnode_segment + query1
    
    # results = driver.session().run(query, parameters=params)
    results = conn.query(query)
    
    nodes_df = pd.DataFrame([dict(_) for _ in results])
    nodes_df.rename(columns={'n.id_node':'id_node',
                             'n.node':'node'}, inplace=True)
    
    nodes_df.sort_values(['id_node'], ascending=[True], inplace=True)
    
    return nodes_df

def FD_academic_model_responses_grouped(xquestion_responses_df, xlabel_valor, 
                                        xlabel_significado):
    
    question_responses_grouped = \
        xquestion_responses_df.groupby([xlabel_valor,'Componente']).count()
    question_responses_grouped.reset_index(level=[0,1], inplace=True)
    question_responses = question_responses_grouped[[xlabel_valor,
                                                           'Componente',
                                                           'conocimiento']]
    question_responses.rename(columns={'conocimiento': xlabel_significado},
                              inplace=True)
    return question_responses



def FD_fetch_academic_model_responses(xquestion, xlabel_valor, 
                                      xlabel_significado):
    
    # ('.-.-.-.-.-.-oihub_AEM_Utlities/FD_fetch_academic_model_responses')

    # query0="""MATCH (pr:Possible_response)-[pro:POSSIBLE_RESPONSE_OF]->
    #             (q:Question{id_question:"""

    # query1="""})<-[FOR_QUESTION]-(r:Response)<-
    #             [hr:HAS_RESPONSE]-(e:Employee)-[FUNCIONARIO_DE]->
    #             (oa:Organization_area)
    #         MATCH (n:Node)<-[a:ABOUT]-(r)-[of:OF_FORM]->(aif:Adjacency_input_form)
    #         WHERE pr.meaning = a.value 
    #         AND oa.id_organization_area IN [1,2,3,4,6,8]
    #         RETURN e.employee,pr.value,a.value,n.id_node,
    #             oa.organization_area, oa.id_organization_area"""
            
    # query = query0 + str(xquestion) + query1
    
    query_parameters = {'cycle': 1,
                        'question': xquestion,
                        'id_network_mode':1}
        
    query="""WITH $cycle AS cycle,
                $question AS question,
                $id_network_mode AS id_network_mode
                MATCH (cy:Cycle)<-[OF_CYCLE]-(aif:Adjacency_input_form)-
                [OF_NETWORK_MODE]->(nwm:Network_mode)
                WHERE cy.id_cycle = cycle AND
                nwm.id_network_mode = id_network_mode
                MATCH (oa:Organization_area)<-[FUNCIONARIO_DE]-(e:Employee)<-
                  [OF_EMPLOYEE]-(aif)
                MATCH (q:Question)<-[FOR_QUESTION]-(res:Response)-[OF_FORM]->
                (aif)
                WHERE q.id_question = question
                MATCH (rpi:Response_pattern_item)<-[IS_ITEM]-(res)-
                [a:ABOUT]->(n:Node)-[ES_DE_SEGMENTO]->(ns:Node_segment)-
                [ES_DE_CATEGORIA]->(nsc:Node_segment_category)
                RETURN e.employee,rpi.item_value,rpi.item_meaning,n.id_node,
                oa.organization_area, oa.id_organization_area"""
                
    results = conn.query(query, parameters=query_parameters)
    
    funcionario_vs_componente_df = pd.DataFrame([dict(_) for _ in results])
    funcionario_vs_componente_df.rename(columns={'e.employee':'funcionario',
                                                 'rpi.item_value':xlabel_valor,
                                                 'rpi.item_meaning':
                                                     xlabel_significado,
                                                 'n.id_node':'id_componente',
                                                 'oa.id_organization_area':
                                                     'id_organization_area',
                                                 'oa.organization_area':
                                                     'organization_area'}, 
                                        inplace=True)
        
    # print('>>> funcionario_vs_componente_df (FD_fetch_academic_model_responses)')
    # print(funcionario_vs_componente_df)
    
    return funcionario_vs_componente_df

# question_9_responses_df = FD_fetch_academic_model_responses(9, 
#                                                           'valor_conocimiento',
#                                                           'conocimiento')
# question_9_responses_df.loc[(question_9_responses_df.valor_conocimiento \
#                              == '3')\
#                             & (question_9_responses_df.id_componente \
#                                                           == 1)]

def FD_component_frequencies(xacademic_model_frequencies_count,
                             xid_component):
    
    def add_frequency(xv_con, xv_exp, xfrec):
        frequencies_array[xv_con+1, xv_exp+1] = xfrec
        frequencies_array[0, xv_exp+1] = frequencies_array[0, xv_exp+1] + xfrec
        frequencies_array[xv_con+1, 0] = frequencies_array[xv_con+1, 0] + xfrec
        
    component_frequencies = \
        xacademic_model_frequencies_count.\
            loc[xacademic_model_frequencies_count.id_componente == \
                xid_component]
                
    frequencies_tuples = \
        [tuple(x) for x in component_frequencies.to_records(index=False)]
        
    frequencies_array = np.zeros((7,7))
    
    [add_frequency(int(v_con), int(v_exp), frec) \
     for v_con, _, v_exp, frec in frequencies_tuples]
        
    return frequencies_array.flatten()

def UTBo_component_frequencies(xcell_frequencies, 
                               dimension_x_length, dimension_y_length, 
                               xtotal_cells = False, xstart_x_index = 0, 
                               xstart_y_index = 0):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_frequencies')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_frequencies')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_frequencies')
    
    def add_frequency(xindex_x, xindex_y, xfrec):
        # if (xindex_y == 4) | (xindex_y == 6) | (xindex_y == 7):
        xindex_x = xindex_x - xstart_x_index
        xindex_y = xindex_y - xstart_y_index
        # print('>>>>>>>>> xindex_x (UTBo_component_frequencies)')
        # print(xindex_x)
        # print('>>>>>>>>> xindex_y (UTBo_component_frequencies)')
        # print(xindex_y)
        # print('>>>>>>>>> xfrec (UTBo_component_frequencies)')
        # print(xfrec)
        
        
        if xtotal_cells == True:
            frequencies_array[xindex_y+1, xindex_x+1] = xfrec
            frequencies_array[0, xindex_x+1] = \
                frequencies_array[0, xindex_x+1] + xfrec
            frequencies_array[xindex_y+1, 0] = \
                frequencies_array[xindex_y+1, 0] + xfrec
            frequencies_array[0, 0] = \
                frequencies_array[0, 0] + xfrec
        else:
            frequencies_array[xindex_y, xindex_x] = xfrec
        # print(frequencies_array)
            
        
    # print('>>>>>>>>> xcell_frequencies.columns (UTBo_component_frequencies)')
    # print(xcell_frequencies.columns)
    # print('>>>>>>>>> xcell_frequencies.shape (UTBo_component_frequencies)')
    # print(xcell_frequencies.shape)
    # print('>>>>>>>>> xcell_frequencies (UTBo_component_frequencies)')
    # print(xcell_frequencies.to_dict('records'))
    
    frequencies_tuples = \
        [tuple(x) for x in xcell_frequencies.to_records(index=False)]
    # print('>>>>>>>>> frequencies_tuples (UTBo_component_frequencies)')
    # print(frequencies_tuples)    
        
    if xtotal_cells == True:
        frequencies_array = np.zeros((dimension_y_length + 1, 
                                      dimension_x_length + 1))
    else:
        frequencies_array = np.zeros((dimension_y_length, dimension_x_length))
    
    [add_frequency(int(index_x), int(index_y), frec) \
     for  _, index_x, index_y, frec in frequencies_tuples]
        
    frequencies_array = np.transpose(frequencies_array)
        
    # print('>>>>>>>>> frequencies_array (UTBo_component_frequencies)')
    # print(frequencies_array)    
    # print(frequencies_array.flatten())    
        
    return frequencies_array.flatten()

# a, b = FD_component_frequencies(academic_model_frequencies_count, 1)

# a
# b

# possible_responses_9_dict,
#                        possible_responses_10_dict, 
#                        component_frequencies,
#                        nodes_dict.get(component_id)

# def UTBo_Component_hm(xnodes_list, xcomponent_id,
#                     xcomponent_frequencies):
def UTBo_Component_hm(xdimension_x_dict, xdimension_y_dict,
                      xcell_frequencies, xtitle,
                      xtotal_cells = False, xtotal_cells_label = '',
                      xstart_x_index = 0, xstart_y_index = 0,
                      xlabel_x_axis = '', xlabel_y_axis = '',
                      xwidth=400, xheight=400):
    
    """
    Returns a heatmap
    
    Input:  - xdimension_x_dict: dictionary with x axis coordinates
            - xdimension_y_dict: dictionary with y axis coordinates
            - xcell_frequencies
    
    """
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    # print('>>>>>>>>>>>>>>>>>> xtitle (UTBo_Component_hm)')
    # print(xtitle)
    # print('>>>>>>>>>>>>>>>>>> xdimension_x_dict (UTBo_Component_hm)')
    # print(xdimension_x_dict)
    # print('>>>>>>>>>>>>>>>>>> xdimension_y_dict (UTBo_Component_hm)')
    # print(xdimension_y_dict)
    # print('>>>>>>>>> xcell_frequencies (UTBo_Component_hm)')
    # print(xcell_frequencies.to_dict('records'))
    # print('>>>>>>>>> xtotal_cells (UTBo_Component_hm)')
    # print(xtotal_cells)
    dimension_x_list = [v for _,v in xdimension_x_dict.items()]
    # print('>>>>>>>>>>>>>>>>>> dimension_x_list (UTBo_Component_hm)')
    # print(dimension_x_list)
    dimension_y_list = [v for _,v in xdimension_y_dict.items()]
    # print('>>>>>>>>>>>>>>>>>> dimension_y_list (UTBo_Component_hm)')
    # print(dimension_y_list)
    dimension_x_length = len(dimension_x_list)
    dimension_y_length = len(dimension_y_list)
    
    if xtotal_cells == True:
        x_lists = [[xtotal_cells_label]*(dimension_y_length + 1)] + \
            [[dimension_x_list[i]]*(dimension_y_length + 1) \
             for i in range(0,dimension_y_length)]
        y_lists = [[xtotal_cells_label]+[dimension_y_list[i] \
                                        for i in range(0,dimension_x_length)] \
               for j in range(0,(dimension_x_length + 1))]
    else:
        x_lists = [[dimension_x_list[i]] * dimension_y_length \
             for i in range(0,dimension_x_length)]
        y_lists = [[dimension_y_list[i] \
                                        for i in range(0,dimension_y_length)] \
               for j in range(0,dimension_x_length)]
    
    # print('>>>>>>>>>>>>>>>>>> x_lists (UTBo_Component_hm)')
    # print(x_lists)
    # print('>>>>>>>>>>>>>>>>>> y_lists (UTBo_Component_hm)')
    # print(y_lists)
    
    x = reduce(lambda a, b: a + b, x_lists)
    y = reduce(lambda a, b: a + b, y_lists)
    # print('>>>>>>>>>>>>>>>>>> x (UTBo_Component_hm)')
    # print(x)
    # print(len(x))
    # print('>>>>>>>>>>>>>>>>>> y (UTBo_Component_hm)')
    # print(y)
    # print(len(y))
    
    factors_x = [dimension_x_list[i] for i in range(0,dimension_x_length)]
    factors_y = [dimension_y_list[i] for i in range(0,dimension_y_length)]
    if xtotal_cells == True:
        factors_x = [xtotal_cells_label] + factors_x
        factors_y = [xtotal_cells_label] + factors_y
    # print('>>>>>>>>>>>>>>>>>> factors_x (UTBo_Component_hm)')
    # print(factors_x)
    # print('>>>>>>>>>>>>>>>>>> factors_y (UTBo_Component_hm)')
    # print(factors_y)
        
    
    frequencies = \
        [int(frequency) for frequency in \
         UTBo_component_frequencies(xcell_frequencies, 
                                    dimension_x_length,
                                    dimension_y_length,
                                    xtotal_cells= xtotal_cells,
                                    xstart_x_index = xstart_x_index, 
                                    xstart_y_index = xstart_y_index)]
    # print('>>>>>>>>>>>>>>>>>> frequencies (UTBo_Component_hm)')
    # print(frequencies)
        
    colors = UTBo_Create_proportional_palette(frequencies, 
                                     'Greens', 256, 0)
    
    _tools=['hover','tap']
    
    frequencies_str = [str(frequency) if frequency > 0 else '' \
                        for frequency in frequencies]
    # frequencies_str = ['aa\nbb'
    #                    for frequency in frequencies]
    # print('>>>>>>>>>>>>>>>>>> frequencies_str (UTBo_Component_hm)')
    # print(frequencies_str)
    
    source_dict = {'x': x,
                   'y': y,
                   'fill_colors': colors,
                   'frequencies': frequencies_str}
    source_df = pd.DataFrame.from_dict(source_dict)
    source = ColumnDataSource(source_df)
    
    hm = figure(title=xtitle, tools=_tools,
                toolbar_location=None,
                x_range=factors_x, y_range=factors_y, width = xwidth, 
                height = xheight,
                x_axis_label=xlabel_x_axis, 
                y_axis_label=xlabel_y_axis)
    
    # hm.rect(x, y, color=colors, width=1, height=1)
    hm.rect(
        x="x",
        y="y",
        width=1,
        height=1,
        source=source,
        fill_color={'field': 'fill_colors'},
        line_color=None
    )
    
    hm.xaxis.major_label_orientation = pi/4
    
    taptool = hm.select(type=TapTool)
    
    
    # print('>>>>>>>>>>>>>>>>>> labels_dict (UTBo_Component_hm)')
    # print(labels_dict)
    
    # print('>>>>>>>>>>>>>>>>>> labels_df (UTBo_Component_hm)')
    # print(labels_df)
    
    
    
    labels = LabelSet(
        x='x',
        y='y',
        text='frequencies',
        level='glyph',
        text_align='center',
        y_offset=-7,
        source=source,
        text_color = 'black'
    )
    
    # render_mode='css',
    
    
    # labels = LabelSet(x, y, text=frequencies_str, level='glyph',
    #                   text_align='center',  y_offset=-7, render_mode='canvas')
    # labels = LabelSet(x=x, y=y, text=frequencies_str)
    
    hm.add_layout(labels)
    
    # print('hm.renderers[0].data_source.selected.indices')
    # print(hm.renderers[0].data_source.selected.indices)
    
    
    # hm_source = \
    #     hm.renderers[0].data_source
        
    # return hm_source, hm
    return hm


def FD_questions_responses_frequencies(xquestion_index, xvalue_field,
                                       xvalue_label, xteachers_school_id):
    
    # print('.-.-.-.-.-.-.-.-.- FD_questions_responses_frequencies')
    # print('>>>>>> xteachers_school_id (FD_questions_responses_frequencies)')
    # print(xteachers_school_id)
    
    question_responses_df = FD_fetch_academic_model_responses(xquestion_index, 
                                                              xvalue_field,
                                                              xvalue_label)
    question_responses_df.fillna(0, inplace=True)
    # print('>>>>>> question_responses_df (FD_questions_responses_frequencies)')
    # print(question_responses_df.to_dict('records'))
    
    if xteachers_school_id != 0:
        question_responses_df = \
            question_responses_df.loc\
                [question_responses_df.id_organization_area == \
                 xteachers_school_id]
        
    # print('>>>>>> question_responses_df (FD_questions_responses_frequencies)')
    # print(question_responses_df.to_dict('records'))
    
    question_responses_frequencies_series = \
        question_responses_df.groupby([xvalue_field,
                                            'id_componente']).size()
    
    question_responses_frequencies_count = \
        question_responses_frequencies_series.to_frame().reset_index()
    question_responses_frequencies_count.rename(columns={0:'frecuencia'},
                                            inplace=True)
    # print('>>>>>> question_responses_frequencies_count (FD_questions_responses_frequencies)')
    # print(question_responses_frequencies_count.to_dict('records'))
    
    
    nodes_df = FD_Fetch_nodes('Modelo educativo')
    nodes_df
    
    question_responses_frequencies_count =\
        question_responses_frequencies_count.\
            merge(nodes_df, left_on='id_componente', right_on='id_node', 
                  how='outer')
    question_responses_frequencies_count = \
        question_responses_frequencies_count[['id_componente', 
                                                xvalue_field,
                                                'id_node', 'frecuencia']]
    # print('>>>>>>>>>>>>>> question_9_responses_frequencies_count.columns')
    # print(question_9_responses_frequencies_count.columns)
    # print('>>>>>>>>>>>>>> question_9_responses_frequencies_count')
    # print(question_9_responses_frequencies_count.to_dict('records'))
    
    return question_responses_frequencies_count, nodes_df


