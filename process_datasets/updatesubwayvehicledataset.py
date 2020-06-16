#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 06:04:37 2020

@author: joshua
"""
from pyspark.sql import SparkSession
from pyspark.sql import Row
import randomdistribution
import mentalhealthservices
from pyspark.sql.functions import udf, struct
from pyspark.sql.functions import monotonically_increasing_id
from pyspark.sql.functions import lit
from pyspark.sql.types import BooleanType
from pyspark.sql.types import IntegerType
from pyspark.sql.types import StructField
from pyspark.sql.types import StructType
import computedistance
from pyspark import SparkContext
from pyspark import SparkFiles

sc = SparkContext("local", "SparkFIle App")
sc.addFile("/home/joshua/Documents/Housing-Insight/computedistance.py")
sc.addFile("/home/joshua/Documents/Housing-Insight/randomdistribution.py")

def g(x):
    print(x)
    
def handle_building(building,mental_health):
    address = building.house_no + " " + building.street_name + " " + building.borough + " " + "New York"
    latlong = computedistance.getLatLong(address)
    latlong2 = [mental_health.longitude, mental_health.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def processhouse(row):
    price = randomdistribution.guesswork(row["Borough"].lower())
    return Row(house_id=row["Job Filing Number"], house_no=row["House No"],street_name=row["Street Name"], borough=row["Borough"], rental_price=int(price))

# def processhouse(row):
#     address = row["House No"] + " " + row["Street Name"] + " " + row["Borough"]+ " " + "New York"
#     latlong = computedistance.getLatLong(address)
#     price = randomdistribution.guesswork(row["Borough"].lower())
#     return Row(house_id=row["Job Filing Number"], house_no=row["House No"],street_name=row["Street Name"], borough=row["Borough"], rental_price=int(price), latitude=latlong[1], longitude=latlong[0])
  
def processmentalhealth(row):
    data = row[0]
    index = row[1]
    return Row(name_1=data.name_1, name_2 = data.name_2, street_1 = data.street_1, street_2 = data.street_2, city_location=data.street_2, zip=data.zip, latitude = data.latitude, longitude = data.longitude, query_id=index)

def process_entrances(row):
    longlat = row["the_geom"]
    longlat = longlat[7:]
    longlat = longlat[:-1]
    longlat = longlat.split(' ')
    longitude = float(longlat[0])
    latitude = float(longlat[1])
    
    return Row( object_id=row.OBJECTID, name=row.NAME, line=row.LINE, longitude=longitude, latitude=latitude)

def process_collissions(row):
    return Row(borough=row["BOROUGH"],zip_code=["ZIP CODE"],latitude=row["LATITUDE"],longitude=row["LONGITUDE"],collision_id=row["COLLISION_ID"], num_injured=row["NUMBER OF PERSONS INJURED"],num_killed=row["NUMBER OF PERSONS KILLED"])

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


buildings = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("/home/joshua/Documents/Housing-Insight/DOB_NOW__Build___Approved_Permits.csv")
# db= data.write.jdbc("jdbc:postgresql://localhost:5432/test_insight", table = 'buildings', properties = { "user": "postgres", "password" : "postgres" })

#data.show()
    
vehicle_collissions = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("/home/joshua/Documents/Housing-Insight/Motor_Vehicle_Collisions_Crashes.csv")
    
    
subway_entrances= spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("/home/joshua/Documents/Housing-Insight/DOITT_SUBWAY_ENTRANCE_01_13SEPT2010.csv")
    
    
test = buildings.rdd.map(processhouse)
test = test.toDF()

vehicle_collissions_rdd = vehicle_collissions.rdd.map(process_collissions)
vehicle_collissions = vehicle_collissions_rdd.toDF()
vehicle_collissions = vehicle_collissions.filter(vehicle_collissions.longitude.isNotNull())


subway_entrances_rdd = subway_entrances.rdd.map(process_entrances)
subway_entrances = subway_entrances_rdd.toDF()
# to_append = [StructField("query_id", IntegerType(), False)]
# new_schema = StructType(mental_health.schema.fields + to_append)
#mental_health = spark.createDataFrame(mental_health_rdd, mental_health.schema)
print(subway_entrances.head(5))
print(vehicle_collissions.head(5))

mental_udf = udf(handle_building,BooleanType())

newdataframe1 = test.limit(20).crossJoin(vehicle_collissions.limit(20)).where(mental_udf(struct([test[x] for x in test.columns]), struct([vehicle_collissions[x] for x in vehicle_collissions.columns]))).select(test.house_id,vehicle_collissions.collision_id)
newdataframe2 = test.limit(20).crossJoin(subway_entrances.limit(20)).where(mental_udf(struct([test[x] for x in test.columns]), struct([subway_entrances[x] for x in subway_entrances.columns]))).select(test.house_id,subway_entrances.object_id)

newdataframe1.limit(20).show()
newdataframe2.limit(20).show()

spark.stop()