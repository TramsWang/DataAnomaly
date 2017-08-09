import csv
import itertools
import os

dir = "Equalized"

if not os.path.exists(os.path.abspath(dir)):
    os.makedirs(os.path.abspath(dir))

for i in range(325):
    ifile = open("../Synthetic/%s/%d.csv" % (dir, i), 'r')
    ofile = open("%s/%d.csv" % (dir, i), 'w')
    reader = csv.reader(ifile)
    for row in reader:
        ofile.write("%s,%s,%d\n" % (row[0], row[1], int(row[2]) / 3600))
    ifile.close()
    ofile.close()
