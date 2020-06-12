#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:40:15 2020

@author: joshua
"""

import readpsql
import computedistance
from sqlalchemy import create_engine
import pandas as pd

databases = readpsql.get_databases()

print(databases)
houses = databases[0]
mental_health = databases[1]
air_quality = databases[2]

housing_insight = { 
                "house_id" : [],
                "mental_hosp" : []
                }

neighborhood_requests = {
            "house_id" : [],
            "unique_key" : []
        }

for row in houses.itertuples():
    if row.job_filing_num in housing_insight["house_id"]:
        continue
    mental_hosps = housing_insight["mental_hosp"]
    address = row.house_num + " " + row.street_name
    #get latitude of house
    latlong = computedistance.getLatLong(address)
    

    for row_2 in mental_health.head(n=20).itertuples():
        latlong2 = [row_2.longitude, row_2.latitude ]
        if computedistance.computeDistance(latlong,latlong2) < 1.5:
            housing_insight["house_id"].append(row.job_filing_num)
            mental_hosps.append(row_2.query_id)
    
#    for row_3 in air_quality.head(n=20).itertuples():
#        if row_3.geo_type_name=="Borough":
#            if computedistance.getBorough(address)==row_3.geo_type_entity:
#                
#        
#        if row_3.geo_type_name=="UHF42":
    
#    for row_4 in _requests.head(n=40).itertuples():
#        latlong4 = [ row_4.longitude, row_4.latitude ]
#        if computedistance.computeDistance(latlong,latlong4) < 1.5:
#            neighborhood_requests["house_id"].append(row.job_filing_num)
#            neighborhood_requests["unique_key"].append(row_4.unique_key)
#        
        
            

final_data = pd.DataFrame.from_dict(housing_insight)
#final_data2 = pd.DataFrame.from_dict(housing_insight)
print(final_data)
#print(final_data2)

final_data.to_sql('housing_health_insight', create_engine(readpsql.engine_string))
#final_data2.to_sql('neighborhood_requests', create_engine(readpsql.engine_string))
