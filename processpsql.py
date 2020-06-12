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
housing_insight = { 
                "house_id" : [],
                "mental_hosp" : []
                }

for row in houses.head(n=5).itertuples():
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

final_data = pd.DataFrame.from_dict(housing_insight)
print(final_data)

final_data.to_sql('housing_health_insight', create_engine(readpsql.engine_string))
