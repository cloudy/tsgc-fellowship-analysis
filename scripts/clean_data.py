#!/usr/bin/env python3

import pandas as pd
import numpy as np
import editdistance as ed
from titlecase import titlecase
import sys

if len(sys.argv) < 2:
    print('Failed to specify input/output file.')
    print('USAGE: python clean_data.py DATAFILE.csv')
    exit(1)

df = pd.read_csv(sys.argv[1])

schools = {}
for i, item in enumerate(df['INSTITUTION']):
    item = titlecase(item).replace('The ', '')
    item = item.replace('University University', 'University')
    if ed.eval(item, 'University of Texas Medical Branch') <= 1:
        item+='-Galveston'
    for key in schools.keys():
        if ed.eval(item, key) <= 3:
            schools[key].append(i)
            break
    else:
        item = item.replace(' - ', '-').replace(', ', '-')
        schools[item] = [i]

for school in schools.keys():
    for ind in schools[school]:
        df.at[ind, 'INSTITUTION']  = school

majors = {}
for i, item in enumerate(df['MAJOR']):
    try:
        item = titlecase(item)
        if ed.eval(item, 'Aerospace') <= 1:
            item = 'Aerospace Engineering'
        for key in majors.keys():
            if ed.eval(item, key) <= 1:
                majors[key].append(i)
                break
        else:
            item = item.replace(' - ', ' & ').replace('- ', ' & ').replace(' / ', ' & ')
            item = item.replace(' and ', ' & ').replace(' /', ' & ').replace('/ ', ' & ')
            item = item.replace('/', ' & ').replace(', ', ' & ').replace('+', '&')
            majors[item] = [i]
    except:
        print(item, 'failed')
        
for major in majors.keys():
    for ind in majors[major]:
        df.at[ind, 'MAJOR']  = major

df.to_csv(sys.argv[1], index_label=False, index=False)
