from data_manager import read_data32b, normalize_0_100_float
from scipy.stats import kstest
import numpy as np
import matplotlib.pyplot as  plt
import math
import pickle

filename = 'parking_dump_final.txt'

with open(filename, 'rb') as f:
    wyniki = pickle.load(f)

plt.hist(wyniki, bins = 10)
plt.show()

print('Wyniki testu Kolomogorowa-Smirnowa: ', kstest(wyniki, 'norm'))
