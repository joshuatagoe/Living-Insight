# -*- coding: utf-8 -*-
"""
Created on Sun Jun  7 22:15:53 2020

@author: joshu
"""

from fastkml import kml
import polygon


#get precinct from KML data
def findprecinct(p, dat):
    precincts = kml.KML()
    precincts.from_string(dat)
    features = list(precincts.features())
    f2 = list(features[0].features())
    f3 = list(f2[0].features())
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = polygon.getPolygon(finallist)
        if polygon.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
        
#get community_district from KML data       
def finddistrict(p, dat):
    districts  = kml.KML()
    districts.from_string(dat)
    features = list(districts.features())
    f2 = list(features[0].features())
    f3 = list(f2[0].features())
    for x in f3:
        placemark = x.geometry
        polygons = list(placemark.geoms)
        finallist = []
        for y in polygons:
            finallist = finallist + list(y.exterior.coords)
        finalpolygon = polygon.getPolygon(finallist)
        if polygon.isInside(finalpolygon, len(finallist)-1, p):
            return x.extended_data.elements[0].value
            
