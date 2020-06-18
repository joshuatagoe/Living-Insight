#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 06:04:37 2020

@author: joshua
"""
from pyspark.sql import SparkSession
from pyspark.sql import Row
import randomdistribution
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import BooleanType
import computedistance
from pyspark import SparkContext

sc = SparkContext("local", "SparkFIle App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
    
def handle_entrances(building,loc):
    latlong = [building.longitude, building.latitude]
    latlong2 = [loc.long, loc.lat ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def handle_collissions(building,loc):
    if building.borough != None and loc.borough != None:
        if building.borough.lower()!=loc.borough.lower():
            return False
    latlong = [building.longitude, building.latitude]
    latlong2 = [loc.long, loc.lat ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False



def process_entrances(row):
    longlat = row["the_geom"]
    longlat = longlat[7:]
    longlat = longlat[:-1]
    longlat = longlat.split(' ')
    longitude = float(longlat[0])
    latitude = float(longlat[1])
    
    return Row( object_id=row.OBJECTID, name=row.NAME, line=row.LINE, long=longitude, lat=latitude)

def process_collissions(row):
    return Row(borough=row["BOROUGH"],zip_code=row["ZIP CODE"],lat=row["LATITUDE"],long=row["LONGITUDE"],collision_id=row["COLLISION_ID"], num_injured=row["NUMBER OF PERSONS INJURED"],num_killed=row["NUMBER OF PERSONS KILLED"])

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

vehicle_collissions = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Motor_Vehicle_Collisions_Crashes.csv")
    
    
subway_entrances= spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/DOITT_SUBWAY_ENTRANCE_01_13SEPT2010.csv")
  
vehicle_collissions = vehicle_collissions.filter(vehicle_collissions["LOCATION"].isNotNull())
vehicle_collissions_rdd = vehicle_collissions.rdd.map(process_collissions)
vehicle_collissions = vehicle_collissions_rdd.toDF()

subway_entrances_rdd = subway_entrances.rdd.map(process_entrances)
subway_entrances = subway_entrances_rdd.toDF()

print(vehicle_collissions.head(5))

proximity_udf = udf(handle_collissions,BooleanType())
proximity_udf2 = udf(handle_entrances, BooleanType())


newdataframe1 = buildings.crossJoin(vehicle_collissions).where(proximity_udf(struct([buildings[x] for x in buildings.columns]), struct([vehicle_collissions[x] for x in vehicle_collissions.columns]))).select(buildings.house_id,vehicle_collissions.collision_id)
newdataframe2 = buildings.crossJoin(subway_entrances).where(proximity_udf2(struct([buildings[x] for x in buildings.columns]), struct([subway_entrances[x] for x in subway_entrances.columns]))).select(buildings.house_id,subway_entrances.object_id)

newdataframe1.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_collissions", properties = { "user" : "postgres", "password" : "postgres" } )
newdataframe2.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_subway", properties = { "user" : "postgres", "password" : "postgres" } )
vehicle_collissions.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="vehicle_collissions", properties = { "user" : "postgres", "password" : "postgres" } )
subway_entrances.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="subway_entrances", properties = { "user" : "postgres", "password" : "postgres" } )


spark.stop()
