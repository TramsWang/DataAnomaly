import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

alphas = [0.1, 0.3, 0.5, 0.7, 0.9]
TPRs1 = [
    [1, 0.99, 0.828, 0.556, 0.263],
    [1, 0.989, 0.827, 0.424, 0.28],
    [1, .993, .771, .579, .281],
    [1, .991, .717, .473, .276],
    [1, .97, .686, .5, .318]
]
FPRs1 = [
    [0.165, 0.018, 0.006, 0.008, 0.004],
    [0.17, 0.015, 0.007, 0.006, 0.003],
    [.16, .015, .014, .005, .007],
    [.104, .004, .01, .007, 0],
    [.127, .023, .004, .013, 0]
]

TPRs2 = [
    [1, 1, .867, .655, .346],
    [1, 1, .833, .357, .085],
    [1, 1, .770, .188, .048],
    [1, 1, .832, .090, .028],
    [1, 1, 1, .215, .015]
]
FPRs2 = [
    [.376, .064, .008, 0, 0],
    [.386, .076, .001, 0, 0],
    [.357, .108, .014, 0, 0],
    [.352, .146, .040, .047, .012],
    [.346, .111, .059, .080, 0]
]

figure = plt.figure(figsize=(10, 5), dpi=100)
plt.subplot(1, 2, 1)
for i in range(5):
    plt.plot(FPRs1[i], TPRs1[i], label="alpha=%.1f" % alphas[i])
plt.title("1st Level Classifier")
plt.legend()
plt.xlabel("FPR")
plt.ylabel("TPR")

plt.subplot(1, 2, 2)
for i in range(5):
    plt.plot(FPRs2[i], TPRs2[i], label="alpha=%.1f" % alphas[i])
plt.title("2nd Level Classifier")
plt.legend()
plt.xlabel("FPR")
plt.ylabel("TPR")

figure.savefig("ROC-alpha.png")
