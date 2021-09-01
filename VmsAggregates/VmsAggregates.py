import xml.etree.ElementTree as ET
import json

import PyPDF2
import re

import statistics

from numpy import cov
from scipy.stats.stats import pearsonr
  
path = 'C:/Users/NTAZINDA/Downloads/year/321/'
f = open(path + 'bps_2021_year.json',)
data = json.load(f)

ret = {}

days = len (data)
totals = {}

for day in data:
    generatedFiles = len (data[day])
    countAll = 0
    counts = {}
    events = {}
    runtime = 0
    headercards = set()
    speed = 0
    totalTime = data[day]['runtimeAll']
    daySpeed = 0

    for _ in data[day]:
        if ' - ' not in _:
            continue
        x = data[day][_]
        runtime += x['runtime']
        countAll += x['count']
        headercards.add ( x['hc'] )

        for event in x['events']:
            if event not in events:
                events[event] = 0
            events[event] += 1

        for qualities in x['data']:
            if qualities['denomname'] + qualities['quality'] not in counts:
                counts[qualities['denomname'] + qualities['quality']] = 0
            counts[qualities['denomname'] + qualities['quality']] += int(qualities['number'])
            
    if runtime > 0:
        speed = countAll / runtime
        daySpeed = countAll / totalTime
    headercardsCount = len (headercards)

    day_ = day.split("-")
    index = day_[2] + "." + day_[1] + "." + day_[0]

    generatedFilesPerHeaderCard = 0
    if headercardsCount > 0:
        generatedFilesPerHeaderCard = generatedFiles / headercardsCount
    
    ret[index] = {
        'generatedFilesPerHeaderCard': generatedFilesPerHeaderCard,
        'countAll': countAll,
        # 'counts': counts,
        # 'events': events,
        'runtime': runtime,
        'headercards': headercardsCount,
        'speed': speed,
        'dayLength': totalTime,
        'daySpeed': daySpeed
        }

f = open(path + "vms_data_perday.json", "w")
f.write(json.dumps(ret, indent=4))
f.close()