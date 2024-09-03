# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 00:10:33 2023

@author: luis.caro
"""

import datetime
import random
import pandas as pd
import numpy as np
from functools import reduce
from math import pi

# from bokeh.models import (Plot, Range1d, MultiLine, Circle, Ellipse, Square, 
#                           ColumnDataSource, Oval, Scatter)
#Se quitó Square
#Se reemplazó Oval por Ellipse
from bokeh.models import (Plot, Range1d, MultiLine, Circle, Ellipse, 
                          ColumnDataSource, Scatter, LabelSet)
from bokeh.plotting import figure, from_networkx

from bokeh.models import (BoxZoomTool, ResetTool, PanTool, HoverTool, \
                          BoxSelectTool, TapTool, FixedTicker, 
                          ColumnDataSource, TableColumn, 
                          StaticLayoutProvider, Range1d)

from bokeh.models.widgets import DataTable

from bokeh.models import EdgesAndLinkedNodes, NodesAndLinkedEdges
from bokeh.palettes import Spectral4, all_palettes

from bokeh.layouts import row, column
from bokeh.models import Paragraph, Div

import networkx as nx
from networkx.algorithms import bipartite

from bokeh.palettes import Spectral6, Turbo256
from bokeh.transform import linear_cmap

from .oihub_UtilitiesNetworkx import (UTNx_Adjust_nodes_size, 
                               UTNx_Adjust_edge_width)


#%%
def UT_CountOcurrences(xtable,xcolumns):
    count=xtable.groupby(xcolumns).size().to_frame()
    count.columns = ['Count']
    count.reset_index(inplace=True)
    return count

#%%
def UT_NumberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]

# numberToBase=UT_NumberToBase(10, 2)
# print(numberToBase)
# print(type(numberToBase))


#%% Dates

def UT_String_to_datetime(string_date, xstring="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strptime(string_date, xstring)        
    
def UT_Datetime_to_string(datetime_date, xstring="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strftime(datetime_date, xstring)
    
def UT_Timestamp_to_datetime(xtimestamp):
    return datetime.datetime.fromtimestamp(xtimestamp)

def UT_Datetime_to_timestamp(xdatetime):
    return datetime.timestamp(xdatetime)
    
#%% Layout

def UTBo_EmptyParagraph(xwidth,xheight):
    return row(Paragraph(text="""  """,width=xwidth, height=xheight))




#%%

def FD_KeyAttributeColor(xG,xkeyColorAttribute,xcolorAttribute,
                         xnodes_colors_keys = True):
    
    print('.-.-.-.-.-.-.-. oihub_UtilitiesBokeh/FD_KeyAttributeColor')
    # print('>>>>>>>>>>>> xkeyAttribute (FD_KeyAttributeColor)')
    # print(xkeyAttribute)
    # print('>>>>>>>>>>>> xcolorAttribute (FD_KeyAttributeColor)')
    # print(xcolorAttribute)
    # print('>>>>>>>>>>>> xG.nodes(data=True) (FD_KeyAttributeColor)')
    # print(xG.nodes(data=True))
    
    # for g,v in xG.nodes(data=True):
    #     print('g')
    #     print(g)
    #     print(v[xkeyAttribute],v[xcolorAttribute])
    
    if xnodes_colors_keys == True:
        tuples = \
            list(set([(v[xkeyColorAttribute],v[xcolorAttribute]) \
                      for g,v in xG.nodes(data=True)]))
    else:
        tuples = \
            list(set([(v[xkeyColorAttribute],v[xcolorAttribute]) \
                      for g,h,v in xG.edges(data=True)]))
    # print('>>>>>>>>>>>>>>>>>> tuples (FD_KeyAttributeColor)')
    # print(tuples)
    
    #Esto era solo para revisar
    # tuplesII = [(g, v[xkeyAttribute],v[xcolorAttribute]) \
    #               for g,v in xG.nodes(data=True)]
    # print('>>>>>>>>>>>>>>>>>> tuplesII (FD_KeyAttributeColor)')
    # print(tuplesII)
    
    keys=[key for (key,color) in tuples]
    # print('>>>>>>>>>>>>>>>>>> keys (FD_KeyAttributeColor)')
    # print(keys)
    
    colors=[color for (key,color) in tuples]
    # print('>>>>>>>>>>>>>>>>>> colors (FD_KeyAttributeColor)')
    # print(colors)
    
    keys_colors_df = \
        pd.DataFrame(list(zip(keys, colors)),
                     columns=['keys','colors']).sort_values('keys')
    sorted_keys = list(keys_colors_df['keys'])
    sorted_colors = list(keys_colors_df['colors'])
    
    return sorted_keys, sorted_colors


#%%

def xtype(xa):
    if type(xa) == int or type(xa) == float:
        print('number')
    else:
        print('The variable is not a number')

#%% Network plot

'''
Devuelve un gráfico de red Bokeh.
Los parámetros de entrada: xGraph: red networkx
                                    - xtooltips: campos para el hover
                                    - xtitle: título
                                    - xbaseLayout: default layout
                                    - xlayout: layout alterno
                                    - xuseLayout: True, use xLayout;
                                                    False, use xbaseLayout
                                    - xnodeSize: el nombre del atributo en 
                                                    xGraph con el tamaño de los
                                                    nodos, puede ser un
                                                    valor. El default es 12.
                                    - xplotHeight: altura del plot
                                    - xedgeLineDash = tipo de línea. Las opciones
                                                      son solid (default), 
                                                      dashed, dotted, dotdash, 
                                                      dashdot.
                                    - xedgeLineDashAttribute = nombre  del
                                                      atributo con el line dash.
                                                      Si se indica xedgeLineDash,
                                                      xedgeLineDashAttribute se
                                                      ignora.
                                    - x_axis_overrides = overrides para etiquetas
                                                        del eje x 
                                    - y_axis_overrides = overrides para etiquetas
                                                        del eje y
                                    - xadjustNodeSize: True: ajusta el tamaño 
                                                        de los nodos
                                    - xminimumNodeSize: tamaño mínimo del nodo
                                                        cuando hay ajuste
                                    - xmaximumNodeSize: tamaño máximo del nodo
                                                        cuando hay ajuste
                                    - xapplyToSizeZero: True: ajusta nodos de
                                                        tamaño cero cuando hay
                                                        ajuste
                                    - xadjustOnlyMinimum: True: quiere decir que
                                                        si el valor es menor
                                                        que el mínimo, se ajusta 
                                                        al mínimo. De lo
                                                        contrario no se ajusta.
                                    - xadjustEdgeWidth: True: ajusta el grosor 
                                                        de las conexiones
                                    - xminimumEdgeWidth: grosor mínimo de la
                                                        conexión cuando hay 
                                                        ajuste
                                    - xmaximumEdgeWidth: grosor máximo de la
                                                        conexión cuando hay 
                                                        ajuste
                                    - xnlist: parámetro de círculos para
                                              nx.shell_layout
                                    - xpos: posiciones de partida para
                                              nx.spring_layout
                                    - xkeyColorAttribute: node color attribute
                                            for left legend
                                    - xright_keyColorAttribute: edge color
                                        attribute for right legend 
                                    - xColorLegendTitle: title for left
                                        legend                                    
                                    - xright_ColorLegendTitle: title for right
                                        legend                                    
                                    - xcircle: lista de de círculos para los
                                                n-cliques. Cada elemento trae:
                                                    - número
                                                    - borde
                                                    - color
                                    - xk: parámetro de spring_layout para
                                            minima distancia entre nodos.
                                            Si es -1 se convierte al default
                                            1/sqrt(n). Solo aplica si xpos!=None.
                                            Esto ultimo porque es un parámetro
                                            de spring_layout que es el que 
                                            normalmente recibe xpos (así
                                            se evitan errores con otros layouts).
                                            Si xpos=None, el valor se ignora.
                                    - xleft_margin: sirve para correr el
                                                    grafo hacia la derecha 
                                                    dejando a la leyenda en su
                                                    lugar original
                                    - xright_margin: sirve para correr el
                                                    grafo hacia la izquierda 
                                                    dejando a la leyenda en su
                                                    lugar original a la derecha
                                    - xlegend_text_font_size: tamaño del
                                            texto de la leyenda
                                    - xvisible_axis: True, muestra etiquetas de
                                                        ambos ejes.
                                                    False, oculta las etiquetas
                                    
Color nodos:  - xgenerateNodeColor funciona cuando el xnodeColorAttribute es
                numérico. Si no es numérico produce error.
              - si xnodeColorAttribute no es un color y el atributo no es numérico,
                se generan colores automáticamente
              - si xnodeColorAttribute no es un color y el atributo es numérico,
                los nodos salen sin color , solo sale el borde. Y el legend se vuelve
                inútil porque sale sin colores.
'''
def UTBo_Network_PlotType2(xGraph, xtooltips,xtitle,xbaseLayout,xlayout,
                         xuseLayout, 
                         xplotHeight, xplotWidth,
                         xnodeSize=12,
                         xcolorBasedOnSize=False,
                         xnodeColorAttribute='',
                         xgenerateNodeColor=False,
                         xedgeColorAttribute='',
                         xedgeLineDash = '',
                         xedgeLineDashAttribute ='',
                         xgenerateEdgeColor=False,
                         xedgeWidthAttribute='',
                         addCentroid=False,
                         xx_range=(-1.1,1.1),xy_range=(-1.1,1.1),
                         x_axis_overrides={},y_axis_overrides={},
                         xadjustNodeSize = False, xminimumNodeSize=3,
                         xmaximumNodeSize=14, xapplyToSizeZero=True,
                         xadjustEdgeWidth = False, xminimumEdgeWidth=1,
                         xmaximumEdgeWidth=12,
                         xadjustOnlyMinimum=False,
                         xgravityAttribute='',
                         xdisplayTools=True,
                         xpos=None,
                         xkeyColorAttribute='',
                         xright_keyColorAttribute='',
                         xColorLegendTitle=[],
                         xright_ColorLegendTitle=[],
                         xnlist=[],
                         xcircle=[],
                         xk=-1,
                         xleft_margin = 0,
                         xright_margin = 0,
                         xlegend_text_font_size = "12px",
                         xvisible_axis = False):
    
    """
    colorPaletteBasedOnAttribute se trae como True si hay un attributo
    numérico sobre el cual se quiere definir el color. En este caso el
    nombre del atributo se pone en xnodeColor. Y es necesario que 
    colorBasedOnSize se traiga como False
    """
    print('.-.-.-.-.-.-.-.-.-.-.- oihub_UtilitiesBokeh/UTBo_Network_PlotType2')
    
    
    random.seed(10000)
    
    if type(xx_range) == Range1d:
        xx_range = (xx_range.start - xleft_margin, xx_range.end + xright_margin)
    else:
        xx_range = (xx_range[0] - xleft_margin, xx_range[1] + xright_margin)
    
    if xadjustNodeSize == True:
        xGraph = UTNx_Adjust_nodes_size(xGraph,xminimumNodeSize,
                                        xmaximumNodeSize, xnodeSize,
                                        xapplyToSizeZero=xapplyToSizeZero,
                                        xadjustOnlyMinimum=xadjustOnlyMinimum)
        
    if (xedgeWidthAttribute != '') & (len(xGraph.edges()) != 0) &\
        (xadjustEdgeWidth == True):
        UTNx_Adjust_edge_width(xGraph,xminimumEdgeWidth, 
                                        xmaximumEdgeWidth, xedgeWidthAttribute)
    
    plotType1 = figure(width=xplotWidth, height=xplotHeight,
                      x_range=xx_range, y_range=xy_range)
    
    
    plotType1.title.text = xtitle
    plotType1.axis.visible = xvisible_axis
    
    #ajusta xkal default si es -1
    number_of_nodes = xGraph.number_of_nodes()
    if (xk == -1) & (number_of_nodes != 0):
        xk = 1 / (number_of_nodes ** 0.5)
    
    #para los cliques
    if len(xcircle) != 0:
        
        # print('>>>>>>>>>>>>>>>>>>> entra a cliques (UTBo_Network_PlotType2)')
        
        def add_circle(xi,xcolor,xborder):
            plotType1.circle(0, 0, radius=(1.1*xi/len(xcircle)), 
                             fill_color=xcolor, line_color=xborder)
        
        [add_circle(i,color,border) for i,color, border in xcircle]
        
    if (xpos == None) & (xnlist == []):
        graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0))
    elif (xpos != None):
        
        graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0), 
                                pos=xpos, k=xk)
    else:
        graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0), 
                                nlist=xnlist)
        
    #Esto está bien se comentarió para esayar el HooverTool
    #ESTO SE VA A PODER QUITAR
    # if xdisplayTools == True:
    #     plotType1.add_tools(PanTool(), BoxZoomTool(), ResetTool(),\
    #                         HoverTool(tooltips=xtooltips), TapTool(),\
    #                             BoxSelectTool())
    # else:
    #     plotType1.toolbar.logo = None
    #     plotType1.toolbar_location = None
    #     plotType1.add_tools(HoverTool(tooltips=xtooltips))

    """
    Esto reemplaza lo de arriba (no se ha quitado aún, precaución)
    Se hace así para que los tooltips solo apliquen al grafo principal
    """
    #Esto es lo de arriba sin el HoverTool
    if xdisplayTools == True:
        plotType1.add_tools(PanTool(), BoxZoomTool(), ResetTool(),\
                            TapTool(),\
                                BoxSelectTool())
    else:
        plotType1.toolbar.logo = None
        plotType1.toolbar_location = None
        # plotType1.add_tools(HoverTool(tooltips=xtooltips))

    #Spectral4 Turbo256
    if xcolorBasedOnSize == True:
        node_sizes=[xGraph.nodes[node][xnodeSize] for node in xGraph.nodes]
        mapper = linear_cmap(field_name=xnodeSize, palette=Turbo256 ,
                              low=min(node_sizes),
                              high=max(node_sizes))   #
        # graph1.node_renderer.glyph = Circle(size=_nodeSize,fill_color=mapper)
        graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=mapper)
    
    else:
        # print('>>>>>>>>>>>>>>>>>>> xnodeColorAttribute (UTBo_Network_PlotType2)')
        # print(xnodeColorAttribute)
        if xnodeColorAttribute != '':
            if xgenerateNodeColor == True:
                node_colors=[xGraph.nodes[node][xnodeColorAttribute] for node in xGraph.nodes]
                mapper = linear_cmap(field_name=xnodeColorAttribute, palette=Turbo256 ,
                                      low=min(node_colors),
                                      high=max(node_colors))   #
                graph1.node_renderer.glyph = Circle(size= xnodeSize,
                                                    fill_color=mapper)
            else:            
                graph1.node_renderer.glyph = Circle(size= xnodeSize,
                                                fill_color=xnodeColorAttribute)
        else:
            graph1.node_renderer.glyph = Circle(size = xnodeSize)
            
        
    graph1.node_renderer.selection_glyph = \
        Circle(size=15, fill_color=Spectral4[2])
    graph1.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    
    graph1.edge_renderer.glyph = MultiLine(line_alpha=0.4,line_width=0.4)
    graph1.edge_renderer.selection_glyph = \
        MultiLine(line_color=Spectral4[2], line_width=5)
    graph1.edge_renderer.hover_glyph = \
        MultiLine(line_color=Spectral4[1], line_width=5)
        
    #esto sigue aquí porque se asumía que el atributo del width siempre era el
    #   weught. Esto se reemplazó por xedgeWidthAttribute 
    # if useEdgeWeight == True:
    #     graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
    #     print('useEdgeWeight está deprecado')
    
    # if xedgeWidthAttribute != '':
    #     graph1.edge_renderer.glyph.line_width = {'field': xedgeWidthAttribute}
    
    if xedgeColorAttribute != '': 
        if xgenerateEdgeColor == True:
            # print('>>>>>>>>>>>>>>> edge colors')
            # print(xnodeColor)
            edge_colors=[xGraph.edges[edge][xedgeColorAttribute] for edge in xGraph.edges]
            # print(edge_colors)
            invTurbo256=[c for c in reversed(Turbo256)]
            invTurbo256=tuple(invTurbo256)
            mapper = linear_cmap(field_name=xedgeColorAttribute, palette=invTurbo256,
                                  low=min(edge_colors), high=max(edge_colors))
            # print('>>>>>>>>>>>>>>>>>>>>>>>>> mapper')
            # print(mapper)
            graph1.edge_renderer.glyph.line_color = mapper #{'field': 'color'}            
        else:
            graph1.edge_renderer.glyph.line_color = \
                {'field': xedgeColorAttribute}
            
    """
    Asigna el tipo de dash según las opciones
    """
    if xedgeLineDash != '':        
        graph1.edge_renderer.glyph.line_dash = xedgeLineDash
    elif xedgeLineDashAttribute != '':
        graph1.edge_renderer.glyph.line_dash = \
            {'field': xedgeLineDashAttribute}
        
    # graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
    graph1.selection_policy = NodesAndLinkedEdges()
    # graph1.selection_policy = EdgesAndLinkedNodes()
    
    if len(y_axis_overrides) > 0:
        print('>>>>>>>>>>>>>>>>>>>y_axis_overrides (UTBo_Network_PlotType2)')
        print(y_axis_overrides)
        # a=5/0
        plotType1.yaxis.ticker = \
            FixedTicker(ticks=[i for i in range(0,len(y_axis_overrides))])
                                              # list(y_axis_overrides.values()))
        plotType1.yaxis.major_label_overrides = y_axis_overrides        
        
    if len(x_axis_overrides) > 0:
        plotType1.xaxis.ticker = \
            FixedTicker(ticks=[i for i in range(0,len(x_axis_overrides))])
                                              # list(y_axis_overrides.values()))
        plotType1.xaxis.major_label_overrides = x_axis_overrides  
        
    
        
    plotType1.renderers.append(graph1)
    
    """
    Así es que se logra que los tooltips solo apliquen al grafo principal
    (Esto permitiría poner diferentes tooltips a renderers diferentes)
    """
    plotType1.add_tools(HoverTool(renderers = [plotType1.renderers[0]],
                                  tooltips = xtooltips))
    
    layout=graph1.layout_provider
    
    if addCentroid==True:
        centroidGraph = nx.DiGraph()
        centroidGraph.add_node('centroid')
        graph2=from_networkx(centroidGraph, xbaseLayout, scale=1, center=(0,0))
        graph2.node_renderer.glyph = Ellipse(height=0.1, width=0.05, 
                                             line_color='black',
                                             fill_color="brown")
        
        plotType1.renderers.append(graph2)
    
    if xuseLayout == True:
        layout.graph_layout=dict(xlayout.graph_layout)
        
    if xgravityAttribute != '':
        weighted_pos = \
            nx.spring_layout(xGraph, weight=xgravityAttribute, pos=xpos, k=xk)
        slp=StaticLayoutProvider(graph_layout=weighted_pos)
        layout.graph_layout=dict(slp.graph_layout)
        
    if xedgeWidthAttribute != '':
        graph1.edge_renderer.glyph.line_width = {'field': xedgeWidthAttribute}
        
    # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - antes')
    # print(len(plotType1.renderers))
    
    if xColorLegendTitle != []:
        plotType1.text(x=[-1 - xleft_margin], y=[1.025], 
                       text=xColorLegendTitle, text_font_size="14px", 
                       text_align="left", text_baseline="middle")
    
    if xright_ColorLegendTitle != []:
        plotType1.text(x=[1 + xright_margin], y=[1.025], 
                       text=xright_ColorLegendTitle, text_font_size="14px", 
                       text_align="right", text_baseline="middle")
    
    if (xkeyColorAttribute != '') & (xnodeColorAttribute != ''):
        keys,colors = FD_KeyAttributeColor(xGraph,xkeyColorAttribute,
                                            xnodeColorAttribute)
        # print('#$%&/(((((())))) xkeyColorAttribute UTBo_Network_PlotType2')
        # print(xkeyColorAttribute)
        # print('>>>>>>>>>>>>> xnodeColorAttribute UTBo_Network_PlotType2')
        # print(xnodeColorAttribute)
        # print('>>>>>>>>>>>>> keys UTBo_Network_PlotType2')
        # print(keys)
        # print('>>>>>>>>>>>>> colors UTBo_Network_PlotType2')
        # print(colors)
        
        # print(len(keys))
        rx=[-0.975 - xleft_margin for i in range(0,len(keys))]
        # print(rx)
        # ry=[1-0.05*(i+1) for i in range(0,len(keys))]
        ry=[1-0.09*(i+1) for i in range(0,len(keys))]
        # print(ry)
        tx=[-0.85 - xleft_margin for i in range(0,len(keys))]
        ty=[ry[i]-0.005 for i in range(0,len(keys))]
        # print(tx)
        
        # imposedBokehGraph = \
        #     from_networkx(nx.Graph(), nx.spring_layout, scale=1, center=(0,0))
        # plotType1.renderers.append(imposedBokehGraph)
    
        # plotType1.text(x=[-1 - xleft_margin], y=[1.025], text=xColorLegendTitle,\
        #     text_font_size="14px", text_align="left", text_baseline="middle")
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de legend')
        # print(len(plotType1.renderers))
        # plotType1.rect(x=rx, y=ry,width=0.040, height=0.040,fill_color=colors)
        plotType1.rect(x=rx, y=ry,width=0.08, height=0.08,fill_color=colors)
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de cuadros')
        # print(len(plotType1.renderers))
        plotType1.text(x=tx, y=ty, text=list(keys), 
                       text_font_size = xlegend_text_font_size,
                        text_align="left", text_baseline="middle")
        # text_line_height = 1,
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de deptos')
        # print(len(plotType1.renderers))
        
    if (xright_keyColorAttribute != '') & (xedgeColorAttribute != ''):
        keys,colors = FD_KeyAttributeColor(xGraph,xright_keyColorAttribute,
                                            xedgeColorAttribute,
                                            xnodes_colors_keys = False)
        
        rx=[0.975 + xright_margin for i in range(0,len(keys))]
        # print(rx)
        # ry=[1-0.05*(i+1) for i in range(0,len(keys))]
        ry=[1-0.09*(i+1) for i in range(0,len(keys))]
        # print(ry)
        tx=[0.9 + xright_margin for i in range(0,len(keys))]
        ty=[ry[i]-0.005 for i in range(0,len(keys))]
        # print(tx)
        
        plotType1.rect(x=rx, y=ry,width=0.08, height=0.08,fill_color=colors)
        
        plotType1.text(x=tx, y=ty, text=list(keys), 
                       text_font_size = xlegend_text_font_size,
                        text_align="right", text_baseline="middle")
        # text_line_height = 1,
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de deptos')
        # print(len(plotType1.renderers))
        
    return plotType1, graph1 

#Esta función tenía errores y aparentemente no se usa
# def create_p2(xdf,_x,_y,xsize,xcolor,xdiscrete,xcontinuous):
#     xs = xdf[_x.value].values
#     ys = xdf[_y.value].values
#     x_title = _x.value.title()
#     y_title = _y.value.title()

#     kw = dict()
#     if _x.value in xdiscrete:
#         kw['x_range'] = sorted(set(xs))
#     if _y.value in xdiscrete:
#         kw['y_range'] = sorted(set(ys))
#     kw['title'] = "%s vs %s" % (x_title, y_title)

#     p = figure(height=600, width=800, tools='pan,box_zoom,hover,reset', **kw)
#     p.xaxis.axis_label = x_title
#     p.yaxis.axis_label = y_title

#     if _x.value in xdiscrete:
#         p.xaxis.major_label_orientation = pd.np.pi / 4

#     sz = 9
#     if xsize.value != 'None':
#         if len(set(df[size.value])) > N_SIZES:
#             groups = pd.qcut(df[size.value].values, N_SIZES, duplicates='drop')
#         else:
#             groups = pd.Categorical(df[size.value])
#         sz = [SIZES[xx] for xx in groups.codes]

#     c = "#31AADE"
#     if xcolor.value != 'None':
#         if len(set(df[color.value])) > N_COLORS:
#             groups = pd.qcut(df[color.value].values, N_COLORS, duplicates='drop')
#         else:
#             groups = pd.Categorical(df[color.value])
#         c = [COLORS[xx] for xx in groups.codes]

#     p.circle(x=xs, y=ys, color=c, size=sz, line_color="white", alpha=0.6, hover_color='white', hover_alpha=0.5)

#     return p


# Esta es la versión anterior. Se dejó aquípor seguridad mientras se prueba la
# nueva. Los cambios son sobre el manejo de colores.
def UTBo_Network_PlotType1(xGraph,xtooltips,xtitle,xbaseLayout,xlayout,
                          xuseLayout, xnodeSize, xnodeColor,xplotHeight,
                          xplotWidth,addCentroid=False,colorBasedOnSize=True,
                          colorPaletteBasedOnAttribute=False,
                          x_range=(-1.1,1.1),y_range=(-1.1,1.1),
                          x_axis_overrides={},y_axis_overrides={},
                          useEdgeWeight = False, 
                          useEdgeColor = False,
                          xedgeColorAttr='',
                          xadjustNodeSize = False, xminimumNodeSize=3,
                          xmaximumNodeSize=14, xapplyToSizeZero=True,
                          xadjustOnlyMinimum=False,
                          xgravityAttribute='',
                          xdisplayTools=True,
                          xedgeWidthAttribute='',
                          pos=None,
                          xkeyColorAttribute='',
                          xColorLegendTitle=[]):
    
    """
    colorPaletteBasedOnAttribute se trae como True si hay un attributo
    numérico sobre el cual se quiere definir el color. En este caso el
    nombre del atributo se pone en xnodeColor. Y es necesario que 
    colorBasedOnSize se traiga como False
    """
    # print('>>>>>>>>>>>>>>> xkeyColorAttribute al entrar')
    # print(xkeyColorAttribute)
        
    
    random.seed(10000)
    
    if xadjustNodeSize == True:
        xGraph = UTNx_Adjust_nodes_size(xGraph,xminimumNodeSize,
                                        xmaximumNodeSize,xnodeSize,
                                        xapplyToSizeZero=xapplyToSizeZero,
                                        xadjustOnlyMinimum=xadjustOnlyMinimum)
    
    # plotType1 = Plot(plot_width=xplotWidth, plot_height=xplotHeight,
    #                  x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    plotType1 = figure(plot_width=xplotWidth, plot_height=xplotHeight,
                      x_range=x_range, y_range=y_range)
    
    plotType1.title.text = xtitle
    
    if pos == None:
        graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0))
    else:
        graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0), pos=pos)
    
    if xdisplayTools == True:
        plotType1.add_tools(PanTool(), BoxZoomTool(), ResetTool(),\
                            HoverTool(tooltips=xtooltips), TapTool(),\
                                BoxSelectTool())
    else:
        plotType1.toolbar.logo = None
        plotType1.toolbar_location = None
        plotType1.add_tools(HoverTool(tooltips=xtooltips))

    #Spectral4 Turbo256
    if colorBasedOnSize == True:
        node_sizes=[xGraph.nodes[node][xnodeSize] for node in xGraph.nodes]
        mapper = linear_cmap(field_name=xnodeSize, palette=Turbo256 ,
                              low=min(node_sizes),
                              high=max(node_sizes))   #
        # graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=mapper)
        graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=mapper)
    
    else:
        if colorPaletteBasedOnAttribute == True:
            node_colors=[xGraph.nodes[node][xnodeColor] for node in xGraph.nodes]
            mapper = linear_cmap(field_name=xnodeColor, palette=Turbo256 ,
                                  low=min(node_colors),
                                  high=max(node_colors))   #
            graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=mapper)
        else:            
            graph1.node_renderer.glyph = Circle(size=xnodeSize,
                                                fill_color=xnodeColor)
        
    graph1.node_renderer.selection_glyph = \
        Circle(size=15, fill_color=Spectral4[2])
    graph1.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    
    graph1.edge_renderer.glyph = MultiLine(line_alpha=0.4,line_width=0.4)
    graph1.edge_renderer.selection_glyph = \
        MultiLine(line_color=Spectral4[2], line_width=5)
    graph1.edge_renderer.hover_glyph = \
        MultiLine(line_color=Spectral4[1], line_width=5)
        
    #esto sigue aquí porque se asumía que el atributo del width siempre era el
    #   weught. Esto se reemplazó por xedgeWidthAttribute 
    # if useEdgeWeight == True:
    #     graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
    #     print('useEdgeWeight está deprecado')
    
    # if xedgeWidthAttribute != '':
    #     graph1.edge_renderer.glyph.line_width = {'field': xedgeWidthAttribute}
    
    if useEdgeColor == True:
        if xedgeColorAttr != '':
            # print('>>>>>>>>>>>>>>> edge colors')
            # print(xnodeColor)
            edge_colors=[xGraph.edges[edge][xedgeColorAttr] for edge in xGraph.edges]
            # print(edge_colors)
            invTurbo256=[c for c in reversed(Turbo256)]
            invTurbo256=tuple(invTurbo256)

            mapper = linear_cmap(field_name=xedgeColorAttr, palette=invTurbo256 ,
                                      low=min(edge_colors),
                                      high=max(edge_colors))
            # print('>>>>>>>>>>>>>>>>>>>>>>>>> mapper')
            # print(mapper)
            graph1.edge_renderer.glyph.line_color = mapper #{'field': 'color'}
        else:
            graph1.edge_renderer.glyph.line_color = {'field': 'color'}
        
    # graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
        
    graph1.selection_policy = NodesAndLinkedEdges()
    # graph1.selection_policy = EdgesAndLinkedNodes()
    
    if len(y_axis_overrides) > 0:
        plotType1.yaxis.ticker = \
            FixedTicker(ticks=[i for i in range(0,len(y_axis_overrides))])
                                              # list(y_axis_overrides.values()))
        plotType1.yaxis.major_label_overrides = y_axis_overrides        
        
    if len(x_axis_overrides) > 0:
        plotType1.xaxis.ticker = \
            FixedTicker(ticks=[i for i in range(0,len(x_axis_overrides))])
                                              # list(y_axis_overrides.values()))
        plotType1.xaxis.major_label_overrides = x_axis_overrides        
        
    plotType1.renderers.append(graph1)
    
    layout=graph1.layout_provider
    
    if addCentroid==True:
        centroidGraph = nx.DiGraph()
        centroidGraph.add_node('centroid')
        graph2=from_networkx(centroidGraph, xbaseLayout, scale=1, center=(0,0))
        graph2.node_renderer.glyph = Ellipse(height=0.1, width=0.05, 
                                             line_color='black',
                                             fill_color="brown")
        
        plotType1.renderers.append(graph2)
    
    if xuseLayout == True:
        layout.graph_layout=dict(xlayout.graph_layout)
        
    if xgravityAttribute != '':
        weighted_pos=nx.spring_layout(xGraph,weight=xgravityAttribute,pos=pos)
        slp=StaticLayoutProvider(graph_layout=weighted_pos)
        layout.graph_layout=dict(slp.graph_layout)
        
    if useEdgeWeight == True:
        graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
        print('useEdgeWeight está deprecado')
    
    if xedgeWidthAttribute != '':
        graph1.edge_renderer.glyph.line_width = {'field': xedgeWidthAttribute}
        
    # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - antes')
    # print(len(plotType1.renderers))
        
    if xkeyColorAttribute != '':
        keys,colors = FD_KeyAttributeColor(xGraph,xkeyColorAttribute,xnodeColor)
        # print(keys)
        # print(colors)
        # print(len(keys))
        rx=[-0.975 for i in range(0,len(keys))]
        # print(rx)
        ry=[1-0.05*(i+1) for i in range(0,len(keys))]
        # print(ry)
        tx=[-0.95 for i in range(0,len(keys))]
        ty=[ry[i]-0.005 for i in range(0,len(keys))]
        # print(tx)
        
        # imposedBokehGraph = \
        #     from_networkx(nx.Graph(), nx.spring_layout, scale=1, center=(0,0))
        # plotType1.renderers.append(imposedBokehGraph)
    
        plotType1.text(x=[-1], y=[1.025], text=xColorLegendTitle,\
            text_font_size="14px", text_align="left", text_baseline="middle")
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de legend')
        # print(len(plotType1.renderers))
        plotType1.rect(x=rx, y=ry,width=0.040, height=0.040,fill_color=colors)
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de cuadros')
        # print(len(plotType1.renderers))
        plotType1.text(x=tx, y=ty, text=list(keys), text_font_size="12px",
                        text_align="left", text_baseline="middle")
        # print('>>>>>>>>>>>>>>>>>> len(plotType1.renderers) - luego de deptos')
        # print(len(plotType1.renderers))
        
    return plotType1, graph1  


# FD_BipartiteGraph(assignedIssues,amplifier,'funcionario','proyecto')


#%% Network plot

'''
Devuelve un gráfico de red Bokeh.
Los parámetros de entrada: xGraph: red networkx
                                    - xtooltips: campos para el hover
                                    - xtitle: título
                                    - xbaseLayout: default layout
                                    - xlayout: layout alterno
                                    - xuseLayout: True, use xLayout;
                                                    False, use xbaseLayout
                                    - xnodeSize: el nombre del atributo en 
                                                    xGraph con el tamaño de los
                                                    nodos
                                    - xplotHeight: altura del plot                                    
'''
def UTBo_Network_MultiGlyphPlot(xGraph,xtooltips,xtitle,xbaseLayout,xlayout,
                         xuseLayout, xnodeSize, xnodeColor,xplotHeight,
                         xplotWidth,ximposedGraph,addCentroid=False,
                         colorBasedOnSize=True):
    random.seed(10000)
    
    plotType1 = Plot(plot_width=xplotWidth, plot_height=xplotHeight,
                     x_range=Range1d(-1.1, 1.1), y_range=Range1d(-1.1, 1.1))
    
    plotType1.title.text = xtitle
    
    graph1 = from_networkx(xGraph, xbaseLayout, scale=1, center=(0,0))
    #graph1 = from_networkx(xGraph, nx.spring_layout, scale=1, center=(0,0))
    
    plotType1.add_tools(PanTool(), BoxZoomTool(), ResetTool(),\
                        HoverTool(tooltips=xtooltips), TapTool(),\
                            BoxSelectTool())

    if colorBasedOnSize == True:
        node_sizes=[xGraph.nodes[node][xnodeSize] for node in xGraph.nodes]
        mapper = linear_cmap(field_name=xnodeSize, palette=Spectral4 ,
                             low=min(node_sizes),
                             high=max(node_sizes))
        graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=mapper)
    
    else:
        graph1.node_renderer.glyph = Circle(size=xnodeSize,fill_color=xnodeColor)
    
    graph1.node_renderer.selection_glyph = \
        Circle(size=15, fill_color=Spectral4[2])
    graph1.node_renderer.hover_glyph = Circle(size=15, fill_color=Spectral4[1])
    
    graph1.edge_renderer.glyph = MultiLine(line_alpha=0.4,line_width=0.4)
    graph1.edge_renderer.selection_glyph = \
        MultiLine(line_color=Spectral4[2], line_width=5)
    graph1.edge_renderer.hover_glyph = \
        MultiLine(line_color=Spectral4[1], line_width=5)
        
    graph1.edge_renderer.glyph.line_width = {'field': 'weight'}
        
    graph1.selection_policy = NodesAndLinkedEdges()
        
    plotType1.renderers.append(graph1)
    
    layout=graph1.layout_provider
    
    if addCentroid==True:
        centroidGraph = nx.DiGraph()
        centroidGraph.add_node('centroid')
        graph2=from_networkx(centroidGraph, xbaseLayout, scale=1, center=(0,0))
        graph2.node_renderer.glyph = Ellipse(height=0.1, width=0.05, 
                                             line_color='black',
                                             fill_color="brown")
        
        plotType1.renderers.append(graph2)
    
    if xuseLayout == True:
        layout.graph_layout=dict(xlayout.graph_layout)   
    
    graph2 = from_networkx(ximposedGraph, xbaseLayout, scale=1, center=(0,0))
    
    # graph2.node_renderer.glyph = Triangle(size=xnodeSize,fill_color='yellow')
    graph2.node_renderer.glyph = Scatter(marker='triangle',size=xnodeSize,
                                         fill_color='yellow')
    
    layout2 = graph2.layout_provider
    
    layout2.graph_layout=dict(layout.graph_layout)
    
    plotType1.renderers.append(graph2)
    
    return plotType1, graph1  

#%%
# def UT_Network_AddGlyph(xGraph,xtooltips,xtitle,xbaseLayout,xlayout,
#                          xuseLayout, xnodeSize, xnodeColor,xplotHeight,
#                          xplotWidth,ximposedGraph,addCentroid=False,
#                          colorBasedOnSize=True):

def UTBo_Network_FlushSelectedNodesGlyph(ximposedGraph):
    
    emptyNxGraph = nx.Graph()
    
    emptyBokehGraph = from_networkx(emptyNxGraph, nx.spring_layout,
                                    scale=1, center=(0,0))
    
    emptyNodes = emptyBokehGraph.node_renderer.data_source
    ximposedGraph.node_renderer.data_source.data = dict(emptyNodes.data)
    
    emptyEdges = emptyBokehGraph.edge_renderer.data_source
    ximposedGraph.edge_renderer.data_source.data = dict(emptyEdges.data)    
    
def UTBo_Network_AddSelectedNodesGraph(xplot,xBaseBokehGraph,ximposedNxGraph,xnodeSize):
    
    """
    Se usa para sobreponer graphs de redes. Es la forma de usar diferentes
        glyphs.
    Adiciona un graph (ximposedNxGraph) a un plot (xplot) que ya contiene 
        un bokeh graph (xBaseBokehGraph).
    ximposedNxGraph se convierte en imposedBokehGraph.
    El layout de imposedBokehGraph se toma del layout de xBaseBokehGraph. 
    
    
    """
    layout=xBaseBokehGraph.layout_provider
    
    # # layout.graph_layout=dict(layout.graph_layout)   
    
    imposedBokehGraph = \
        from_networkx(ximposedNxGraph, nx.spring_layout, 
                      scale=1, center=(0,0))
    
    imposedBokehGraph.node_renderer.glyph = Scatter(marker='triangle',size=xnodeSize,
                                                     fill_color='yellow')
    
    layout2 = imposedBokehGraph.layout_provider
    
    layout2.graph_layout=dict(layout.graph_layout)
    
    xplot.renderers.append(imposedBokehGraph)
    
    return imposedBokehGraph
    
def UTBo_Network_AddSelectedNodesGlyph(xplot,xBaseLayout,ximposedBokehGraph,
                                     ximposedNxGraph,xnodeSize):
    """
    Crea el contenido del graph superpuesto.
    
    Parameters
    ----------
    xplot : es el plot que aloja los graphs
    xBaseBokehGraph : es el bokeh graph de base contenido en el plot
    ximposedBokehGraph : es el bokeh graph superspuesto en el plot
    ximposedNxGraph : es el nxgraph con los nodos a añadir
    xnodeSize : tamaño del nodo

    Se toma el layout de xBaseBokehGraph
    
    """
    # layout=xBaseBokehGraph.layout_provider
    
    newimposedBokehGraph = \
        from_networkx(ximposedNxGraph, nx.spring_layout, scale=1, center=(0,0))
    
    newimposedBokehGraph.node_renderer.glyph = \
        Scatter(marker='triangle',size=xnodeSize,fill_color='yellow')
    
    nodes = newimposedBokehGraph.node_renderer.data_source
    ximposedBokehGraph.node_renderer.data_source.data = dict(nodes.data)
    
    edges = newimposedBokehGraph.edge_renderer.data_source
    ximposedBokehGraph.edge_renderer.data_source.data = dict(edges.data)
    
    layout2 = ximposedBokehGraph.layout_provider
    
    # layout2.graph_layout=dict(layout.graph_layout)
    layout2.graph_layout=dict(xBaseLayout.graph_layout)
    
    # xplot.renderers.append(imposedGraph)
    
    # return imposedGraph
    
# #%%

# def UTBo_GraphFromEdgesAndNodes(xedges,xnodes,xamplifier):
#     graph = nx.from_pandas_edgelist(xedges, 'source', 'target',
#                                         ['weight','color'],
#                                         create_using=nx.DiGraph)
        
#     for x in graph.nodes:
#         graph.add_nodes_from([(x, {'node_color':xnodes.loc[x]['color'],
#                                    'name':xnodes.loc[x]['name']})])
        
#     new_sizes = dict(map(lambda node: (node[0],node[1]*xamplifier),
#                          dict(graph.degree).items()))
#     new_sizes
#     nx.set_node_attributes(graph, new_sizes, 'node_size')
    
#     return graph

#%%


#Parece que no se usa porque tiene un error
# def UTBo_GraphToUpdateObjects(xtooltips,xsourceNxGraph,xtargetBokehGraph,
#                             xlayout,xuseLayout,xnodeSize,xcolorBasedOnSize):
    
#     """
#     Recibe  - tooltips
#             - nx graph (source)
#             - bokeh graph (target)
#             - layout y useLayoot (bool)
           
#     Genera un plot ficticio con el nx graph (target).
#     Despliega el plot ficticio en el bokeh graph (target).
#     Si useLayout = True, aplica layout al bokeh graph
    
#     Devuelve el layout del bokeh graph, que solo interesa a quien lo
#         llama cuando esta reemplazando totalmente el bokeh graph    
#     """
    
#     print('>>>>>>>>>>>>>>>>>>>> UtilitiesBokeh - UTBo_GraphToUpdateObjects se usa?')
    
#     _,graphFromSource = \
#         UT_Network_PlotType1(xsourceNxGraph,xtooltips,
#                                "Dummy title",
#                           nx.spring_layout,xlayout,xuseLayout,
#                           xnodeSize,'node_color',200,200,
#                           colorBasedOnSize=xcolorBasedOnSize)
        
#     renderer = graphFromSource.node_renderer.data_source
#     xtargetBokehGraph.node_renderer.data_source.data = dict(renderer.data)
    
#     renderer = graphFromSource.edge_renderer.data_source
#     xtargetBokehGraph.edge_renderer.data_source.data = dict(renderer.data)
    
#     layout=xtargetBokehGraph.layout_provider
    
#     if xuseLayout == True:
#         layout.graph_layout=dict(xlayout.graph_layout)
#     else:
#         layout.graph_layout=dict(graphFromSource.layout_provider.graph_layout)          

#     return graphFromSource.layout_provider

#%%

def UTBo_BokehGraphToNetworkxGraph(xbgraph, xDiGraph=True, _xedge_attr=True):
    
    """
    Converts bokeh graph object to networkx DiGraph
    """
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_BokehGraphToNetworkxGraph')
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_BokehGraphToNetworkxGraph')
    
    edges=xbgraph.edge_renderer.data_source
    edges_dict=dict(edges.data)
    edgesDF=pd.DataFrame(edges_dict)
    
    # print('>>>>>>>>>>>>>>>>>>>>>>> edgesDF (UTBo_BokehGraphToNetworkxGraph)')
    # print(edgesDF.to_dict('records'))
    
    nodes=xbgraph.node_renderer.data_source
    nodes_dict=dict(nodes.data)
    nodesDF=pd.DataFrame(nodes_dict)
    
    # print('>>>>>>>>>>>>>>>>>>>>>>> nodesDF (UTBo_BokehGraphToNetworkxGraph)')
    # print(nodesDF)   
    
    # a=5/0
    
    if edgesDF.empty:
        if xDiGraph == True:
            nxgraph = nx.DiGraph()
        else:
            nxgraph = nx.Graph()
        nxgraph.add_nodes_from([(node, {'attribute': attr}) \
                                for (node, attr) in nodes_dict.items()])        
    else:
        if xDiGraph == True:
            nxgraph= nx.from_pandas_edgelist(edgesDF, 'start', 'end', 
                                             _xedge_attr, nx.DiGraph())
        else:
            nxgraph= nx.from_pandas_edgelist(edgesDF, 'start', 'end', 
                                             _xedge_attr, nx.Graph())
        nx.set_node_attributes(nxgraph, nodesDF.set_index('index').to_dict('index'))        
    
    return nxgraph


#%%

# UTBo_NodePlot y UTBo_Plot_HorizontalBarAndBubble se trajeron de 
# oihub_CVF_Actor_item_ranking reemplzando los que están abajo comentados
# porque no salían los nombres de los nodos en el eje_y

def UTBo_Plot_HorizontalBarAndBubble(xsizesEndPoints,xtitle,xmaxXRange=1,
                                     xplotHeight1=400,xplotWidth1=350):
    """
    Produces a horizontal bar Bokeh Plot constructed with a networkx grahp.
    The bars are lines with bubbles at the end with sizes and colors related
    to its value.
    

    Parameters
    ----------
    xsizesEndPoints : dictionary, with bar label and value.
    xmaxXRange : numeric, optional, maximu valuein x axis. Default is 1.
    xtitle: string, plot title.

    Returns
    -------
    pvuplot1 : Bokeh plot, described above
    graph1: Bokeh graph object
    """
    
    print('.-.-.-.-.-.-.-.-.-oihub_CVF_Actor_item_ranking/UTBo_Plot_HorizontalBarAndBubble')
    # print('>>>>>>>>>>>>>>> xsizesEndPoints (UTBo_Plot_HorizontalBarAndBubble)')
    # print(xsizesEndPoints.to_dict('records'))
    
    métricaDF=pd.DataFrame(xsizesEndPoints, index=[0])
    # print('>>>>>>>>>>>>>>> métricaDF (UTBo_Plot_HorizontalBarAndBubble)')
    # print(métricaDF.to_dict('records'))
    
    métricas=[métrica for métrica in métricaDF.columns]
    # print('>>>>>>>>>>>>>>> métricas (UTBo_Plot_HorizontalBarAndBubble)')
    # print(métricas)
    
    start_nodes_indexes = [i+1 for i in range(len(métricas))]
    # print('>>>>>>>>>>>>>>> start_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
    # print(start_nodes_indexes)
    
    end_nodes_indexes = [i+1+len(métricas) for i in range(len(métricas))]
    # print('>>>>>>>>>>>>>>> end_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
    # print(end_nodes_indexes)
        
    # métricasInicio=[métrica+'Inicio' for métrica in métricaDF.columns]
    # print('>>>>>>>>>>>>>>> métricasInicio (UTBo_Plot_HorizontalBarAndBubble)')
    # print(métricasInicio)
        
    x_endPoints = métricaDF.loc[0, métricas].values.flatten().tolist()
    # print('>>>>>>>>>>>>>>> x_endPoints (UTBo_Plot_HorizontalBarAndBubble)')
    # print(x_endPoints)
    
    x_startPoints = [0 for i in range(0,len(métricas))]
    # print('>>>>>>>>>>>>>>> x_startPoints (UTBo_Plot_HorizontalBarAndBubble)')
    # print(x_startPoints)
    
    x_nodePositions = x_startPoints + x_endPoints
    # print('>>>>>>>>>>>>>>> x_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
    # print(x_nodePositions)
    
    y_nodePositions = [i+1 for i in range(0,len(métricas))]
    # print('>>>>>>>>>>>>>>> y_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
    # print(y_nodePositions)
    
    complete_y_nodePositions = y_nodePositions + y_nodePositions
    # print('>>>>>>>>>>>>>>> complete_y_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
    # print(complete_y_nodePositions)
    
    # métricasInicioYFin=métricasInicio+métricas
    # print('>>>>>>>>>>>>>>> métricasInicioYFin (UTBo_Plot_HorizontalBarAndBubble)')
    # print(métricasInicioYFin)
    
    start_end_nodes_indexes = start_nodes_indexes + end_nodes_indexes
    # print('>>>>>>>>>>>>>>> start_end_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
    # print(start_end_nodes_indexes)
    
    renames=pd.DataFrame(columns = y_nodePositions )
    
    renames.loc[0]=métricaDF.columns
    # print('>>>>>>>>>>>>>>> renames (UTBo_Plot_HorizontalBarAndBubble)')
    # print(renames)
    
    y_axis_overrides = renames.to_dict('records')[0]
    # print('>>>>>>>>>>>>>>> y_axis_overrides 1 (UTBo_Plot_HorizontalBarAndBubble)')
    # print(y_axis_overrides)
    
    y_axis_overrides_inverse = {v:k for k,v in y_axis_overrides.items()}
    indexed_sizesEndPoints = \
        {len(métricas)+y_axis_overrides_inverse.get(k):v \
         for k,v in xsizesEndPoints.items()}
    # print('>>>>>>>>>>>>>>> indexed_sizesEndPoints (UTBo_Plot_HorizontalBarAndBubble)')
    # print(indexed_sizesEndPoints)
    
    
    y_axis_overrides[0] = ''
    # print('>>>>>>>>>>>>>>> y_axis_overrides 2 (UTBo_Plot_HorizontalBarAndBubble)')
    # print(y_axis_overrides)
    # y_axis_overrides[len(y_axis_overrides)] = ''
    # print('>>>>>>>>>>>>>>> y_axis_overrides 3 (UTBo_Plot_HorizontalBarAndBubble)')
    # print(y_axis_overrides)
    
    # graph_layout = dict(zip(métricasInicioYFin, zip(x_nodePositions,
    #                                               complete_y_nodePositions)))
    graph_layout = dict(zip(start_end_nodes_indexes, zip(x_nodePositions,
                                                  complete_y_nodePositions)))
    # print('>>>>>>>>>>>>>>> graph_layout (UTBo_Plot_HorizontalBarAndBubble)')
    # print(graph_layout)
    
    slp=StaticLayoutProvider(graph_layout=graph_layout)
    
    # edges = pd.DataFrame(
    #         {
    #             "source": métricasInicio,
    #             "target": métricas
    #         }
    #     )
    edges = pd.DataFrame(
            {
                "source": start_nodes_indexes,
                "target": end_nodes_indexes
            }
        )
    # print('>>>>>>>>>>>>>>> edges (UTBo_Plot_HorizontalBarAndBubble)')
    # print(edges)
    
    
    
    # sizesInicio = pd.DataFrame(columns=métricasInicio)
    # sizesInicio.loc[0] = [0] * len(métricasInicio)
    sizesInicio = pd.DataFrame(columns = start_nodes_indexes)
    sizesInicio.loc[0] = [0] * len(start_nodes_indexes)
    # print('>>>>>>>>>>>>>>> sizesInicio (UTBo_Plot_HorizontalBarAndBubble)')
    # print(sizesInicio)
    
    sizesStartPoints = sizesInicio.to_dict('records')[0]
    # print('>>>>>>>>>>>>>>> sizesStartPoints (UTBo_Plot_HorizontalBarAndBubble)')
    # print(sizesStartPoints)
    
    # sizes = {**sizesStartPoints, **xsizesEndPoints}
    sizes = {**sizesStartPoints, **indexed_sizesEndPoints}
    # print('>>>>>>>>>>>>>>> sizes (UTBo_Plot_HorizontalBarAndBubble)')
    # print(sizes)
    
    G = nx.from_pandas_edgelist(edges, 'source', 'target')
    
    nx.set_node_attributes(G, sizes, 'metric')
    sizes.update((x, y*20) for x, y in sizes.items())
    # print('>>>>>>>>>>>>>>> sizes updated (UTBo_Plot_HorizontalBarAndBubble)')
    # print(sizes)
    nx.set_node_attributes(G, sizes, 'node_size')
    nx.set_node_attributes(G, y_axis_overrides, 'name')
    # print('>>>>>>>>>>>>>>> G.nodes (UTBo_Plot_HorizontalBarAndBubble)')
    # print(G.nodes(data=True))
    # print('>>>>>>>>>>>>>>> G.edges (UTBo_Plot_HorizontalBarAndBubble)')
    # print(G.edges(data=True))
    
        
    tooltipsProject=[("index", "@index"),("métrica", "@metric")]
    # pvuplot1, graph1 = \
    #     UTBo_Network_PlotType1(G,tooltipsProject,xtitle,
    #                       nx.spring_layout,slp,True, #nx.spring_layout,False,
    #                       'node_size','node_color',xplotHeight1,xplotWidth1,
    #                       colorBasedOnSize=True,
    #                       x_range=Range1d(0,xmaxXRange),
    #                       y_range=(0,1+len(y_nodePositions)),
    #                       y_axis_overrides = y_axis_overrides,
    #                       xadjustNodeSize = True, xapplyToSizeZero=False,
    #                       xadjustOnlyMinimum=True,xminimumNodeSize=2)
    
    pvuplot1, graph1 = \
        UTBo_Network_PlotType2(G,tooltipsProject,xtitle,
                               nx.spring_layout,slp,True,
                               xplotHeight1,xplotWidth1,
                               xnodeSize='node_size',
                               xcolorBasedOnSize=True,
                               xx_range=(0,xmaxXRange),
                               xy_range=(0,1+len(y_nodePositions)),
                               y_axis_overrides = y_axis_overrides,
                               xadjustNodeSize = True, xapplyToSizeZero=False,
                               xadjustOnlyMinimum=True,xminimumNodeSize=2,
                               xvisible_axis = True)
                               
   
    return pvuplot1, graph1


def UTBo_NodePlot(xnodeDF, xmetric, xselectedCount,
                  xnode_name = 'node', xdivisor = 1,
                  xtop = True):

    print('.-.-.-.-.-.-.-.-.-.- oihib_CVF_Actor_itm_ranking/UTBo_NodePlot')
    print('>>>>>>>>>>>>>>>xnodeDF (UTBo_NodePlot)')
    print(xnodeDF)
    print(xnodeDF.shape)
    print(xnodeDF.columns)
    print('>>>>>>>>>>>>>>> xmetric (UTBo_NodePlot)')
    print(xmetric)
    print('>>>>>>>>>>>>>>>xnodeDF[["node",xmetric]] (UTBo_NodePlot)')
    print(xnodeDF[[xnode_name, xmetric]])
    _nodeDF = xnodeDF.copy(deep=True)
    _nodeDF[xmetric] = _nodeDF[xmetric] / xdivisor
    nodeDFSelected = _nodeDF[[xnode_name, xmetric]]  # .set_index('node')
    if xtop == True:
        nodeDFSelected = nodeDFSelected.sort_values(
            xmetric, ascending=True).tail(xselectedCount)
    else:
        nodeDFSelected = nodeDFSelected.sort_values(
            xmetric, ascending=True).head(xselectedCount)
        
    selectedNodesMetricDict = \
        nodeDFSelected.set_index(xnode_name).to_dict().get(xmetric)
    print('>>>>>>>>>>>>>>> selectedNodesMetricDict (UTBo_NodePlot)')
    print(selectedNodesMetricDict)
    
    # return selectedNodesMetricDict
    
    selectedNodesPlot, selectedNodesGraph = \
        UTBo_Plot_HorizontalBarAndBubble(selectedNodesMetricDict, xmetric)

    return selectedNodesPlot, selectedNodesGraph

# UTBo_NodePlot y UTBo_Plot_HorizontalBarAndBubble se reemplazaron por los
# que están arriba, que vienen de oihub_CVF_Actor_item_ranking porque no 
# salían los nombres de los nodos en el eje_y
# def UTBo_Plot_HorizontalBarAndBubble(xsizesEndPoints,xtitle,xmaxXRange=1,
#                                      xplotHeight1=400,xplotWidth1=400,
#                                      xy_override_dict={}):
#     """
#     Produces a horizontal bar Bokeh Plot constructed with a networkx grahp.
#     The bars are lines wiyh bubbles at the end with sizes and colors related
#     to its value.
    

#     Parameters
#     ----------
#     xsizesEndPoints : dictionary, with bar label and value.
#     xtitle: string, plot title.
#     xmaxXRange : numeric, optional, maximu valuein x axis. Default is 1.
#     xplotHeight1 and xplotWidth1
#     xy_override_dict : dictionary to relabel y axis (key is node label,
#                                                      value is new label)
    
#     Returns
#     -------
#     pvuplot1 : Bokeh plot, described above
#     graph1: Bokeh graph object
#     """
    
#     print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-. UTBo_Plot_HorizontalBarAndBubble')
#     # print('>>>>>>>>>>>>>> xsizesEndPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(xsizesEndPoints)
#     # print('>>>>>>>>>>>>>> xmaxXRange (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(xmaxXRange)
    
#     #métricaDF: dataframe with:
#     #           - 1 row with metric's values
#     #           - 1 column per node. Columnname is node label.
#     métricaDF=pd.DataFrame(xsizesEndPoints, index=[0])
#     # print('>>>>>>>>>>>>>>>>>>>> métricaDF (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(métricaDF.columns)
#     # print(métricaDF.shape)
#     # print(métricaDF)
    
#     node_labels = [node_label for node_label in métricaDF.columns]
#     print('>>>>>>>>>>>>>>>>>>>> node_labels (UTBo_Plot_HorizontalBarAndBubble)')
#     print(node_labels)
    
#     # métricasInicio=[métrica_str+'Inicio' for métrica_str in métricas_str]
#     node_labels_inicio=[-1*node_label for node_label in node_labels]
#     print('>>>>>>>>>>>>>>>node_labels_inicio (UTBo_Plot_HorizontalBarAndBubble)')
#     print(node_labels_inicio)
        
#     x_endPoints = métricaDF.loc[0, node_labels].values.flatten().tolist()
#     # print('>>>>>>>>>>>>>>> x_endPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(x_endPoints)
    
#     x_startPoints = [0 for i in range(0,len(node_labels))]
#     # print('>>>>>>>>>>>>>>> x_startPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(x_startPoints)
    
#     x_nodePositions = x_startPoints + x_endPoints
#     # print('>>>>>>>>>>>>>>> x_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(x_nodePositions)
    
#     y_nodePositions = [i+1 for i in range(0,len(node_labels))]
#     complete_y_nodePositions = y_nodePositions + y_nodePositions
#     # print('>>>>> complete_y_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(complete_y_nodePositions)
    
#     node_labels_inicio_y_fin = node_labels_inicio + node_labels
    
#     renames=pd.DataFrame(columns = y_nodePositions )
#     print('>>>>>>>>>> renames (UTBo_Plot_HorizontalBarAndBubble)')
#     print(renames)
    
#     if len(xy_override_dict) == 0:
#         renames.loc[0] = [str(column) for column in métricaDF.columns]
#     else:
#         renames.loc[0] = \
#             [str(xy_override_dict.get(column)) for column in métricaDF.columns]
#     print('>>>>>>>>>> renames (UTBo_Plot_HorizontalBarAndBubble)')
#     print(renames)
    
#     y_axis_overrides = renames.to_dict('records')[0]
    
#     y_axis_overrides[0] = ''
    
#     y_axis_overrides[len(y_axis_overrides)] = ''
#     print('>>>>>>>>>> y_axis_overrides (UTBo_Plot_HorizontalBarAndBubble)')
#     print(y_axis_overrides)
    
#     graph_layout = dict(zip(node_labels_inicio_y_fin, 
#                             zip(x_nodePositions, complete_y_nodePositions)))
#     print('>>>>>>>>>>>>>> graph_layout (UTBo_Plot_HorizontalBarAndBubble)')
#     print(graph_layout)
    
#     slp=StaticLayoutProvider(graph_layout=graph_layout)
    
#     edges = pd.DataFrame(
#             {
#                 "source": node_labels_inicio,
#                 "target": node_labels
#             }
#         )
    
#     sizesInicio = pd.DataFrame(columns = node_labels_inicio)
#     sizesInicio.loc[0] = [0] * len(node_labels_inicio)
    
#     sizesStartPoints=sizesInicio.to_dict('records')[0]
    
#     sizes = {**sizesStartPoints, **xsizesEndPoints}
    
#     G = nx.from_pandas_edgelist(edges, 'source', 'target')
    
#     nx.set_node_attributes(G, sizes, 'metric')
#     sizes.update((x, y*20) for x, y in sizes.items())
#     nx.set_node_attributes(G, sizes, 'node_size')
        
#     tooltipsProject=[("index", "@index"),("métrica", "@metric")]
    
#     pvuplot1,graph1 = \
#         UTBo_Network_PlotType2(G,tooltipsProject,xtitle,
#                                nx.circular_layout, slp, True,
#                                xplotHeight1,xplotWidth1,
#                                xnodeSize='node_size',
#                                xcolorBasedOnSize = True,
#                                xx_range=Range1d(0,xmaxXRange),
#                                xy_range=(0,1+len(y_nodePositions)),
#                                y_axis_overrides=y_axis_overrides,
#                                xminimumNodeSize=2,
#                                xadjustNodeSize=True,
#                                xapplyToSizeZero=False,
#                                xadjustOnlyMinimum = True)
        
        
#     return pvuplot1, graph1


# def UTBo_NodePlot(xnodeDF, xmetric, xselectedCount,
#                   label_column = ''):
    
#     """
#     Creates a horizontal bar and bubble plot, defining the parameteres and
#     calling UTBo_Plot_HorizontalBarAndBubble.
#     Input:  xnodeDF: -  dataframe with one record per node and columns,
#                         one of which is xmetric
#             xmetric: columns containing metric
#             xselectedCount: number of items to display
#             xlabel_column: column in xnodeDF to be displayed as identifier
#                             in the plot       
#     """

#     print('.-.-.-.-.-.-.-.-.-.- UTBo_NodePlot')
#     print('>>>>>>>>>>>>>>>xmetric (UTBo_NodePlot)')
#     print(xmetric)
#     print('>>>>>>>>>>>>>>>xnodeDF.columns (UTBo_NodePlot)')
#     print(xnodeDF.columns)
#     print('>>>>>>>>>>>>>>>xnodeDF[["node",xmetric]] (UTBo_NodePlot)')
#     print(xnodeDF[['node',xmetric]])
    
#     if (label_column != '') & (label_column != 'node'):
#         y_list_dict = \
#             xnodeDF.groupby(['node'])[label_column].apply(list).to_dict()
#         y_override_dict = {k:v[0] for k,v in y_list_dict.items()}
#     else:
#         y_override_dict = {}
#     print('>>>>>>>>>>>>>>> y_override_dict (UTBo_NodePlot)')
#     print(y_override_dict)
    
#     nodeDFSelected = xnodeDF[['node', xmetric]]  # .set_index('node')
#     nodeDFSelected = nodeDFSelected.sort_values(
#         xmetric, ascending=True).tail(xselectedCount)
#     selectedNodesMetricDict = \
#         nodeDFSelected.set_index('node').to_dict().get(xmetric)
#     print('>>>>>>>>>>>>>>> selectedNodesMetricDict (UTBo_NodePlot)')
#     print(selectedNodesMetricDict)
#     selectedNodesPlot, selectedNodesGraph = \
#         UTBo_Plot_HorizontalBarAndBubble(selectedNodesMetricDict, xmetric,
#                                          xy_override_dict = y_override_dict)

#     return selectedNodesPlot, selectedNodesGraph

#%%
#%% Palettes utilities

def UTBo_Create_mapped_palette(xoriginPalette, xoriginPaletteLength,
                             xstartColorIndex, xnumberOfIndexes):
    
    print('.-.-.-.-.-.-.-.-. oihub_UtilitiesBokeh/UTBo_Create_mapped_palette')
    _palette = list(
        reversed(list(all_palettes[xoriginPalette][xoriginPaletteLength])))

    _colorsToUse = xoriginPaletteLength - xstartColorIndex

    if xnumberOfIndexes == 1:
        _palette = [_palette[int(xstartColorIndex+(_colorsToUse/2))]]
    elif xnumberOfIndexes == 2:
        _interval = int(_colorsToUse/4)
        _colorIndexes = [xstartColorIndex+_interval,
                         xstartColorIndex+(3*_interval)]
        _palette = [_palette[colorIndex] for colorIndex in _colorIndexes]
    elif xnumberOfIndexes == 3:
        _interval = int(_colorsToUse/4)
        _colorIndexes = [xstartColorIndex+_interval,
                         xstartColorIndex+(2*_interval),
                         xstartColorIndex+(3*_interval)]
        _palette = [_palette[colorIndex] for colorIndex in _colorIndexes]
    else:

        _interval = _colorsToUse // (xnumberOfIndexes - 1)

        _colorIndexes = [i*_interval for i in range(0, xnumberOfIndexes-2)]
        _lastInterval = _colorsToUse-max(_colorIndexes)
        _colorIndexes1 = \
            _colorIndexes+[max(_colorIndexes) +
                           (_lastInterval // 2), _colorsToUse-1]
        _colorIndexes2 = [_colorIndexes1[colorIndex]
                          for colorIndex in range(0, len(_colorIndexes1))]

        _palette = [_palette[colorIndex] for colorIndex in _colorIndexes2]

    return _palette


def UTBo_Create_proportional_palette(xvalues_to_map, 
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


#%%

def UTBo_DataFrame_to_DataTable(x_data_frame, xwidth=200, xheight=200):
    
    column_data_source = ColumnDataSource(x_data_frame)
    
    columnsDT = [TableColumn(field=Ci, title=Ci) \
                 for Ci in x_data_frame.columns]

    data_table_from_data_frame = \
        DataTable(source = column_data_source, 
                  columns = columnsDT, 
                  width = xwidth, height = xheight)
        
    return data_table_from_data_frame
    

def UTBo_nx_nodes_to_DataTable(xgraph, xattributes = [], xnode_name='',
                               xinclude_node_name = False,
                               xwidth = 200, xheight = 200):
    
    """
    Converts nodes of an nx_graph to a DataTable
    Input:  - nx graph
            - xattributes: if empty all attributes are included in
                            DataTable
            - xnode_name: optional name for node name column. If empty
                            'Nodes' will appear as node name.
            - xinclude_node_name: if False, exclude node name from DataTable            
    Output: - DataTable
    """
    # print('.-.-.-.-.-.-.-.-.-.- UTBo_nx_to_DataTable')
    # print('>>>>>>>>>>>>>>>>> xattributes (UTBo_nx_to_DataTable)')
    # print(xattributes)    
    
    nodes_and_attributes = \
        [(x,y) for x,y in xgraph.nodes(data=True)]
            
    # print('>>>>>>>>>>>>>>>>>nodes_and_attributes (UTBo_nx_to_DataTable)')
    # print(nodes_and_attributes)    
    
    nodes, attributes = zip(*nodes_and_attributes)
    # print('>>>>>>>>>>>>>>>>nodes (UTBo_nx_to_DataTable)')
    # print(nodes)
    # print('>>>>>>>>>>>>>>>attributes (UTBo_nx_to_DataTable)')
    # print(attributes)
    
    if xnode_name == '':
        nodes_df = pd.DataFrame({'Nodes': nodes})
    else:
        nodes_df = pd.DataFrame({xnode_name: nodes})
    # print('>>>>>>>>>>>>>>>>nodes_df (UTBo_nx_to_DataTable)')
    # print(nodes_df)
        
    attributes_df = pd.DataFrame(attributes)
    # print('>>>>>>>>>>>>>>>attributes_df (UTBo_nx_to_DataTable)')
    # print(attributes_df)
    # print(attributes_df.to_dict('records'))
    
    if xattributes != []:    
        attributes_df = attributes_df[xattributes]
    
    if xinclude_node_name == True:
        nodes_and_attributes_df = pd.concat([nodes_df.reset_index(drop=True),
                                             attributes_df], axis=1)
    else:
        nodes_and_attributes_df = attributes_df
        
    # print('>>>>>>>>>>>>>>>>>nodes_and_attributes_df (UTBo_nx_to_DataTable)')
    # print(nodes_and_attributes_df)
    # print(nodes_and_attributes_df.columns)
    
    data_table_from_graph = \
        UTBo_DataFrame_to_DataTable(nodes_and_attributes_df,
                                    xwidth = xwidth, xheight = xheight)    
    
    # nodes_and_attributes_CDS = ColumnDataSource(nodes_and_attributes_df)
    
    # columnsDT = \
    #     [TableColumn(field=Ci, title=Ci) \
    #      for Ci in nodes_and_attributes_df.columns]

    # data_table_from_graph = \
    #     DataTable(source = nodes_and_attributes_CDS, 
    #               columns = columnsDT, 
    #               width = xwidth, height = xheight)
        
    return data_table_from_graph

#%%
#%% Heatmap

def UTBo_component_contents(xcell_frequencies, 
                               xdimension_x_length, xdimension_y_length, 
                               xcontent_is_str = False,                               
                               xtotal_cells = False, xstart_x_index = 0, 
                               xstart_y_index = 0):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_contents')
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-UTBo_component_contents')
    print('.-.-.-.-.-.-.-.-.-.-.-oihub_UtilitiesBokeh/UTBo_component_contents')
    # print('>>>>>>>>> xdimension_x_length (UTBo_component_contents)')
    # print(xdimension_x_length)
    # print('>>>>>>>>> xdimension_y_length (UTBo_component_contents)')
    # print(xdimension_y_length)
    
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
    print('>>>>>>>>> content_tuples (UTBo_component_contents)')
    print(content_tuples)    
        
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


def UTBo_Component_hm(xdimension_x_dict, xdimension_y_dict,
                      xcell_contents, xtitle,
                      xtotal_cells = False, xtotal_cells_label = '',
                      xcontent_is_str = False,
                      xstart_x_index = 0, xstart_y_index = 0,
                      xlabel_x_axis = '', xlabel_y_axis = '',
                      xwidth=400, xheight=400,
                      xreverse_content = False,
                      xsingle_color = 'lightblue',
                      xx_offset = -400, xy_offset = -25):
    
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
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.- oihub_UtilitiesBokeh/UTBo_Component_hm')
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.- UTBo_Component_hm')
    print('>>>>>>>>>>>>>>>>>> xtitle (UTBo_Component_hm)')
    print(xtitle)
    print('>>>>>>>>>>>>>>>>>> xdimension_x_dict (UTBo_Component_hm)')
    print(xdimension_x_dict)
    print('>>>>>>>>>>>>>>>>>> xdimension_y_dict (UTBo_Component_hm)')
    print(xdimension_y_dict)
    print('>>>>>>>>> xcell_contents (UTBo_Component_hm)')
    print(xcell_contents.to_dict('records'))
    print('>>>>>>>>> xtotal_cells (UTBo_Component_hm)')
    print(xtotal_cells)
    
    dimension_x_list = [v for _,v in xdimension_x_dict.items()]
    print('>>>>>>>>>>>>>>>>>> dimension_x_list (UTBo_Component_hm)')
    print(dimension_x_list)
    
    dimension_y_list = [v for _,v in xdimension_y_dict.items()]
    print('>>>>>>>>>>>>>>>>>> dimension_y_list (UTBo_Component_hm)')
    print(dimension_y_list)
    
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
    
    print('>>>>>>>>>>>>>>>>>> x_lists (UTBo_Component_hm)')
    print(x_lists)
    print('>>>>>>>>>>>>>>>>>> y_lists (UTBo_Component_hm)')
    print(y_lists)
    
    x = reduce(lambda a, b: a + b, x_lists)
    y = reduce(lambda a, b: a + b, y_lists)
    print('>>>>>>>>>>>>>>>>>> x (UTBo_Component_hm)')
    print(x)
    print(len(x))
    print('>>>>>>>>>>>>>>>>>> y (UTBo_Component_hm)')
    print(y)
    print(len(y))
    
    factors_x = [dimension_x_list[i] for i in range(0,dimension_x_length)]
    factors_y = [dimension_y_list[i] for i in range(0,dimension_y_length)]
    if xtotal_cells == True:
        factors_x = [xtotal_cells_label] + factors_x
        factors_y = [xtotal_cells_label] + factors_y
    print('>>>>>>>>>>>>>>>>>> factors_x (UTBo_Component_hm)')
    print(factors_x)
    print('>>>>>>>>>>>>>>>>>> factors_y (UTBo_Component_hm)')
    print(factors_y)
        
    
    if xcontent_is_str == False:
        contents = \
            [int(frequency) for frequency in \
             UTBo_component_contents(xcell_contents, 
                                    dimension_x_length,
                                    dimension_y_length,
                                    xtotal_cells= xtotal_cells,
                                    xcontent_is_str = xcontent_is_str,
                                    xstart_x_index = xstart_x_index, 
                                    xstart_y_index = xstart_y_index)]
        colors = UTBo_Create_proportional_palette(contents, 'Greens', 256, 0)
        contents_str = [str(content) if content > 0 else '' \
                        for content in contents]
    else:
        contents = \
             UTBo_component_contents(xcell_contents, 
                                        dimension_x_length,
                                        dimension_y_length,
                                        xtotal_cells= xtotal_cells,
                                        xcontent_is_str = xcontent_is_str,
                                        xstart_x_index = xstart_x_index, 
                                        xstart_y_index = xstart_y_index)
        colors = [xsingle_color] * len(x)
        contents_str = [content for content in contents]
    
    print('>>>>>>>>>>>>>>>>>> contents (UTBo_Component_hm)')
    print(contents)
    print('>>>>>>>>>>>>>>>>>> colors (UTBo_Component_hm)')
    print(colors)
    print('>>>>>>>>>>>>>>>>>> contents_str (UTBo_Component_hm)')
    print(contents_str)
    
    _tools=['tap']
    
    source_dict = {'x': x,
                   'y': y,
                   'fill_colors': colors,
                   'frequencies': contents_str}
    print('>>>>>>>>>>>>>>>>>> source_dict (UTBo_Component_hm)')
    print(source_dict)
    source_df = pd.DataFrame.from_dict(source_dict)
    print('>>>>>>>>>>>>>>>>>> source_df (UTBo_Component_hm)')
    print(source_df)
    
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
        text_align='left',
        x_offset = xx_offset,
        y_offset= xy_offset,
        source=source,
        text_color = 'black'
    )
    
    # a=5/0
    
# render_mode='css',
# y_offset=-7,

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


def UTBo_update_plot(xplot, iplot, arrows = False):
    
    """
    Updates a network plot
        - xplot is the original plot that will be updated
        - iplot is the newly calculated plot
    """
    
    xg = xplot.renderers[0]
    idata_source = iplot.renderers[0].node_renderer.data_source
    xg.node_renderer.data_source.data = dict(idata_source.data)
    # iglyph = iplot.renderers[0].node_renderer.glyph
    # xg.node_renderer.glyph.fill_color = iglyph.fill_color
    
    i_edge_data_source = iplot.renderers[0].edge_renderer.data_source
    xg.edge_renderer.data_source.data = dict(i_edge_data_source.data)
    
    if arrows == True:
        xg_arrow =xplot.renderers[1]
        iarrow_data_source = iplot.renderers[1].node_renderer.data_source
        xg_arrow.node_renderer.data_source.data = dict(iarrow_data_source.data)
        
    xg_layout_provider = xg.layout_provider
    
    xg_layout_provider.graph_layout = \
        dict(iplot.renderers[0].layout_provider.graph_layout)
    




