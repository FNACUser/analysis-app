# -*- coding: utf-8 -*-
"""
Created on Mon Nov 20 20:18:50 2023

@author: luis.caro
"""

import pandas as pd
import numpy as np
from functools import reduce
from math import pi

from bokeh.models import ColumnDataSource, TapTool, LabelSet

from bokeh.plotting import figure

from bokeh.palettes import all_palettes


def UTBoHM_Create_mapped_palette(xoriginPalette, xoriginPaletteLength,
                             xstartColorIndex, xnumberOfIndexes,
                             xreversed = True):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-UTBo_Create_mapped_palette')
    # print('>>>>>>>>>>>>>>>>>>> xoriginPalette (UTBo_Create_mapped_palette)')
    # print(xoriginPalette)
    # print('>>>>>>>>>>>>>>>>>>> xoriginPaletteLength (UTBo_Create_mapped_palette)')
    # print(xoriginPaletteLength)
    # print('>>>>>>>>>>>>>>>>>>> xnumberOfIndexes (UTBo_Create_mapped_palette)')
    # print(xnumberOfIndexes)
    
    if xreversed == True:
        _palette = list(
            reversed(list(all_palettes[xoriginPalette][xoriginPaletteLength])))
    else:
        _palette = list(all_palettes[xoriginPalette][xoriginPaletteLength])

    _colorsToUse = xoriginPaletteLength - xstartColorIndex
    # print('>>>>>>>>>>>>>>>>>>> _palette (UTBo_Create_mapped_palette)')
    # print(_palette)
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
        
        # print('>>>>>>>>>>>>>>>>>>> _palette (UTBo_Create_mapped_palette)')
        # print(_palette)        

    return _palette


def UTBoHM_Create_proportional_palette(xvalues_to_map, 
                                     xoriginPalette, xoriginPaletteLength,
                                     xstartColorIndex, xmax_value = None,
                                     xreversed = True):
    
    print('.-.-.-.-.-.-.-.-.-. UTBo_Create_proportional_palette')
    # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
    # print(xmax_value)
    # print('>>>>>>>>>>>>>>>> values_to_map (UTBo_Create_proportional_palette)')
    # print(xvalues_to_map)
    
    if xmax_value == None:
        xmax_value = max(xvalues_to_map) + 1
    #     print('none mv')
    # print('>>>>>>>>>>>>>>>> xmax_value (UTBo_Create_proportional_palette)')
    # print(xmax_value)
    
    _base_palette = UTBoHM_Create_mapped_palette(xoriginPalette, 
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


def UTBoHM_component_contents(xcell_frequencies, 
                               xdimension_x_length, xdimension_y_length, 
                               xcontent_is_str = False,                               
                               xtotal_cells = False, xstart_x_index = 0, 
                               xstart_y_index = 0):
    
    print('.-.-.-.-.-.-.-.-.-.-.-oihub_UtilitiesBokeh/UTBo_component_contents')
    # print('>>>>>>>>> xdimension_x_length (UTBo_component_contents)')
    # print(xdimension_x_length)
    # print('>>>>>>>>> xdimension_y_length (UTBo_component_contents)')
    # print(xdimension_y_length)
    # print('>>>>>>>>> xcell_frequencies (UTBo_component_contents)')
    # print(xcell_frequencies['cuatro'].to_list())
    
    def string_array(xnrows,xncolumns):
        
        
        columns = ['']*xncolumns
        # array = [columns]*xnrows
        array = [columns.copy() for i in range(xnrows)]
        
        return array

    def transpose_string_array(xarray):

        nrows = len(xarray)
        ncolumns = len(xarray[0])

        transposed_array = string_array(ncolumns,nrows)

        for i in range(nrows):
            for j in range(ncolumns):
                transposed_array[j][i] = xarray[i][j]
                
        return transposed_array
        
    def flatten_string_array(xarray):
        
        dim1_length = len(xarray)
        dim2_length = len(xarray[0])
        flattened_array = \
            [xarray[i][j] for i in range(dim1_length) for j in range(dim2_length)]
        return flattened_array
    
    def add_content(xindex_x, xindex_y, xcontent):
        # if (xindex_y == 4) | (xindex_y == 6) | (xindex_y == 7):
        index_x = xindex_x - xstart_x_index
        index_y = xindex_y - xstart_y_index
        # print('>>>>>>>>> index_x (add_content)')
        # print(index_x)
        # print('>>>>>>>>> index_y (add_content)')
        # print(index_y)
        # print('>>>>>>>>> xcontent (add_content)')
        # print(xcontent)
        
        if xcontent_is_str == False:
            if xtotal_cells == True:
                contents_array[index_y+1, index_x+1] = xcontent
                contents_array[0, index_x+1] = \
                    contents_array[0, index_x+1] + xcontent
                contents_array[index_y+1, 0] = \
                    contents_array[index_y+1, 0] + xcontent
                contents_array[0, 0] = \
                    contents_array[0, 0] + xcontent
            else:
                contents_array[index_y, index_x] = xcontent
            # print(frequencies_array)
        else:
            contents_array[index_y][index_x] = xcontent
            
        # print('>>>>>>>>> contents_array (add_content)')
        # print(contents_array)    
        
    # print('>>>>>>>>> xcell_frequencies.columns (UTBo_component_contents)')
    # print(xcell_frequencies.columns)
    # print('>>>>>>>>> xcell_frequencies.shape (UTBo_component_contents)')
    # print(xcell_frequencies.shape)
    # print('>>>>>>>>> xcell_frequencies (UTBo_component_contents)')
    # print(xcell_frequencies.to_dict('records'))
    
    content_tuples = \
        [tuple(x) for x in xcell_frequencies.to_records(index=False)]
    # print('>>>>>>>>> frequencies_tuples (UTBo_component_contents)')
    # print(content_tuples)    
        
    if xcontent_is_str == False:
        if xtotal_cells == True:
            contents_array = np.zeros((xdimension_y_length + 1, 
                                          xdimension_x_length + 1))
        else:
            contents_array = np.zeros((xdimension_y_length, 
                                       xdimension_x_length))
        
        [add_content(int(index_x), int(index_y), frec) \
         for  _, index_x, index_y, frec in content_tuples]
        contents_array = np.transpose(contents_array)
        contents_array_flattened = contents_array.flatten()
    
    else:
        contents_array = string_array(xdimension_y_length, 
                                      xdimension_x_length)
        [add_content(int(index_x), int(index_y), content) \
         for  _, index_x, index_y, content in content_tuples]
        contents_array = transpose_string_array(contents_array)
        contents_array_flattened = flatten_string_array(contents_array)
    
        
    # print('>>>>>>>>> contents_array (UTBo_component_contents)')
    # print(contents_array)    
    
    # print('>>>>>>>>> contents_array_flattened (UTBo_component_contents)')
    # print(contents_array_flattened)    
        
    return contents_array_flattened



def UTBoHM_Component_hm(xdimension_x_dict, xdimension_y_dict,
                      xcell_contents, xtitle,
                      xtotal_cells = False, xtotal_cells_label = '',
                      xcontent_is_str = False,
                      xstart_x_index = 0, xstart_y_index = 0,
                      xlabel_x_axis = '', xlabel_y_axis = '',
                      xwidth=400, xheight=400,
                      xreverse_content = False,
                      xsingle_color = 'lightblue',
                      xx_offset = 0, xy_offset = 0,
                      xtext_align = 'center',
                      xtools = ['tap']):
    
#Asi eran:
# xx_offset = -400, xy_offset = -25,
# xtext_align = 'left',

    
    """
    Returns a heatmap
    
    Input:  - xdimension_x_dict: dictionary with x axis coordinates
            - xdimension_y_dict: dictionary with y axis coordinates
            - xcell_frequencies: DataFrame with 4 columns:
                - col1: irrevelant
                - col2: x index
                - col3: y index
                - col4: content to put in the cell
            - xx_offset and xy_offset are used to center the contents
                in each cell            
    
    """
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_UtilitiesBokeh/UTBoHM_Component_hm')
    
    # print('>>>>>>>>>>>>>>>>>> xtitle (UTBoHM_Component_hm)')
    # print(xtitle)
    # print('>>>>>>>>>>>>>>>>>> xdimension_x_dict (UTBoHM_Component_hm)')
    # print(xdimension_x_dict)
    # print('>>>>>>>>>>>>>>>>>> xdimension_y_dict (UTBoHM_Component_hm)')
    # print(xdimension_y_dict)
    # print('>>>>>>>>> xcell_contents (UTBoHM_Component_hm)')
    # print(xcell_contents)
    # print('>>>>>>>>> xtotal_cells (UTBoHM_Component_hm)')
    # print(xtotal_cells)
    
    dimension_x_list = [v for _,v in xdimension_x_dict.items()]
    # print('>>>>>>>>>>>>>>>>>> dimension_x_list (UTBoHM_Component_hm)')
    # print(dimension_x_list)
    
    dimension_y_list = [v for _,v in xdimension_y_dict.items()]
    # print('>>>>>>>>>>>>>>>>>> dimension_y_list (UTBoHM_Component_hm)')
    # print(dimension_y_list)
    # print('>>>>>>>>>>>>>>>>>> xcell_contents (UTBoHM_Component_hm)')
    # print(xcell_contents['cuatro'].to_list())
    
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
    
    # print('>>>>>>>>>>>>>>>>>> x_lists (UTBoHM_Component_hm)')
    # print(x_lists)
    # print('>>>>>>>>>>>>>>>>>> y_lists (UTBoHM_Component_hm)')
    # print(y_lists)
    
    x = reduce(lambda a, b: a + b, x_lists)
    y = reduce(lambda a, b: a + b, y_lists)
    # print('>>>>>>>>>>>>>>>>>> x (UTHM_Component_hm)')
    # print(x)
    # print(len(x))
    # print('>>>>>>>>>>>>>>>>>> y (UTHM_Component_hm)')
    # print(y)
    # print(len(y))
    
    factors_x = [dimension_x_list[i] for i in range(0,dimension_x_length)]
    factors_y = [dimension_y_list[i] for i in range(0,dimension_y_length)]
    if xtotal_cells == True:
        factors_x = [xtotal_cells_label] + factors_x
        factors_y = [xtotal_cells_label] + factors_y
    # print('>>>>>>>>>>>>>>>>>> factors_x (UTHM_Component_hm)')
    # print(factors_x)
    # print('>>>>>>>>>>>>>>>>>> factors_y (UTHM_Component_hm)')
    # print(factors_y)
        
    
    if xcontent_is_str == False:
        contents = \
            [int(frequency) for frequency in \
             UTBoHM_component_contents(xcell_contents, 
                                    dimension_x_length,
                                    dimension_y_length,
                                    xtotal_cells= xtotal_cells,
                                    xcontent_is_str = xcontent_is_str,
                                    xstart_x_index = xstart_x_index, 
                                    xstart_y_index = xstart_y_index)]
        colors = UTBoHM_Create_proportional_palette(contents, 'Greens', 256, 0)
        contents_str = [str(content) if content > 0 else '' \
                        for content in contents]
    else:
        contents = \
             UTBoHM_component_contents(xcell_contents, 
                                        dimension_x_length,
                                        dimension_y_length,
                                        xtotal_cells= xtotal_cells,
                                        xcontent_is_str = xcontent_is_str,
                                        xstart_x_index = xstart_x_index, 
                                        xstart_y_index = xstart_y_index)
        colors = [xsingle_color] * len(x)
        contents_str = [content for content in contents]
    
    # print('>>>>>>>>>>>>>>>>>> contents (UTHM_Component_hm)')
    # print(contents)
    # print('>>>>>>>>>>>>>>>>>> colors (UTHM_Component_hm)')
    # print(colors)
    # print('>>>>>>>>>>>>>>>>>> contents_str (UTHM_Component_hm)')
    # print(contents_str)
    
    _tools = xtools
    
    source_dict = {'x': x,
                   'y': y,
                   'fill_colors': colors,
                   'frequencies': contents_str}
    # print('>>>>>>>>>>>>>>>>>> source_dict (UTHM_Component_hm)')
    # print(source_dict)
    source_df = pd.DataFrame.from_dict(source_dict)
    # print('>>>>>>>>>>>>>>>>>> source_df (UTHM_Component_hm)')
    # print(source_df)
    
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
        text_align= xtext_align,
        x_offset = xx_offset,
        y_offset= xy_offset,
        source=source,
        text_color = 'black'
    )
    
    hm.add_layout(labels)
    
    # print('hm.renderers[0].data_source.selected.indices')
    # print(hm.renderers[0].data_source.selected.indices)
    
    return hm


def UTBoHM_Create_proportional_palette2(xvalues, xpalette, xpalette_length,                                        
                                        xstart_index = 0,
                                        xend_index = 0,
                                        xreversed = True):

    if xreversed == True:
        _palette = list(
            reversed(list(all_palettes[xpalette][xpalette_length])))
    else:
        _palette = list(all_palettes[xpalette][xpalette_length])
        
    if xend_index == 0:
        xend_index = xpalette_length - 1
    # print('xend_index')
    # print(xend_index)
    indexes_length = xend_index - xstart_index + 1
    # print('indexes_length')
    # print(indexes_length)
    #-->151
    
    case_palette = _palette[xstart_index:xend_index+1]
    length_case_palette = len(case_palette)
    
    case_palette_dict = {i:case_palette[i] for i in range(length_case_palette)}
    # print('case_palette_dict')
    # print(case_palette_dict)
    
    
    minimum_value = min(xvalues)
    minimum_value
    maximum_value = max(xvalues)
    maximum_value
    values_span = maximum_value - minimum_value + 1
    values_span
    #--> 55
    
    step = indexes_length / values_span
    step
    
    case_palette_indexes_dict =\
        {i:min(int(round(i*step, 0)), length_case_palette - 1) 
         for i in range(values_span)}
    # print('case_palette_indexes_dict')
    # print(case_palette_indexes_dict)
    
    
    _colors = [case_palette_dict[case_palette_indexes_dict[value - minimum_value]]
              for value in xvalues]
    
    return _colors

def UTBoHM_create_bicolor_proportional_palette(xvalues, xpalette_length,
                                               xstart_index = 0,
                                               xend_index = 0,
                                               xreversed = True,
                                               xpositive_palette = 'Greens',
                                               xnegative_palette = 'Reds', 
                                               center_offset = 0):

    xcenter_offset = 50

    positive_values = [i for i in xvalues if i >= center_offset]
    positive_values
    negative_values = [i for i in xvalues if i < center_offset]
    negative_values

    positive_values_tuples = \
        [(i, xvalues[i]-xcenter_offset) 
         for i in range(len(xvalues)) if xvalues[i] >= center_offset]
    positive_values_tuples
    positive_values = [v for i,v in positive_values_tuples]
    positive_values

    negative_values_tuples = \
        [(i, -1 * (xvalues[i] - center_offset)) 
          for i in range(len(xvalues)) if xvalues[i] < center_offset]
    negative_values = [v for i,v in negative_values_tuples]
    negative_values_tuples

    colors_positive =\
        UTBoHM_Create_proportional_palette2(positive_values, xpositive_palette,
                                            xpalette_length,
                                            xstart_index = xstart_index,
                                            xend_index = xend_index,
                                            xreversed = xreversed)
    colors_positive
    
    colors_negative =\
        UTBoHM_Create_proportional_palette2(negative_values, xnegative_palette, 
                                            xpalette_length,
                                            xstart_index = xstart_index,
                                            xend_index = xend_index,
                                            xreversed = xreversed)
    colors_negative

    negative_values_and_colors =\
        list(zip(negative_values_tuples,colors_negative))

    colors_dict =\
        {index:color for (index, _), color in negative_values_and_colors}
    colors_dict

    positive_values_and_colors =\
        list(zip(positive_values_tuples, colors_positive))

    for (index,_), color in positive_values_and_colors:
        colors_dict.update({index: color})
    
    index_and_colors_list = [(index, color) for index,color in colors_dict.items()]
    index_and_colors_list.sort()
    colors = [color for (_, color) in index_and_colors_list]
    colors
    
    return colors

