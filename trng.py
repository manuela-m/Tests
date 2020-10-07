#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pprint import pprint
import matplotlib.pyplot as  plt
import numpy as np
#import sounddevice as sd
import struct
import array

# In[12]:
def float2bin(f):
    [d] = struct.unpack(">Q", struct.pack(">d", f))
    return d

def _bin(num, size=64):
    num_bin = np.array([np.uint8(i) for i in np.binary_repr(num)])
    padding = np.zeros((size-num_bin.shape[0]))
    return np.concatenate([padding, num_bin]).astype(np.uint8)

def mod_addition(a, b):
    assert isinstance(a, np.uint64), "a is not np.uint64 "
    assert isinstance(b, np.uint64), "b is not np.uint64 "
    bin_a = _bin(a, 64)
    bin_b = _bin(b, 64)
    xor = np.logical_xor(bin_a, bin_b).astype(np.uint64)
    return bin_to_int(xor)

def f_tenting(x, alpha=1.99999):
    return alpha * x if (0 <= x < 0.5) else alpha * (1 - x)

def swap64(i):
    assert isinstance(i, np.uint64), "i is not np.uint64"
    # zamiana połówkami
    bin_i = _bin(i, 64)
    swapped = np.concatenate([bin_i[32:], bin_i[:32]])
    return bin_to_int(swapped)

def bin_to_int(bin_i, dtype=np.uint64):
    return bin_i.dot(2**np.arange(bin_i.size, dtype = dtype)[::-1])

def extract(i):
    # 7 bitów
    return i & 0x07

def rec(n):
    assert isinstance(n, np.uint64), "n is not int"
    fs = 44100
    samples = np.int64(n + 10000)
    recording = sd.rec(samples, samplerate=fs, channels = 1)
    sd.wait()

    # do testowania na tych samych danych
    #with open('test.npy', 'wb') as f:
    #    np.save(f, recording)
    #sd.play(recording, fs, blocking=True) 
    # for tests:
    #with open('test.npy', 'rb') as f:
    #    recording = np.load(f)

    recording = -recording[:n]
    print(recording.min())
    print(recording.max())
    recording -= recording.min()
    recording /= recording.max()
    recording = (255 * recording).astype(np.uint8)
    return recording
    # normalize and convert to unsigned 8-bit int


# ![image.png](attachment:ba1b0030-16a0-4d95-9835-226b9855a97a.png)

# In[69]:


#N = 4096
#N = 100000
# 2,4M probek do parking lot test
N = 24000000

epsilon=0.05
L=6
omega=0.5 
s = 64
# bits  with higher  unpredictability  within  each  byte  are  first  extracted and concatenated to form a b-bit random number, yi.
b = 3  # 3-bitowe LSB znormalizowanych probek

assert isinstance(N, int), "N should be integer"
# assert N<s, "N should be smaller than s"

gamma = np.floor(L / 2).astype(np.uint8)
n = np.uint64(2 *N /s)
A = rec(n)[:, 0]

#plt.hist(A)
#plt.show()

# extract 3 bits from each sample
y = [int(extract(ai)) for ai in A]
#plt.hist(y, bins=100)
#plt.show()


# In[60]:



if L == 6:
    x = np.zeros((6, 5))
    x[:, 0] = [0.141592,0.653589,0.793238,0.462643,0.383279,0.502884]
elif L == 8:
    x = np.zeros((8, 5))
    x[:, 0] = [0.141592,0.653589,0.793238,0.462643,0.383279,0.502884, 0.197169, 0.399375]

c = 0
O = []
z = np.zeros((L), dtype = np.uint64)
while len(O)<N:
    if len(O) % 100000 == 0:
        print ('len(O) = ', len(O))

    t = 0
    for i in range(L):
        x[i, t] = ((omega * y[c%len(y)] / (2**b - 1)) + x[i, t]) * 1 / (1 + omega)
        c += 1
    for tt in range(gamma):
        for i in range(L):
            x[i, tt + 1] = (1 - epsilon) * f_tenting(x[i, tt]) + (epsilon / 2) * (f_tenting(x[(i + 1) % L, tt])
                                           + f_tenting(x[(i - 1) % L, tt]))
    for i in range(L):
        z[i] = np.uint64(float2bin(x[i, gamma-1]))
        x[i, 0] = x[i, gamma-1]

    for i in range(gamma):
        z[i] = mod_addition(z[i], swap64(z[i+gamma]))

    # concatenate and store the B-bit random number
    temp = []
    for i in range(gamma):
        bin_z = _bin(z[i], 64)
        temp = np.concatenate([temp, bin_z]).astype(np.uint8)
        
    # dodanie 192-bitowych liczb losowych do listy O
    #O.append(''.join([str(x) for x in temp]))

    #dodanie 8-bitowych liczb calkowitych dodatnich do listy
    #O.append(np.uint8(int(''.join([str(x) for x in temp[-8:]]),2)))

    #dodanie 32-bitowych liczb calkowitych dodatnich do listy
    O.append(np.uint32(int(''.join([str(x) for x in temp[-32:]]),2)))

    #print(temp)

# In[73]:

# wydrukowanie pierwszych 5 liczb losowych
#print(O[:5])

#zapisanie do pliku
#filename = "100k8b.bin"
#filename = "100k32b.bin"
#filename = "2400k32b.bin"
filename = "24M32b.bin"
newFile = open(filename, "wb")

# dla liczb 32b
values = array.array('I')
values.fromlist(O)
newFileByteArray = values.tobytes()

# dla liczb 8b
#newFileByteArray = bytes(O)

newFile.write(newFileByteArray)
newFile.close()

# Etropia

# In[70]:


bits = 8
binary_A = np.array([_bin(a_i, bits) for a_i in A])
binary_A_p = binary_A.sum(axis=0)/len(A)
A_enthropy = -sum([p_i*np.log2(p_i) for p_i in binary_A_p])
print(f"Entropia A: {A_enthropy}, maksymalna możliwa entropia: {bits}")

bits = 3
binary_y = np.array([_bin(y_i, bits) for y_i in y])
binary_y_p = binary_y.sum(axis=0)/len(y)
y_enthropy = -sum([p_i*np.log2(p_i) for p_i in binary_y_p])
print(f"Entropia y: {y_enthropy}, maksymalna możliwa entropia: {bits}")


