
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020

@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark.sql import Row
import randomdistribution
from pyspark.sql.functions import udf, struct, asc, col, lower
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
address = '11 crooke avenue brooklyn new york'
latlng = computedistance.getLatLong(address)

def handle_building(lat, lng,latlng=latlng):
    latlong2 = [lng, lat ]
    if computedistance.computeDistance(latlng,latlong2) < 3:
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
buildings = buildings.filter(_building_udf('latitude','longitude'))
buildings.show()
#precinct and community district
buildings_rdd = buildings.rdd.map(find_building_distance)
buildings = buildings_rdd.toDF()
buildings.show()
precinctrow = buildings.orderBy(asc("distance")).take(1)
buildings.orderBy(asc("distance")).limit(1).first()
print("Precinct is")
print()
print(precinctrow[0].precinct)
print(precinctrow[0].precinct)
print(precinctrow[0].precinct)
print(precinctrow[0].precinct)
precinctrow = precinctrow[0]

#mental_health
house_ids = [ row.house_id for row in buildings.collect()]
id_string = ('('+','.join("'"+str(x)+"'" for x in house_ids)+')')
query_string = 'SELECT query_id FROM house_id_mental_health WHERE house_id IN '+id_string+' GROUP BY query_id'


id_mh = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

id_mh.show()
query_ids = [ row.query_id for row in id_mh.collect()]
data_string = ('('+','.join("'"+str(x)+"'" for x in query_ids)+')')
query_string = 'SELECT * FROM mental_health WHERE query_id IN '+data_string
print(query_string)




mh = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
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
results.show()
print(building_id)


#subway_entrances
query_string = 'SELECT object_id FROM building_to_subway WHERE house_id IN '+id_string+' GROUP BY object_id'
print(query_string)

subway = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


subway.show()
object_ids = [ row.object_id for row in subway.collect()]
data_string = ('('+','.join("'"+str(x)+"'" for x in object_ids)+')')
query_string = 'SELECT * FROM subway_entrances WHERE object_id IN '+data_string
print(query_string)




subway_entrances = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


#checks if the chosen mental_health institutions fit the condition
subway_entrances.createOrReplaceTempView("house_sub")
potentialsub = spark.sql('SELECT * FROM house_sub WHERE _distance_udf(lat,long)')
potentialsub.createOrReplaceTempView("house_sub")
results = spark.sql("SELECT object_id, '"+building_id+"' AS house_id FROM house_sub")
results.show()

#crime


query_string = 'SELECT `CMPLNT_NUM` FROM building_id_to_crime_id WHERE house_id IN '+id_string+' GROUP BY `CMPLNT_NUM`'
print(query_string)


crime_ids = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

crime_ids.show()
cmplnt_ids = [ row.CMPLNT_NUM for row in crime_ids.collect()]
data_string = ('('+','.join("'"+str(x)+"'" for x in cmplnt_ids)+')')
query_string = 'SELECT * FROM nypd_crime_data WHERE `CMPLNT_NUM` IN '+data_string
print(query_string)



crimes = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()



crimes.createOrReplaceTempView("house_crime")
potentialcrimes = spark.sql('SELECT * FROM house_crime WHERE _distance_udf(Latitude,Longitude)')
potentialcrimes.createOrReplaceTempView("house_crime")
results = spark.sql("""SELECT `CMPLNT_NUM`, '"""+building_id+"""' AS house_id FROM house_crime""")
results.show()


#air_quality
def handle_air(geo_entity_name,geo_entity_id, building=precinctrow):
    if building.borough.lower() == geo_entity_name.lower():
        return True 
    if building.community_district == geo_entity_id:
        print("worked")
        return True
    return False

air_udf = udf(handle_air, BooleanType())
spark.udf.register("air_udf",handle_air, BooleanType())
print(precinctrow)
data = spark.sql("SHOW USER FUNCTIONS")
data.show()

query_string = 'SELECT indicator_data_id FROM building_to_air_quality WHERE house_id IN '+id_string+' GROUP BY indicator_data_id'
print(query_string)

building_air = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

building_air.show()
data_ids = [ row.indicator_data_id for row in building_air.collect()]
data_string = ('('+','.join("'"+str(x)+"'" for x in data_ids)+')')
query_string = 'SELECT * FROM air_quality WHERE indicator_data_id IN '+data_string
print(query_string)

air_quality = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()


air_quality.createOrReplaceTempView("house_air")
#checks if the chosen mental_health institutions fit the condition
potential_datapoints = spark.sql('SELECT * FROM house_air WHERE air_udf(geo_entity_name,geo_entity_id)')
potential_datapoints.show()
potential_datapoints.createOrReplaceTempView("house_air")
results = spark.sql("SELECT indicator_data_id, '"+building_id+"' AS house_id FROM house_air")
results.show()


#collissions



query_string = 'SELECT collision_id FROM building_to_collissions WHERE house_id IN '+id_string+' GROUP BY collision_id'
print(query_string)
collissions = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

collissions.show()
collission_ids = [ row.collision_id for row in collissions.collect()]
collission_string = ('('+','.join("'"+str(x)+"'" for x in collission_ids)+')')
query_string = 'SELECT * FROM vehicle_collissions WHERE collision_id IN '+collission_string
print(query_string)

vehicle_collissions = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("query",query_string) \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

#checks if the chosen vehicle_collissions fit the condition
vehicle_collissions.createOrReplaceTempView("house_collission")
potentialcol = spark.sql('SELECT * FROM house_collission WHERE _distance_udf(lat,long)')
potentialcol.createOrReplaceTempView("house_collission")
potentialcol.show()
results = spark.sql("SELECT collision_id, '"+building_id+"' AS house_id FROM house_collission")
results.show()

#results.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="air_quality", properties = { "user" : "postgres", "password" : "postgres" } )



spark.stop()
