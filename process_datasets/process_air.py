#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import BooleanType
import computedistance


sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")



def handle_building(building,air_quality):
    if air_quality.geo_type_name == "Borough":
        if building.borough.lower() == air_quality.geo_entity_name.lower():
            return True 
        else:
            return False
    if building.community_district == air_quality.geo_entity_id:
        print("worked")
        return True
    else:
        return False

spark = SparkSession \
    .builder \
    .appName("Process to pSql") \
    .getOrCreate()


air_quality = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Air_Quality.csv")


buildings = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","buildings_with_kml") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()
    

air_quality_udf = udf(handle_building,BooleanType())

newdataframe = buildings.crossJoin(air_quality).where(air_quality_udf(struct([buildings[x] for x in buildings.columns]), struct([air_quality[x] for x in air_quality.columns]))).select(buildings.house_id,air_quality.indicator_data_id)
air_quality.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="air_quality", properties = { "user" : "postgres", "password" : "postgres" } )
newdataframe.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_air_quality", properties = { "user" : "postgres", "password" : "postgres" } )
spark.stop()
