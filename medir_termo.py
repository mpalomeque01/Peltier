import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvisa as visa
import time

rm = visa.ResourceManager()
multi = rm.open_resource('GPIB0::23::INSTR')

try:

    t = []  # tiempo
    V = []  # voltaje
    duracion = 5  # s

    t0 = time.time()
    while time.time() - t0 <= duracion:
        t.append(time.time() - t0)
        dc = multi.query_ascii_values('MEASURE:VOLTAGE:DC?')[0]
        V.append(dc)
    
    data_termo = pd.DataFrame({'Tiempo [s]' : t, 'Tension [V]' : V})
    data_termo.to_csv('data_termo.csv', index=False)


except:
    pass
multi.close()
