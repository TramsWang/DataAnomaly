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
input_dir_fake_centralized = "Fake_Centralized_Frequencies"
input_dir_fake_equalized = "Fake_Equalized_Frequencies"
distributions = []
distributions_fake_centralized = []
distributions_fake_equalized = []

for file in os.listdir(os.path.abspath(input_dir)):
    with open("%s/%s" % (input_dir, file), 'r') as f:
        reader = csv.reader(f)
        distribution = {}
        for row in islice(reader, 0, None):
            distribution[int(row[0])] = float(row[2])
        distributions += [distribution]

for file in os.listdir(os.path.abspath(input_dir_fake_centralized)):
    with open("%s/%s" % (input_dir_fake_centralized, file), 'r') as f:
        reader = csv.reader(f)
        distribution = {}
        for row in islice(reader, 0, None):
            distribution[int(row[0])] = float(row[2])
        distributions_fake_centralized += [distribution]

for file in os.listdir(os.path.abspath(input_dir_fake_equalized)):
    with open("%s/%s" % (input_dir_fake_equalized, file), 'r') as f:
        reader = csv.reader(f)
        distribution = {}
        for row in islice(reader, 0, None):
            distribution[int(row[0])] = float(row[2])
        distributions_fake_equalized += [distribution]

total_distribution = Divergence.blendDistributions(distributions)
jsds = []
jsds_fake_centralized = []
jsds_fake_equalized = []

for distribution in distributions:
    jsds += [Divergence.jsd(distribution, total_distribution)]

for distribution in distributions_fake_centralized:
    jsds_fake_centralized += [Divergence.jsd(distribution, total_distribution)]

for distribution in distributions_fake_equalized:
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
plt.savefig("tmp.png", dpi=300)
