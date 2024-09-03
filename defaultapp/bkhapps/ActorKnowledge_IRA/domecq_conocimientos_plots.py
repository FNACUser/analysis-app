"""
Retorna un dashboard de bokeh sobre los datos del formulario Conocimientos
"""
import math
import numpy as np
import pandas as pd

from defaultapp.bkhapps.common.neo4j_learn_ONA import conn, insert_data
# from defaultapp.bkhapps.common.neo4j_connection_sandbox import conn, insert_data

from bokeh.io import curdoc
from bokeh.models import (ColumnDataSource, Select, DataCube, DataTable,
                            TableColumn, GroupingInfo, StringFormatter,
                            SumAggregator, Div, BasicTicker, PrintfTickFormatter,
                            MultiSelect, TabPanel, Tabs,
                            MultiChoice, ColorBar, Spacer,
                            # HTMLTemplateFormatter, DataTable,
                            # CustomJS,LinearAxis, NumeralTickFormatter,
                            )
from bokeh.palettes import Viridis256, RdYlGn, YlGn, GnBu, Pastel2
from bokeh.plotting import figure
from bokeh.layouts import column, row, gridplot
from bokeh.transform import linear_cmap
# from domecq_conocimientos_data import get_data_from_db
from .domecq_conocimientos_data_neo4j import get_data_from_db

question_order = [
    '¿Le gustaría conocer más de este tema?', '¿Cuál es su relación con este proceso?',
    '¿Cada cuánto lo usa?', '¿Cree que una mayor capacitación sobre éste seria beneficiosa?',
    '¿Esto afecta su trabajo?', '¿Esto afecta al cliente?',
    '¿Cree que una mayor capacitación sobre estos procesos y sus tiempos seria beneficiosa?',
    '¿Tiene acceso? ', '¿Lo usa? ',
    ]
texto_order = [
    'Sí', 'No', 'Ninguna', 'Lo ejecuto', 'Le envío información', 'Uso el resultado',
    'Dependo de su ejecución', 'Nunca', 'Permanentemente', 'Frecuentemente',
    'Ocasionalmente', 'Algo', 'Mucho', 'No sé',  'Diariamente',
    'Semanalmente', 'Mensualmente', 'Otro',
        ]

def get_dataset(xdata, xknowlegde, xarea, xuser, xdata_users):
    """sumary_line"""

    data = xdata[xdata["name_es"] == xknowlegde].copy()

    if ("ALL" not in xarea):
        data = data[data.Organization_area_es.isin(xarea)]

    if ("ALL" not in xuser):
        data = data[data.username.isin(xuser)]

    data_plot = (data.groupby(["id_node", "node_es", "id_question", "Question_es",
                                "valor", "texto"])
                    .agg(frecuencia=("texto","count")))
    data_plot = data_plot.reset_index()
    # Calcular el total de frecuencias por pregunta y nodo
    data_plot['total_frecuencia'] = (
        data_plot.groupby(["id_question", 'id_node'])['frecuencia'].transform('sum'))

    # Calcular el porcentaje de cada frecuencia dentro de cada grupo de pregunta
    data_plot['porcentaje'] = (
        (data_plot['frecuencia'] / data_plot['total_frecuencia']) * 100).round(2)

    # Eliminar la columna de total de frecuencia si no es necesaria
    data_plot = data_plot.drop(columns=['total_frecuencia'])
    data_plot["frecuencia_str"] = data_plot["frecuencia"].astype(str)
    data_plot["porcentaje_str"] = data_plot["porcentaje"].astype(str)+"%"
    # Asigna estos órdenes a las columnas correspondientes
    data_plot['Question_es'] = pd.Categorical(data_plot['Question_es'],
                                                categories=question_order, ordered=True)
    data_plot['texto'] = pd.Categorical(data_plot['texto'], categories=texto_order,
                                            ordered=True)
    # Ordena el DataFrame por las columnas Question_es y texto
    data_plot = data_plot.sort_values(['Question_es', 'texto'])

    data_users = (xdata_users[["Organization_area_es", "id_employee"]]
                    .drop_duplicates().copy())
    data_users = (data_users.groupby(["Organization_area_es"])
                    .agg(total_users_per_area=("id_employee","count")).reset_index())

    data_table = (data[["Organization_area_es", "id_employee", "username"]]
                    .drop_duplicates().copy())
    data_table = (data_table.groupby(["Organization_area_es"])
                    .agg(users_per_area=("id_employee","count")).reset_index())

    data_table = data_table.merge(data_users, on="Organization_area_es", how="left")
    data_table["porcentaje"] = (
        (data_table['users_per_area'] / data_table['total_users_per_area']) * 100).round(2)

    # Crear una nueva fila con el total
    total_row = pd.DataFrame({
        'Organization_area_es': ['Total'],
        'users_per_area': [data_table['users_per_area'].sum()],
        'total_users_per_area': [data_table['total_users_per_area'].sum()],
        'porcentaje': [
            (data_table['users_per_area'].sum() / data_table['total_users_per_area'].sum()
                * 100).round(2)]
    })

    data_table = pd.concat([data_table, total_row], ignore_index=True)
    data_table["porcentaje_str"] = data_table["porcentaje"].astype(str)+"%"

    return ColumnDataSource(data_plot), ColumnDataSource(data_table)

def make_table(xsource_table):
    """Realiza la tabla del npumero de personas por área"""
    columns_table =[
        TableColumn(field="Organization_area_es", title="Área", width=110),
        TableColumn(field="users_per_area", title="# respuestas", width=75),
        TableColumn(field="total_users_per_area", title="# Empleados Área",
                    width=100),
        TableColumn(field="porcentaje_str", title="Empleados encuestados(%)",
                    width=150),
    ]

    table = DataTable(columns=columns_table, source=xsource_table, width=350,
                        index_position=None)
    return table

def make_plot(xsource_plot):
    """Realiza el heatmap y el gridplot de las barras de las
    opciones de Uso para cada recurso"""
    # Obtener las preguntas únicas
    questions = list(set(xsource_plot.data['Question_es']))

    # Lista para almacenar las figuras
    tabs = []

    # Crear una figura para cada pregunta
    for question in questions:
        new_data = pd.DataFrame(xsource_plot.data)
        # Filtrar los datos según la pregunta
        new_data = new_data[new_data["Question_es"] == question]
        # Asigna estos órdenes a las columnas correspondientes
        new_data['Question_es'] = pd.Categorical(new_data['Question_es'],
                                                    categories=question_order, ordered=True)
        new_data['texto'] = pd.Categorical(new_data['texto'], categories=texto_order,
                                            ordered=True)
        # Ordena el DataFrame por las columnas Question_es y texto
        new_data = new_data.sort_values(['Question_es', 'texto'])

        # Crear un nuevo ColumnDataSource con los datos filtrados
        filtered_source = ColumnDataSource(data=new_data) #filtered_data

        # Configurar el mapa de color
        colors_heatmap = linear_cmap(field_name="porcentaje", palette=Pastel2[8],
                                    low=np.min(filtered_source.data["porcentaje"]),
                                    high=np.max(filtered_source.data["porcentaje"]))

        # Crear figura
        p = figure(
                    # title=f'Pregunta: {question}',
                    x_range=list(set(filtered_source.data['texto'])),
                    y_range=list(set(filtered_source.data['node_es'])),
                    x_axis_location="above", width=1100, height=450,
                    tools="hover", toolbar_location=None,
                    tooltips=[('Total Respuestas', '@frecuencia')],)
        #                         ("Porcentaje", "@porcentaje{% 00.00}")],)
        # # ('Pregunta', '@Question_es'), ('Conocimiento', '@node_es'), ('Respuestas', '@texto'),

        # Agregar rectángulos para el heatmap
        p.rect(x='texto', y='node_es', width=1, height=1, source=filtered_source,
                line_color="black", fill_color=colors_heatmap)
        # Agregar el texto de la frecuencia
        p.text(x='texto', y='node_es', text='porcentaje_str', source=filtered_source,
            text_align='center', text_baseline='middle', text_font_size='10pt',
            text_color='black')


        # Configurar los ejes
        p.xaxis.axis_label = "Respuestas"
        p.yaxis.axis_label = "Conocimientos"
        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_text_font_size = "10pt"
        p.axis.major_label_standoff = 0
        p.xaxis.major_label_orientation = math.pi / 4
        p.title.align = "right"

        # Crear la barra de color
        color_bar = ColorBar(color_mapper=colors_heatmap['transform'], width=8,
                                location=(0,0), ticker=BasicTicker())

        # Agregar la barra de color a la figura
        p.add_layout(color_bar, 'right')

        # Crear un TabPanel para la figura
        tab = TabPanel(child=p, title=question)
        tabs.append(tab)

    # Crear los Tabs con los TabPanels
    tabs_layout = Tabs(tabs=tabs, width=1100)

    return tabs_layout

def update_plot(xarea, xusername, xknowledge, xsource_plot, xdata, xsource_table,
                xlayout_heatmap, xdata_users):
    """actualiza el codigo segun los filtros seleccionados"""
    # update filtro username y resource segun el area
    if "ALL" not in xarea.value:
        data_area = xdata[xdata["Organization_area_es"].isin(xarea.value)]
        list_user = ["ALL"]+sorted(data_area["username"].unique())
    else:
        list_user = ["ALL"]+sorted(xdata["username"].unique())

    xusername.options = list_user

    ### update the data acordign the selected filters values
    new_data_plot, new_data_table = get_dataset(xdata, xknowledge.value, xarea.value,
                                                xusername.value, xdata_users)
    ######### Update:
    ### HEATMAP
    xsource_plot.data = dict(new_data_plot.data)
    ### Table
    xsource_table.data = dict(new_data_table.data)
    ### PLOTS
    xlayout_heatmap.children[0] = make_plot(xsource_plot=new_data_plot) # type: ignore
    # xlayout_plot.children[0] = make_table(xsource_table=new_data_table) # type: ignore

def fd_main():
    """función principal"""
    response_final, users_df = get_data_from_db(conn)
    data = response_final.copy()
    ###### Widgets
    list_area = ["ALL"]+sorted(data["Organization_area_es"].unique())
    list_username = ["ALL"]+sorted(data["username"].unique())
    list_knowledge = sorted(data["name_es"].unique())

    filter_area = MultiChoice(value=["ALL"], title='Área', options=list_area,
                                width=400, )
    filter_username = MultiChoice(value=["ALL"], title='Usuario', options=list_username,
                                    width=700, )
    filter_knowledge = Select(value=list_knowledge[0], title='Conocimientos',
                                options=list_knowledge, max_width =250)

    ##### Data
    source_plot, source_table = get_dataset(data, filter_knowledge.value,
                                            filter_area.value, filter_username.value,
                                            users_df)
    ### Plots and Tables
    grid_heatmap = make_plot(source_plot)
    table = make_table(source_table)

    ### show widgets and figures
    controls = row(children=[filter_knowledge, filter_area, filter_username])
    layout_heatmap = row(children=[grid_heatmap])
    layout_plot = row(children=[layout_heatmap, table])
    layout_final = column(children=[controls, layout_plot])

    ### Update widgets
    filter_area.on_change('value', lambda attr, old, new:
        update_plot(xarea=filter_area, xusername=filter_username, xdata=data,
                    xknowledge=filter_knowledge, xsource_plot=source_plot,
                    xsource_table=source_table, xlayout_heatmap=layout_heatmap,
                    xdata_users=users_df))
    filter_username.on_change('value', lambda attr, old, new:
        update_plot(xarea=filter_area, xusername=filter_username, xdata=data,
                    xknowledge=filter_knowledge, xsource_plot=source_plot,
                    xsource_table=source_table, xlayout_heatmap=layout_heatmap,
                    xdata_users=users_df))
    filter_knowledge.on_change('value', lambda attr, old, new:
        update_plot(xarea=filter_area, xusername=filter_username, xdata=data,
                    xknowledge=filter_knowledge, xsource_plot=source_plot,
                    xsource_table=source_table, xlayout_heatmap=layout_heatmap,
                    xdata_users=users_df))

    return layout_final

def AK_IRA_launch(doc):
    layout = fd_main()
    doc.add_root(layout)

