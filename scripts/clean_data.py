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

exit()

# Fix typos in university names/make them uniform.
import editdistance as ed
from titlecase import titlecase

df = s_df

schools = {}
for i, item in enumerate(df['INSTITUTION']):
    item = titlecase(item).replace('The ', '')
    item = item.replace('University University', 'University')
    if ed.eval(item, 'University of Texas Medical Branch') <= 1:
        item = 'University of Texas Medical Branch-Galveston'
    for key in schools.keys():
        if ed.eval(item, key) <= 3:
            schools[key].append(i)
            break
    else:
        item = item.replace(' - ', '-').replace(', ', '-')
        schools[item] = [i]

print(len(schools.keys()))

print(sum([len(schools[k]) for k in schools.keys()]))

for k in sorted(schools.keys()):
    print(k, ': ', len(schools[k]))

df.groupby('INSTITUTION').size() #.sort_values(ascending=False)



for school in schools.keys():
    for ind in schools[k]:
        df.iloc[ind, df.columns.get_loc('INSTITUTION')]  = school

df.groupby('INSTITUTION').size() #.sort_values(ascending=False)


# fix typos in discipline
track = {}
for i, item in enumerate(df['MAJOR']):
    try:
        item = titlecase(item)
        if ed.eval(item, 'Aerospace') <= 1:
            item = 'Aerospace Engineering'
        for key in track.keys():
            if ed.eval(item, key) <= 3:
                track[key].append(i)
                break
        else:
            item = item.replace(' - ', ' & ').replace('- ', ' & ').replace(' / ', ' & ')
            item = item.replace(' and ', ' & ').replace(' /', ' & ').replace('/ ', ' & ')
            item = item.replace('/', ' & ').replace(', ', ' & ').replace('+', '&')
            track[item] = [i]
    except:
        print(item, 'failed')
print(track)

print(len(track.keys()))

print(sum([len(track[k]) for k in track.keys()]))

for k in sorted(track.keys()):
    print(k, ': ', len(track[k]))

with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    display(df.groupby('MAJOR').size()) 
