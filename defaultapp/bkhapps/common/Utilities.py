# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 12:43:01 2020

@author: luis.caro
"""

import datetime
import random

import pandas as pd

from bokeh.palettes import Turbo256


def generate_random_string(N = 7):

    # using random.choices()
    # generating random strings
    res = ''.join(random.choices(string.ascii_uppercase +
                                 string.digits, k=N))
    return str(res)

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

#devuelve datetime.datetime
def UT_String_to_datetime(string_date, xstring="%Y-%m-%d %H:%M:%S"):
        # print(string_date)
        return datetime.datetime.strptime(string_date, xstring)        

def UT_String_simple_to_datetime(string_date, xstring="%Y-%m-%d"):
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
def FD_cut_name(input_str):
    """
    Parameters
    ----------
    input_str : TYPE
        DESCRIPTION.
        Recibe:     - nombre1, nombre2, apellido1, apellido2
                o:  - nombre1, apellido1, apellido2
    Returns
    -------
    string
        DESCRIPTION.
        Elimina 2o apellido y deja solo inicial de nombre 2
    
    """
   
    words = input_str.split()
    
    # Eliminate the last word
    if len(input_str.split()) >= 3: 
        words = words[:-1]
        
        # If the original string had 4 or more words, modify the second word
        if len(input_str.split()) >= 4:
            for i in range(1,len(input_str.split())-2):
                words[i] = words[i][0]  # Keep only the first letter of the second word
    
    return ' '.join(words)

# n='MARIA LUISA DEL C MONTAÑEZ PEREZ'
# FD_cut_name('Luis Gabriel Caro Restrepo')

# words = n.split()
# words
# words = words[:-1]
# words
# for i in range(1,len(n.split())-2):
#     print(i)


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

#dividía mal el espacio, No se usa.
def UT_DividirSecuencia_viejo(xp,xn):
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
    print('.-.-.-.-.-.-.-.-.- UT_DividirSecuencia')
    
    print('>>>>>>>>>>>>>>>>>>>> len(xp) (UT_DividirSecuencia)')
    print(len(xp))
    print('>>>>>>>>>>>>>>>>>>>> xn (UT_DividirSecuencia)')
    print(xn)
    segment = len(xp)//(xn-1)
    print('>>>>>>>>>>>>>>>>>>>> segment (UT_DividirSecuencia)')
    print(segment)
    indexes =  [min(len(xp)-1,i*segment) for i in range(0,xn)]
    print('>>>>>>>>>>>>>>>>>>>> indexes (UT_DividirSecuencia)')
    print(indexes)
    colorDictDF=pd.DataFrame({'colorIndex':[i for i in range(0,xn)],
                              'colors':[xp[i] for i in indexes]})
    colorDict=colorDictDF.to_dict()['colors']
    print('>>>>>>>>>>>>>>>>>>>> colorDict (UT_DividirSecuencia)')
    print(colorDict)
    return colorDict

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
    # print('.-.-.-.-.-.-.-.-.- UT_DividirSecuencia')
    
    # print('>>>>>>>>>>>>>>>>>>>> len(xp) (UT_DividirSecuencia)')
    # print(len(xp))
    # print('>>>>>>>>>>>>>>>>>>>> xn (UT_DividirSecuencia)')
    # print(xn)
    segment = len(xp)//xn
    # print('>>>>>>>>>>>>>>>>>>>> segment (UT_DividirSecuencia)')
    # print(segment)
    indexes_non_centered =  [(i+1)*segment for i in range(0,xn)]
    # print('>>>>>>>>>>>>>>>>>>>> indexes_non_centered (UT_DividirSecuencia)')
    # print(indexes_non_centered)
    right_edge = len(xp)-indexes_non_centered[len(indexes_non_centered)-1]
    # print('>>>>>>>>>>>>>>>>>>>> right_edge (UT_DividirSecuencia)')
    # print(right_edge)
    average_edge = (segment + right_edge) // 2
    # print('>>>>>>>>>>>>>>>>>>>> average_edge (UT_DividirSecuencia)')
    # print(average_edge)
    adjustment = segment - average_edge
    indexes = [non_centered_index - adjustment\
               for non_centered_index in indexes_non_centered]
    # print('>>>>>>>>>>>>>>>>>>>> indexes (UT_DividirSecuencia)')
    # print(indexes)
    
    colorDictDF=pd.DataFrame({'colorIndex':[i for i in range(0,xn)],
                              'colors':[xp[i] for i in indexes]})
    colorDict=colorDictDF.to_dict()['colors']
    # print('>>>>>>>>>>>>>>>>>>>> colorDict (UT_DividirSecuencia)')
    # print(colorDict)
    return colorDict

# UT_DividirSecuencia(Turbo256,2)


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
    
    print('.-.-.-.-.-.-.-.-.-.-.-.-.Utilities/UT_CreateColorAttributeFromKeyComponent')
    # print('>>>>>>>> xkeyComponents(UT_CreateColorAttributeFromKeyComponent)')
    # print(xkeyComponents)
    # print('>>>>>>>> xcomponents(UT_CreateColorAttributeFromKeyComponent)')
    # print(xcomponents)
    
    componentNumber_color_Dict = \
        UT_DividirSecuencia(Turbo256,len(set(xkeyComponents)))
    # print('>>>>>componentNumber_color_Dict (UT_CreateColorAttributeFromKeyComponent)')
    # print(componentNumber_color_Dict)
    componentName_componentNumber_Dict = \
        FD_ConvertListToIndexDictionary(xkeyComponents)
    # print('>>>>componentName_componentNumber_Dict (UT_CreateColorAttributeFromKeyComponent)')
    # print(componentName_componentNumber_Dict)
        
    componentColors=\
        [componentNumber_color_Dict.get(componentName_componentNumber_Dict.\
                                        get(keyComponent))
         for keyComponent in xkeyComponents]
    # print('>>>>>> componentColors (UT_CreateColorAttributeFromKeyComponent)')
    # print(componentColors)
    
    componentName_color_Dict = \
        {k:componentNumber_color_Dict[v] \
         for k,v in componentName_componentNumber_Dict.items()}
    # print('>>>>> componentName_color_Dict (UT_CreateColorAttributeFromKeyComponent)')
    # print(componentName_color_Dict)
    
    colorDF=pd.DataFrame({'color': componentColors,
                          'component': xcomponents})
    colorDF.set_index('component',inplace=True)
    colorDictionary=colorDF.to_dict()['color']
    # print('>>>>>>>> colorDictionary (UT_CreateColorAttributeFromKeyComponent)')
    # print(colorDictionary)
    
    # print('>componentName_color_Dict (UT_CreateColorAttributeFromKeyComponent)')
    # print(componentName_color_Dict)
    
        
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

#%%
def UT_bring_legend(xlegend, xlanguage, xlegends_dict):
    legend = xlegends_dict.get(xlegend)[xlanguage]
    return legend


    




