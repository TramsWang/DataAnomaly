import csv
import itertools
import os

input_dir = "Correct"
output_dir = "Equalized"

if not os.path.exists(os.path.abspath(output_dir)):
    os.makedirs(output_dir)

for i in range(325):
    ifile = open("%s/%d.csv" % (input_dir, i), 'r')
    ofile = open("%s/%d.csv" % (output_dir, i), 'w')
    for line in ifile:
        ofile.write(line)
        ofile.write(line)
    ifile.close()
    ofile.close()

