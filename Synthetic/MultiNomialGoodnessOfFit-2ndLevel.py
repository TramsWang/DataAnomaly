import csv
import Divergence
import statistics
import random
import scipy.stats as stats
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


input_dir = "Correct"
input_dir_err = "Centralized"

time_span = 300
error_rate = 0.9
step = 1.17
correct_cnt = 0
correct_recognized = 0
error_cnt = 0
error_recognized = 0

T99s = [0, 6.635, 9.210, 11.345, 13.277, 15.086, 16.812, 18.475, 20.090, 21.666, 23.209, 24.725, 26.217, 27.688,
        29.141, 30.578, 32.000, 33.409, 34.805, 36.191, 37.566, 38.932, 40.289, 41.638, 42.980, 44.314]
T95s = [0, 3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675, 21.026, 22.362,
        23.685, 24.996, 26.296, 27.587, 28.869, 30.144, 31.410, 32.671, 33.924, 35.172, 36.415, 37.652]
c_th = 10  # TODO: c_th?
m = 0
P = []
c = []

print("\nTest %s Cheating..." % input_dir_err)


def KLD(p, q):
    # TODO: Complete this
    d = 0.0
    for i in range(25):
        if (p[i] != 0) and (q[i] != 0):
            d += p[i] * math.log(p[i] / q[i])
    return d


for n in range(30, 325):
    is_err = False
    declare_err = False
    W = 0
    kld_min = 999
    c_min = 999
    if random.uniform(0.0, 1.0) < error_rate:
        # Error
        is_err = True
        reader_err = csv.reader(open("%s/%d.csv" % (input_dir_err, n), 'r'))
        tmp_freq, dropped = Divergence.histogram(list(int(row[2]) for row in reader_err), time_span)
        data_err = list(tmp_freq.values())
        W = len(data_err)

        error_cnt += 1

        dropped, dist = Divergence.histogram(data_err, step)

    else:
        # Correct
        reader = csv.reader(open("%s/%d.csv" % (input_dir, n), 'r'))
        tmp_freq, dropped = Divergence.histogram(list(int(row[2]) for row in reader), time_span)
        data = list(tmp_freq.values())
        W = len(data)

        correct_cnt += 1

        dropped, dist = Divergence.histogram(data, step)

    # Regularize dist
    tmp_dist = {}
    nbins = 0
    for i in range(25):
        if i in dist.keys():
            tmp_dist[i] = dist[i]
            nbins += 1
        else:
            tmp_dist[i] = 0
    dist = tmp_dist

    T = T95s[nbins]  # TODO: T?

    if 0 == m:
        P += [dist]
        m = 1
        c += [1]
    else:
        for i in range(m):
            tmp_kld = KLD(dist, P[i])
            if tmp_kld < kld_min:
                kld_min = tmp_kld
                c_min = i

        if (2 * W * kld_min) < T:
            c[c_min] += 1
            if c[c_min] > c_th:
                declare_err = False
            else:
                declare_err = True
        else:
            declare_err = True
            P += [dist]
            m += 1
            c += [1]

    if is_err:
        if declare_err:
            error_recognized += 1
    else:
        if not declare_err:
            correct_recognized += 1

    if is_err:
        ch = 'X'
    else:
        ch = '.'
    print("[%s]2W*KLD=%f\t%f" % (ch, 2 * W * kld_min, T))

print(c)
tp = error_recognized
fp = correct_cnt - correct_recognized
tn = correct_recognized
fn = error_cnt - error_recognized
print("tp=%d, fp=%d, tn=%d, fn=%d" % (tp, fp, tn, fn))
print("TPR=%.2f, FPR=%.2f, ACC=%.2f" % (tp / (tp + fn) * 100, fp / (fp + tn) * 100, (tp + tn) / (tp + fp + tn + fn) * 100))
