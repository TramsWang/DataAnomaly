import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open("CountEqualized.csv", 'r') as f:
    y = []
    for row in f:
        y += [int(row)]

    figure = plt.figure(figsize=(1400/300, 1400/300), dpi=300)
    plt.plot(range(len(y)), y, ms=1)
    plt.savefig("TotalSellsEqualized.png")

