import csv
from itertools import *
from datetime import time
import os
import random

input_dir = "Inputs"
output_dir = "Fake_Equalized_Frequencies"
d = os.path.abspath(output_dir)
if not os.path.exists(d):
    os.makedirs(d)

for file in os.listdir(os.path.abspath(input_dir)):
    print("Processing: " + file)
    with open("%s/%s" % (input_dir, file), "r") as f:
        freq = {}
        cnt = 0
        reader = csv.reader(f)
        for row in islice(reader, 0, None):
            hour = int(row[2].split(' ')[1].split(":")[0])
            if hour in freq:
                freq[hour] += 1
            else:
                freq[hour] = 1

        for i in freq:
            freq[i] *= int(random.uniform(2.0, 3.0))
            cnt += freq[i]

        with open("%s/%s" % (output_dir, file), 'w') as of:
            for i in freq:
                of.write("%d,%d,%f\n" % (i, freq[i], freq[i] / cnt))
