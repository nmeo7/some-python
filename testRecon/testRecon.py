import xml.etree.ElementTree as ET
import json

import PyPDF2
import re
  
path = 'C:/Users/NTAZINDA/Downloads/year/320/'
f = open(path + 'aggr.json',)
data = json.load(f)

c = 0
b = 0
i = 0
for x in data:
    if i < 13:
        b += x['c']
    i = i + 1
    c += x['c']

a = 25643 + 22876 + 18406 + 15756 + 14986 + 14419 + 12644 + 11655 + 11125 + 12903
print (a, c, a * 100 / c, b * 100 / c)