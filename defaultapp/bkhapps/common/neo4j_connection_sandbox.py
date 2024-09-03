# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 13:37:32 2023

@author: luis.caro
"""

import pandas as pd
from neo4j import GraphDatabase
import time
import networkx as nx

#%% https://www.youtube.com/watch?v=EDav6TfAOUs&list=PL9Hl4pk2FsvVShoT5EysHcrs-hyCsXaWC&index=3

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        
        if self.__driver is not None:
            self.__driver.close()
        
    def query(self, query, parameters=None, db=None):
        
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
    

user='neo4j'
pwd='responses-meet-opinions'
uri = "bolt://44.192.109.221:7687"




conn = Neo4jConnection(uri=uri, user=user, pwd=pwd)


def insert_data(query, rows, batch_size = 10000):
    # Function to handle the updating the Neo4j database in batch mode.
    
    total = 0
    batch = 0
    start = time.time()
    result = None
    
    while batch * batch_size < len(rows):

        res = conn.query(query, 
                         parameters = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')})
        total += res[0]['total']
        batch += 1
        result = {"total":total, 
                  "batches":batch, 
                  "time":time.time()-start}
        
    return result
