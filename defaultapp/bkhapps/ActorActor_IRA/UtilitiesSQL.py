# -*- coding: utf-8 -*-
"""
Created on Sat Nov 13 21:34:04 2021

@author: luis.caro
"""

import pandas as pd
# import sqlite3

def FD_Table_to_dataframe(xconnection,xtable):

    query = xconnection.cursor().execute("SELECT * From "+xtable)
    cols = [column[0] for column in query.description]
    results = pd.DataFrame.from_records(data =query.fetchall(), columns = cols)
    
    return results
