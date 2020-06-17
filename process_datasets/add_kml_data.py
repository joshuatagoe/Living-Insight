#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql import Row
from pyspark.sql.functions import lit
from user_functions import testingprocesses
from user_functions import dataprocessing
import boto3




sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/user_functions/testingprocesses.py")
sc.addFile("/home/ubuntu/Housing-Insight/user_functions/dataprocessing.py")

s3 = boto3.resource('s3')
obj1 = s3.Object('living-insight-data', "Police Precincts.kml")
obj2 = s3.Object('living-insight-data', "Community Districts.kml")
precincts = obj1.get()['Body'].read()
districts = obj2.get()['Body'].read()

def process_precincts(row, dat=precincts):
    p = dataprocessing.Point(row.longitude,row.latitude)
    precinct = testingprocesses.findprecinct(p, dat)
    data = row.asDict()
    row["precinct"] = precinct
    return Row(**data)
    
def process_districts(row, dat=districts):
    p = dataprocessing.Point(row.longitude, row.latitude)
    district = testingprocesses.finddistrict(p,dat)
    data = row.asDict()
    row["community_district"] = district
    return Row(**data)



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
    
    
building_with_precinct_rdd = buildings.withColumn("precinct", lit(int(1))).rdd.map(process_precincts)
building_with_precinct = building_with_precinct_rdd.toDF()
print(building_with_precinct.head(5))

    


#air_quality.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="air_quality", properties = { "user" : "postgres", "password" : "postgres" } )

spark.stop()