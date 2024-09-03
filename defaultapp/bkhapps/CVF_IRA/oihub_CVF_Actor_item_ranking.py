# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 22:11:52 2023

@author: luis.caro
"""

import pandas as pd
import networkx as nx

# from neo4j_learn_ONA import conn, insert_data

from bokeh.layouts import row, column
from bokeh.io import curdoc

from bokeh.models import StaticLayoutProvider, Range1d

from bokeh.models.widgets import RadioGroup, Select

from bokeh.plotting import figure, output_file, show

from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_NodePlot
from defaultapp.bkhapps.common.oihub_UtilitiesBokeh import UTBo_Network_PlotType2, UTBo_EmptyParagraph

from defaultapp.bkhapps.common.Utilities import FD_cut_name

#%% Temporal para tomar válidos - hay que arreglar GDB
# from sqlalchemy_pure_connection_cloud import session_scope
# from new_db_schema import CVF_Culture_input_form

# def temp_FD_valid_employees():
    
#     with session_scope() as session:
#         culture_input_forms = session.query(CVF_Culture_input_form).all()
    
#     culture_input_forms
    
#     culture_input_forms_tuples = [(cif.id, cif.id_employee, cif.id_cycle,
#                                    cif.id_culture_mode, cif.Is_concluded) \
#                                        for cif in culture_input_forms]
#     culture_input_forms_df = \
#         pd.DataFrame.from_records(culture_input_forms_tuples, 
#                                   columns=['id', 'id_employee',
#                                            'id_cycle', 'id_culture_mode',
#                                            'Is_concluded'])
    
#     # valid_employees = list(culture_input_forms_df.loc\
#     #                        [culture_input_forms_df.Is_concluded == True]\
#     #                            ['id_employee'])
#     valid_employees = list(culture_input_forms_df['id_employee'])

#     return valid_employees


#%%

def FD_fetch_theme_culture_GDB(xconn, xid_tema, xvalid_employees):
    
    print('.-.--.-.-.-.-.-.-.-.-.-.-.-.-. FD_fetch_theme_culture_GDB')
    
    query = """MATCH (e:Employee)<-[OF_EMPLOYEE]-
                (cif:Culture_input_form)<-[OF_CULTURE_FORM]-(r:Respuesta)-
                [RESPUESTA_DE]->(p:Pregunta)-[DE_TEMA]->
                (t:Tema{id_tema:$tema_id})
                MATCH (p)-[DE_CUADRANTE]->(c:Cuadrante)
                RETURN e.employee as employee, e.id_employee,
                r.id_respuesta AS id_question_response, 
                t.id_tema AS id_culture_mode_theme, 
                t.tema AS culture_mode_theme, 
                p.id_pregunta AS id_culture_mode_theme_question, 
                c.id_cuadrante AS id_culture_quadrant, 
                c.cuadrante AS culture_quadrant, 
                r.actual AS actual, 
                r.preferido AS preferido"""
          
    
    # query = """MATCH (e:Employee)
    #                     <-[CONTESTADA_POR]-(r:Respuesta)-
    #                     [RESPUESTA_DE]->(p:Pregunta),
    #                     (p:Pregunta)-[DE_TEMA]->(t:Tema{id_tema:$tema_id}),
    #                     (p:Pregunta)-[DE_CUADRANTE]->(c:Cuadrante) 
    #                     RETURN e.employee as employee, e.id_employee,
    #                     r.id_respuesta AS id_question_response,
    #                     t.id_tema AS id_culture_mode_theme,
    #                     t.tema AS culture_mode_theme,
    #                     p.id_pregunta AS id_culture_mode_theme_question, 
    #                     c.id_cuadrante AS id_culture_quadrant,
    #                     c.cuadrante AS culture_quadrant,
    #                     r.actual AS actual, r.preferido AS preferido
    #         """

    params = {'tema_id': xid_tema}

    result = xconn.query(query, parameters=params)

    theme_culture_df = pd.DataFrame([dict(_) for _ in result])
    
    theme_culture_df = \
        theme_culture_df.loc[theme_culture_df['e.id_employee'].\
                                isin(xvalid_employees)]
    
    print('theme_culture_df.to_dict("records")')
    print(theme_culture_df.to_dict('records'))
    print(theme_culture_df.shape)
    print(theme_culture_df.columns)
    
    theme_culture_df['employee'] =\
        theme_culture_df['employee'].apply(lambda x: FD_cut_name(x), axis=1)
    
    
    theme_culture = \
        theme_culture_df.pivot_table(index=['employee'],
                                     columns='culture_quadrant',
                                     values=['actual','preferido']).reset_index()
        
    theme_culture.columns = \
        [' '.join(col).strip() for col in theme_culture.columns.values]
    
    return theme_culture

# FD_fetch_theme_culture_GDB(1)

def FD_update_preferred_actual(xconn, xpreferred_actual_radio_group_active,
                               xtop_bottom_radio_group_active,
                               xculture_theme_select_value,
                               xtotal_culture_df, xculture_themes_dict,
                               xplots, xvalid_employees):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_update_preferred_actual')
    print('>>>>>>>>>>>>>>>>>>> xculture_theme_select_value (FD_update_preferred_actual)')
    print(xculture_theme_select_value)
    
    culture_theme_index = \
        xculture_themes_dict.get(xculture_theme_select_value)[0]
    print('>>>>>>>>>>>>>>>>>>> culture_theme_index (FD_update_preferred_actual)')
    print(culture_theme_index)
    
    if culture_theme_index != 0:
        ocdf = FD_fetch_theme_culture_GDB(xconn, culture_theme_index, 
                                          xvalid_employees)
        # print('ocdf.to_dict("records")')
        # print(ocdf.to_dict('records'))
        # print(ocdf.shape)
        # print(ocdf.columns)
        # print('xtotal_culture_df.to_dict("records")')
        # print(xtotal_culture_df.to_dict('records'))
        # print(xtotal_culture_df.shape)
        # print(xtotal_culture_df.columns)
        reference_culture_df = ocdf.copy(deep=True)
    else:
        reference_culture_df = xtotal_culture_df.copy(deep=True)
        
    
    _quadrants=['Control', 'Clan', 'Adhocracia', 'Mercado']
    _measures=['actual', 'preferido']

    _columns = [_measures[xpreferred_actual_radio_group_active]+' '+quadrant \
                for quadrant in _quadrants]
    
    if xtop_bottom_radio_group_active == 0:
        _top = True
    else:
        _top = False
        
    _plots = [UTBo_NodePlot(reference_culture_df, column, 20,
                           xnode_name = 'employee', xdivisor = 100, xtop = _top) \
             for column in _columns]
        
    for plot_index in range(0,4):
        xg1=xplots[plot_index][0].renderers[0]
        dsnrp1 = _plots[plot_index][0].renderers[0].node_renderer.data_source
        xg1.node_renderer.data_source.data = dict(dsnrp1.data)
        dsnrp1g = _plots[plot_index][0].renderers[0].node_renderer.glyph
        xg1.node_renderer.glyph.fill_color = dsnrp1g.fill_color
        
        dshrp1 = _plots[plot_index][0].renderers[0].edge_renderer.data_source
        xg1.edge_renderer.data_source.data = dict(dshrp1.data)
        
        yaxis_overrides = _plots[plot_index][0].yaxis.major_label_overrides
        xplots[plot_index][0].yaxis.major_label_overrides = yaxis_overrides
        
        layout_graph1_AA=xg1.layout_provider
        
        layout_graph1_AA.graph_layout = \
            dict(_plots[plot_index][0].renderers[0].layout_provider.graph_layout)
            
        xplots[plot_index][0].title.text = _columns[plot_index]
    
    return reference_culture_df


def FD_update_theme_select(xconn, xpreferred_actual_radio_group_active,
                               xtop_bottom_radio_group_active,
                               xculture_theme_select_value,
                               xtotal_culture_df, xculture_themes_dict,
                               xplots, xbox_plots, xquadrants,
                               xvalid_employees):
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.-. FD_update_theme_select')
    
    _reference_culture_df = \
        FD_update_preferred_actual(xconn, xpreferred_actual_radio_group_active,
                                   xtop_bottom_radio_group_active,
                                   xculture_theme_select_value,
                                   xtotal_culture_df, xculture_themes_dict,
                                   xplots, xvalid_employees)
    
    _box_plots = [FD_total_culture_box_plot(_reference_culture_df, quadrant)\
                 for quadrant in xquadrants]
    
    def udpate_theme_box_plot(xbox_plot, _box_plot):
        
        # print('.-.-.-.-.-.-.-.-.-.- udpate_theme_box_plot')
        
        for i in range(0,8):
            # print(i)
            renderer_i = xbox_plot.renderers[i] 
            updated_datasource = _box_plot.renderers[i].data_source
            
            # print(dict(updated_datasource.data))
            renderer_i.data_source.data = dict(updated_datasource.data)

    for box_plot_index in range(0,4):
        udpate_theme_box_plot(xbox_plots[box_plot_index],
                              _box_plots[box_plot_index])
    
    # xg1=xplots[plot_index][0].renderers[0]
    # dsnrp1 = _plots[plot_index][0].renderers[0].node_renderer.data_source
    # xg1.node_renderer.data_source.data = dict(dsnrp1.data)
    
    

def FD_horizontal_box_plot(xdata_df, xgrouping_column, xvalue_column,
                           xgroup_values = True,
                           _x_range = (0,100), _xheight = 200,
                           _xwidth = 200, xtitle = ""):
    
    # print('.-.-.-.-.-.-.-.-.-.-.-.-.-.- FD_horizontal_box_plot')
    # print('>>>>>>>>>>>>>>>>>>>>>> xgrouping_column (FD_horizontal_box_plot)')
    # print(xgrouping_column)
    # print('>>>>>>>>>>>>>>>>>>>>>> xvalue_column (FD_horizontal_box_plot)')
    # print(xvalue_column)
    
    # if xgrouping_column == '': 
        
    _data_df = xdata_df.copy(deep=True)
    if xgroup_values == False:
        if xgrouping_column == '':
            _data_df['single_group']='value'
            xgrouping_column = 'single_group'
        else:
            if xgrouping_column == xvalue_column:
                xgrouping_column = '_'+xgrouping_column
            _data_df[xgrouping_column] = xvalue_column
    
    # print('>>>>>>>>>>>>>>>>>>>>>> xgrouping_column 2 (FD_horizontal_box_plot)')
    # print(xgrouping_column)
    # print('>>>>>>>>>>>>>>>>>>>>>> xvalue_column 2 (FD_horizontal_box_plot)')
    # print(xvalue_column)
    
    _data_df = _data_df[[xgrouping_column,xvalue_column]]
    
    # print('>>>>>>>>>>>>>>>>>>>>>> _data_df (FD_horizontal_box_plot)')
    # print(_data_df)
    
    
    # find the quartiles and IQR for each category
    groups = _data_df.groupby(xgrouping_column)
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

# mat = {'Culture_quadrant':['Adhocracia','Clan','Mercado','Control','Mercado',
#                             'Control','Adhocracia','Clan','Adhocracia','Clan',
#                             'Control','Mercado','Mercado','Control','Adhocracia',
#                             'CCClan'],
#         'Value':[25,40,25,10,20,0,0,80,15,60,10,15,15,10,25,50]}

# # mat = {'Culture_quadrant':['Adhocracia','Mercado','Mercado','Control','Mercado',
# #                                   'Control','Adhocracia','Mercado','Adhocracia','Mercado',
# #                                   'Control','Mercado','Mercado','Control','Adhocracia',
# #                                   'Mercado'],
# #               'Value':[25,40,25,10,20,0,0,80,15,60,10,15,15,10,25,50]}

# # mat = {'Culture_quadrant':['Control','Control','Control','Control','Control',
# #                                   'Control','Control','Control','Control','Control',
# #                                   'Control','Control','Control','Control','Control',
# #                                   'Control'],
# #               'Value':[25,40,25,10,20,0,0,80,15,60,10,15,15,10,25,50]}

# mat_df = pd.DataFrame.from_dict(mat)
# mat_df

# p = FD_horizontal_box_plot(mat_df, 'Culture_quadrant', 'Value', 
#                            xgroup_values = False,
#                             _xheight = 150)

# show(p)


# UTBo_NodePlot y UTBo_Plot_HorizontalBarAndBubble se pasaron a 
# oibhub_UtilitiesBokeh
# def UTBo_Plot_HorizontalBarAndBubble(xsizesEndPoints,xtitle,xmaxXRange=1,
#                                       xplotHeight1=400,xplotWidth1=350):
#     """
#     Produces a horizontal bar Bokeh Plot constructed with a networkx grahp.
#     The bars are lines with bubbles at the end with sizes and colors related
#     to its value.
    

#     Parameters
#     ----------
#     xsizesEndPoints : dictionary, with bar label and value.
#     xmaxXRange : numeric, optional, maximu valuein x axis. Default is 1.
#     xtitle: string, plot title.

#     Returns
#     -------
#     pvuplot1 : Bokeh plot, described above
#     graph1: Bokeh graph object
#     """
    
#     print('.-.-.-.-.-.-.-.-.-oihub_CVF_Actor_item_ranking/UTBo_Plot_HorizontalBarAndBubble')
#     # print('>>>>>>>>>>>>>>> xsizesEndPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(xsizesEndPoints.to_dict('records'))
    
#     métricaDF=pd.DataFrame(xsizesEndPoints, index=[0])
#     print('>>>>>>>>>>>>>>> métricaDF (UTBo_Plot_HorizontalBarAndBubble)')
#     print(métricaDF.to_dict('records'))
    
#     métricas=[métrica for métrica in métricaDF.columns]
#     print('>>>>>>>>>>>>>>> métricas (UTBo_Plot_HorizontalBarAndBubble)')
#     print(métricas)
    
#     start_nodes_indexes = [i+1 for i in range(len(métricas))]
#     print('>>>>>>>>>>>>>>> start_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
#     print(start_nodes_indexes)
    
#     end_nodes_indexes = [i+1+len(métricas) for i in range(len(métricas))]
#     print('>>>>>>>>>>>>>>> end_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
#     print(end_nodes_indexes)
        
#     # métricasInicio=[métrica+'Inicio' for métrica in métricaDF.columns]
#     # print('>>>>>>>>>>>>>>> métricasInicio (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(métricasInicio)
        
#     x_endPoints = métricaDF.loc[0, métricas].values.flatten().tolist()
#     print('>>>>>>>>>>>>>>> x_endPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     print(x_endPoints)
    
#     x_startPoints = [0 for i in range(0,len(métricas))]
#     print('>>>>>>>>>>>>>>> x_startPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     print(x_startPoints)
    
#     x_nodePositions = x_startPoints + x_endPoints
#     print('>>>>>>>>>>>>>>> x_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
#     print(x_nodePositions)
    
#     y_nodePositions = [i+1 for i in range(0,len(métricas))]
#     print('>>>>>>>>>>>>>>> y_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
#     print(y_nodePositions)
    
#     complete_y_nodePositions = y_nodePositions + y_nodePositions
#     print('>>>>>>>>>>>>>>> complete_y_nodePositions (UTBo_Plot_HorizontalBarAndBubble)')
#     print(complete_y_nodePositions)
    
#     # métricasInicioYFin=métricasInicio+métricas
#     # print('>>>>>>>>>>>>>>> métricasInicioYFin (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(métricasInicioYFin)
    
#     start_end_nodes_indexes = start_nodes_indexes + end_nodes_indexes
#     print('>>>>>>>>>>>>>>> start_end_nodes_indexes (UTBo_Plot_HorizontalBarAndBubble)')
#     print(start_end_nodes_indexes)
    
#     renames=pd.DataFrame(columns = y_nodePositions )
    
#     renames.loc[0]=métricaDF.columns
#     print('>>>>>>>>>>>>>>> renames (UTBo_Plot_HorizontalBarAndBubble)')
#     print(renames)
    
#     y_axis_overrides = renames.to_dict('records')[0]
#     print('>>>>>>>>>>>>>>> y_axis_overrides 1 (UTBo_Plot_HorizontalBarAndBubble)')
#     print(y_axis_overrides)
    
#     y_axis_overrides_inverse = {v:k for k,v in y_axis_overrides.items()}
#     indexed_sizesEndPoints = \
#         {len(métricas)+y_axis_overrides_inverse.get(k):v \
#           for k,v in xsizesEndPoints.items()}
#     print('>>>>>>>>>>>>>>> indexed_sizesEndPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     print(indexed_sizesEndPoints)
    
    
#     y_axis_overrides[0] = ''
#     print('>>>>>>>>>>>>>>> y_axis_overrides 2 (UTBo_Plot_HorizontalBarAndBubble)')
#     print(y_axis_overrides)
#     # y_axis_overrides[len(y_axis_overrides)] = ''
#     # print('>>>>>>>>>>>>>>> y_axis_overrides 3 (UTBo_Plot_HorizontalBarAndBubble)')
#     # print(y_axis_overrides)
    
#     # graph_layout = dict(zip(métricasInicioYFin, zip(x_nodePositions,
#     #                                               complete_y_nodePositions)))
#     graph_layout = dict(zip(start_end_nodes_indexes, zip(x_nodePositions,
#                                                   complete_y_nodePositions)))
#     print('>>>>>>>>>>>>>>> graph_layout (UTBo_Plot_HorizontalBarAndBubble)')
#     print(graph_layout)
    
#     slp=StaticLayoutProvider(graph_layout=graph_layout)
    
#     # edges = pd.DataFrame(
#     #         {
#     #             "source": métricasInicio,
#     #             "target": métricas
#     #         }
#     #     )
#     edges = pd.DataFrame(
#             {
#                 "source": start_nodes_indexes,
#                 "target": end_nodes_indexes
#             }
#         )
#     print('>>>>>>>>>>>>>>> edges (UTBo_Plot_HorizontalBarAndBubble)')
#     print(edges)
    
    
    
#     # sizesInicio = pd.DataFrame(columns=métricasInicio)
#     # sizesInicio.loc[0] = [0] * len(métricasInicio)
#     sizesInicio = pd.DataFrame(columns = start_nodes_indexes)
#     sizesInicio.loc[0] = [0] * len(start_nodes_indexes)
#     print('>>>>>>>>>>>>>>> sizesInicio (UTBo_Plot_HorizontalBarAndBubble)')
#     print(sizesInicio)
    
#     sizesStartPoints = sizesInicio.to_dict('records')[0]
#     print('>>>>>>>>>>>>>>> sizesStartPoints (UTBo_Plot_HorizontalBarAndBubble)')
#     print(sizesStartPoints)
    
#     # sizes = {**sizesStartPoints, **xsizesEndPoints}
#     sizes = {**sizesStartPoints, **indexed_sizesEndPoints}
#     print('>>>>>>>>>>>>>>> sizes (UTBo_Plot_HorizontalBarAndBubble)')
#     print(sizes)
    
#     G = nx.from_pandas_edgelist(edges, 'source', 'target')
    
#     nx.set_node_attributes(G, sizes, 'metric')
#     sizes.update((x, y*20) for x, y in sizes.items())
#     print('>>>>>>>>>>>>>>> sizes updated (UTBo_Plot_HorizontalBarAndBubble)')
#     print(sizes)
#     nx.set_node_attributes(G, sizes, 'node_size')
#     nx.set_node_attributes(G, y_axis_overrides, 'name')
#     print('>>>>>>>>>>>>>>> G.nodes (UTBo_Plot_HorizontalBarAndBubble)')
#     print(G.nodes(data=True))
#     print('>>>>>>>>>>>>>>> G.edges (UTBo_Plot_HorizontalBarAndBubble)')
#     print(G.edges(data=True))
    
        
#     tooltipsProject=[("index", "@index"),("métrica", "@metric")]
#     # pvuplot1, graph1 = \
#     #     UTBo_Network_PlotType1(G,tooltipsProject,xtitle,
#     #                       nx.spring_layout,slp,True, #nx.spring_layout,False,
#     #                       'node_size','node_color',xplotHeight1,xplotWidth1,
#     #                       colorBasedOnSize=True,
#     #                       x_range=Range1d(0,xmaxXRange),
#     #                       y_range=(0,1+len(y_nodePositions)),
#     #                       y_axis_overrides = y_axis_overrides,
#     #                       xadjustNodeSize = True, xapplyToSizeZero=False,
#     #                       xadjustOnlyMinimum=True,xminimumNodeSize=2)
    
#     pvuplot1, graph1 = \
#         UTBo_Network_PlotType2(G,tooltipsProject,xtitle,
#                                 nx.spring_layout,slp,True,
#                                 xplotHeight1,xplotWidth1,
#                                 xnodeSize='node_size',
#                                 xcolorBasedOnSize=True,
#                                 xx_range=(0,xmaxXRange),
#                                 xy_range=(0,1+len(y_nodePositions)),
#                                 y_axis_overrides = y_axis_overrides,
#                                 xadjustNodeSize = True, xapplyToSizeZero=False,
#                                 xadjustOnlyMinimum=True,xminimumNodeSize=2)
                               
   
#     return pvuplot1, graph1


# def UTBo_NodePlot(xnodeDF, xmetric, xselectedCount,
#                   xnode_name = 'node', xdivisor = 1,
#                   xtop = True):

#     print('.-.-.-.-.-.-.-.-.-.- oihib_CVF_Actor_itm_ranking/UTBo_NodePlot')
#     print('>>>>>>>>>>>>>>>xnodeDF (UTBo_NodePlot)')
#     print(xnodeDF)
#     print(xnodeDF.shape)
#     print(xnodeDF.columns)
#     print('>>>>>>>>>>>>>>> xmetric (UTBo_NodePlot)')
#     print(xmetric)
#     print('>>>>>>>>>>>>>>>xnodeDF[["node",xmetric]] (UTBo_NodePlot)')
#     print(xnodeDF[[xnode_name, xmetric]])
#     _nodeDF = xnodeDF.copy(deep=True)
#     _nodeDF[xmetric] = _nodeDF[xmetric] / xdivisor
#     nodeDFSelected = _nodeDF[[xnode_name, xmetric]]  # .set_index('node')
#     if xtop == True:
#         nodeDFSelected = nodeDFSelected.sort_values(
#             xmetric, ascending=True).tail(xselectedCount)
#     else:
#         nodeDFSelected = nodeDFSelected.sort_values(
#             xmetric, ascending=True).head(xselectedCount)
        
#     selectedNodesMetricDict = \
#         nodeDFSelected.set_index(xnode_name).to_dict().get(xmetric)
#     print('>>>>>>>>>>>>>>> selectedNodesMetricDict (UTBo_NodePlot)')
#     print(selectedNodesMetricDict)
    
#     # return selectedNodesMetricDict
    
#     selectedNodesPlot, selectedNodesGraph = \
#         UTBo_Plot_HorizontalBarAndBubble(selectedNodesMetricDict, xmetric)

#     return selectedNodesPlot, selectedNodesGraph

test_dict = {'yenny.acosta': 0.0164, 'cristian.sarmiento': 0.0167, 
             'david.munoz': 0.0237, 'kevin.pineda': 0.0264, 
             'albeiro.sarmiento': 0.0277, 'karen.ruiz': 0.0288, 
             'lina.manrique': 0.0365, 'paola.florez': 0.0443, 
             'anyi.arevalo': 0.0478, 'william.bonilla': 0.0682, 
             'fredy.gonzalez': 0.082, 'diego.guzman': 0.0885, 
             'ximena.bonilla': 0.0937, 'jessica.jimenez': 0.1477, 
             'oscar.guzman': 0.2208}

def FD_fetch_total_culture_GDB(xconn, xvalid_employees):
    
    print('.-.-.-.-. (oihub_CVF_Actor_item_ranking/FD_fetch_total_culture_GDB')
    
    # query = """MATCH (e:Employee)-[p:PERCIBE_CULTURA_TOTAL]->(c:Cuadrante) 
    #             RETURN e.employee as employee, e.id_employee,
    #             p.actual as actual, 
    #             p.preferido as preferido, c.cuadrante as cuadrante
    #         """
    query = """MATCH (e:Employee)<-[OF_EMPLOYEE]-(cip:Culture_input_form)
                <-[OF_CULTURE_FORM]-(r:Respuesta)-[RESPUESTA_DE]
                ->(p:Pregunta)-[DE_CUADRANTE]->(c:Cuadrante) 
                RETURN e.employee as employee, e.id_employee, 
                    r.actual as actual, r.preferido as preferido, 
                    c.cuadrante as cuadrante"""
    
    result = xconn.query(query)

    total_culture_df_query = pd.DataFrame([dict(_) for _ in result])
    
    total_culture_df_valid = \
        total_culture_df_query.loc[total_culture_df_query['e.id_employee'].\
                                   isin(xvalid_employees)]
    
    total_culture_df_valid['employee'] =\
        total_culture_df_valid['employee'].apply(lambda x: FD_cut_name(x))
    
    
    total_culture_df_thin = total_culture_df_valid[['employee',
                                                    'cuadrante',
                                                    'actual',
                                                    'preferido']].\
        copy(deep=True)
    
    total_culture_df = \
        total_culture_df_thin.groupby(['employee', 'cuadrante'],
                                      as_index=False).mean()

    # total_culture = \
    #     (totals.pivot_table(index=['e.id_employee'],
    #                                   columns='c.cuadrante',
    #                                   values=['r.actual','r.preferido']).\
    #      reset_index())

    
    # total_culture_df = \
    #     total_culture_df.loc[total_culture_df['e.id_employee'].\
    #                             isin(xvalid_employees)]
    
    total_culture = \
        (total_culture_df.pivot_table(index=['employee'],
                                      columns='cuadrante',
                                      values=['actual','preferido']).\
         reset_index())
    
            
    total_culture.columns = \
        [' '.join(col).strip() for col in total_culture.columns.values]       
    
    return total_culture

def FD_total_culture_box_plot(xtotal_culture_df, xquadrant):
    
    _value_vars = ['actual '+xquadrant, 'preferido '+xquadrant]
    
    melted_total_culture_df = pd.melt(xtotal_culture_df, 
                                                    id_vars =['employee'],
                                                    value_vars = _value_vars)
    
    melted_total_culture_df['value'] = melted_total_culture_df['value'] / 100
    
    culture_box_plot = FD_horizontal_box_plot(melted_total_culture_df, 
                                              'variable', 'value', 
                                              xgroup_values = True, 
                                              _x_range = [0,1], _xheight = 100,
                                              _xwidth = 350)
    
    return culture_box_plot


def FD_fetch_culture_themes(xconn):
    query = """MATCH (t:Tema) RETURN t.id_tema as id_tema, t.tema as tema"""
    
    result = xconn.query(query)

    culture_themes_df = pd.DataFrame([dict(_) for _ in result])
    
    #Así estaba
    # culture_themes = pd.DataFrame({'id_tema':[0], 'tema':['Cultura total']}).\
    #     append(culture_themes_df)
        
    culture_themes = pd.DataFrame({'id_tema':[0], 'tema':['Cultura total']})
        
    culture_themes = pd.concat([culture_themes, culture_themes_df], 
                               ignore_index=True)
    
    return culture_themes   



# b=FD_fetch_total_culture_GDB()

# plot, _ = UTBo_Plot_HorizontalBarAndBubble(test_dict, 'aa')

def FD_Main_actor_item_ranking(xconn, xira_employees_areas):
    
    
    valid_employees = list(xira_employees_areas['id_employee'])
    print('.-.-.-.-.- oihub_CVF_Actor_item_ranking/FD_Main_actor_item_ranking')
    print('>>>>>>>>>>>>>>>> xvalid_employees (FD_Main_actor_item_ranking)')
    print(valid_employees)
    
    
    # valid_employees = temp_FD_valid_employees()
    # print('>>>>>>>>>>>>>>>> xvalid_employees (FD_Main_actor_item_ranking)')
    # print(valid_employees)
    

    quadrants=['Control', 'Clan', 'Adhocracia', 'Mercado']
    measures=['actual', 'preferido']
    
    measure_index = 1
    top = True
    culture_theme_index = 0
    
    if top == True:
        active_top_down = 0
    else:
        active_top_down = 1
    
    columns = [measures[measure_index]+' '+quadrant for quadrant in quadrants]
    
    # plot1, _ = UTBo_NodePlot(FD_fetch_total_culture_GDB(), 'actual Control', 20,
    #                         xnode_name = 'employee', xdivisor = 100)
    
    # plot2, _ = UTBo_NodePlot(FD_fetch_total_culture_GDB(), 'actual Adhocracia', 20,
    #                         xnode_name = 'employee', xdivisor = 100)
    
    total_culture_df = FD_fetch_total_culture_GDB(xconn, valid_employees)
    total_culture_df.columns
    
    culture_themes_df = FD_fetch_culture_themes(xconn)
    culture_themes_dict = culture_themes_df.set_index('tema').T.to_dict('list')
    
    # pd.melt(total_culture_df, id_vars =['employee'], 
    #         value_vars =['actual Adhocracia','preferido Adhocracia'])
    # pd.melt(total_culture_df, id_vars =['employee'], 
    #         value_vars = _value_vars)
    
    # print('>>>>>>>>>>>>>>>>>> total_culture_df (FD_Main_actor_item_ranking)')
    # print(total_culture_df)
    
    # a=5/0
    
    plots = [UTBo_NodePlot(total_culture_df, column, 20,
                           xnode_name = 'employee', xdivisor = 100, xtop = top) \
             for column in columns]
    
        
    # xquadrant = 'Adhocracia'    
    # _value_vars = ['actual '+xquadrant, 'preferido '+xquadrant]
    # _value_vars
    
    
    
    # p = FD_total_culture_box_plot(total_culture_df, 'Adhocracia')   
    
    # show(p)    
    # box_plots = [FD_horizontal_box_plot(total_culture_df, column, column, 
    #                                     xgroup_values = False, _x_range = [0,1], 
    #                                     _xheight = 100,
    #                                     _xwidth = 350)\
    #              for column in columns]
    box_plots = [FD_total_culture_box_plot(total_culture_df, quadrant)\
                 for quadrant in quadrants]
        
    culture_themes_list = list(culture_themes_df['tema'])
    print('>>>>>>>>>>>>>>> culture_themes_list')
    print(culture_themes_list)
    
    culture_theme_select = Select(title = "Tema cultural:", value="Cultura total", 
                                  options = culture_themes_list)
        
    LABELS = ["Actual","Preferido"]
    
    preferred_actual_radio_group = RadioGroup(labels=LABELS, active= measure_index)
    
    LABELS = ["Arriba","Abajo"]
    
    top_bottom_radio_group = RadioGroup(labels=LABELS, active= active_top_down)
    
    culture_theme_select.on_change("value", lambda attr, old, new: \
                                           FD_update_theme_select(xconn,
                                               preferred_actual_radio_group.active,
                                               top_bottom_radio_group.active,
                                               culture_theme_select.value,
                                               total_culture_df,
                                               culture_themes_dict,
                                               plots, box_plots, quadrants,
                                               valid_employees))
    
    preferred_actual_radio_group.on_change("active", lambda attr, old, new: \
                                           FD_update_preferred_actual(xconn,
                                               preferred_actual_radio_group.active,
                                               top_bottom_radio_group.active,
                                               culture_theme_select.value,
                                               total_culture_df,
                                               culture_themes_dict,
                                               plots, valid_employees))
    
    top_bottom_radio_group.on_change("active", lambda attr, old, new: \
                                           FD_update_preferred_actual(xconn,
                                               preferred_actual_radio_group.active,
                                               top_bottom_radio_group.active,
                                               culture_theme_select.value,
                                               total_culture_df,
                                               culture_themes_dict,
                                               plots, valid_employees))
        
    return preferred_actual_radio_group, top_bottom_radio_group, \
        culture_theme_select, plots, box_plots

