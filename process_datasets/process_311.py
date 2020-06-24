#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import BooleanType
from pyspark import SparkContext
import computedistance


sc = SparkContext("local", "SparkFile App")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")

boroughs = [ "BRONX", "BROOKLYN", "STATEN ISLAND", "QUEENS", "MANHATTAN"]


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

def process_311(row):
    return Row(unique_key=row["Unique Key"], created_data=row["Created Date"], agency = row["Agency"], agency_name=row["Agency Name"], complaint_type=row["Complaint Type"], descriptor = row["Descriptor"], location_type = row["Location Type"], incident_zip=row["Incident Zip"], incident_address=row["Incident Address"], street_name=row["Street Name"], cross_street_1 = row["Cross Street 1"], \
               cross_street_2 = row["Cross Street 2"], intersection_street_1 = row["Intersection Street 1"], intersection_street_2 = row["Intersection Street 2"], city=row["City"], landmark=row["Landmark"], \
               community_board = row["Community Board"], bbl = row["BBL"], borough=row["Borough"], x_coordinate = row["X Coordinate (State Plane)"], y_coordinate =row["Y Coordinate (State Plane)"], park_borough=row["Park Borough"],  \
               latitude=row["Latitude"], longitude=row["Longitude"], location=row["Location"])


spark = SparkSession \
    .builder \
    .appName("Process to pSql") \
    .getOrCreate()


buildings = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","buildings") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


    
_311_requests = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/311_Service_Requests_from_2010_to_Present.csv")
    
print(_311_requests.head(5))
_311_rdd = _311_requests.rdd.map(process_311)
_311_requests = _311_rdd.toDF(sampleRatio=0.01)
_311_requests = _311_requests.filter(_311_requests["latitude"].isNotNull())
_311_requests = _311_requests.filter(_311_requests["longitude"].isNotNull())
#_311_requests.printSchema()
#print(_311_requests.head(5))

_311_udf = udf(handle_building,BooleanType())

#newdataframe = buildings.crossJoin(_311_requests).where(_311_udf(struct([buildings[x] for x in buildings.columns]), struct([_311_requests[x] for x in _311_requests.columns]))).select(buildings.house_id,_311_requests.unique_key)
#newdataframe.limit(20).show()

#newdataframe.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_311_requests", properties = { "user" : "postgres", "password" : "postgres" } )
_311_requests.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="_311_requests", properties = { "user" : "postgres", "password" : "postgres" } )


spark.stop()
