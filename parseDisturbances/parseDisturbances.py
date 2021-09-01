import xml.etree.ElementTree as ET
import json

from os import walk
# importing required modules

import PyPDF2
import re

path = "C:\\Users\\NTAZINDA\\Downloads\\year\\320\\"

_, _, filenames = next(walk(path + "dist\\"))
disturbancesObject = {}
st = ''

for filename in filenames:
    disturbances = open (path + "dist\\" + filename, 'rb')
    disturbancesReader = PyPDF2.PdfFileReader(disturbances)

    print (filename)

    dist = ''

    for j in range(disturbancesReader.numPages):
        pageObj = disturbancesReader.getPage(j)
        for i in pageObj.extractText().splitlines():
            if re.match(r'^\d\d\.\d\d\.\d\d', i) or i == '':
                continue
            if re.match(r'^\d+', i):
                st = re.sub (r'[^a-zA-Z]', ' ', st).strip()
                st = re.sub (r' s$', '', st).strip()
                st = re.sub (r' +', ' ', st).strip()
                if  (st != ''):
                    if 'Disturbance Messages' in st:
                        st = re.sub (r'Disturbance Messages', '###', st)
                        st = re.sub (r'Count', '###', st)
                        # st = re.sub (r'[a-zA-Z]+ID', '', st)
                        # st = ">>>>> " + st.split ("###")[1].strip() + " <<<<<"
                        dist = st.split ("###")[1].strip()
                        if dist not in disturbancesObject:
                            disturbancesObject[dist] = []
                    else:
                        if st.find('ProductionBPS') == -1:
                            disturbancesObject[dist].append(st.lower())
                st = i
            else:
                st += i

    disturbances.close()

print (json.dumps(disturbancesObject, indent=4))

f = open(path + "dist.json", "w")
f.write(json.dumps(disturbancesObject, indent=4))
f.close()