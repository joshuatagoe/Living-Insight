#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 06:54:46 2020
@author: joshua
"""

from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import udf, struct
from pyspark.sql.types import BooleanType

sc = SparkContext("local", "SparkFile App")



spark = SparkSession \
    .builder \
    .appName("Process to pSql") \
    .getOrCreate()


police_misconduct = spark.read.format("csv") \
    .option("header","true") \
    .option("inferSchema","true") \
    .load("s3a://living-insight-data/precinct_complaints.csv")

police_misconduct.write.jdbc("jdbc:postgresql://localhost:5432/living_insight", table="police_misconduct", properties = { "user" : "postgres", "password" : "postgres" } )

spark.stop()
