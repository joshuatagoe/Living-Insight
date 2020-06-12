#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:29:28 2020

@author: joshua
"""

import pandas as pd
from sqlalchemy import create_engine

# follows django database settings format, replace with your own settings
DATABASES = {
    'production':{
        'NAME': 'living_insight',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': 5432,
    },
}

# choose the database to use
db = DATABASES['production']

# construct an engine connection string
engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
    user = db['USER'],
    password = db['PASSWORD'],
    host = db['HOST'],
    port = db['PORT'],
    database = db['NAME'],
)

def get_databases():
    

    # create sqlalchemy engine
    engine = create_engine(engine_string)
    
    # read a table from database into pandas dataframe, replace "tablename" with your table name
    df2 = pd.read_sql_table('mental_health',engine)
    df = pd.read_sql_table('dob_buildings',engine)
    df3 = pd.read_sql_table('air_quality',engine)
    df4 = pd.read_sql_table('_311_requests',engine)
    
    return [df, df2, df3, df4]
