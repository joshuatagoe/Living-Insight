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


def handle_building(building,_311_service):
    latlong = [building.longitude, building.latitude]
    latlong2 = [_311_service.longitude, _311_service.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def process_311(row):
    return Row(unique_key=row["Unique Key"], created_data=row["Created Data"], closed_data = row["Closed Data"], agency = row["Agency"], agency_name=row["Agency Name"], complaint_type=row["Complaint Type"], descriptor = row["Descriptor"], location_type = row["Location Type"], incident_zip=row["Incident Zip"], incident_address=row["Incident Address"], street_name=row["Street Name"], cross_street_1 = row["Cross Street 1"], \
               cross_street_2 = row["Cross Street 2"], intersection_street_1 = row["Intersection Street 1"], intersection_street_2 = row["Intersection Street 2"], address_type=row["Address Type"], city=row["City"], landmark=row["Landmark"], facility_type = row["Facility Type"], status=row["Status"], due_data = row["Due Date"], resolution_description=row["Resolution Description"], resolution_action_updated_date=row["Resolution Action Updated Date"], \
               community_board = row["Community Board"], bbl = row["BBL"], borough=row["Borough"], x_coordinate = row["X Coordinate(State Plane)"], y_coordinate =row["Y Coordinate(State Plane)"], open_data_channel_type=row["Open Data Channel Type"], park_facility_name = row["Park Facility Name"], park_borough=row["Park Borough"], vehicle_type=row["Vehicle Type"], taxi_company_borough = row["Taxi Company Borough"], \
               taxi_pick_up_location = row["Taxi Pick Up Location"], bridge_highway_name=row["Brige Highway Name"], bridge_highway_direction=row["Bridge Highway Direction"], road_ramp = row["Road Ramp"], bridge_highway_segment = row["Bridge Highway Segment"], latitude=row["Latitude"], longitude=row["Longitude"], location=row["Location"])

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


    
_311_requests = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load(" s3a://living-insight-data/311_Service_Requests_from_2010_to_Present.csv")
    
_311_rdd = _311_requests.rdd.map(process_311)
_311_requests = _311_rdd.toDF()
_311_requests.printSchema()
print(_311_requests.head(5))

_311_udf = udf(handle_building,BooleanType())

newdataframe = buildings.limit(20).crossJoin(_311_requests.limit(200)).where(_311_udf(struct([buildings[x] for x in buildings.columns]), struct([_311_requests[x] for x in _311_requests.columns]))).select(buildings.house_id,_311_requests.unique_id)
newdataframe.limit(20).show()

spark.stop()
