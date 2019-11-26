import csv
import os
import itertools
import random


input_dir = "../RealWorld/Inputs"
output_dir = "Inputs"
d = os.path.abspath(output_dir)
if not os.path.exists(d):
    os.makedirs(d)

for file in os.listdir(input_dir):
    ifile = open("%s/%s" % (input_dir, file), 'r')
    ofile = open("%s/%s" % (output_dir, file), 'w')
    reader = csv.reader(ifile)
    for row in itertools.islice(reader, 0, None):
        hh = int(row[2].split(" ")[1].split(":")[0])
        mm = random.randint(0, 59)
        ss = random.randint(0, 59)
        t = hh * 3600 + mm * 60 + ss
        ofile.write("%s,%s,%d\n" % (row[0], row[1], t))
    ifile.close()
    ofile.close()
