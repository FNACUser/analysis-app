# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:43:01 2020

@author: luis.caro
"""

import datetime
import pandas as pd
from bokeh.palettes import Turbo256
import random
import string
from pathlib import Path
from defaultapp.config import Config
from defaultapp.models import IRA_Nodes_segments_categories


def generate_random_string(N = 7):

    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return str(res)


def UT_CountOcurrences(xtable,xcolumns):
    count=xtable.groupby(xcolumns).size().to_frame()
    count.columns = ['Count']
    count.reset_index(inplace=True)
    return count


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

#devuelve datetime.datetime
def UT_String_to_datetime(string_date, xstring="%Y-%m-%d %H:%M:%S"):
        # print(string_date)
        return datetime.datetime.strptime(string_date, xstring)        
    
def UT_Datetime_to_string(datetime_date, xstring="%Y-%m-%d %H:%M:%S"):
        return datetime.datetime.strftime(datetime_date, xstring)

def UT_DatetimeDate_to_datetimeDatetime(xdatetime_date):
    return datetime.datetime.combine(xdatetime_date, datetime.time.min)
    
def UT_Timestamp_to_datetime(xtimestamp):
    return datetime.datetime.fromtimestamp(xtimestamp)

def UT_Datetime_to_timestamp(xdatetime):
    return datetime.datetime.timestamp(xdatetime)

#%%

def UT_is_number(s):
    """ Returns True is string is a number. """
    return s.replace('.','',1).isdigit()

#%%

def FD_ConvertListToIndex(xlist):
    """
    Returns list of indexes of list
    ['a','b','a'] returns [0,1,0]     

    Parameters
    ----------
    xlist : list that will be converted to index
    Returns
    -------
    listAsIndex : list of indexes.
    """
    
    listSet=set(xlist)
    
    setDF=pd.DataFrame({'nameNumber':[i for i in range(0,len(listSet))],
                        'name':[name for name in listSet]})
    setDF.set_index('name',inplace=True)

    setDFDict=setDF.to_dict()['nameNumber']

    listAsIndex=[setDFDict[name] for name in xlist]

    return listAsIndex

# l=['uno','dos','tres','cuatro','dos','tres','cuatro','tres','cuatro','cuatro']
# a=FD_ConvertListToIndex(l)   
# a


def FD_ConvertListToIndexDictionary(xlist):
    """
    Returns dictionary of list
    ['a','b','a'] returns {'a':0,'b':1]     

    Parameters
    ----------
    xlist : list that will be converted to index dictionary
    Returns
    -------
    listAsIndex : list of indexes.
    """
    
    listAsIndex=FD_ConvertListToIndex(xlist)
    
    listAsIndexDF=pd.DataFrame({'name':xlist,'nameIndex':listAsIndex})
    listAsIndexDF.set_index('name',inplace=True)
    listAsIndexDict=listAsIndexDF.to_dict()['nameIndex']

    return listAsIndexDict

# l=['uno','dos','tres','cuatro','dos','tres','cuatro','tres','cuatro','cuatro']
# b=FD_ConvertListToIndexDictionary(l)   
# b

#%%

def UT_DividirSecuencia(xp,xn):
    """
    Selecciona n valores equidistantes de una secuencia y los devuelve 
    como un diccionario. 
    
    Parameters
    ----------
    xp : Secuencia. Puede ser lista o tupla.
    xn : TYPE
        DESCRIPTION.

    Returns
    -------
    colorDict : Diccionario con valores seleccionados e índice como
    numeración.
    """
    
    segment = len(xp)//(xn-1)
    indexes =  [min(len(xp)-1,i*segment) for i in range(0,xn)]
    colorDictDF=pd.DataFrame({'colorIndex':[i for i in range(0,xn)],
                              'colors':[xp[i] for i in indexes]})
    colorDict=colorDictDF.to_dict()['colors']
    return colorDict




def UT_CreateColorAttributeFromKeyComponent(xkeyComponents,xcomponents):
    """
    Crea un diccionario en donde la llave es el component y el color
    es el keyComponent.
    Sirve para agregarlo como atributo a un nx.graph

    Parameters
    ----------
    xkeyComponents : lista con agrupación de componentes (ej:area de los actores)
    xcomponents : lista de components (ej: actores)

    Returns
    -------
    colorDictionary : Diccionarui de colores

    """
    
    # print('UT_CreateColorAttributeFromKeyComponent')
    componentNumber_color_Dict=UT_DividirSecuencia(Turbo256,len(set(xkeyComponents)))
    # print('componentNumber_color_Dict')
    # print(componentNumber_color_Dict)
    componentName_componentNumber_Dict = \
        FD_ConvertListToIndexDictionary(xkeyComponents)
    # print('componentName_componentNumber_Dict')
    # print(componentName_componentNumber_Dict)
        
    componentColors=\
        [componentNumber_color_Dict.get(componentName_componentNumber_Dict.get(keyComponent))
         for keyComponent in xkeyComponents]
    # print('componentColors')
    # print(componentColors)
    
    componentName_color_Dict = \
        {k:componentNumber_color_Dict[v] \
         for k,v in componentName_componentNumber_Dict.items()}
    # print('componentName_color_Dict')
    # print(componentName_color_Dict)
    
    colorDF=pd.DataFrame({'color': componentColors,
                          'component': xcomponents})
    colorDF.set_index('component',inplace=True)
    colorDictionary=colorDF.to_dict()['color']
    # print('colorDictionary')
    # print(colorDictionary)
    
    
    return colorDictionary, componentName_color_Dict

#%%

def UT_RoundDictionary(xdictionary,xdecimals):
    """
    Rounds value in a dictionary.
    Dictionary must have one numerical value.

    Parameters
    ----------
    xdictionary : dictionary.
    xdecimals : decimals after rounding.

    Returns
    -------
    xdictionary : dictionary, as explained above.

    """
    for k, v in xdictionary.items():
        xdictionary[k] = round(v,xdecimals)
    return xdictionary

#%%

def UT_RemoveAccent(xstring):
    nonAccentString = xstring.replace('á', 'a')
    nonAccentString = nonAccentString.replace('é', 'e')
    nonAccentString = nonAccentString.replace('í', 'i')
    nonAccentString = nonAccentString.replace('ó', 'o')
    nonAccentString = nonAccentString.replace('ú', 'u')
    return nonAccentString


def strip(x):
    return x.strip()


def getDataPath():
    return Path(Config.BOKEH_DATA_PATH)


def FD_IRA_cycle_vs_networks_modes_to_DF(xira_networks_modes, xcycle):
    r = [(xcycle, nm.id_network_mode,) for nm in xira_networks_modes]
    df = pd.DataFrame.from_records(r, columns=['id_cycle', 'id_network_mode'])

    return df


# .-.-.-.-.-.-.-.-.-.-.-.-.-.- nodes_vs_networks_modes
def FD_IRA_Nodes_to_DF(xira_nodes, xcategory):
    r = [(n.id_node, xcategory) for n in xira_nodes]
    df = pd.DataFrame.from_records(r, columns=['id_node', 'id_network_mode'])

    return df


def FD_nodes_vs_networks_modes(xcategory):
    category = IRA_Nodes_segments_categories. \
        query.filter_by(id_node_segment_category=xcategory).first()
    segments = category.nodes_segments
    nodes_flat = [node for segment in segments for node in segment.nodes]
    return FD_IRA_Nodes_to_DF(nodes_flat, xcategory)




    




