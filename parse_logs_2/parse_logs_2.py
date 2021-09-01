import xml.etree.ElementTree as ET
import json

from os import walk

import PyPDF2
import re

path = "C:\\Users\\NTAZINDA\\Downloads\\year\\320\\"
date = '26.03.2021, 17:08:08'
date = '26.03.2021, 16:51:49'

operations = open (path + "M01000320_20210326_170755_Operation Log.pdf", 'rb')

operationsReader = PyPDF2.PdfFileReader(operations)

st = ''
dist = ''

print ("starting...")

def printString (st):
    if (st != ''):
        st1 = re.sub (r'[^a-zA-Z]', '', st).lower()
        nature = ''
                    
        if 'logged' in st1:
            nature = 'User log on/off'
        if 'error' in st1 or 'failure' in st1:
            nature = 'Error or Failure'
        if 'preparingreport' in st1 or 'logdata' in st1 or 'analysisdata' in st1 or 'errorlog' in st1:
            nature = 'Reporting'
        if 'systemevent' in st1:
            nature = 'System Event'
        if 'please' in st1:
            nature = 'Prompt to user'
        if 'callservice' in st1:
            nature = 'Escalation Needed'

        if re.match(r'^\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', st) and st[20:] != '':
            if re.match(r'^\d\d:\d\d:\d\d', st[20:]):
                # print (st[:20] + '\t' + st[20:28] + '\t' + st[28:])
                return { 't': st[:20], 'd': st[20:28], 'm': st[28:].strip(), 'n': nature }
            else:
                # print (st[:20] + '\t00:00:00\t' + st[20:])
                return { 't': st[:20], 'd': '00:00:00', 'm': st[20:].strip(), 'n': nature }

st = ''

ret = {}

for j in range(operationsReader.numPages):
    pageObj = operationsReader.getPage(j)
    for i in pageObj.extractText().splitlines():
        if re.match(r'.*int774b.*', i) or i == 'Production' or re.match(r'BPS M7.*1000.*', i) or re.match(r'Page.+of.+', i):
            continue
        if (i == date):
            continue
        if re.match(r'\d\d\.\d\d\.2021, \d\d:\d\d:\d\d.*\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', i):
            continue
        if (re.match(r'START.*DURATION.*OPERATION', i)):
            continue
        if re.match(r'.*Total duration.*', i):
            continue
        if re.match(r'^\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', i):
            r = printString (st)
            if (r):
                dd = r["t"].split(", ")[0]
                r["t"] = r["t"].split(", ")[1]
                if (dd not in ret):
                    ret[dd] = []
                ret[dd].append(r)
            st = i
        else:
            st += i

r = printString (st)

if (r):
    dd = r['t'].split(', ')[0]
    r["t"] = r["t"].split(", ")[1]
    if (dd not in ret):
        ret[dd] = []
    ret[dd].append(r)
    
print ("done.")
    
f = open(path + "logs1.json", "w")
f.write(json.dumps(ret, indent=4))
f.close()
    
# closing the pdf file object
operations.close()