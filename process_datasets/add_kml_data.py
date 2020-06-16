#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark import SparkFiles
from pyspark.sql import Row
from pyspark.sql.functions import lit
import testingprocesses
import dataprocessing.py


sc = SparkContext("local", "SparkFIle App")
sc.addFile("/home/joshua/Documents/Housing-Insight/testingprocesses.py")
sc.addFile("/home/joshua/Documents/Housing-Insight/dataprocessing.py")



def process_precincts(row):
    p = dataprocessing.Point(row.longitude,row.latitude)
    precinct = testingprocesses.findprecinct(p)
    data = row.asDict()
    row["precinct"] = precinct
    return Row(**data)
    

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


precincts = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Police Precincts.kml")


community_districts = spark.read.format("xml") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Community Districts.kml")
    
    

buildings = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/DOB_NOW__Build___Approved_Permits.csv")
    
    
building_with_precinct_rdd = buildings.withColumn("precinct", lit(int(1))).rdd.map(process_precincts)


    


air_quality.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="air_quality", properties = { "user" : "postgres", "password" : "postgres" } )

spark.stop()