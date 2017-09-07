import csv
import Divergence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.axis as ax

days = (5, 113, 287)
lim_x = 40
lim_y = 0.3

figure = plt.figure(figsize=(9, 9), dpi=100)
for ii in range(3):
    day = days[ii]
    reader = csv.reader(open("Correct/%d.csv" % day, 'r'))
    reader_cen = csv.reader(open("Centralized/%d.csv" % day, 'r'))
    reader_equ = csv.reader(open("Equalized/%d.csv" % day, 'r'))

    freq, dropped = Divergence.histogram(list(int(row[2]) for row in reader), step=1)
    freq_cen, dropped = Divergence.histogram(list(int(row[2]) for row in reader_cen), step=1)
    freq_equ, dropped = Divergence.histogram(list(int(row[2]) for row in reader_equ), step=1)

    data = freq.values()
    data_cen = freq_cen.values()
    data_equ = freq_equ.values()
    step = 21.48

    # data = list(int(row[2]) for row in reader)
    # data_cen = list(int(row[2]) for row in reader_cen)
    # data_equ = list(int(row[2]) for row in reader_equ)
    #
    # step = 1
    #
    dropped, hist = Divergence.histogram(data, step)
    droped, hist_cen = Divergence.histogram(data_cen, step)
    dropped, hist_equ = Divergence.histogram(data_equ, step)

    id = 1 * 3 + ii + 1
    plt.subplot(3, 3, id)
    x = []
    y = []
    for i in hist:
        x += [i]
        y += [hist[i]]
    plt.bar(x, y, color='r', label="Normal")
    plt.xlim(0, lim_x)
    plt.ylim(0, lim_y)
    plt.xticks(())
    if 0 != ii:
        plt.yticks(())
    else:
        plt.legend(loc="upper right")
        plt.ylabel("Probability")

    id = 0 * 3 + ii + 1
    plt.subplot(3, 3, id)
    x = []
    y = []
    for i in hist_cen:
        x += [i]
        y += [hist_cen[i]]
    plt.bar(x, y, color='b', label="Centralized")
    plt.title("Day %d" % day)
    plt.xlim(0, lim_x)
    plt.ylim(0, lim_y)
    plt.xticks(())
    if 0 != ii:
        plt.yticks(())
    else:
        plt.legend(loc="upper right")
    if 2 == ii:
        plt.xlim(0, 70)
        plt.xticks((0, 20, 40, 60, 70))
    #plt.ylabel("Probability")
    #plt.xlabel("Hour", labelpad=-3)

    id = 2 * 3 + ii + 1
    plt.subplot(3, 3, id)
    x = []
    y = []
    for i in hist_equ:
        x += [i]
        y += [hist_equ[i]]
    plt.bar(x, y, color='g', label="Equalized")
    plt.xlim(0, lim_x)
    plt.ylim(0, lim_y)
    if 0 != ii:
        plt.yticks(())
    else:
        plt.legend(loc="upper right")
    if 1 == ii:
        plt.xlabel("Hour")

plt.savefig("SampleHistogram.png")
