import xml.etree.ElementTree as ET
import json

from os import walk

import PyPDF2
import re
  

# path = 'D:/BPS Files 2021 - Copy/BPS Files 2021 - Copy/'
path = input()

_, _, filenames = next(walk(path))

ops_320 = {}
ops_321 = {}

f = open("C:/Users/Public/js/currency-report/src/assets/321/logs_321.json",)
operations_321 = json.load(f)
f.close

f = open("C:/Users/Public/js/currency-report/src/assets/320/logs_320.json",)
operations_320 = json.load(f)
f.close

for filename in filenames:
    tree = ET.parse(path + filename)

    root = tree.getroot()

    machine = ''

    for child in root.iter('MACHINE'):
        machine = child.attrib.get("name")

    for child in root.iter('Operator'):
        operator = child.attrib.get("Name")

    for child in root.iter('HCUNIT'):
        headercard = child.attrib.get("headercardid")
        start = child.attrib.get("startdate") + " " + child.attrib.get("starttime")
        end = child.attrib.get("startdate") + " " + child.attrib.get("lastmodify")
        rejects = child.attrib.get("rejects")
        
    runtime = 1

    events = []

    logs = {}

    for child in root.iter('EVENT'):
        events.append(child.attrib.get("type"))

    data = operations_320
    if '321' in machine:
        data = operations_321

    if machine == '':
        continue

    if start.split(" ")[0] in data:
        for x in data[start.split(" ")[0]]:
            x1 = x['m']
            x1 = re.sub (r': [X0-9]+', ': X', x1)
            x1 = re.sub (r'[X0-9]+ / [X0-9]+', 'X / X', x1)
            x1 = re.sub (r'Operator [X0-9]+', 'Operator X', x1)
            x1 = re.sub (r'ID = [X0-9]+', 'ID = X', x1)
            x1 = re.sub (r'[X0-9]+ banknote', 'X banknote', x1)
            if x['t'] > start.split(" ")[1] and x['t'] < end.split(" ")[1]:
                if x1 not in logs:
                    logs[x1] = 0
                logs[x1] = logs[x1] + 1

    for child in root.iter('COUNTER'):
        d = {
            'quality': child.attrib.get("quality"),
            'denom': child.attrib.get("denomname"),
            'number': child.attrib.get("number")
            }

        if '321' in machine:
            if start.split(' ')[0] not in ops_321:
                ops_321[start.split(' ')[0]] = {  }
        else:
            if start.split(' ')[0] not in ops_320:
                ops_320[start.split(' ')[0]] = {  }

        index = start.split(' ')[1] + ' - ' + end.split(' ')[1]

        if '321' in machine:
            if index not in ops_321[start.split(' ')[0]]:
                end_ = list(map(lambda x: int(x), end.split(' ')[1].split(':')))
                start_ = list(map(lambda x: int(x), start.split(' ')[1].split(':')))
                rt = end_[0] * 3600 + end_[1] * 60 + end_[2] - (start_[0] * 3600 + start_[1] * 60 + start_[2])
                ops_321[start.split(' ')[0]][index] = { 'data': [], 'runtime': rt, 'count': 0, 'hc': headercard, 'rejects': rejects, 'events': events, 'logs': logs }

            ops_321[start.split(' ')[0]][index]['data'].append (d)
            ops_321[start.split(' ')[0]][index]['count'] += int(d['number'])

        else:
            if index not in ops_320[start.split(' ')[0]]:
                end_ = list(map(lambda x: int(x), end.split(' ')[1].split(':')))
                start_ = list(map(lambda x: int(x), start.split(' ')[1].split(':')))
                rt = end_[0] * 3600 + end_[1] * 60 + end_[2] - (start_[0] * 3600 + start_[1] * 60 + start_[2])
                ops_320[start.split(' ')[0]][index] = { 'data': [], 'runtime': rt, 'count': 0, 'hc': headercard, 'rejects': rejects, 'events': events, 'logs': logs }

            ops_320[start.split(' ')[0]][index]['data'].append (d)
            ops_320[start.split(' ')[0]][index]['count'] += int(d['number'])
            

out_321 = {}
for key in sorted(ops_321):
    batches = {}
    for batch in sorted(ops_321[key]):
        batches[batch] = ops_321[key][batch]
    out_321[key] = batches


f = open("C:/Users/Public/js/currency-report/src/assets/320/operations_320.json",)
data = json.load(f)
f.close

for x in ops_320:
    if x not in data:
        data[x] = ops_320[x]

out_320 = {}
for key in sorted(data):
    batches = {}
    for batch in sorted(data[key]):
        batches[batch] = data[key][batch]
    out_320[key] = batches
        
f = open("C:/Users/Public/js/currency-report/src/assets/320/operations_320.json", "w")
f.write(json.dumps(out_320, indent=4))
f.close()
        

f = open("C:/Users/Public/js/currency-report/src/assets/321/operations_321.json",)
data = json.load(f)
f.close

for x in ops_321:
    if x not in data:
        data[x] = ops_321[x]

out_321 = {}
for key in sorted(data):
    batches = {}
    for batch in sorted(data[key]):
        batches[batch] = data[key][batch]
    out_321[key] = batches

f = open("C:/Users/Public/js/currency-report/src/assets/321/operations_321.json", "w")
f.write(json.dumps(out_321, indent=4))
f.close()