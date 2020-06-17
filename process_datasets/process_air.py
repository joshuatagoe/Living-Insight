#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
import computedistance


sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")


def handle_building(building,_311_service):
    latlong = [building.longitude, building.latitude]
    latlong2 = [_311_service.longitude, _311_service.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def process_air_quality(row):
    return None

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


air_quality = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Air_Quality.csv")


air_quality.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="air_quality", properties = { "user" : "postgres", "password" : "postgres" } )

spark.stop()
