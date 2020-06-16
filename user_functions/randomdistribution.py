#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 01:02:43 2020

@author: joshua
"""


import numpy as np

averages = {
    "new york" : 3902,
    "manhattan" : 4208,
    "brooklyn" : 2951,
    "queens" : 2568,
    "bronx" : 1708,
    "staten island" : 2138
    } 

def guesswork(borough):
    avg = averages[borough]
    sigma = 82
    
    s = np.random.normal(avg, sigma, 1)
    return s[0]

