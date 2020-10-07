from data_manager import normalize_float, read_data32b
from scipy.stats import chisquare, normaltest
import math
import numpy as np
import matplotlib.pyplot as  plt
import pickle

filename = '2400k32b.bin'
data = read_data32b(filename)
floats = normalize_float(data)

il_iteracji = []
wyniki = []

for i in range(43):
    wyniki.append(0)

n = 0
for i in range(100000):
    k = 2147483648
    j = 0

    while (k != 1) and (j < 48):
        k = math.ceil(floats[n] * k)
        j += 1
        n += 1

    if i%10000 == 0:
        print('i: ', i)

    if j < 6:
        j = 6

    elif j > 48:
        j = 48

    wyniki[j-6] += 1
    il_iteracji.append(j)

filename = "squeeze_dump_final.txt"
with open(filename, "wb") as fp:
    pickle.dump(il_iteracji, fp)

