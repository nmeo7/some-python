import xml.etree.ElementTree as ET
import json

from os import walk
# importing required modules

import PyPDF2
import re

path = "C:\\Users\\NTAZINDA\\Downloads\\11.06.2021\\320\\"
date = '11.06.2021, 17:00:33'

operations = open (path + "M01000320_20210611_170027_Operation Log.pdf", 'rb')
disturbances = open (path + "M01000320_20210611_170045_Disturbance Log.pdf", 'rb')

operationsReader = PyPDF2.PdfFileReader(operations)
disturbancesReader = PyPDF2.PdfFileReader(disturbances)

st = ''

disturbancesObject = {}
dist = ''

for j in range(disturbancesReader.numPages):
    pageObj = disturbancesReader.getPage(j)
    for i in pageObj.extractText().splitlines():
        if re.match(r'^\d\d\.\d\d\.\d\d', i) or i == '':
            continue
        if re.match(r'^\d+', i):
            st = re.sub (r'[^a-zA-Z]', ' ', st).strip()
            st = re.sub (r' s$', '', st).strip()
            st = re.sub (r' +', ' ', st)
            if  (st != ''):
                if 'Disturbance Messages' in st:
                    st = re.sub (r'Disturbance Messages', '###', st)
                    st = re.sub (r'Count', '###', st)
                    st = re.sub (r'[a-zA-Z]+ID', '', st)
                    # st = ">>>>> " + st.split ("###")[1].strip() + " <<<<<"
                    dist = st.split ("###")[1].strip()
                    disturbancesObject[dist] = []
                else:
                    if st.find('ProductionBPS') == -1:
                        disturbancesObject[dist].append(re.sub (r'[^a-zA-Z]', '', st).lower())
            st = i
        else:
            st += i

disturbances.close()

def printString (st):
    if (st != ''):
        st1 = re.sub (r'[^a-zA-Z]', '', st).lower()
        nature = ''
                    
        if 'logged' in st1:
            nature = 'User log on/off'
        if 'preparingreport' in st1 or 'logdata' in st1 or 'analysisdata' in st1:
            nature = 'Reporting'
        if 'error' in st1:
            nature = 'Error'
        if 'systemevent' in st1:
            nature = 'System Event'
        if 'please' in st1:
            nature = 'Prompt to user'

        for key, value in disturbancesObject.items():
            for dist in value:
                if st1.find (dist) > -1:
                    nature = key

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
    
f = open(path + "logs.json", "w")
f.write(json.dumps(ret, indent=4))
f.close()
    
# closing the pdf file object
operations.close()