import xml.etree.ElementTree as ET
import json

from os import walk

import PyPDF2
import re
  
machine_ = '321'
path = 'C:/Users/NTAZINDA/Downloads/year/' + machine_ +'/'

_, _, filenames = next(walk('D:/BPS Files 2021/'))

ops = {}

for filename in filenames:
    tree = ET.parse('D:/BPS Files 2021/' + filename)

    root = tree.getroot()

    for child in root.iter('MACHINE'):
        machine = child.attrib.get("name")

    if 'M01000' + machine_ != machine:
        continue

    for child in root.iter('USER'):
        operator = child.attrib.get("name")

    for child in root.iter('HCUNIT'):
        headercard = child.attrib.get("headercardid")
        startdate = child.attrib.get("startdate")
        starttime = child.attrib.get("starttime")
        lastmodify = child.attrib.get("lastmodify")
        
    runtime = 1
    
    if startdate not in ops:
        ops[startdate] = { 'st': '23:59:59', 'end': '00:00:00' }

    index = starttime + ' - ' + lastmodify
    
    if index not in ops[startdate]:
        end_ = list(map(lambda x: int(x), lastmodify.split(':')))
        start_ = list(map(lambda x: int(x), starttime.split(':')))
        rt = end_[0] * 3600 + end_[1] * 60 + end_[2] - (start_[0] * 3600 + start_[1] * 60 + start_[2])
        ops[startdate][index] = { 'data': [], 'runtime': rt, 'count': 0, 'hc': headercard, 'events': [] }
        
        if starttime < ops[startdate]['st']:
            ops[startdate]['st'] = starttime
        if lastmodify > ops[startdate]['end']:
            ops[startdate]['end'] = lastmodify

    for child in root.iter('COUNTER'):
        d = {
            'quality': child.attrib.get("quality"),
            'denomname': child.attrib.get("denomname"),
            'number': child.attrib.get("number"),
            'stacker': child.attrib.get("stacker")
            }

        ops[startdate][index]['data'].append (d)
        ops[startdate][index]['count'] += int(d['number'])

    for child in root.iter('EVENT'):
        ops[startdate][index]['events'].append(child.attrib.get("type"))

    print ('.')

for x in ops:
    end_ = list(map(lambda x: int(x), ops[x]['end'].split(':')))
    start_ = list(map(lambda x: int(x), ops[x]['st'].split(':')))
    rt = end_[0] * 3600 + end_[1] * 60 + end_[2] - (start_[0] * 3600 + start_[1] * 60 + start_[2])
    ops[x]['runtimeAll'] = rt
        
f = open(path + "bps_2021_year.json", "w")
f.write(json.dumps(ops, indent=4))
f.close()