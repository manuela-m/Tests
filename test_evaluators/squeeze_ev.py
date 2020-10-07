from data_manager import read_data32b, normalize_0_100_float
from scipy.stats import kstest, chisquare, normaltest
import numpy as np
import matplotlib.pyplot as  plt
import math
import pickle

filename = "squeeze_dump_final.txt"

with open(filename, 'rb') as f:
    wyniki = pickle.load(f)

plt.hist(wyniki, bins=43)
plt.show()
print(chisquare(wyniki))
print(normaltest(wyniki))