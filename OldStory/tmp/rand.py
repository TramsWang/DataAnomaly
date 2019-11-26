import random
from itertools import *

print("Start")
with open("original.csv", 'rt') as infile:
    with open("dropped.csv", 'w') as outfile:
        for line in infile:
            if (0.2 > random.random()): #modify
                i = int(int(line) * 0.1);
                outfile.write(str(i) + '\n')
            else:
                outfile.write(line)

