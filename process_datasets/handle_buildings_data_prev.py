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
import time

start_time = time.time()
sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")

start_time = time.time()
def handle_building(building,mental_health):
    latlong = [building.longitude, building.latitude]
    latlong2 = [mental_health.longitude, mental_health.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False


#renames columns, and creates new columns for latitude and longitude of the specific building
def processhouse(row):
    address = row["House No"] + " " + row["Street Name"] + " " + row["Borough"]+ " " + "New York"
    latlong = computedistance.getLatLong(address)
    price = randomdistribution.select_sample(row["Borough"].lower())
    return Row(house_id=row["Job Filing Number"], address=address.lower(), borough=row["Borough"], rental_price=int(price), latitude=latlong[1], longitude=latlong[0])
  
#removes unneccessary columns from dataset and provides an extra column to keep a unique index
def processmentalhealth(row):
    data = row[0]
    index = row[1]
    return Row(name_1=data.name_1, name_2 = data.name_2, street_1 = data.street_1, street_2 = data.street_2, city_location=data.city, zip=data.zip, latitude = data.latitude, longitude = data.longitude, query_id=index)


spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


buildings = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/DOB_NOW__Build___Approved_Permits.csv")
    
mental_health = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Mental_Health_Service_Finder_Data.csv")

buildings_rdd = buildings.limit(1000).rdd.map(processhouse)
buildings = buildings_rdd.toDF()

buildings.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table = 'buildings', properties = { "user": "postgres", "password" : "postgres" })


mental_health_rdd = mental_health.rdd.zipWithIndex().map(processmentalhealth)
mental_health = mental_health_rdd.toDF()
mental_health = mental_health.filter(mental_health.longitude.isNotNull())

mental_udf = udf(handle_building,BooleanType())



house_id_with_mental_health = buildings.crossJoin(mental_health).where(mental_udf(struct([buildings[x] for x in buildings.columns]), struct([mental_health[x] for x in mental_health.columns]))).select(buildings.house_id,mental_health.query_id)


mental_health.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table = 'mental_health', properties = { "user": "postgres", "password" : "postgres" })

house_id_with_mental_health.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table = 'house_id_mental_health', properties = { "user": "postgres", "password" : "postgres" })
print("--- %s seconds ---" % (time.time() - start_time))

spark.stop()
