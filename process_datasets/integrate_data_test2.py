
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
import time





start_time = time.time()
sc = SparkContext("local", "SparkFile App")
sqlContext = SQLContext(sc)
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/process_datasets/randomdistribution.py")
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
buildings = buildings.filter(_building_udf('latitude','longitude'))
#precinct and community district
buildings_rdd = buildings.rdd.map(find_building_distance)
buildings = buildings_rdd.toDF()
precinctrow = buildings.orderBy(asc("distance")).take(1)
buildings.orderBy(asc("distance")).limit(1).first()
precinctrow = precinctrow[0]
newbuilding = precinctrow.asDict()
newbuilding['latitude'] =latlng[1]
newbuilding['longitude'] = latlng[0]
newbuilding['address'] = address
newbuilding['rental_price'] = 0
building_id = uuid.uuid1()
building_id = building_id.hex
newbuilding['house_id'] = building

#collissions
collissions = spark.read \
    .format("jdbc") \
    .option("url","jdbc:postgresql://localhost:5432/living_insight") \
    .option("dbtable",'building_to_collissions') \
    .option("user","postgres") \
    .option("password", "postgres") \
    .load()

collission_ids = [ row.collision_id for row in collissions.collect()]
collission_string = ('('+','.join("'"+str(x)+"'" for x in collission_ids)+')')
query_string = 'SELECT * FROM vehicle_collissions WHERE collision_id IN '+collission_string

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
results = spark.sql("SELECT collision_id, '"+building_id+"' AS house_id FROM house_collission")
results.write.mode('append').jdbc("jdbc:postgresql://localhost:5432/living_insight", table="building_to_collissions", properties = { "user" : "postgres", "password" : "postgres" } )
#update new building row
newbuilding['total_collissions'] = results.count()
calculated_info = potentialcol.agg(sum("num_injured"),sum("num_killed")).collect()[0]
newbuilding['total_injured'] = calculated_info[0]
newbuilding['total_killed'] = calculated_info[1]
newbuilding['total_affected'] = calculated_info[0]+calculated_info[1]

print(building_id)
print("--- %s seconds ---" % (time.time() - start_time))

spark.stop()