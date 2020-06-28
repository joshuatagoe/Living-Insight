
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
address = '310 3rd Ave, New York, NY 10010'

def handle_building(lat, lng, address=address):
    latlong = computedistance.getLatLong(address)
    latlong2 = [lat, lng ]
    return computedistance.computeDistance(latlong,latlong2) < 1.5:
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

def handle_building(building,_311_service):
    if _311_service.city in boroughs:
        if building.borough != _311_service.city:
            return False
    latlong = [building.longitude, building.latitude]
    latlong2 = [_311_service.longitude, _311_service.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False


_building_udf = udf(handle_building,BooleanType())

buildings = buildings.filter(_building_udf('lat','long'))
buildings.show()

spark.stop()
