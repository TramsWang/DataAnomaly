import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

cor = []
cen = []
equ = []
for i in range(325):
    print("Counting %d.csv ..." % i)
    cor += [len(open("Correct/%d.csv" % i, 'r').readlines()) / 1000]
    cen += [len(open("Centralized/%d.csv" % i, 'r').readlines()) / 1000]
    equ += [len(open("Equalized/%d.csv" % i, 'r').readlines()) / 1000]

print("Plotting...")
figure = plt.figure(figsize=(1800/300, 600/300), dpi=300)
plt.subplot(131)
plt.plot(range(325), cor, 'r', label="Correct", lw=0.3)
plt.xlabel("Records(K)")
plt.legend(fontsize="xx-small", loc="upper left")
plt.subplot(132)
plt.plot(range(325), cen, 'b', label="Centralized", lw=0.3)
plt.xlabel("Records(K)")
plt.legend(fontsize="xx-small", loc="upper left")
plt.subplot(133)
plt.plot(range(325), equ, 'g', label="Equalized", lw=0.3)
plt.xlabel("Records(K)")
plt.legend(fontsize="xx-small", loc="upper left")
plt.savefig("Count.png")
print("Done.")
