import xml.etree.ElementTree as ET
import json

import PyPDF2
import re
  
path = 'C:/Users/NTAZINDA/Downloads/year/320/'
f = open(path + 'logs.json',)
data = json.load(f)

dist = json.load(open('C:/Users/NTAZINDA/Downloads/year/321/dist.json'))
dist2 = {}

for x in dist:
    for i in dist[x]:
        m = re.sub (r' +', '', i).strip()
        dist2[m] = x
        
dist = json.load(open('C:/Users/NTAZINDA/Downloads/year/320/dist.json'))

for x in dist:
    for i in dist[x]:
        m = re.sub (r' +', '', i).strip()
        dist2[m] = x


aggr = {}

def toSeconds (st):
    x = st.split (":")
    return int(x[0]) * 3600 + int(x[1]) * 60 + int (x[2])

for day in data:
    for x in data[day]:
        m = x['m']
        m = re.sub (r'[0-9]+', 'X', m)
        # m = re.sub (r'[^a-zA-Z]', ' ', m).strip()
        m = re.sub (r' +', ' ', m).strip()

        if day not in aggr:
            aggr[day] = {}

        if m not in aggr[day]:
            aggr[day][m] = { 'count': 1, 'd': toSeconds(x['d']), 'n': x['n'] }
        else:
            aggr[day][m]['count'] = aggr[day][m]['count'] + 1
            aggr[day][m]['count'] = aggr[day][m]['count'] + toSeconds(x['d'])

ret = {}

for day in aggr:
    for x in aggr[day]:
        h = str(int(aggr[day][x]['d'] / 3600))
        m = str(int((aggr[day][x]['d'] % 3600) / 60))
        s = str(int(aggr[day][x]['d'] % 60))
        if len(h) == 1:
            h = '0' + h
        if len(m) == 1:
            m = '0' + m
        if len(s) == 1:
            s = '0' + s
        d =  h + ':' + m + ':' + s
        n = aggr[day][x]['n']

        mm = x
        mm = re.sub (r'[^a-zA-Z]', ' ', mm).strip()
        mm = re.sub (r' s$', '', mm).strip()
        mm = re.sub (r' +', '', mm).strip().lower()

        for xx in dist2:
            if xx in mm:
                n = dist2[xx]

        if day not in ret:
            ret[day] = []

        ret[day].append ( { 'm': x, 'c': aggr[day][x]['count'], 'd': d, 'n': n } )

for x in ret:
    ret[x].sort (key=lambda i : i['c'], reverse=True)


f = open(path + "aggrDay.json", "w")
f.write(json.dumps(ret, indent=4))
f.close()