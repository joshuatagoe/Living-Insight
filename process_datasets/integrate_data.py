
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020

@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark.sql import Row
import randomdistribution
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import BooleanType
import computedistance
from pyspark import SparkContext
from pyspark.sql import SQLContext
import sys

sc = SparkContext("local", "SparkFile App")
sqlContext = SQLContext(sc)
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
address = '11 crooke avenue brooklyn new york'

def handle_building(lat, lng, address=address):
    latlong = computedistance.getLatLong(address)
    latlong2 = [lng, lat ]
    if computedistance.computeDistance(latlong,latlong2) < 3:
        return True
    else:   
        return False


#removes unneccessary columns from dataset and provides an extra column to keep a unique index

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


buildings = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","buildings") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


""" mental_health = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Mental_Health_Service_Finder_Data.csv")
    
     """

_building_udf = udf(handle_building,BooleanType())

buildings = buildings.filter(_building_udf('latitude','longitude'))
buildings.show()

#mental_health
mh = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","mental_health") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()
id_mh = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","house_id_mental_health") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

sqlquery = 'WITH upd AS ( SELECT * FROM mh NATURAL JOIN id_mh ) SELECT * FROM upd WHERE house_id IN ('


def createquery(row):    
    print(row)
    sqlquery = sqlquery+row.house_id+','

buildings.rdd.map(createquery)

sqlquery = sqlquery + ')'
print(sqlquery)
sqlDF = spark.sql(sqlquery)
sqlDF.show()


#subway_entrances

#crime

spark.stop()
