import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open("count.csv", 'r') as f:
    y = []
    for row in f:
        y += [int(row)]

    figure = plt.figure(figsize=(6, 6), dpi=100)
    plt.plot(range(len(y)), y, ms=1)
    plt.xlabel("Day", fontsize='x-large')
    plt.ylabel("Transaction Volume", fontsize='x-large')
    plt.savefig("TotalSells.png")

