import csv
import math
import os
import statistics
from itertools import *

import matplotlib

import Divergence

matplotlib.use('Agg')
import matplotlib.pyplot as plt


input_dir = "Frequencies"
input_dir_cen = "Fake_Centralized_Frequencies"
input_dir_equ = "Fake_Equalized_Frequencies"
dists = []
dists_cen = []
dists_equ = []

for file in os.listdir(os.path.abspath(input_dir)):
    with open("%s/%s" % (input_dir, file), 'r') as f:
        reader = csv.reader(f)
        dists += [Divergence.getDistribution(list(int(row[1]) for row in islice(reader, 0, None)))]

for file in os.listdir(os.path.abspath(input_dir_cen)):
    with open("%s/%s" % (input_dir_cen, file), 'r') as f:
        reader = csv.reader(f)
        dists_cen += [Divergence.getDistribution(list(int(row[1]) for row in islice(reader, 0, None)))]

for file in os.listdir(os.path.abspath(input_dir_equ)):
    with open("%s/%s" % (input_dir_equ, file), 'r') as f:
        reader = csv.reader(f)
        dists_equ += [Divergence.getDistribution(list(int(row[1]) for row in islice(reader, 0, None)))]

total_distribution = Divergence.blendDistributions(dists)
jsds = []
jsds_fake_centralized = []
jsds_fake_equalized = []

for distribution in dists:
    jsds += [Divergence.jsd(distribution, total_distribution)]

for distribution in dists_cen:
    jsds_fake_centralized += [Divergence.jsd(distribution, total_distribution)]

for distribution in dists_equ:
    jsds_fake_equalized += [Divergence.jsd(distribution, total_distribution)]

mu = statistics.mean(jsds)
sigma = math.sqrt(statistics.variance(jsds))
print(jsds)
print("mu: %f" % (mu))
print("sigma: %f" % (sigma))

figure = plt.figure()
zeros = [0] * len(jsds)
plt.plot(jsds, zeros, "ro", ms=1, label="normal")
plt.plot(jsds_fake_centralized, [0.5] * len(jsds), "bo", ms=1, label="centralized")
plt.plot(jsds_fake_equalized, [-0.5] * len(jsds), "go", ms=1, label="equalized")
plt.legend()
plt.grid()
plt.savefig("CompareFrequency.png", dpi=300)
