
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
import uuid 


sc = SparkContext("local", "SparkFile App")
sqlContext = SQLContext(sc)
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
address = '11 crooke avenue brooklyn new york'
latlng = computedistance.getLatLong(address)

def handle_building(lat, lng,latlng=latlng):
    latlong2 = [lng, lat ]
    if computedistance.computeDistance(latlng,latlong2) < 3:
        return True
    else:   
        return False

def handle_distance(lat, lng, latlng=latlng):
    latlong2 = [ lng, lat ]
    if computedistance.computeDistance(latlng, latlong2) <1.5:
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

_distance_udf = udf(handle_distance, BooleanType())
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



buildings.createOrReplaceTempView("building_view")
mh.createOrReplaceTempView("mental_health")
id_mh.createOrReplaceTempView("housing_id_mental_health")



get_query_ids = 'WITH upd AS ( SELECT * FROM building_view NATURAL JOIN housing_id_mental_health ) SELECT query_id FROM upd'
sqlDF = spark.sql(get_query_ids)
sqlDF.show()
sqlDF.createOrReplaceTempView("query_identifications")
get_mh = 'WITH upd AS ( SELECT * FROM mental_health NATURAL JOIN query_identifications) SELECT DISTINCT * FROM upd'
print("SHould print out mental healths that much previous queries from table above")
print(get_mh)
potentialmh = spark.sql(get_mh)
potentialmh.show()
print("Should printo out mental_health within 1.5 miles")
potentialmh.filter(_distance_udf('latitude','longitude'))
potentialmh.show()
building_id = uuid.uuid1()
building_id = building_id.hex
results = spark.sql("SELECT *, '"+building_id"' AS house_id FROM query_identifications")
results.show()


#subway_entrances

#crime

spark.stop()
