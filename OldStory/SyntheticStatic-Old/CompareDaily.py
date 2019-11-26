import csv
import itertools
import math
import os
import statistics

import matplotlib

import Divergence

matplotlib.use('Agg')
import matplotlib.pyplot as plt


input_dir = "Inputs"
input_dir_fake_centralized = "InputsCentralized"
input_dir_fake_equalized = "InputsEqualized"
distributions = []
distributions_fake_centralized = []
distributions_fake_equalized = []

f = open("brackets.txt", 'r')
min_val = int(f.readline())
max_val = int(f.readline())
f.close()

print("Calculating Distributions(Real)...")
for file in os.listdir(os.path.abspath(input_dir)):
    with open("%s/%s" % (input_dir, file), 'r') as f:
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records)
        distributions += [distribution]

print("Calculating Distributions(Centralized Cheating)...")
for file in os.listdir(os.path.abspath(input_dir_fake_centralized)):
    with open("%s/%s" % (input_dir_fake_centralized, file), 'r') as f:
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records)
        distributions_fake_centralized += [distribution]

print("Calculating Distributions(Equalized Cheating)...")
for file in os.listdir(os.path.abspath(input_dir_fake_equalized)):
    with open("%s/%s" % (input_dir_fake_equalized, file), 'r') as f:
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records)
        distributions_fake_equalized += [distribution]

total_distribution = Divergence.blendDistributions(distributions)
jsds = []
jsds_fake_centralized = []
jsds_fake_equalized = []

print("Calculating JSDs(Real)...")
for distribution in distributions:
    jsds += [Divergence.jsd(distribution, total_distribution)]

print("Calculating JSDs(Centralized Cheating)...")
for distribution in distributions_fake_centralized:
    jsds_fake_centralized += [Divergence.jsd(distribution, total_distribution)]

print("Calculating JSDs(Equalized Cheating)...")
for distribution in distributions_fake_equalized:
    jsds_fake_equalized += [Divergence.jsd(distribution, total_distribution)]

print("Normal Distribution(Real):")
print("mu: %f" % statistics.mean(jsds))
print("sigma: %f" % math.sqrt(statistics.variance(jsds)))

print("Normal Distribution(Centralized Cheating):")
print("mu: %f" % statistics.mean(jsds_fake_centralized))
print("sigma: %f" % math.sqrt(statistics.variance(jsds_fake_centralized)))

print("Normal Distribution(Equalized Cheating):")
print("mu: %f" % statistics.mean(jsds_fake_equalized))
print("sigma: %f" % math.sqrt(statistics.variance(jsds_fake_equalized)))

print("Plotting...")
figure = plt.figure()
zeros = [0] * len(jsds)
plt.plot(jsds, zeros, "ro", ms=1, label="normal")
plt.plot(jsds_fake_centralized, [0.5] * len(jsds), "bo", ms=1, label="centralized")
plt.plot(jsds_fake_equalized, [-0.5] * len(jsds), "go", ms=1, label="equalized")
plt.legend()
plt.grid()
plt.savefig("CompareDaily.png", dpi=300)
print("Done.")
