from math import *

sa = 0.006571
ua = 0.009587
sb = 0.03078
ub = 0.06759
alpha = 0.1

A = sb * sb - sa * sa
B = -2 * (ua * sb * sb - ub * sa * sa)
C = ua * ua * sb * sb - ub * ub * sa * sa - 2 * sa * sa * sb * sb * log(((1 - alpha) * sb) / (alpha * sa))

D = B * B - 4 * A * C
print(A)
print(B)
print(C)
print(D)

print("Solution: ")
print((-B + sqrt(D)) / (2 * A))
print((-B - sqrt(D)) / (2 * A))