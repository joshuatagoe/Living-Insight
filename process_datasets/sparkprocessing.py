#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020

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
sc.addFile("/home/ubuntu/Housing-Insight/computedistance.py")
sc.addFile("/home/ubuntu/Housing-Insight/randomdistribution.py")

def g(x):
    print(x)
    
def handle_building(building,mental_health):
    latlong = [building.longitude, building.latitude]
    latlong2 = [mental_health.longitude, mental_health.latitude ]
    if computedistance.computeDistance(latlong,latlong2) < 1.5:
        return True
    else:   
        return False

#def processhouse(row):
#    price = randomdistribution.guesswork(row["Borough"].lower())
#    return Row(house_id=row["Job Filing Number"], house_no=row["House No"],street_name=row["Street Name"], borough=row["Borough"], rental_price=int(price))

def processhouse(row):
    address = row["House No"] + " " + row["Street Name"] + " " + row["Borough"]+ " " + "New York"
    latlong = computedistance.getLatLong(address)
    price = randomdistribution.guesswork(row["Borough"].lower())
    return Row(house_id=row["Job Filing Number"], house_no=row["House No"],street_name=row["Street Name"], borough=row["Borough"], rental_price=int(price), latitude=latlong[1], longitude=latlong[0])
  
def processmentalhealth(row):
    data = row[0]
    index = row[1]
    return Row(name_1=data.name_1, name_2 = data.name_2, street_1 = data.street_1, street_2 = data.street_2, city_location=data.street_2, zip=data.zip, latitude = data.latitude, longitude = data.longitude, query_id=index)

spark = SparkSession \
    .builder \
    .appName("Process to pSqL") \
    .getOrCreate()


buildings = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/DOB_NOW__Build___Approved_Permits.csv")
# db= data.write.jdbc("jdbc:postgresql://localhost:5432/test_insight", table = 'buildings', properties = { "user": "postgres", "password" : "postgres" })

#data.show()
    
mental_health = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/Mental_Health_Service_Finder_Data.csv")
    
    
test = buildings.limit(100).rdd.map(processhouse)
test = test.toDF()
#mental_health = mental_health.withColumn("query_id",lit(int(1)))
mental_health_rdd = mental_health.rdd.zipWithIndex().map(processmentalhealth)
mental_health = mental_health_rdd.toDF()
mental_health = mental_health.filter(mental_health.longitude.isNotNull())
# to_append = [StructField("query_id", IntegerType(), False)]
# new_schema = StructType(mental_health.schema.fields + to_append)
#mental_health = spark.createDataFrame(mental_health_rdd, mental_health.schema)
mental_health.printSchema()
print(mental_health.head(5))

mental_udf = udf(handle_building,BooleanType())

newdataframe = test.crossJoin(mental_health).where(mental_udf(struct([test[x] for x in test.columns]), struct([mental_health[x] for x in mental_health.columns]))).select(test.house_id,mental_health.query_id)
#data.printSchema()
newdataframe.limit(20).show()

test.write.format("csv").save("buildings.csv")

mental_health.write.format("csv").save("mental_health.csv")

newdataframe.write.format("csv").save("house_id_mental_health.csv")

spark.stop()
