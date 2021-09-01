import xml.etree.ElementTree as ET
import json

import PyPDF2
import re

import statistics

from numpy import cov
from scipy.stats.stats import pearsonr

machine = "320"

# C:/Users/NTAZINDA/source/repos/PythonApplication1/parse_vms_files/operations_320.json
file = 'C:/Users/NTAZINDA/source/repos/PythonApplication1/parse_vms_files/operations_' + machine + '.json' # input()

f = open(file,)
data = json.load(f)
f.close()

logs = set ()

def get_all_logs ():
    ret = {}

    for x1 in data:
        for x2 in data[x1]:
            for x3 in data[x1][x2]['logs']:
                if x3 not in ret:
                    ret[x3] = 0
                ret[x3] = ret[x3] + data[x1][x2]['logs'][x3]

    return dict(sorted(ret.items(), key=lambda item:item[1], reverse=True))

def get_all_days ():
    ret = []

    for x1 in data:
        ret.append (x1)

    return sorted(ret)

def logs_per_batch(param):
    ret = {}

    for x1 in data:
        for x2 in data[x1]:
            ret[x1 + ' ' + x2] = 0
            for x3 in data[x1][x2]['logs']:
                if x3 == param:
                    ret[x1 + ' ' + x2] = data[x1][x2]['logs'][x3]
                    break

    ret1 = []
    for x in ret:
        ret1.append (ret[x])

    return ret1

def quality_per_batch(quality):
    ret = {}

    for x1 in data:
        for x2 in data[x1]:
            ret[x1 + ' ' + x2] = 0
            for x3 in data[x1][x2]['data']:
                if x3['quality'] == quality:
                    ret[x1 + ' ' + x2] = ret[x1 + ' ' + x2] + int(x3['number'])

    ret1 = []
    for x in ret:
        ret1.append (ret[x])

    return ret1

def params_per_batch():
    ret = {}

    for x1 in data:
        for x2 in data[x1]:
            ret[x1 + ' ' + x2] = 0
            speed = 22
            if data[x1][x2]['runtime'] > 0:
                speed = data[x1][x2]['count'] / data[x1][x2]['runtime']
            ret[x1 + ' ' + x2] = { 
                'runtime': data[x1][x2]['runtime'], 
                'count': data[x1][x2]['count'], 
                'speed': speed }

    ret1 = { 'runtime': [], 'count': [], 'speed': [] }
    for x in ret:
        ret1['runtime'].append (ret[x]['runtime'])
        ret1['count'].append (ret[x]['count'])
        ret1['speed'].append (ret[x]['speed'])

    return ret1

def params_per_day():
    ret = {}

    for x1 in data:
        ret[x1] = {
            'runtime': 0,
            'count': 0
            }
        for x2 in data[x1]:
            ret[x1] = { 
                'runtime': ret[x1]['runtime'] + data[x1][x2]['runtime'] / 3600, 
                'count': ret[x1]['count'] + data[x1][x2]['count'] }

    ret1 = { 'runtime': [], 'count': [] }
    print (json.dumps(ret))
    for x in ret:
        ret1['runtime'].append (ret[x]['runtime'])
        ret1['count'].append (ret[x]['count'])

    return ret1


def makeAggregates():
    res = params_per_day()
    days = len(get_all_days ())
    res['count'].sort()
    res['runtime'].sort()
    counts = {
        'mean': statistics.mean (res['count']),
        'median': statistics.median (res['count']),
        # 'mode': statistics.mode (res['count']),
        'stdev': statistics.stdev (res['count']),
        'min': res['count'][0],
        'max': res['count'][-1]
    }

    runtimes = {
        'mean': statistics.mean (res['runtime']),
        'median': statistics.median (res['runtime']),
        # 'mode': statistics.mode (res['runtime']),
        'stdev': statistics.stdev (res['runtime']),
        'min': res['runtime'][0],
        'max': res['runtime'][-1]
    }
    data = { 'days': len(get_all_days ()), 'counts': counts, 'runtimes': runtimes, 'logs': get_all_logs () }
    f = open("logs_" + machine + ".json", "w")
    f.write(json.dumps(data, indent=4))
    f.close()

lst = {}

logs = get_all_logs()

for x in logs:
    lst[x] = logs_per_batch(x)

for x in ['Fit', 'Shredded', 'ATM']:
    lst[x] = quality_per_batch(x)

res = params_per_batch()
# lst['runtime'] = res['runtime']
# lst['count'] = res['count']
# lst['speed'] = res['speed']

# print ('count ', 'mean: ', statistics.mean (res['count']))
# print ('count ', 'median: ', statistics.median (res['count']))
# print (label, 'mode: ', statistics.multimode (x))
# print ('count ', 'standard deviation: ', statistics.stdev (res['count']))
# print (json.dumps(res['count'], indent=4))

# res['runtime'].sort()

# print ('runtime ', 'max: ', x['runtime'][-1])
# print ('runtime ', 'min: ', x['runtime'][0])

done = {}

def remove_nulls (x, y):
    x2 = []
    y2 = []

    for i in range(0, len(x)):
        if x[i] > 1:
            x2.append(x[i])
            y2.append(y[i])

    return x2, y2

# m = statistics.median (res['count'])
# print ('count ', 'median: ', m)
def remove_small_batches(x):
    ret = []
    for i in range(0, len(res['count'])):
        if res['count'][i] >= 100:
            ret.append(x[i])

    return ret

# data = { 'params': lst, 'res': res }

# f = open("data_" + machine + ".json", "w")
# f.write(json.dumps(data, indent=4))
# f.close()


def makeCorrelations():
    ret = []
    
    for y in lst:
        x1 = remove_small_batches (lst[y])
        y1 = remove_small_batches (res['speed'])
        
        x1, y1 = remove_nulls(x1, y1)
        if ( len(x1) > 2 ):
        
            c,p = pearsonr(x1, y1)
        
            # p value means random chances generated the data, or something that is equal or rarer (some constant value)
            # p value threshold for significance: .05
            # p value measures the strength of evidence against bias => null hypothesis: the 2 populations are identical
            # 2% means there is so much chances of observing a difference as large (or larger) than what we observed in our sample.
            # hypothesis testing
            if p < 1: #< .05: # the smaller the value, the stronger the evidence.
                ret.append({'c': float("{:.2f}".format(c * 100)), 'p': float("{:.2f}".format(p * 100)), 'y': y, 'o': len(x1) })

    ret.sort(key=lambda x: x['c'], reverse=True)

    f = open("correlations_" + machine + ".json", "w")
    f.write(json.dumps(ret, indent=4))
    f.close()

makeCorrelations()