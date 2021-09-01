import xml.etree.ElementTree as ET
import json

from os import walk

import PyPDF2
import re
  

path = 'C:/Users/NTAZINDA/Downloads/11.06.2021/321/'

_, _, filenames = next(walk(path + 'FTXMoved'))

ops = {}

for filename in filenames:
    tree = ET.parse(path + "FTXMoved/" + filename)

    root = tree.getroot()

    for child in root.iter('Machine'):
        machine = child.attrib.get("Name")

    for child in root.iter('Operator'):
        operator = child.attrib.get("Name")

    for child in root.iter('HeadercardUnit'):
        headercard = child.attrib.get("HeaderCardID")
        start = child.attrib.get("StartTime")
        end = child.attrib.get("EndTime")
        
    runtime = 1

    for child in root.iter('Counter'):
        d = {
            'quality': child.attrib.get("Quality"),
            'denom': child.attrib.get("DenomName"),
            'number': child.attrib.get("Number")
            }
            
        if start.split(' ')[0] not in ops:
            ops[start.split(' ')[0]] = {  }

        index = start.split(' ')[1] + ' - ' + end.split(' ')[1]

        if index not in ops[start.split(' ')[0]]:
            end_ = list(map(lambda x: int(x), end.split(' ')[1].split(':')))
            start_ = list(map(lambda x: int(x), start.split(' ')[1].split(':')))
            rt = end_[0] * 3600 + end_[1] * 60 + end_[2] - (start_[0] * 3600 + start_[1] * 60 + start_[2])
            ops[start.split(' ')[0]][index] = { 'data': [], 'runtime': rt, 'count': 0, 'hc': headercard }

        ops[start.split(' ')[0]][index]['data'].append (d)
        ops[start.split(' ')[0]][index]['count'] += int(d['number'])
        
f = open(path + "operations.json", "w")
f.write(json.dumps(ops, indent=4))
f.close()