import numpy as np
import struct
import matplotlib.pyplot as  plt

# do czytania liczb 32-bitowych
def read_data32b(filename = '100k32b.bin'):
    data = []
    try:
        with open(filename, "rb") as f:
            byte = f.read(4)
            while byte != b'':
                data.append(np.frombuffer(byte, dtype=np.uint32)[0])
                byte = f.read(4)
            return data
    except Exception as e:
        print(e)

        
# do czytania liczb 8-bitowych
def read_data8b(filename = '100k8b.bin'):
    data = []
    try:
        with open(filename, "rb") as f:
            byte = f.read(1)
            while byte != b'':
                data.append(np.frombuffer(byte, dtype=np.uint8)[0])
                byte = f.read(4)
            return data
    except Exception as e:
        print(e)

        
def normalize_0_100_uint8(data):
    return np.uint8(100 * ((data - np.min(data)) / (np.max(data) - np.min(data))))
        
def normalize_0_100_float(data):
    return 100 * ((data - np.min(data)) / (np.max(data) - np.min(data)))

def normalize_float(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))
