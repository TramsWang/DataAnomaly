import math


#alpha = 0.1
#ua = 0.0468286
#sa = 0.02193664792
#ub = 0.26474683588
#sb = 0.06838939266
threshold = 0.1812176383876

sa = 0.006571
ua = 0.009587
sb = 0.03078
ub = 0.06759
alpha = 0.1
ret = 0.029330522042026866

def grad(t):
    tmp = (t - ub) / sb
    ret = alpha * math.exp(-tmp * tmp / 2) / sb / math.sqrt(2 * math.pi)
    tmp = (ua - t) / sa
    ret -= (1 - alpha) * math.exp(-tmp * tmp / 2) / sa / math.sqrt(2 * math.pi)
    return ret

accuracy = 1e-20
t = ua
delta = 1
while (abs(delta) > accuracy):
    new_t = t - 1e-7 * grad(t)
    delta = new_t - t
    t = new_t
    print(t)