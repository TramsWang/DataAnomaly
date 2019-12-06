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
    plt.plot(xs, ys, 'o-', ms=5, color=BLACK, label='Normal')

    coordinates = sorted(dist_jsd_centralized.items(), key=lambda kv: kv[0])
    xs = [c[0] * step for c in coordinates]
    ys = [c[1] for c in coordinates]
    plt.plot(xs, ys, 'x--', ms=5, color=BLACK, label='Centralized')

    coordinates = sorted(dist_jsd_equalized.items(), key=lambda kv: kv[0])
    xs = [c[0] * step for c in coordinates]
    ys = [c[1] for c in coordinates]
    plt.plot(xs, ys, 'v-.', ms=5, color=BLACK, label='Equalized')

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
        [93.66153846, 98.27692308, 95.93846154, 90.58461538, 87.38461538, 94.58461538, 86.09230769],
        [85.47692308, 98.03076923, 92.55384615, 84.43076923, 89.29230769, 93.66153846, 78.27692308],
        [79.32307692, 98.4, 89.6, 80.98461538, 91.87692308, 93.90769231, 61.90769231],
        [74.21538462, 98.15384615, 85.90769231, 81.41538462, 92.24615385, 92.92307692, 58.83076923],
        [69.96923077, 98.76923077, 82.76923077, 82.76923077, 95.50769231, 95.50769231, 62.89230769],
        [79.2, 98.89230769, 80.55384615, 89.96923077, 96.43076923, 96.30769231, 67.50769231],
        [94.33846154, 98.52307692, 76.98461538, 97.29230769, 97.84615385, 97.72307692, 65.84615385],
        [98.89230769, 99.01538462, 74.15384615, 97.6, 96.8, 98.27692308, 58.27692308],
        [94.03076923, 99.75384615, 71.13846154, 89.84615385, 90.4, 92.24615385, 74.15384615],
    ]
    acc_2nd_equalized = [
        [72.12307692, 88.92307692, 82.46153846, 88.24615385, 63.26153846, 81.66153846, 86.4],
        [43.87692308, 75.50769231, 82.95384615, 87.07692308, 66.70769231, 79.69230769, 77.10769231],
        [40.92307692, 64.18461538, 84, 85.96923077, 75.93846154, 80, 69.04615385],
        [35.75384615, 50.4, 85.16923077, 85.72307692, 73.66153846, 75.01538462, 60.06153846],
        [36.24615385, 36.24615385, 85.53846154, 85.53846154, 66.03076923, 66.03076923, 50.89230769],
        [29.78461538, 29.10769231, 87.44615385, 87.01538462, 42.46153846, 39.13846154, 42.46153846],
        [26.83076923, 40.30769231, 88.36923077, 88, 35.63076923, 39.56923077, 32.67692308],
        [32.24615385, 60, 89.84615385, 90.83076923, 37.90769231, 49.90769231, 24.30769231],
        [29.78461538, 79.69230769, 91.01538462, 81.84615385, 41.6, 38.33846154, 15.13846154],
    ]
    f1_1st_centralized = [
        [57.57389349, 91.25, 76.45511625, 17.22222222, 61.02943407, 78.71687362, 17.18181818],
        [45.86829813, 95.07692308, 78.26281972, 39.3177833, 78.91201994, 86.74649603, 3.287671233],
        [48.1193443, 97.31958763, 79.41357977, 54.59784803, 88.10329984, 90.7833538, 34.75444985],
        [53.36176917, 97.69230769, 79.04480642, 70.38537608, 91.16001629, 91.86117857, 44.98034977],
        [57.48992599, 98.7654321, 79.35313503, 79.35313503, 95.69295105, 95.69295105, 53.72599797],
        [79.18507818, 99.07692308, 80.75567585, 90.91951711, 97.15963555, 97.06277995, 78.51170409],
        [95.7842839, 98.94273128, 80.37687705, 98.04959742, 98.46719192, 98.40071268, 74.7937514],
        [99.31435408, 99.38461538, 80.82243155, 98.52311697, 97.97441603, 98.93282093, 69.08487212],
        [96.81616715, 99.8630137, 80.88028636, 94.65153971, 94.37196402, 95.53719281, 85.67352473],
    ]
    f1_2nd_equalized = [
        [34.04834896, 43.75, 50.63784283, 57.92582004, 33.94223004, 47.8015974, 9.126004076],
        [36.89564821, 38.76923077, 68.71518137, 72.66172715, 53.79455989, 62.14818075, 9.129501426],
        [41.51413476, 40, 77.65070424, 79.1872031, 69.69520103, 70.09920222, 12.60304141],
        [46.10640908, 38, 83.21550298, 83.23611133, 66.85573953, 67.09913799, 11.70068027],
        [48.00151077, 36.04938272, 86.37153093, 86.37153093, 60.81326485, 60.81326485, 11.74227493],
        [38.53845967, 40.92307692, 89.82760951, 89.63131819, 40.64288344, 43.6980296, 12.4035976],
        [37.95142396, 57.26872247, 91.74137199, 91.69058499, 44.3007285, 50.01608716, 10.32786885],
        [46.07845504, 75, 93.53513965, 94.43487217, 51.89175483, 64.02375957, 11.77812285],
        [44.87583281, 88.69863014, 94.86659608, 88.87567509, 57.80500383, 54.06355362, 11.78079731],
    ]
    algorithm_indices = {
        "SDD-R": 0,
        "SDD-R+": 1,
        "SDD-E Static": 2,
        "SDD-E Static+": 3,
        "SDD-E Dynamic": 4,
        "SDD-E Dynamic+": 5,
        "MGoF": 6
    }

    # 绘制Accuracy #
    fig_acc = plt.figure(figsize=(8, 4), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(
        [(i+1)/10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-R"]] for row in acc_1st_centralized],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-R+"]] for row in acc_1st_centralized],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc_1st_centralized],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Static+"]] for row in acc_1st_centralized],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc_1st_centralized],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in acc_1st_centralized],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
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
        [(i+1)/10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-R"]] for row in acc_2nd_equalized],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-R+"]] for row in acc_2nd_equalized],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc_2nd_equalized],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static+"]] for row in acc_2nd_equalized],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc_2nd_equalized],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in acc_2nd_equalized],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
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
        [row[algorithm_indices["SDD-R"]] for row in f1_1st_centralized],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-R+"]] for row in f1_1st_centralized],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1_1st_centralized],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Static+"]] for row in f1_1st_centralized],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1_1st_centralized],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_1st_centralized))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in f1_1st_centralized],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
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
        [(i+1)/10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-R"]] for row in f1_2nd_equalized],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-R+"]] for row in f1_2nd_equalized],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1_2nd_equalized],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Static+"]] for row in f1_2nd_equalized],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1_2nd_equalized],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1_2nd_equalized))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in f1_2nd_equalized],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
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
        [89.47692308, 84, 9.846153846, 89.6, 74.21538462, 83.81538462, 80.86153846],
        [89.41538462, 86.83076923, 17.16923077, 89.6, 79.63076923, 87.93846154, 84.73846154],
        [89.78461538, 90.64615385, 75.81538462, 89.6, 78.46153846, 90.33846154, 84.8],
        [90.70769231, 93.35384615, 78.52307692, 89.6, 80.18461538, 88.43076923, 85.35384615],
        [91.69230769, 95.07692308, 93.53846154, 89.6, 83.56923077, 90.64615385, 85.6],
        [92.92307692, 96.06153846, 93.72307692, 89.6, 84.67692308, 89.6, 85.6],
        [92.86153846, 97.41538462, 94.64615385, 89.6, 85.10769231, 89.6, 85.35384615],
        [93.66153846, 97.53846154, 94.4, 90.03076923, 86.21538462, 91.38461538, 85.29230769],
        [93.35384615, 98.15384615, 96.36923077, 89.66153846, 86.70769231, 94.27692308, 85.41538462],
    ]
    f1 = [
        [2.285714286, 18.75, 17.92717087, 0, 20.19966522, 11.18012422, 13.25855459],
        [2.162162162, 33.125, 18.42402425, 0, 35.12660568, 30.88938655, 9.75243811],
        [8.547717842, 52.5, 40.41026039, 0, 42.84576124, 50.27397693, 11.66119893],
        [22.88501855, 66.25, 44.67110328, 0, 46.82212177, 51.95887699, 12.66666667],
        [35.92319055, 75, 69.35517024, 0, 53.49359249, 63.68510559, 15.07650765],
        [50.1533556, 80, 71.1963245, 0, 54.73779539, 62.09527575, 15.42562339],
        [49.34951548, 86.875, 66.36816848, 0, 57.07305456, 63.63042293, 14.25166826],
        [57.40786961, 87.5, 64.19374082, 7.78593914, 59.37286322, 69.95259746, 13.46364347],
        [54.55053918, 90.625, 79.46663053, 1.142857143, 59.5602401, 76.80124706, 16.3275069],
    ]
    algorithm_indices = {
        "SDD-R": 0,
        "SDD-R+": 1,
        "SDD-E Static": 2,
        "SDD-E Static+": 3,
        "SDD-E Dynamic": 4,
        "SDD-E Dynamic+": 5,
        "MGoF": 6
    }

    # 绘制图像 #
    fig = plt.figure(figsize=(8, 4), dpi=300)
    plt.subplot(1, 2, 1)
    plt.plot(
        [(i+1)/10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-R"]] for row in acc],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-R+"]] for row in acc],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Static"]] for row in acc],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Static+"]] for row in acc],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in acc],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in acc],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(acc))],
        [row[algorithm_indices["MGoF"]] for row in acc],
        'd-', label='MGoF', color=BLACK, ms=5,
    )
    plt.xlabel("ν", fontsize='large')
    plt.ylabel("Accuracy(%)")
    plt.ylim(0, 100)
    plt.legend(loc="lower right")
    plt.subplot(1, 2, 2)
    plt.plot(
        [(i+1)/10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-R"]] for row in f1],
        'o--', label='SDD-R', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-R+"]] for row in f1],
        'o-', label='SDD-R+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Static"]] for row in f1],
        'x--', label='SDD-E Static', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Static+"]] for row in f1],
        'x-', label='SDD-E Static+', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Dynamic"]] for row in f1],
        's--', label='SDD-E Dynamic', color=BLACK, ms=5,
    )
    plt.plot(
        [(i + 1) / 10 for i in range(len(f1))],
        [row[algorithm_indices["SDD-E Dynamic+"]] for row in f1],
        's-', label='SDD-E Dynamic+', color=BLACK, ms=5,
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
        [36.14209878, 89.6, 85.47888473, 91.22166435, 80.19227295, 94.32846376],
        [18.18181818, 56.6, 78.77908135, 88.43535957, 40.278886, 80.83635215],
        [18.21162167, 39.8, 72.24052502, 82.67600159, 38.22909102, 67.80137569],
        [18.18181818, 39.8, 70.67915023, 82.85524191, 36.94366841, 69.33834968],
        [18.18181818, 48, 53.39900732, 59.65069844, 36.33676018, 54.20278966],
    ]

    # 绘制条形图 #
    algorithms = ["SDD-R", "SDD-R+", "SDD-E Static", "SDD-E Static+", "SDD-E Dynamic", "SDD-E Dynamic+"]
    metrics = ["KLD", "JSD", "BD", "HD", "KSS"]
    colors = [DEFAULT, RED, GREEN, ORANGE, BLACK]
    step = 3
    x = np.arange(len(algorithms)) * step
    width = 0.5

    fig, ax = plt.subplots(figsize=(8, 3), dpi=300)
    rects = [
        ax.bar(x - (len(metrics) / 2.0 - i - 0.5) * width, f1[i], width, label=metrics[i], color=colors[i]) for i in range(len(metrics))
    ]

    ax.set_ylabel("F1(%)")
    ax.set_xticks(x)
    # ax.set_xlim(-width * (len(metrics) / 2 + 1), x[-1] + step)
    ax.set_xticklabels(algorithms)
    ax.set_ylim(0, 100)
    ax.legend(loc="upper left")

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
    sdd_e_rocs = {}
    sdd_r_rocs = {}
    for metric, shortname in metric_shortname.items():
        input_file = open("Exp-Results/Exp-ROC(SDD-E)-%s.csv" % shortname, 'r')
        roc = []
        lines = input_file.readlines()
        for line in lines:
            paras = line.strip('\n').split('\t')
            roc.append((float(paras[0]), float(paras[1])))
        sdd_e_rocs[shortname] = roc

        input_file = open("Exp-Results/Exp-ROC(SDD-R)-%s.csv" % shortname, 'r')
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

    plt.subplot(1, 2, 2)
    for shortname, color in colors:
        coordinates = sdd_e_rocs[shortname]
        fpr = [coordinate[0] for coordinate in coordinates]
        tpr = [coordinate[1] for coordinate in coordinates]
        plt.plot(fpr, tpr, '-', color=color, label=shortname)
    plt.xlabel("FPR", fontsize='large')
    plt.ylabel("TPR", fontsize='large')
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.title("ROC of SDD-E")

    fig.tight_layout()
    fig.savefig("fig/ROCUnderDifferentMetrics")
    print("Done.")


if __name__ == '__main__':
    # drawClickFarmComparison()
    # drawDivergenceWithReference()
    # drawDifferentAnomalyProbability()
    drawDifferentAnomalyMagnitude()
    # drawDifferentDivergenceMetric()
    # drawROC()
