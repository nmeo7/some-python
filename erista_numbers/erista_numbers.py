from openpyxl import load_workbook, Workbook
import json

def char_range(c1, c2):
    for c in range(ord(c1), ord(c2)+1):
        yield chr(c)

wb = load_workbook(filename = "C:/Users/NTAZINDA/Downloads/C I C 24 08 2021.xlsx")
sheet_ranges = wb['Curency in circulation']

out = {}

for x in range(1, 77):
    xx = {}
    for y in char_range ('A', 'N'):
        xx[y] = sheet_ranges[ y + str(x)].value
    out[str(x)] = xx

wb = load_workbook(filename = "C:/Users/NTAZINDA/Downloads/C I C 24 08 2021.xlsx", data_only = True)
sheet_ranges = wb['Curency in circulation']

series = ( '2003-2004', '2007', '2008', '2009', '2011', '2013', '2014', '2015', '2019' )
denomination = [ 1, 5, 10, 20, 50, 100, 500, 1000, 2000, 5000 ]

def retrieve_range(st, end):
    ret = {}
    for x in range (st, end + 1):
        s = str(sheet_ranges[ 'C' + str(x) ].value)
        if s in series:
            ret[s] = []

            for y in  char_range('D', 'N'):
                n = sheet_ranges[ y + str(x)].value
                if n is None:
                    n = 0
                else:
                    n = int (1000 * n)

                ret[s].append (n)
    return ret

def retrieve_range_branch(st, end):
    ret = {}
    for x in char_range('C', 'N'):
        s = str(sheet_ranges[ x + '4' ].value)
        ret[s] = 0
        
        for y in range (st, end + 1):
            n = sheet_ranges[ x + str(y)].value
            if n is None:
                n = 0
            else:
                n = int (1000 * n)

            ret[s] += n
    return ret

def retrieve_line_hq(line):
    ret = []
    for x in char_range('C', 'L'):
        n = str(sheet_ranges[ x + str(line) ].value)

        try:
            n = int (1000 * int(n))
        except:
            n = 0

        ret.append(n)
    return ret

def retrieve_laila ():
    ret = []
    for x in range(19, 25):
        n = str(sheet_ranges[ 'D' + str(x) ].value)
        try:
            n = int (1000 * int(n))
        except:
            n = 0
        ret.append(n)

    for x in range(6, 10):
        n = str(sheet_ranges[ 'D' + str(x) ].value)
        try:
            n = int (1000 * int(n))
        except:
            n = 0
        ret.append(n)

    return ret

def retrieve_line (l):
    return retrieve_range (l, l)

printed = retrieve_range (4, 12)
uncirculated = retrieve_range (14, 23)
crushed = retrieve_range (25, 32)
net = retrieve_range (34, 42)


branches_unfit = {
    'musanze': retrieve_line(53),
    'rubavu': retrieve_line(56),
    'huye': retrieve_line(59),
    'rusizi': retrieve_line(62),
    'rwamagana': retrieve_line(65)
}

branches_not_unfit = {
    'musanze': retrieve_line(52),
    'rubavu': retrieve_line(55),
    'huye': retrieve_line(58),
    'rusizi': retrieve_line(61),
    'rwamagana': retrieve_line(64)
}

main_cash_desk = retrieve_line(49)

cs_fit = retrieve_line(44)
cs_unfit = retrieve_line(45)
cs_tobe_sorted = retrieve_line(46)
cs_untreated = retrieve_line(47)

# print (json.dumps(printed, indent=4))
# print (json.dumps(uncirculated, indent=4))
# print (json.dumps(crushed, indent=4))
# print (json.dumps(net, indent=4))




wb = load_workbook(filename = "C:/Users/NTAZINDA/Downloads/Musanze Cash Balance Situation 25.08.2021.xlsx", data_only = True)
sheet_ranges = wb['25-08-2021']

from_branches_not_unfit = {
    'musanze': retrieve_range_branch (5, 7)
}

from_branches_unfit = {
    'musanze': retrieve_range_branch (8, 8)
}

# print (json.dumps(from_branches_unfit, indent=4))
# print (json.dumps(from_branches_not_unfit, indent=4))




wb = load_workbook(filename = "C:/Users/NTAZINDA/Downloads/HQ Daily Cash Situation report 25.08.2021.xlsx", data_only = True)
sheet_ranges = wb['Cash situation report']
hq = {
    'fit': retrieve_line_hq (9),
    'unfit': retrieve_line_hq (10),
    'mixed': retrieve_line_hq (11),
    'untreated': retrieve_line_hq (12),
    'new': retrieve_line_hq (13)
}

# print (json.dumps(hq, indent=4))


wb = load_workbook(filename = "C:/Users/NTAZINDA/Downloads/CAISSE RWF Laila 25.08.2021.xlsx", data_only = True)
sheet_ranges = wb['Summary Report']
retrieve_laila = retrieve_laila ()
print (json.dumps(retrieve_laila, indent=4))


wb = Workbook()
ws = wb.active

for x in range(1, 77):
    for y in char_range ('A', 'N'):
        ws[y + str(x)] = out[str(x)][y]

wb.save("C I C 24 08 2021.xlsx")