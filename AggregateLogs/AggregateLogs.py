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
        if m not in aggr:
            aggr[m] = { 'count': 1, 'd': toSeconds(x['d']) }
        else:
            aggr[m]['count'] = aggr[m]['count'] + 1
            aggr[m]['count'] = aggr[m]['count'] + toSeconds(x['d'])

ret = []
for x in aggr:
    print (x)
    h = str(int(aggr[x]['d'] / 3600))
    m = str(int((aggr[x]['d'] % 3600) / 60))
    s = str(int(aggr[x]['d'] % 60))
    if len(h) == 1:
        h = '0' + h
    if len(m) == 1:
        m = '0' + m
    if len(s) == 1:
        s = '0' + s
    d =  h + ':' + m + ':' + s
    n = '-'

    mm = x
    mm = re.sub (r'[^a-zA-Z]', ' ', mm).strip()
    mm = re.sub (r' s$', '', mm).strip()
    mm = re.sub (r' +', '', mm).strip().lower()

    for xx in dist2:
        if xx in mm:
            n = dist2[xx]
            
    if n == '-' and 'logged' in mm:
        n = 'User log on/off'
    if n == '-' and ('preparingreport' in mm or 'logdata' in mm or 'analysisdata' in mm):
        n = 'Reporting'
    if n == '-' and 'error' in mm:
        n = 'Error'
    if n == '-' and 'systemevent' in mm:
        n = 'System Event'
    if n == '-' and 'please' in mm:
        n = 'Prompt to user'

    ret.append ( { 'm': x, 'c': aggr[x]['count'], 'd': d, 'n': n } )

ret.sort (key=lambda i : i['c'], reverse=True)

f = open(path + "aggr.json", "w")
f.write(json.dumps(ret, indent=4))
f.close()

print (len(ret))

ret1 = []
for x in ret:
    if x['n'] == '-':
        ret1.append (x['m'])

f = open(path + "aggr1.json", "w")
f.write(json.dumps(ret1, indent=4))
f.close()