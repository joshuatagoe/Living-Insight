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
sc.addFile("/home/joshua/Documents/Housing-Insight/computedistance.py")
sc.addFile("/home/joshua/Documents/Housing-Insight/randomdistribution.py")

def g(x):
    print(x)
    
def handle_building(building,loc):
    latlong = [building.longitude, building.latitude]
    latlong2 = [loc.longitude, loc.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def processhouse(row):
    price = randomdistribution.guesswork(row["Borough"].lower())
    return Row(house_id=row["Job Filing Number"], house_no=row["House No"],street_name=row["Street Name"], borough=row["Borough"], rental_price=int(price))

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

vehicle_collissions = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("/home/joshua/Documents/Housing-Insight/Motor_Vehicle_Collisions_Crashes.csv")
    
    
subway_entrances= spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("/home/joshua/Documents/Housing-Insight/DOITT_SUBWAY_ENTRANCE_01_13SEPT2010.csv")
    
    
building_rdd = buildings.rdd.map(processhouse)
buildings = building_rdd.toDF()

vehicle_collissions_rdd = vehicle_collissions.rdd.map(process_collissions)
vehicle_collissions = vehicle_collissions_rdd.toDF()
vehicle_collissions = vehicle_collissions.filter(vehicle_collissions.longitude.isNotNull())


subway_entrances_rdd = subway_entrances.rdd.map(process_entrances)
subway_entrances = subway_entrances_rdd.toDF()

print(vehicle_collissions.head(5))

proximity_udf = udf(handle_building,BooleanType())

newdataframe1 = buildings.crossJoin(vehicle_collissions.where(proximity_udf(struct([buildings[x] for x in buildings.columns]), struct([vehicle_collissions[x] for x in vehicle_collissions.columns])))).select(buildings.house_id,vehicle_collissions.collision_id)
newdataframe2 = buildings.crossJoin(subway_entrances.where(proximity_udf(struct([buildings[x] for x in buildings.columns]), struct([subway_entrances[x] for x in subway_entrances.columns])))).select(buildings.house_id,subway_entrances.object_id)

newdataframe1.limit(20).show()
newdataframe2.limit(20).show()

spark.stop()