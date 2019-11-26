import csv
from itertools import *
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

input_dir = "Distributions"
output_dir = "Ecdfs"
d = os.path.abspath(output_dir)
if not os.path.exists(d):
    os.makedirs(d)

figure = plt.figure()
for file in os.listdir(os.path.abspath(input_dir)):
    print("Processing: " + file)
    with open("%s/%s" % (input_dir, file), 'r') as f:
        reader = csv.reader(f)
        prob = {}
        for row in islice(reader, 0, None):
            prob[int(row[0])] = float(row[1])

        cprob = 0.0
        y = []
        x = range(-500, 1500)
        for i in x:
            if i in prob:
                cprob += prob[i]
            y += [cprob]

        plt.plot(x, y)
        plt.savefig("%s/%s.png" % (output_dir, file))
        figure.clear()