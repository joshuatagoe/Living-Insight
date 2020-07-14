
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020

@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark.sql import Row
import randomdistribution
from pyspark.sql.functions import udf, struct, asc, col, lower, count, when, sum
from pyspark.sql.types import BooleanType, IntegerType
import computedistance
from pyspark import SparkContext
from pyspark.sql import SQLContext
import sys
import uuid 

sc = SparkContext("local", "SparkFile App")
sqlContext = SQLContext(sc)
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/apiconfig.py")
address = '11 crooke avenue brooklyn new york'
if(len(sys.argv)>1):
    address = sys.argv[1].lower()
latlng = computedistance.getLatLong(address)

def handle_building(lat, lng,latlng=latlng):
    latlong2 = [lng, lat ]
    if computedistance.computeDistance(latlng,latlong2) < 1.5:
        return True
    else:   
        return False

def handle_distance(lat, lng, latlng=latlng):
    latlong2 = [ lng, lat ]
    if computedistance.computeDistance(latlng, latlong2) <1.5:
        return True
    else:
        return False

def find_building_distance(row,latlng=latlng):
    latlong2 = [row['longitude'], row['latitude'] ]
    dist = computedistance.computeDistance(latlng,latlong2)
    newrow = row.asDict()
    newrow["distance"] = dist
    return Row(**newrow)



#removes unneccessary columns from dataset and provides an extra column to keep a unique index

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()

buildings = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","final_buildings_set") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


""" mental_health = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Mental_Health_Service_Finder_Data.csv")
    
     """

#define custom functions
_building_udf = spark.udf.register("_building_udf", handle_building, BooleanType())
_distance_udf = spark.udf.register("_distance_udf", handle_distance, BooleanType())

#filter for buildings within 3 miles of address
#precinct and community district
buildings_rdd = buildings.rdd.map(find_building_distance)
buildings = buildings_rdd.toDF()
precinctrow = buildings.orderBy(asc("distance")).take(1)
precinctrow = precinctrow[0]
newbuilding = precinctrow.asDict()
newbuilding['latitude'] =latlng[1]
newbuilding['longitude'] = latlng[0]
newbuilding['address'] = address
newbuilding['rental_price'] = 0

#mental_health
mh = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","mental_health") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


#create view from potentialmh 
mh.createOrReplaceTempView("house_mh")
#checks if the chosen mental_health institutions fit the condition
potentialmh = spark.sql('SELECT * FROM house_mh WHERE _distance_udf(latitude,longitude)')
potentialmh.createOrReplaceTempView("house_mh")
#creates house_id for house being added
building_id = uuid.uuid1()
building_id = building_id.hex
#slect queries from mhs, pairing it with the house_id
results = spark.sql("SELECT query_id, '"+building_id+"' AS house_id FROM house_mh")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="house_id_mental_health", properties = { "user" : "postgres", "password" : "postgres" } )

#update new building row
newbuilding['house_id'] = building_id

#subway_entrances

subway_entrances = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","subway_entrances") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


#checks if the chosen mental_health institutions fit the condition
subway_entrances.createOrReplaceTempView("house_sub")
potentialsub = spark.sql('SELECT * FROM house_sub WHERE _distance_udf(lat,long)')
potentialsub.createOrReplaceTempView("house_sub")
results = spark.sql("SELECT object_id, '"+building_id+"' AS house_id FROM house_sub")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_subway", properties = { "user" : "postgres", "password" : "postgres" } )



#crime

crimes = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable","nypd_crime_data") \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()



crimes.createOrReplaceTempView("house_crime")
potentialcrimes = spark.sql('SELECT * FROM house_crime WHERE _distance_udf(Latitude,Longitude)')
potentialcrimes.createOrReplaceTempView("house_crime")
results = spark.sql("""SELECT `CMPLNT_NUM`, '"""+building_id+"""' AS house_id FROM house_crime""")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_id_to_crime_id", properties = { "user" : "postgres", "password" : "postgres" } )

#air_quality
def handle_air(geo_entity_name,geo_entity_id, building=precinctrow):
    if building.borough.lower() == geo_entity_name.lower():
        return True 
    if building.community_district == geo_entity_id:
        return True
    return False

air_udf = udf(handle_air, BooleanType())
spark.udf.register("air_udf",handle_air, BooleanType())

air_quality = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable",'air_quality') \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


air_quality.createOrReplaceTempView("house_air")
#checks if the chosen mental_health institutions fit the condition
potential_datapoints = spark.sql('SELECT * FROM house_air WHERE air_udf(geo_entity_name,geo_entity_id)')
potential_datapoints.createOrReplaceTempView("house_air")
results = spark.sql("SELECT indicator_data_id, '"+building_id+"' AS house_id FROM house_air")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_air_quality", properties = { "user" : "postgres", "password" : "postgres" } )


#collissions
vehicle_collissions = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable",'vehicle_collissions') \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

#checks if the chosen vehicle_collissions fit the condition
vehicle_collissions.createOrReplaceTempView("house_collission")
potentialcol = spark.sql('SELECT * FROM house_collission WHERE _distance_udf(lat,long)')
potentialcol.createOrReplaceTempView("house_collission")
results = spark.sql("SELECT collision_id, '"+building_id+"' AS house_id FROM house_collission")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_collissions", properties = { "user" : "postgres", "password" : "postgres" } )
""" #update new building row
newbuilding['total_collissions'] = results.count()
calculated_info = potentialcol.agg(sum("num_injured"),sum("num_killed")).collect()[0]
newbuilding['total_injured'] = calculated_info[0]
newbuilding['total_killed'] = calculated_info[1]
newbuilding['total_affected'] = calculated_info[0]+calculated_info[1]


 """

del newbuilding['distance']



newbuilding = Row(**newbuilding)
rdd = sc.parallelize([newbuilding])
df = rdd.toDF()
df.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="final_buildings_set", properties = { "user" : "postgres", "password" : "postgres" } )
print(building_id)
spark.stop()
