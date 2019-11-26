import csv
from itertools import *
from datetime import time
import os
import random

input_dir = "Inputs"
output_dir = "Fake_Centralized_Frequencies"
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
            cnt += 1
            hour = int(row[2].split(' ')[1].split(":")[0])
            if hour in freq:
                freq[hour] += 1
            else:
                freq[hour] = 1

        # Randomly modify records in 1 to 5 hours
        n = random.randint(1, 3)
        tmp = list(freq.keys())
        for i in range(0, n):
            ridx = random.randint(0, len(tmp) - 1)
            idx = tmp[ridx]
            del tmp[ridx]
            new_freq = int(freq[idx] * random.uniform(5.0, 7.0))
            cnt += new_freq - freq[idx]
            freq[idx] = new_freq

        with open("%s/%s" % (output_dir, file), 'w') as of:
            for i in freq:
                of.write("%d,%d,%f\n" % (i, freq[i], freq[i] / cnt))
