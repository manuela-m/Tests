
from data_manager import read_data32b, normalize_0_100_float
from scipy.stats import kstest
import numpy as np
import matplotlib.pyplot as  plt
import math
import pickle


def if_crashed(parking, carX, carY):
    for x in parking:
        if math.fabs(x[0] - carX) <= 1.0 and math.fabs(x[1] - carY) <= 1.0:
            return True
    return False

filename = '24M32b.bin'
data = read_data32b(filename)
coords = normalize_0_100_float(data)

x = 0
data = list()
counter = 0

while x + 2 < len(coords):
    k, crash = 0, 0
    n = 12000
    parking = []

    while n and x + 2 != len(coords):
        if if_crashed(parking, coords[x], coords[x + 1]):
            crash += 1
        else:
            k += 1
            parking.append([coords[x], coords[x + 1]])

        x += 2
        n -= 1

    res = (k - 3523) / 21.9
    data.append(res)

    print('parked: ', k, ' xi: ', x)
    counter += 1
    if counter % 100 == 0:
        with open("parking_dump_" + str(counter) + ".txt", "wb") as fp:
            pickle.dump(data, fp)
        print('Proba nr. ', counter, ' zapisana')


with open("parking_dump_final.txt", "wb") as fp:
    pickle.dump(data, fp)