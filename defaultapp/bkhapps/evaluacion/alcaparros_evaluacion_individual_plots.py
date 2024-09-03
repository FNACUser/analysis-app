"""
Retorna una vizualización de los datos la evaluación de los dominios
"""
#%%
from math import pi
import pandas as pd
from bokeh.io import curdoc
from bokeh.models import (ColumnDataSource, Select, AnnularWedge, Legend,
                            LegendItem, Range1d, HoverTool, DataTable, Spacer,
                            TableColumn, StringFormatter, Div, TabPanel, Tabs)
from bokeh.palettes import Category10
from bokeh.plotting import figure
from bokeh.layouts import column, row, gridplot, layout
from .alcaparros_evaluacion_domains_data import get_data_from_db_domains


def get_dataset(data, xuser, xdomain):
    """
    Retorna 4 ColumnDataSource para cada una de las gráficas y tablas
    """
    # Copiar el DataFrame original
    data_plots = data.copy()

    # Aplicar las condiciones de filtrado
    data_plots = data_plots[data_plots['username'] == xuser]
    data_plots_2 = data[data['username_interacting_employee'] == (xuser)]

    if xdomain != "ALL":
        data_plots = data_plots[data_plots['name_es'] == xdomain]
        data_plots_2 = data_plots_2[data_plots_2['name_es'] == xdomain]
        group = "id_question"
    else:
        group = "name_es"

    # Se define una lista de colores de Bokeh
    palette = Category10[5] # 5 porque son los texto unicos de las respuestas

    def assign_color(valor):
        """función para asignar colores según en el valor"""
        return palette[int(valor)]

    def process_df(df):
        """Función encargada de procesar el dataframe ingresado"""
        # Group by group and valor and count frequency
        df = (df.groupby(by=[group,"valor"], as_index=False)
                .agg(freq=("valor","count")))
        # Calculate end angles
        df['end_angles'] = (df.groupby(group)['freq']
                                .transform(lambda x: (2 * pi * (x / x.sum())).cumsum()))
        # Apply color function
        df['color'] = df['valor'].apply(assign_color)
        # Calculate total frequency
        total_freq = df.groupby(group)['freq'].transform('sum')
        # Calculate percentage
        df['porcentaje'] = (df['freq'] / total_freq) * 100
        # Merge additional data
        df = df.merge(data[[group, "valor", "texto"]],
                        on=[group, "valor"], how="left")
        # Drop duplicates
        df = df.drop_duplicates(subset=[group, "valor"])

        return df

    data_individual = process_df(
        data_plots[data_plots['username_interacting_employee'] == xuser])
    data_donut = process_df(
        data_plots_2[~data_plots_2['username'].str.contains(xuser)])

    ########################################
    ### Data for the general table
    data_table = (data_plots_2[["id_question","Question_es", "code", "name_es",
                            "texto", "descripcion"]].copy())
    data_table = data_table.drop_duplicates()
    # data_table = data_table.sort_values(by=["username", group,])

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

    return (ColumnDataSource(data_individual), ColumnDataSource(data_donut),
            ColumnDataSource(data_table_questions),
            ColumnDataSource(data_table_descriptions))

def make_table(xsource_questions, xsource_descriptions):
    """
    Retorna 2 tablas:
    * layout_questions: contiene el código del dominio, el id de la pregunta y
        el texto de la pregunta.
    * layout_descriptions: contiene el código del dominio, el id de la pregunta,
        la respuesta y la descripción de la respuesta.
    """

    formatter = StringFormatter(font_style='bold', text_color="black")

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

    return layout_questions, layout_descriptions

def make_individual_plot(xsource, xdomain):
    """
    Retorna un grid de bokeh conformado por donuts con sus respectivos títulos y leyendas
    con las respuestas individuales para el usuario seleccionado
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
    div_grid = Div(text="""<b>****** Respuestas Individuales ******</b>""",
                        margin=10, align='center')
    layout_grid = column(children=[div_grid, grid])

    return layout_grid

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
    div_grid = Div(text="""<b>****** Respuestas de Pares ******</b>""",
                        margin=10, align='center')
    layout_grid = column(children=[div_grid, grid])

    return layout_grid

def update(xsource_donut, xsource_individual, xdata, xuser, xsource_questions, xdomain,
            xdonut, xindividual, xsource_descriptions):
    """
    Función encargada de actualizar las gráficas y tablas según los valores de
    los filtros
    """

    ### update the data acordign the selected filters values
    new_data_individual, new_data_donut, new_data_questions, new_data_descriptions = (
        get_dataset(xdata, xuser.value, xdomain.value))

    ######### Update:
    ### SOURCE DATA
    xsource_donut.data = dict(new_data_donut.data)
    xsource_individual.data = dict(new_data_individual.data)
    xsource_questions.data = dict(new_data_questions.data)
    xsource_descriptions.data = dict(new_data_descriptions.data)

    ### PLOTS
    xindividual.children[0] = make_individual_plot(xsource_individual, xdomain.value)
    xdonut.children[0] = make_plot(xsource_donut, xdomain.value)

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
    source_individual, source_donut, source_questions, source_descriptions = (
        get_dataset(response, filter_username.value, filter_domain.value))

    ### Plots and Tables
    questions, descriptions = make_table(source_questions, source_descriptions)
    unique_plot = make_individual_plot(source_individual, filter_domain.value)
    donut = make_plot(source_donut, filter_domain.value)

    ### Layouts
    layout_filters = row(children=[filter_username, filter_domain]) #filter_leader,
    layout_donut = row(children=[donut])
    layout_individual = column(children=[unique_plot])
    spacer = Spacer(width=70,)
    layout_complete = row(children=[layout_individual, spacer, layout_donut])
    ### Tabs
    tab_questions = TabPanel(child=questions, title= "Preguntas")
    tab_descriptions = TabPanel(child=descriptions, title="Descripción")
    tabs = Tabs(tabs=[tab_questions ,tab_descriptions], active=0,)
    ### Div
    div_texto = Div(text="""
        <h3>Explicación de las gráficas</h3>
        <p>En <b>Respuestas Individuales</b> muestra los resultados de la
        auto evaluación, si no se aparecen indica que el usuario no la realizo.</p>
        <p>En <b>Respuestas de Pares</b> muestra los resultados de la evaluación
        de los otros usuario hacia usted como líder, si no se aparecen indica
        que el usuario no fue elegido como líder.</p>
        """, margin=10)
    ### Final Layout
    layout_final = column(children=[layout_filters,div_texto, tabs, layout_complete])# tabs,

    ### Update filters
    filter_leader.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_individual=source_individual,
                xdonut=layout_donut, xdata=response, xindividual=layout_individual,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))
    filter_username.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_individual=source_individual,
                xdonut=layout_donut, xdata=response, xindividual=layout_individual,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))
    filter_domain.on_change('value', lambda attr, old, new:
        update(xuser=filter_username, xdomain=filter_domain,
                xsource_donut=source_donut, xsource_individual=source_individual,
                xdonut=layout_donut, xdata=response, xindividual=layout_individual,
                xsource_questions=source_questions, xsource_descriptions=source_descriptions))
    return layout_final



def eval_individual(doc):
    logged_user=eval(doc.session_context.request.headers['Logged_user'])
    layout = fd_main(logged_user)
    doc.add_root(layout)


