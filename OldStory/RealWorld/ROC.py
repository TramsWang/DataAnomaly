import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fpr_cen_1 = (0.09916, 0.01734, 0.00784, 0.00532, 0.00402, 0.002651, 0.00405, 0.00392, 0.00405, 0.00267)
tpr_cen_1 = (1, 1, 1, 0.9412, 0.7566, 0.5912, 0.4019, 0.3027, 0.3261, 0.0882)

figure = plt.figure(figsize=(9, 9), dpi=100)
plt.plot(fpr_cen_1, tpr_cen_1, label='1st Level Centralized')
plt.legend()

figure.savefig("ROC.png")