
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
import sys

sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
address = '11 crooke avenue brooklyn new york'

def handle_building(lat, lng, address=address):
    print(lat)
    print(lng)
    latlong = computedistance.getLatLong(address)
    latlong2 = [lng, lat ]
    print(latlong)
    print(latlong2)
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

spark.stop()
