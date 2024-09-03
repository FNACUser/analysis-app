"""
Retorna una vizualización de los datos la evaluación de los dominios
"""
#%%
from math import pi
import pandas as pd
from bokeh.io import curdoc
from bokeh.models import (ColumnDataSource, Select, AnnularWedge, Legend,
                            LegendItem, Range1d, HoverTool, DataTable,
                            TableColumn, StringFormatter, Div, TabPanel, Tabs)
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.layouts import column, row, gridplot, layout
from .alcaparros_evaluacion_domains_data import get_data_from_db_domains

#%%
def get_dataset(data, xuser, xdomain, xleader):
    """
    Retorna 4 ColumnDataSource para cada una de las gráficas y tablas
    """
    # Copiar el DataFrame original
    data_plots = data.copy()

    # Aplicar las condiciones de filtrado
    if xuser != "ALL":
        data_plots = data_plots[data_plots['username'] == xuser]

    if xleader != "ALL":
        data_plots = data_plots[data_plots['username_interacting_employee'] == xleader]

    if xdomain != "ALL":
        data_plots = data_plots[data_plots['name_es'] == xdomain]
        group = "id_question"
    else:
        group = "name_es"

    ### Data for the general table
    data_table = (data_plots[["id_question","Question_es", "code", "name_es",
                                "username", "texto", "descripcion",
                                "username_interacting_employee"]].copy())
    data_table = data_table.drop_duplicates()
    data_table = data_table.sort_values(by=["username", group,])

    ### Data for the questions table
    data_table_questions = data_table[["code", "id_question", "Question_es",
                                        "texto", "descripcion"]].copy()
    data_table_questions = data_table_questions.drop_duplicates(subset="id_question")
    data_table_questions = data_table_questions.sort_values(by="id_question")

    ### Data for the descriptions  table
    data_table_descriptions = data_table[["code", "id_question", "texto",
                                            "descripcion"]].copy()
    data_table_descriptions = data_table_descriptions.drop_duplicates()
    data_table_descriptions = data_table_descriptions.sort_values(by="id_question")

    ### Data for the donuts plots
    data_donut = (data_plots.groupby(by=[group,"valor"], as_index=False)
                    .agg(freq=("valor","count")))
    data_donut['end_angles'] = (data_donut.groupby(group)['freq']
                                .transform(lambda x: (2 * pi * (x / x.sum())).cumsum()))

    # Se define una lista de colores de Bokeh
    palette = Category10[5] # 5 porque son los texto unicos de las respuestas

    def assign_color(valor):
        """función para asignar colores según en el valor"""
        return palette[int(valor)]

    # Aplicar la función para crear la columna de colores
    data_donut['color'] = data_donut['valor'].apply(assign_color)
    # Calcular la suma total de frecuencia
    total_freq = data_donut.groupby(group)['freq'].transform('sum')
    # Calcular el porcentaje
    data_donut['porcentaje'] = (data_donut['freq'] / total_freq) * 100

    data_donut = data_donut.merge(data_plots[[group, "valor", "texto"]],
                                    on=[group, "valor"], how="left")
    data_donut = data_donut.drop_duplicates(subset=[group, "valor"])

    return (ColumnDataSource(data_donut), ColumnDataSource(data_table),
            ColumnDataSource(data_table_questions),
            ColumnDataSource(data_table_descriptions))

#%%
def make_table(xsource_table, xsource_questions, xsource_descriptions):
    """
    Retorna 3 tablas:
    * table: contiene los datos generales, es decir, el id de la pregunta, el nombre del
        usuario, la respuesta y el líder elegido.
    * layout_questions: contiene el código del dominio, el id de la pregunta y
        el texto de la pregunta.
    * layout_descriptions: contiene el código del dominio, el id de la pregunta,
        la respuesta y la descripción de la respuesta.
    """

    formatter = StringFormatter(font_style='bold', text_color="black")

    columns_table = [
        TableColumn(field="id_question", title="Id", width=50),
        TableColumn(field="username", title="Usuario", width=350, formatter= formatter),
        TableColumn(field="texto", title="Respuesta", width=120),
        TableColumn(field="username_interacting_employee", title="Líder elegido", width=350,
                    formatter= formatter),
    ]

    table = DataTable(source=xsource_table, columns=columns_table, selectable = True,
                        width=700, height=400)

    columns_questions = [
        TableColumn(field="code", title="Dominio", width=100),
        TableColumn(field="id_question", title="Id", width=50, formatter=formatter),
        TableColumn(field="Question_es", title="Pregunta", width=1500),
    ]

    table_question = DataTable(source=xsource_questions, columns=columns_questions,
                                width=1320, height=150)
    div_question = Div(text="""<b>Listado de preguntas</b>""", margin=10, align='center')
    layout_questions=column(children=[div_question, table_question])

    columns_description = [
        TableColumn(field="code", title="Dominio", width=100),
        TableColumn(field="id_question", title="Id", width=50, formatter=formatter),
        TableColumn(field="texto", title="Respuesta", width=120),
        TableColumn(field="descripcion", title="Descripción", width=1500),
    ]
    table_descriptions = DataTable(source=xsource_descriptions, columns=columns_description,
                                    width=1320, height=150)
    div_descriptions = Div(text="""<b>Descripción de las respuestas</b>""", margin=10,
                            align='center')
    layout_descriptions=column(children=[div_descriptions, table_descriptions])

    return table, layout_questions, layout_descriptions

#%%
def make_plot(xsource, xdomain):
    """
    Retorna un grid de bokeh conformado por donuts con sus respectivos títulos y leyendas
    """
    if "ALL" == xdomain:
        group = "name_es"
        title = ""
    else:
        group = "id_question"
        title = "Pregunta: "

    data_source = pd.DataFrame(xsource.data)
    list_domain = data_source[group].unique()

    # Crear un gráfico de dona para cada dominio
    plots = []
    for i in list_domain:
        data = data_source.loc[data_source[group] == i]
        list_angles = data['end_angles'].tolist()
        data.loc[:, "start_angles"] = [0] + list_angles[:-1]

        source = ColumnDataSource(data)
        xdr = Range1d(start=-1, end=1)
        ydr = Range1d(start=-1, end=1)

        plot = figure(x_range=xdr, y_range=ydr, x_axis_location=None,
                        y_axis_location=None, title = f"{title}{i}",
                        toolbar_location=None)
        plot.title.align = "left" # type: ignore
        plot.title.text_font_size = "9pt" # type: ignore
        plot.xgrid.grid_line_color = None
        plot.ygrid.grid_line_color = None

        glyph = AnnularWedge(x=0, y=0, inner_radius=0.6, outer_radius=0.9,
                                start_angle="start_angles", end_angle="end_angles",
                                line_color="white", line_width=3, fill_color="color")
        r = plot.add_glyph(source, glyph)

        legend = Legend(location="center", label_text_font_size="8pt")
        for i, val in enumerate(data['texto'].unique()):
            legend.items.append(LegendItem(label=str(val), renderers=[r], index=i)) # type: ignore
        plot.add_layout(legend, "center")

        hoover = HoverTool(tooltips=[('Respuesta', '@texto'), ('Frecuencia', '@freq'),
                                        ('Porcentaje', '@porcentaje %')])
        plot.add_tools(hoover)

        plots.append(plot)

    # Organizar los gráficos en un gridplot
    grid = gridplot(plots, ncols=2, width=310, height=310)#650

    return grid

#%%
def update(xsource_donut, xsource_table, xdata, xuser, xsource_questions, xdomain,
            xleader, xgrid, xsource_descriptions):
    """
    Función encargada de actualizar las gráficas y tablas según los valores de
    los filtros
    """
    if xuser.value != "ALL":
        data_user = xdata[xdata["username"] == xuser.value]
        leader = ["ALL"]+sorted(data_user["username_interacting_employee"].unique())
    else:
        leader = ["ALL"]+sorted(xdata["username_interacting_employee"].unique())

    xleader.options = leader

    if xleader.value != "ALL":
        data_leader = xdata[xdata["username_interacting_employee"] == xleader.value]
        user = ["ALL"]+sorted(data_leader["username"].unique())
    else:
        user = ["ALL"]+sorted(xdata["username"].unique())

    xuser.options = user

    ### update the data acordign the selected filters values
    new_data_donut, new_data_table, new_data_questions, new_data_descriptions = (
        get_dataset(xdata, xuser.value, xdomain.value, xleader.value))

    ######### Update:
    ### SOURCE DATA
    xsource_donut.data = dict(new_data_donut.data)
    xsource_table.data = dict(new_data_table.data)
    xsource_questions.data = dict(new_data_questions.data)
    xsource_descriptions.data = dict(new_data_descriptions.data)

    ### PLOTS
    xgrid.children[0] = make_plot(xsource_donut, xdomain.value)

def fd_main(current_user):
    """sumary_line"""
    response = get_data_from_db_domains()

    ###### Widgets
    list_leaders = ["ALL"]+sorted(response["username_interacting_employee"].unique().tolist())
    list_domains = ["ALL"]+sorted(response["name_es"].unique().tolist())
    
    if current_user['main_role'] == 'admin':
        list_users = ["ALL"]+sorted(response["username"].unique())
    else:
        list_users =[current_user['name']]
        

    filter_leader = Select(value=list_leaders[0], title='Líderes', options=list_leaders,
                            max_width =300)
    filter_username = Select(value=list_users[0], title='Usuario', options=list_users,
                                max_width =300)
    filter_domain = Select(value=list_domains[0], title='Dominios', options=list_domains,
                            max_width =300)

    ### Data
    source_donut, source_table, source_questions, source_descriptions = (
        get_dataset(response, filter_username.value,
                    filter_domain.value, filter_leader.value))

    ### Plots and Tables
    table, questions, descriptions = make_table(source_table, source_questions,
                                                source_descriptions)
    donut = make_plot(source_donut, filter_domain.value)

    ### Layouts
    layout_filters = row(children=[filter_username, filter_leader, filter_domain])
    layout_plots = row(children=[donut])
    layout_complete = row(children=[table, layout_plots])
    div_complete = Div(text="""<b>**************** RESULTADOS ****************</b>""",
                        margin=10, align='center')
    layout_div = column(children=[div_complete, layout_complete])
    ### Tabs
    tab_questions = TabPanel(child=questions, title= "Preguntas")
    tab_descriptions = TabPanel(child=descriptions, title="Descripción")
    tabs = Tabs(tabs=[tab_questions ,tab_descriptions], active=0,)
    ## Final layout
    layout_final = column(children=[layout_filters, tabs, layout_div])

    ### Update filters
    filter_leader.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_table=source_table,
                xgrid=layout_plots,xdata=response, xleader=filter_leader,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))
    filter_username.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_table=source_table,
                xgrid=layout_plots,xdata=response, xleader=filter_leader,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))
    filter_domain.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_table=source_table,
                xgrid=layout_plots,xdata=response, xleader=filter_leader,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))

    return layout_final


def eval_total(doc):
    logged_user = eval(doc.session_context.request.headers['Logged_user'])
    layout = fd_main(logged_user)
    doc.add_root(layout)


