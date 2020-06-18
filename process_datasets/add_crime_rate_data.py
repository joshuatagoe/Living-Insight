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


def handle_building(building,crime_report):
    if building.borough != crime_report.BORO_NM or building.precinct != crime_report.ADDR_PCT_CD:
        return False
    latlong = [building.longitude, building.latitude]
    latlong2 = [crime_report.Longitude, crime_report.Latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

def process_data(row):
    #return Row(query_id=row['COMPLNT_NUM'], precinct=row['ADDR_PCT_CD'],borough=['BORO_NM'],offense_level=row['LAW_CAT_CD'],offense=row['OFNS_DESC'], \
    #latitude=row['Latitude'],longitude=row['Longitude'])
    return row

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


    
nypd_crime_data = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/NYPD_Complaint_Data_Current__Year_To_Date_.csv")
    
nypd_crime_data.printSchema()
print(nypd_crime_data.head(5))

proximity_udf = udf(handle_building,BooleanType())

newdataframe = buildings.crossJoin(nypd_crime_data).where(proximity_udf(struct([buildings[x] for x in buildings.columns]), struct([nypd_crime_data[x] for x in nypd_crime_data.columns]))).select(buildings.house_id,nypd_crime_data.CMPLNT_NUM)
nypd_crime_data.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="nypd_crime_data", properties = { "user" : "postgres", "password" : "postgres" } )
newdataframe.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_id_to_crime_id", properties = { "user" : "postgres", "password" : "postgres" } )


spark.stop()
