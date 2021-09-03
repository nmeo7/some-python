import xml.etree.ElementTree as ET
import json
import sys

from os import walk
# importing required modules

import PyPDF2
import re

operationsPath = ""
if len(sys.argv) > 1:
    operationsPath = sys.argv[1]
else:
    operationsPath = input()

operations = open (operationsPath, 'rb')
operationsReader = PyPDF2.PdfFileReader(operations)

# if 'M01000320' in operationsPath:
    # print ('Machine: 320')
# elif 'M01000321' in operationsPath:
    # print ('Machine: 321')
# else:
    # print ('Machine: Unknown')

st = ''

def reformatDate (date):
    d = date.split(".")
    return d[2] + "-" + d[1] + "-" + d[0]


def removeNumbersString (st):
    st = re.sub (r': [X0-9]+', ': X', st)
    st = re.sub (r'[X0-9]+ / [X0-9]+', 'X / X', st)
    st = re.sub (r'Operator [X0-9]+', 'Operator X', st)
    st = re.sub (r'ID = [X0-9]+', 'ID = X', st)
    st = re.sub (r'DSC [X0-9]+ - BNP: Initialization is active \(Stacker [X0-9]+\)', 'DSC X - BNP: Initialization is active (Stacker X)', st)
    st = re.sub (r'[X0-9]+ banknote', 'X banknote', st)

    return st

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

        st = re.sub (r' KGL', '', st)

        if re.match(r'^\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', st) and st[20:] != '':
            if re.match(r'^\d\d:\d\d:\d\d', st[20:]):
                # print (st[:20] + '\t' + st[20:28] + '\t' + st[28:])
                return { 't': st[:20], 'd': st[20:28], 'm': st[28:].strip(), 'n': nature }
            else:
                # print (st[:20] + '\t00:00:00\t' + st[20:])
                return { 't': st[:20], 'd': '00:00:00', 'm': st[20:].strip(), 'n': nature }

def appendMessage (msg, log2):

    if msg['m'] == log2['m']:
        return { 'm': msg['m'], 's': msg['s'],  'e': log2['t'], 'd': log2['d'] }

    return { 'm': log2['m'], 's': log2['s'],  'e': log2['t'], 'd': log2['d'] }

def summarizeMessages (logs):
    ret = {}

    lastMsg = ''

    for x in logs:
        ret[x] = []

        for y in logs[x]:
            m = removeNumbersString (y['m'])
            if lastMsg == 'HC-Recovery' and m == 'End HC-Recovery:':
                lastMsg = ''
                continue
            elif lastMsg == 'HC-Recovery':
                continue
            if m == 'Begin HC-Recovery:':
                m = 'HC-Recovery'

            if m == lastMsg:
                # ret[x][-1]['e'] = y['t']
                # ret[x][-1]['d'] = y['d']
                a = ret[x][-1]['m']
            else:
                ret[x].append ({ 't': y['t'], 'm': m }) # ({ 'm': m, 'd': y['d'], 's': y['t'], 'e': y['t'] })
                lastMsg = m

    return ret


def onlyMessages (msgs):
    ret = {}
    for x in msgs:
        ret[x] = []
        for y in msgs[x]:
            ret[x].append(y['m'])

    return ret




def ignoreLine (st):
    if re.match(r'.*int774b.*', st) or st == 'Production' or re.match(r'BPS M7.*1000.*', st) or re.match(r'Page.+of.+', st):
        return True
    if re.match(r'\d\d\.\d\d\.2021, \d\d:\d\d:\d\d.*\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', st):
        return True
    if (re.match(r'START.*DURATION.*OPERATION', st)):
        return True
    if re.match(r'.*Total duration.*', st):
        return True
    if re.match(r'OPERATION LOG.*', st):
        return True
    return False

def parseDays ():
    st = ''

    ret = {}

    for j in range(operationsReader.numPages):
        pageObj = operationsReader.getPage(j)
        for i in pageObj.extractText().splitlines():
            if ignoreLine(i):
                continue

            if re.match(r'^\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', i):
                r = printString (st)
                if (r):
                    dd = reformatDate(r["t"].split(", ")[0])
                    r["t"] = r["t"].split(", ")[1]
                    if (dd not in ret):
                        ret[dd] = []
                    ret[dd].append(r)
                st = i
            else:
                st += i

    r = printString (st)
    if (r):
        dd = reformatDate(r['t'].split(', ')[0])
        r["t"] = r["t"].split(", ")[1]
        if (dd not in ret):
            ret[dd] = []
        ret[dd].append(r)

    return ret

def parseAggregates ():
    st = ''

    ret = {}

    for j in range(operationsReader.numPages):
        pageObj = operationsReader.getPage(j)
        for i in pageObj.extractText().splitlines():
            if ignoreLine(i):
                continue

            if re.match(r'^\d\d\.\d\d\.2021, \d\d:\d\d:\d\d', i):
                r = printString (st)
                if (r):
                    dd = r["t"].split(", ")[0]
                    r["t"] = r["t"].split(", ")[1]
                    if (dd not in ret):
                        ret[dd] = {}
                    if (r["m"] not in ret[dd]):
                        ret[dd][r["m"]] = 0
                    ret[dd][r["m"]] += 1
                st = i
            else:
                st += i

    r = printString (st)
    if (r):
        dd = r['t'].split(', ')[0]
        r["t"] = r["t"].split(", ")[1]
        if (dd not in ret):
            ret[dd] = {}
        if (r["m"] not in ret[dd]):
            ret[dd][r["m"]] = 0
        ret[dd][r["m"]] += 1

    ret2 = {}
    for x in ret:
        ret2[x] = dict(sorted(ret[x].items(), key=lambda item:item[1], reverse=True))

    return ret2

def removeNumbers (dictIn):
    ret = {}

    for x in dictIn:
        x1 = removeNumbersString (x)
        if (x1 not in ret):
            ret[x1] = 0
        ret[x1] += dictIn[x]

    return dict(sorted(ret.items(), key=lambda item:item[1], reverse=True))

# ret = parseAggregates ()
# ret = removeNumbers ( ret )

if 'M01000320' in operationsPath:
    filename = "320/logs_320.json"
elif 'M01000321' in operationsPath:
    filename = "321/logs_321.json"

filename = 'C:/Users/Public/js/currency-report/src/assets/' + filename

def appendToFile ():
    data = {}


    f = open(filename,)
    data = json.load(f)
    f.close

    for x in ret:
        if x not in data:
            data[x] = ret[x]
            
    f = open(filename, "w")
    f.write(json.dumps(data, indent=4))
    f.close()

def createFile ():
    f = open(filename.split('/')[-1], "w")
    f.write(json.dumps(ret, indent=4))
    f.close()
           
def summarizeDays():
    ret = parseDays()
    data = summarizeMessages (ret)
    # data = onlyMessages ( summarizeMessages (ret) )

    f = open(filename, "w")
    f.write(json.dumps(data, indent=4))
    f.close()

    operations.close()

# print(json.dumps(ret, indent=4))
# sys.stdout.flush()

ret = parseDays ()
appendToFile ()

# ret = parseAggregates ()
# createFile ()