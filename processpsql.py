#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 20:40:15 2020

@author: joshua
"""

import readpsql
import computedistance

databases = readpsql.get_databases()

print(databases)
houses = databases[0]
mental_health = databases[1]
housing_insight = { 
                "house_id" : [],
                "mental_hosp" : []
                }

for row in houses.head(n=5).itertuples():
    if row.job_filing_num in housing_insight["house_id"]:
        continue
    housing_insight["house_id"].append(row)
    mental_hosps = housing_insight["mental_hosp"]
    mental_hosps.append([])
    curr_row_hosps = mental_hosps[len(mental_hosps)-1]
    
    address = row.house_num + " " + row.street_name
    #get latitude of house
    latlong = computedistance.getLagLong(address)
    for row_2 in mental_health.head(n=20).itertuples():
        latlong2 = [row_2.longitude, row_2.latitude ]
        if computedistance.computedistance(latlong,latlong2) < 1.5:
            
            curr_row_hosps.append(row_2.query_id)
            
        