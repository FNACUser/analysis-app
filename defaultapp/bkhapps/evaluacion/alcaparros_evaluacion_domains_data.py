"""
Created on 26 April 2024

Retorna un dataframe de las respuestas de la evaluación de los dominios de
Marzano Center(Alcaparros)

"""
#%%
import json
import pandas as pd
from sqlalchemy.orm import load_only
from defaultapp.sqlalchemy_pure_connection import session_scope
from defaultapp.models import (User, IRA_Questions,
                            IRA_Questions_possible_answers,
                            IRA_Responses, IRA_Adjacency_input_form,
                            IRA_Organization_areas, IRA_Networks,
                            IRA_Networks_modes,)

def get_data_from_db_domains():
    """Retorna un dataframe con las respuestas de la evaluación de los dominios"""
#%%
    with session_scope() as session:
        users = (session.query(User).options(
                load_only(User.id, User.username, User.id_organization_area)).all())
        areas = session.query(IRA_Organization_areas).all()
        adjacency_input_form = session.query(IRA_Adjacency_input_form).all()
        questions = session.query(IRA_Questions).all()
        possible_answers = session.query(IRA_Questions_possible_answers).all()
        responses = session.query(IRA_Responses).all()
        ira_networks = session.query(IRA_Networks).all()
        ira_networks_modes = (session.query(IRA_Networks_modes).options(
                load_only(IRA_Networks_modes.id_network_mode,
                            IRA_Networks_modes.id_network)).all())

#%%
    ####################### Convertirlos a un Dataframe ##########################

    users_df = pd.DataFrame(
            data=[(user.id, user.username,user.id_organization_area)
                    for user in users],
            columns=["id_employee", "username", "id_organization_area"])

    areas_df = (pd.DataFrame(
            data=[(area.id_organization_area, area.Organization_area_es)
                    for area in areas],
            columns=["id_organization_area", "Organization_area_es"])
                    .set_index("id_organization_area"))

    adjacency_input_form_df = (pd.DataFrame(
            data=[(aif.id_adjacency_input_form, aif.id_employee,
                    aif.id_network_mode, aif.Is_concluded)
                    for aif in adjacency_input_form],
            columns=['id_adjacency_input_form', 'id_employee',
                    'id_network_mode', 'is_concluded']))

    questions_df = pd.DataFrame(
            data=[(question.id_question, question.Question_es,
                    question.id_question_possible_answers)
                    for question in questions],
            columns=["id_question", "Question_es", "id_question_possible_answers"])

    possible_answers_df = pd.DataFrame(
            data=[(answer.id_question_possible_answers,
                    answer.Question_possible_answers_es)
                    for answer in possible_answers],
            columns=["id_question_possible_answers", "Question_possible_answers_es"])

    responses_df = pd.DataFrame(
            data=[(response.id_response, response.Response,
                    response.id_question, response.id_adjacency_input_form)
                    for response in responses],
            columns=["id_response", "response", "id_question",
                        "id_adjacency_input_form"])

    ira_networks_df = pd.DataFrame(
        data=[(network.id, network.code, network.name_es)
                for network in ira_networks],
        columns=["id_network", "code", "name_es"])

    ira_networks_modes_df = pd.DataFrame(
        data=[(network_mode.id_network_mode, network_mode.id_network)
                for network_mode in ira_networks_modes],
        columns=["id_network_mode", "id_network"])

#%%
    ###### Reescribir el json del dataframe: possible_answers_df

    def ira_possible_answers_json(dataframe):
        """Función para reescribir el json del dataframe: possible_answers_df"""
        lista_df_json = []
        for index in range(len(dataframe)):
            data = json.loads(
                    (dataframe.loc[index]["Question_possible_answers_es"]))
            df_json = pd.DataFrame(data)
            df_json["id_question_possible_answers"] = (
                    dataframe.loc[index]["id_question_possible_answers"])

            lista_df_json.append(df_json)

        df_final = pd.concat(lista_df_json, ignore_index=True)
        return df_final

    possible_answers_final = ira_possible_answers_json(possible_answers_df)

#%%
    ###### Reescribir el json del dataframe: response_df

    def ira_responses_json(dataframe):
        """Función para reescribir el json del dataframe: responses_df
        """
        lista_new_data = []
        for index in range(len(dataframe)):
            data = json.loads(dataframe.loc[index]["response"])
            new_data = pd.DataFrame(data)
            new_data["id_response"] = dataframe.loc[index]["id_response"]
            new_data["id_question"] = dataframe.loc[index]["id_question"]
            new_data["id_adjacency_input_form"] = (
                dataframe.loc[index]["id_adjacency_input_form"])

            lista_new_data.append(new_data)

        df_final = pd.concat(lista_new_data, ignore_index=True)
        return df_final
    response_final = ira_responses_json(responses_df)

#%%
    ############## Complementar los datos de responses_final
    adjacency_input_form_df = adjacency_input_form_df.merge(
        ira_networks_modes_df, on="id_network_mode", how="left")
    adjacency_input_form_df = adjacency_input_form_df.merge(
        ira_networks_df, on="id_network", how="left")

    questions_df = (questions_df.merge(
        possible_answers_final, on="id_question_possible_answers", how="left"))
                    #.set_index("id_question"))

    users_df = users_df.merge(areas_df, on="id_organization_area", how="left")

    response_final = response_final.merge(questions_df, on= ["id_question", "valor"],
                                            how="left")

    response_final = response_final.merge(
        adjacency_input_form_df, on="id_adjacency_input_form", how="left")

    response_final = response_final.merge(users_df, on="id_employee", how="left")

    response_final = response_final.merge(users_df[["id_employee", "username"]],
                                            left_on="item_id", right_on="id_employee")

    response_final = response_final.rename(columns={
        "id_employee_x": "id_employee", "id_employee_y": "id_interacting_employee",
        "username_x": "username", "username_y": "username_interacting_employee",})

#%%
    #### Eliminar a las personas que no pertenecen a la evaluación:
    # Luis Gabriel Caro, Humberto Zuluaga, Ingrid Valero

    people_to_delete = {"Luis Gabriel Caro", "Humberto Zuluaga", "Ingrid Valero"}
    # Crear una condición bool para las filas que contienen el conjunto
    # de strings a eliminar en la columna ingresada
    condition = response_final["username"].apply(lambda x: x in people_to_delete)
    # Eliminar las filas que cumplen con la condición
    response_final = response_final.drop(response_final[condition].index)

#%%
    #### Eliminar filas que en la base de datos presentan problemas
    # solo aplica para la DB = "evaluacionDB"

    # id_response de las filas a eliminar
    rows_to_delete = [1777, 1778, 1779, 1781, 1782, 1783, 1786, 1789]
    # Eliminar filas donde los valores de la columna 'id_response' estén en rows_to_delete
    response_final = response_final[~response_final['id_response'].isin(rows_to_delete)]

    return (response_final)
