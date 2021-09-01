import xml.etree.ElementTree as ET
import json

import PyPDF2
import re

import statistics

from numpy import cov
from scipy.stats.stats import pearsonr
  
path = 'C:/Users/NTAZINDA/Downloads/year/320/'
f1 = open(path + 'aggrDay.json',)
data = json.load(f1)
f2 = open(path + 'vms_data_perday.json',)
data2 = json.load(f2)

types = set ()
unwanted = set({'-', '', 'User log on/off', 'System Event', 'Prompt to user', 'Reporting'})

def ftolistperday (param):
    ret = {}
    for x in data:
        ret[x] = 0
        for xx in data[x]:
            types.add (xx['n'])
            if xx['m'] == param:
                ret[x] = xx['c']

    ret1 = []
    for x in ret:
        ret1.append (ret[x])

    return ret1
                
def ftolistperdayVms (param):
    ret = {}
    for x in data:
        ret[x] = 0
        if x not in data2:
            continue
        for xx in data2[x]:
            if xx == param:
                ret[x] = data2[x][xx]

    ret1 = []
    for x in ret:
        ret1.append (ret[x])

    return ret1

lst1 = ftolistperday ("DSC X - Bander controller: Bander error: Stacking area blocked (standing BN?)")
lst2 = ftolistperday ("SMC - Singler Gate Control: Please close the top cover of the singler.")

lst = {}

for x in data:
    for entry in data[x]:
        if entry['n'] not in unwanted and 'Error Log' not in entry['m']:
            if entry['m'] not in lst:
                lst[entry['m']] = ftolistperday (entry['m'])

lst['VMS - Generated Files Per Headercard'] = ftolistperdayVms ('generatedFilesPerHeaderCard')
lst['VMS - Processed banknotes'] = ftolistperdayVms ('countAll')
lst['VMS - runtime'] = ftolistperdayVms ('runtime')
lst['VMS - headercards'] = ftolistperdayVms ('headercards')
lst['VMS - speed uninterrupted'] = ftolistperdayVms ('speed')
lst['VMS - day length'] = ftolistperdayVms ('dayLength')
lst['VMS - overall speed'] = ftolistperdayVms ('daySpeed')

label = 'VMS - speed uninterrupted'

def withoutZeroes (x):
    ret = []
    for _ in x:
        if _ != 0:
            ret.append (_)

    return ret

x = withoutZeroes (lst[label])

print (label, 'mean: ', statistics.mean (x))
print (label, 'median: ', statistics.median (x))
# print (label, 'mode: ', statistics.multimode (x))
print (label, 'standard deviation: ', statistics.stdev (x))

x.sort()

print (label, 'max: ', x[-1])
print (label, 'min: ', x[0])


ret = []
done = {}

def makeCorrelations():
    for x in lst:
        print ('.')
        for y in lst:
            if y + '' + x not in done and x != y:
                done[x + '' + y] = 1
                c,p = pearsonr(lst[x],lst[y])
                # p value means random chances generated the data, or something that is equal or rarer (some constant value)
                # p value threshold for significance: .05
                # p value measures the strength of evidence against bias => null hypothesis: the 2 populations are identical
                # 2% means there is so much chances of observing a difference as large (or larger) than what we observed in our sample.
                # hypothesis testing
                if p < .05: # the smaller the value, the stronger the evidence.
                    ret.append({'c': float("{:.2f}".format(c * 100)), 'p': float("{:.2f}".format(p * 100)), 'x':x, 'y':y })

    ret.sort(key=lambda x: x['c'], reverse=True)

    print(types)

    f = open(path + "correlations.json", "w")
    f.write(json.dumps(ret, indent=4))
    f.close()