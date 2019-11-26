import csv
import itertools
import os

import Divergence

input_dir = "Inputs"
output_dir = "Distributions"
d = os.path.abspath(output_dir)
if not os.path.exists(d):
    os.makedirs(d)

f = open("brackets.txt", 'r')
min_val = int(f.readline())
max_val = int(f.readline())
f.close()

for file in os.listdir(input_dir):
    print("Processing: ", file)
    with open("%s/%s" % (input_dir, file), 'r') as ifile:
        reader = csv.reader(ifile)
        distribution = Divergence.histogramNaive(min_val, max_val, (int(row[2]) for row in itertools.islice(reader, 0, None)))
        with open("%s/%s" % (output_dir, file), 'w') as ofile:
            for i in distribution:
                ofile.write("%d,%f\n" % (i, distribution[i]))
