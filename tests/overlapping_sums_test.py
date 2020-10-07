from data_manager import normalize_float, read_data32b
from scipy.stats import chisquare, normaltest, chisquare
from statistics import mean, variance
import math
import numpy as np
import matplotlib.pyplot as  plt
import pickle

# Overlapping sums test: Generate a long sequence of random floats on (0,1). Add sequences of 100 consecutive floats. The sums should be normally distributed with characteristic mean and variance.
# https://wiki.christophchamp.com/index.php?title=Diehard_tests

filename = '2400k32b.bin'
data = read_data32b(filename)
floats = normalize_float(data)

wyniki = []

n = 0
for i in range(200000):
    sum = 0.0
    for j in range(i, i + 5):
        #print(j, ' ', end = '')
        sum += floats[j]
    #print(sum)
    wyniki.append(sum)
    if i % 1000 == 0:
        print(i)

filename = "overlapping_sums_dump_final.txt"
with open(filename, "wb") as fp:
    pickle.dump(wyniki, fp)