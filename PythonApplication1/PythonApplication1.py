import math
import decimal

from functions import solve
# from matplotlib import pyplot as plt
from collections import Counter
from math import sqrt
import random

import xml.etree.ElementTree as ET

import json

# Opening JSON file
f = open("C:/Users/NTAZINDA/Downloads/320_out.json",)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
  
# Iterating through the json
# list
for i in data:
    print(i)
  
# Closing file
f.close()


tree = ET.parse('C:/Users/NTAZINDA/Downloads/data/320/FTXMoved/BPSAbrData_1000320_20210323_141752_0_1.xml')
root = tree.getroot()

print (root)

T = int(input())
for t in range(1, T + 1):
    w,h,l,u,r,d = map(int,input().split())

    p = 0

    if r < w:
        curr = decimal.Decimal(0.5) ** r
        for i in range(u - 1):
            #print(curr)
            p += curr
            curr *= (r + i)
            curr /= (i + 1)
            curr /= 2

    if d < h:
        curr = decimal.Decimal(0.5) ** d
        for i in range(l - 1):
            p += curr
            curr *= (d + i)
            curr /= (i + 1)
            curr /= 2
            
    print("Case #{0}: {1}".format(t,p))
