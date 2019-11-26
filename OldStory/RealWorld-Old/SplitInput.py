import csv
from itertools import *
from datetime import date
import os

#fname = input("File Name: ")
#path = input("Output Directory: ")
fname = "1629.csv"
dirpath = "./Inputs"
d = os.path.abspath(dirpath)
print("Split files into: ", d)
if not os.path.exists(d):
    os.makedirs(d)

base_date = date(2015, 7, 1)
ofiles = {}

with open(fname) as file:
    reader = csv.reader(file)
    for row in islice(reader, 0, None):
        paras = row[2].split(' ')[0].split('-')
        row_date = date(int(paras[0]), int(paras[1]), int(paras[2]))
        days = (row_date - base_date).days
        if days not in ofiles:
            ofiles[days] = open("%s/%d.csv" % (dirpath, days), "w")
        ofiles[days].write(row[0] + ',' + row[1] + ',' + row[2] + '\n')

for of in ofiles:
    ofiles[of].close()
