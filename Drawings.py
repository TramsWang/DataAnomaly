import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import matplotlib.axis as ax
from Divergence import *
import numpy as np


DEFAULT = "#1F77B4"
RED = '#E74C3C'
GREEN = '#117A65'
ORANGE = '#FF9900'
BLACK = '#000000'


def drawClickFarmComparison():
    print("Drawing click farming comparison figure...")
    figure = plt.figure(figsize=(7, 7), dpi=300)
    days = [5, 113, 287]
    data_normal_file = open('Koubei/RawCorrect.csv', 'r')
    data_normal = data_normal_file.readlines()
    collection_normal = [
        [int(num) for num in data_normal[d].strip('\n').split('\t')] for d in days
    ]
    data_normal_file.close()

    data_centralized_file = open('Koubei/RawCentralized.csv', 'r')
    data_centralized = data_centralized_file.readlines()
    collection_centralized = [
        [int(num) for num in data_centralized[d].strip('\n').split('\t')] for d in days
    ]
    data_centralized_file.close()

    data_equalized_file = open('Koubei/RawEqualized.csv', 'r')
    data_equalized = data_equalized_file.readlines()
    collection_equalized = [
        [int(num) for num in data_equalized[d].strip('\n').split('\t')] for d in days
    ]
    data_equalized_file.close()

    step = 1
    hist_normal = [histogram(collection, step)[1] for collection in collection_normal]
    hist_centralized = [histogram(collection, step)[1] for collection in collection_centralized]
    hist_equalized = [histogram(collection, step)[1] for collection in collection_equalized]

    lim_x = 24
    lim_y = 0.25
    for col in range(3):
        # Draw Normal Data #
        plt.subplot(3, 3, 1 * 3 + col + 1)
        xs = []
        ys = []
        for x, y in hist_normal[col].items():
            xs.append(x)
            ys.append(y)
        plt.bar(xs, ys, color=RED, label="Normal")
        plt.xlim(0, lim_x)
        plt.ylim(0, lim_y)
        plt.xticks(())
        if 0 != col:
            plt.yticks(())
        else:
            plt.legend(loc="upper left")
            plt.ylabel("Probability", fontsize='x-large')

        # Draw Centralized Data #
        plt.subplot(3, 3, 0 * 3 + col + 1)
        xs = []
        ys = []
        for x, y in hist_centralized[col].items():
            xs.append(x)
            ys.append(y)
        # plt.bar(xs, ys, color='b', label="Centralized")
        plt.bar(xs, ys, label="Centralized")
        plt.title("Day %d" % days[col])
        plt.xlim(0, lim_x)
        plt.ylim(0, lim_y)
        plt.xticks(())
        if 0 != col:
            plt.yticks(())
        else:
            plt.legend(loc="upper left")

        # Draw Equalized Data #
        plt.subplot(3, 3, 2 * 3 + col + 1)
        xs = []
        ys = []
        for x, y in hist_equalized[col].items():
            xs.append(x)
            ys.append(y)
        plt.bar(xs, ys, color=GREEN, label="Equalized")
        plt.xlim(0, lim_x)
        plt.ylim(0, lim_y)
        if 0 != col:
            plt.yticks(())
        else:
            plt.legend(loc="upper left")
        if 1 == col:
            plt.xlabel("Hour", fontsize='x-large')

    plt.savefig("fig/SampleHistogram.png")
    figure.tight_layout()
    print("Done.")


def drawDivergenceWithReference():
    print("Drawing divergence comparison with reference figure...")
    step = 1

    figure = plt.figure(figsize=(7, 7), dpi=300)
    data_normal_file = open('Koubei/RawCorrect.csv', 'r')
    data_normal = data_normal_file.readlines()
    collection_normal = [
        [int(num) for num in d.strip('\n').split('\t')] for d in data_normal
    ]
    dist_normal = [histogram(collection, step)[0] for collection in collection_normal]
    level2_dist_normal = [histogram(collection.values(), step)[1] for collection in dist_normal]
    data_normal_file.close()

    data_centralized_file = open('Koubei/RawCentralized.csv', 'r')
    data_centralized = data_centralized_file.readlines()
    collection_centralized = [
        [int(num) for num in d.strip('\n').split('\t')] for d in data_centralized
    ]
    dist_centralized = [histogram(collection, step)[0] for collection in collection_centralized]
    level2_dist_centralized = [histogram(collection.values(), step)[1] for collection in dist_centralized]
    data_centralized_file.close()

    data_equalized_file = open('Koubei/RawEqualized.csv', 'r')
    data_equalized = data_equalized_file.readlines()
    collection_equalized = [
        [int(num) for num in d.strip('\n').split('\t')] for d in data_equalized
    ]
    dist_equalized = [histogram(collection, step)[0] for collection in collection_equalized]
    level2_dist_equalized = [histogram(collection.values(), step)[1] for collection in dist_equalized]
    data_equalized_file.close()

    # reference = blendDistributions(dist_normal[:30])
    # jsd_normal = [jensenShannonDivergence([dist, reference]) for dist in dist_normal]
    # jsd_centralized = [jensenShannonDivergence([dist, reference]) for dist in dist_centralized]
    # jsd_equalized = [jensenShannonDivergence([dist, reference]) for dist in dist_equalized]
    reference = blendDistributions(level2_dist_normal[:30])
    jsd_normal = [jensenShannonDivergence([dist, reference]) for dist in level2_dist_normal]
    jsd_centralized = [jensenShannonDivergence([dist, reference]) for dist in level2_dist_centralized]
    jsd_equalized = [jensenShannonDivergence([dist, reference]) for dist in level2_dist_equalized]

    nbins = 20
    step = (max(jsd_normal) - min(jsd_normal))/ nbins
    dropped, dist_jsd_normal = histogram(jsd_normal, step)
    dropped, dist_jsd_centralized = histogram(jsd_centralized, step)
    dropped, dist_jsd_equalized = histogram(jsd_equalized, step)

    figure = plt.figure(figsize=(7, 4), dpi=300)
    coordinates = sorted(dist_jsd_normal.items(), key=lambda kv: kv[0])
    xs = [c[0] * step for c in coordinates]
    ys = [c[1] for c in coordinates]
    plt.plot(xs, ys, '.-', ms=5, color=RED, label='Normal')

    coordinates = sorted(dist_jsd_centralized.items(), key=lambda kv: kv[0])
    xs = [c[0] * step for c in coordinates]
    ys = [c[1] for c in coordinates]
    plt.plot(xs, ys, 'x-', ms=5, label='Centralized')

    coordinates = sorted(dist_jsd_equalized.items(), key=lambda kv: kv[0])
    xs = [c[0] * step for c in coordinates]
    ys = [c[1] for c in coordinates]
    plt.plot(xs, ys, 'o-', ms=5, color=GREEN, label='Equalized')

    plt.xlabel("JSD", fontsize='large')
    plt.ylabel("Probability")
    plt.legend(loc="upper left")
    figure.tight_layout()
    figure.savefig("fig/Overview")
    print("Done.")


def drawDifferentAnomalyProbability():
    print("Drawing performance on different anomaly probability figure...")
    # 加载数据 #
    acc_1st_centralized = [
        [97.16923077, 98.03076923, 90.95384615, 93.41538462, 88.30769231],
        [94.95384615, 97.90769231, 85.41538462, 93.90769231, 78.52307692],
        [88.55384615, 98.03076923, 82.33846154, 94.83076923, 70.09230769],
        [73.41538462, 98.4, 81.47692308, 95.01538462, 61.10769231],
        [49.04615385, 98.64615385, 83.63076923, 95.01538462, 51.01538462],
        [37.72307692, 99.13846154, 90.46153846, 96.8, 56.67692308],
        [41.04615385, 99.01538462, 97.90769231, 97.04615385, 56.06153846],
        [60, 99.26153846, 98.09230769, 98.58461538, 66.83076923],
        [79.69230769, 98.89230769, 89.84615385, 87.75384615, 89.53846154],
    ]
    acc_2nd_equalized = [
        [95.07692308, 89.04615385, 88.49230769, 83.81538462, 87.63076923],
        [92.12307692, 77.23076923, 87.81538462, 81.10769231, 77.84615385],
        [87.32307692, 64.55384615, 85.10769231, 80.06153846, 68.30769231],
        [86.95384615, 51.87692308, 85.96923077, 73.41538462, 59.69230769],
        [82.4, 37.72307692, 86.15384615, 62.27692308, 50.09230769],
        [79.69230769, 28.49230769, 86.46153846, 37.53846154, 41.53846154],
        [78.58461538, 40.55384615, 87.56923077, 45.96923077, 32.12307692],
        [77.23076923, 60, 91.26153846, 53.23076923, 23.56923077],
        [79.93846154, 79.69230769, 84.61538462, 40.98461538, 14.03076923],
    ]
    f1_1st_centralized = [
        [85.625, 90, 23.77320622, 75.84002904, 5],
        [87.38461538, 94.76923077, 45.25262672, 87.21971004, 4.383561644],
        [80.82474227, 96.70103093, 59.2443689, 92.14092709, 22.24750536],
        [66.76923077, 98, 70.39782154, 94.13107544, 24.94623656],
        [48.88888889, 98.64197531, 80.61271069, 95.26872358, 29.91945536],
        [48.1025641, 99.28205128, 91.40485981, 97.40365089, 67.56043416],
        [57.79735683, 99.29515419, 98.49546714, 97.92894256, 63.00618722],
        [75, 99.53846154, 98.82440546, 99.12370624, 75.79527547],
        [88.69863014, 99.38356164, 94.65153971, 92.88641499, 94.48051948],
    ]
    f1_2nd_equalized = [
        [75, 44.375, 57.80215388, 51.19763762, 17.95918367],
        [80.30769231, 43.07692308, 73.73549452, 63.4651716, 12.19512195],
        [78.7628866, 40.6185567, 77.38636638, 67.93931572, 11.06409155],
        [83.69230769, 39.84615385, 83.41607173, 63.68207644, 10.88435374],
        [82.34567901, 37.5308642, 86.72562906, 54.73509438, 9.38547486],
        [83.07692308, 40.41025641, 89.26120767, 42.35781549, 11.04509213],
        [84.66960352, 57.44493392, 91.38971347, 55.93785041, 9.373358441],
        [85.76923077, 75, 94.68624809, 66.69393299, 10.89647682],
        [88.83561644, 88.69863014, 90.73027701, 56.47628427, 9.579288026],
    ]
    algorithm_indices = {
        "SDD-kNN": 0,
        "SDD-R": 1,
        "SDD-E Static": 2,
        "SDD-E Dynamic": 3,
        "MGoF": 4
    }

    # 绘制Accuracy #
    fig_acc = plt.figure(figsize=(8, 4), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(
        [(i+1)/10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-kNN"]] for row in acc_1st_centralized],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-R"]] for row in acc_1st_centralized],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc_1st_centralized],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc_1st_centralized],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["MGoF"]] for row in acc_1st_centralized],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("α", fontsize='large')
    plt.ylabel("Accuracy(%)")
    plt.ylim(0, 100)
    plt.legend(loc="lower left")
    plt.title("1st Level Centralized")
    plt.subplot(1, 2, 2)
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-kNN"]] for row in acc_2nd_equalized],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-R"]] for row in acc_2nd_equalized],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc_2nd_equalized],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc_2nd_equalized],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["MGoF"]] for row in acc_2nd_equalized],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("α", fontsize='large')
    plt.ylim(0, 100)
    plt.yticks(())
    plt.title("2nd Level Equalized")
    fig_acc.tight_layout()
    fig_acc.savefig("fig/AccuracyOnAnomalyProbability")

    # 绘制F1 #
    fig_f1 = plt.figure(figsize=(8, 4), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(
        [(i+1)/10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-kNN"]] for row in f1_1st_centralized],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-R"]] for row in f1_1st_centralized],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1_1st_centralized],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1_1st_centralized],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["MGoF"]] for row in f1_1st_centralized],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("α", fontsize='large')
    plt.ylabel("F1(%)")
    plt.ylim(0, 100)
    plt.legend(loc="lower right")
    plt.title("1st Level Centralized")
    plt.subplot(1, 2, 2)
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-kNN"]] for row in f1_2nd_equalized],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-R"]] for row in f1_2nd_equalized],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1_2nd_equalized],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1_2nd_equalized],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["MGoF"]] for row in f1_2nd_equalized],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("α", fontsize='large')
    plt.ylim(0, 100)
    plt.yticks(())
    plt.title("2nd Level Equalized")
    fig_f1.tight_layout()
    fig_f1.savefig("fig/F1OnAnomalyProbability")
    print("Done")


def drawDifferentAnomalyMagnitude():
    print("Drawing performance on different anomaly magnitude figure...")
    # 加载数据 #
    acc = [
        [84.73846154, 83.26153846, 89.72307692, 82.64615385, 80.86153846],
        [89.41538462, 86.83076923, 89.72307692, 88.18461538, 81.6],
        [91.75384615, 91.38461538, 89.72307692, 87.44615385, 81.53846154],
        [93.84615385, 93.10769231, 89.72307692, 87.93846154, 81.78461538],
        [95.2, 94.95384615, 89.72307692, 90.76923077, 85.84615385],
        [96.30769231, 95.69230769, 89.66153846, 89.84615385, 85.66153846],
        [96.06153846, 97.04615385, 89.72307692, 90.09230769, 85.6],
        [96.67692308, 97.29230769, 89.84615385, 92.06153846, 85.78461538],
        [97.04615385, 98.03076923, 89.72307692, 93.72307692, 85.90769231],
    ]
    f1 = [
        [22.5, 15, 1.176470588, 15.18700974, 13.87975266],
        [46.25, 33.125, 1.176470588, 44.79863675, 15.16109422],
        [58.125, 56.25, 1.176470588, 47.09606666, 16.19631902],
        [68.75, 65, 1.176470588, 53.31017366, 16.74437462],
        [75.625, 74.375, 1.176470588, 65.38668174, 15.88235294],
        [81.25, 78.125, 0, 63.9611945, 14.74285714],
        [80, 85, 1.176470588, 64.61086821, 16.09448819],
        [83.125, 86.25, 3.428571429, 71.13761038, 15.15852812],
        [85, 90, 1.176470588, 76.56820579, 16.88704193],
    ]
    algorithm_indices = {
        "SDD-kNN": 0,
        "SDD-R": 1,
        "SDD-E Static": 2,
        "SDD-E Dynamic": 3,
        "MGoF": 4
    }

    # 绘制图像 #
    fig = plt.figure(figsize=(8, 4), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-kNN"]] for row in acc],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-R"]] for row in acc],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["MGoF"]] for row in acc],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("ν", fontsize='large')
    plt.ylabel("Accuracy(%)")
    plt.ylim(0, 100)
    plt.legend(loc="lower left")
    plt.subplot(1, 2, 2)
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-kNN"]] for row in f1],
        'o-', label='SDD-kNN', ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-R"]] for row in f1],
        'v-', label='SDD-R', color=RED, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1],
        'x-', label='SDD-E Static', color=GREEN, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1],
        's-', label='SDD-E Dynamic', color=ORANGE, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["MGoF"]] for row in f1],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("ν", fontsize='large')
    plt.ylabel("F1(%)")
    plt.ylim(0, 100)
    fig.tight_layout()
    fig.savefig("fig/PerformanceOnAnomalyMagnitude")
    print("Done.")


def drawDifferentDivergenceMetric():
    print("Drawing F1 on different divergence metrics...")
    # 加载数据 #
    f1 = [
        [0, 87.2, 88, 88.2, 49.4],
        [87.8, 54.6, 39.4, 39.4, 47],
        [88.80048923, 86.18349393, 80.93781058, 81.61680562, 57.98597465],
        [93.08569596, 77.57255782, 63.39747237, 63.23223708, 51.34881004],
    ]
    algorithm_indices = {
        "SDD-kNN": 0,
        "SDD-R": 1,
        "SDD-E Static": 2,
        "SDD-E Dynamic": 3
    }

    # 绘制条形图 #
    algorithms = ["SDD-kNN", "SDD-R", "SDD-E Static", "SDD-E Dynamic"]
    metrics = ["KLD", "JSD", "BD", "HD", "KSS"]
    colors = [DEFAULT, RED, GREEN, ORANGE, BLACK]
    step = 3
    x = np.arange(len(algorithms)) * step
    width = 0.5

    fig, ax = plt.subplots(figsize=(8, 3), dpi=300)
    rects = [
        ax.bar(x - (len(metrics) / 2.0 - i - 0.5) * width, [row[i] for row in f1], width, label=metrics[i], color=colors[i]) for i in range(len(metrics))
    ]

    ax.set_ylabel("F1(%)")
    ax.set_xticks(x)
    ax.set_xlim(-width * (len(metrics) / 2 + 1), x[-1] + step)
    ax.set_xticklabels(algorithms)
    ax.set_ylim(0, 100)
    ax.legend(loc="lower right")

    # Attach a text label above each bar in *rects*, displaying its height. #
    for rect in rects:
        for bar in rect:
            height = bar.get_height()
            ax.annotate('%.0f' % height,
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    fig.tight_layout()
    fig.savefig("fig/F1OnDivergenceMetric")

    print("Done")


def drawROC():
    print("Drawing performance on different anomaly probability figure...")
    # 加载数据 #
    metric_shortname = {
        kullbackLeiblerDivergence: "KLD",
        jensenShannonDivergence: "JSD",
        bhattacharyyaDistance: "BD",
        hellingerDistance: "HD",
        kolmogorovSmirnovStatistic: "KSS"
    }
    sdd_knn_rocs = {}
    sdd_r_rocs = {}
    for metric, shortname in metric_shortname.items():
        input_file = open("Exp-ROC(SDD-kNN)-%s.csv" % shortname, 'r')
        roc = []
        lines = input_file.readlines()
        for line in lines:
            paras = line.strip('\n').split('\t')
            roc.append((float(paras[0]), float(paras[1])))
        sdd_knn_rocs[shortname] = roc

        input_file = open("Exp-ROC(SDD-R)-%s.csv" % shortname, 'r')
        roc = []
        lines = input_file.readlines()
        for line in lines:
            paras = line.strip('\n').split('\t')
            roc.append((float(paras[0]), float(paras[1])))
        sdd_r_rocs[shortname] = roc

    # 绘制ROC曲线 #
    fig = plt.figure(figsize=(8, 4), dpi=300)
    colors = [
        ("KLD", DEFAULT),
        ("JSD", RED),
        ("BD", GREEN),
        ("HD", ORANGE),
        ("KSS", BLACK)
    ]
    plt.subplot(1, 2, 1)
    for shortname, color in colors:
        coordinates = sdd_knn_rocs[shortname]
        fpr = [coordinate[0] for coordinate in coordinates]
        tpr = [coordinate[1] for coordinate in coordinates]
        plt.plot(fpr, tpr, '-', color=color, label=shortname)
    plt.xlabel("FPR", fontsize='large')
    plt.ylabel("TPR", fontsize='large')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("ROC of SDD-kNN")

    plt.subplot(1, 2, 2)
    for shortname, color in colors:
        coordinates = sdd_r_rocs[shortname]
        fpr = [coordinate[0] for coordinate in coordinates]
        tpr = [coordinate[1] for coordinate in coordinates]
        plt.plot(fpr, tpr, '-', color=color, label=shortname)
    plt.xlabel("FPR", fontsize='large')
    plt.ylabel("TPR", fontsize='large')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("ROC of SDD-R")
    plt.legend(loc="lower right")

    fig.tight_layout()
    fig.savefig("fig/ROCUnderDifferentMetrics")
    print("Done.")


if __name__ == '__main__':
    # drawClickFarmComparison()
    # drawDivergenceWithReference()
    drawDifferentAnomalyProbability()
    drawDifferentAnomalyMagnitude()
    drawDifferentDivergenceMetric()
    # drawROC()
