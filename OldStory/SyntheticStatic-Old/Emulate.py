import csv
import itertools
import math
import os
import statistics

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import Divergence


input_dir = "Inputs"
input_dir_cen = "InputsCentralized"
input_dir_equ = "InputsEqualized"

f = open("brackets.txt", 'r')
min_val = int(f.readline())
max_val = int(f.readline())
f.close()

for pw in range(1, 11):
#for nbins in [4, 8, 16, 32, 64, 128, 256, 512, 1024]:
    dists = []
    jsds = []
    jsds_cen = []
    jsds_equ = []
    nbins = 2 ** pw
    print("N bins: ", nbins)

    # Record History
    print("Reading History...")
    num_hists = 30
    for i in range(133, 133 + num_hists):
        with open("%s/%d.csv" % (input_dir, i), 'r') as f:
            reader = csv.reader(f)
            records = (int(row[2]) for row in itertools.islice(reader, 0, None))
            distribution = Divergence.histogramNaive(min_val, max_val, records, nbins=nbins)
            dists += [distribution]

    # Test Rest Days
    print("Performing Tests...")
    for i in range(133 + num_hists, 489):
        total_dist = Divergence.blendDistributions(dists)

        if not os.path.exists(os.path.abspath("%s/%d.csv" % (input_dir, i))):
            continue

        # Calculate Real Distribution
        f = open("%s/%d.csv" % (input_dir, i), 'r')
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records, nbins=nbins)
        jsds += [Divergence.jsd(total_dist, distribution)]
        dists += [distribution]
        f.close()

        # Calculate Centralized Distribution
        f = open("%s/%d.csv" % (input_dir_cen, i), 'r')
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records, nbins=nbins)
        jsds_cen += [Divergence.jsd(total_dist, distribution)]
        f.close()

        # Calculate Equalized Distribution
        f = open("%s/%d.csv" % (input_dir_equ, i), 'r')
        reader = csv.reader(f)
        records = (int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records, nbins=nbins)
        jsds_equ += [Divergence.jsd(total_dist, distribution)]
        f.close()

        # Window Sliding Forward
        del dists[0]

    # Plot
    print("Normal Distribution(Real):")
    print("mu: %f" % statistics.mean(jsds))
    print("sigma: %f" % math.sqrt(statistics.variance(jsds)))

    print("Normal Distribution(Centralized Cheating):")
    print("mu: %f" % statistics.mean(jsds_cen))
    print("sigma: %f" % math.sqrt(statistics.variance(jsds_cen)))

    print("Normal Distribution(Equalized Cheating):")
    print("mu: %f" % statistics.mean(jsds_equ))
    print("sigma: %f" % math.sqrt(statistics.variance(jsds_equ)))

    print("Plotting...")
    figure = plt.figure(figsize=(1400/300, 1400/300), dpi=300)
    plt.plot(jsds, [0] * len(jsds), "r.", ms=1, label="normal")
    plt.plot(jsds_cen, [0.5] * len(jsds), "bo", ms=1, label="centralized")
    plt.plot(jsds_equ, [-0.5] * len(jsds), "go", ms=1, label="equalized")
    plt.legend()
    plt.grid()
    plt.savefig("Emulate'(nbins=%d).png" % nbins)
    print("Done.")