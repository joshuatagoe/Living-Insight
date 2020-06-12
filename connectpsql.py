#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:07:10 2020

@author: joshua
"""

import psycopg2
from configparser import ConfigParser
import pandas as pd
from sqlalchemy import create_engine

conn = pyscopg2.conenct("dbname=living_insight user=postgres password=postgres")

def config(filename='database.ini', section='postgresql'):
    #create a parser
    parser = ConfigParser()
    #read config file
    parser.read(filename)
    
    #get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section,filename))
        
    return db


def connect():
    "Connect to the PostgreSQL database server"
    conn = None
    try:
        params = config()
        
        #connect to the postgresql server
        print('connecting to the PostgreSQL database....')
        conn = psycopg2.connect(**params)
        #create a cursor
        cur = conn.cursor()
        
        #execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        
        #display the postgresql database server version
        db_version = cur.fetchone()
        print(db_version)
        
        #close the communication with the postgresql
        
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
            

if __name__ == '___main__':
    connect()