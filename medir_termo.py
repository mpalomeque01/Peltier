import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())
multi = rm.open_resource('GPIB0::23::INSTR')

try:

    print(multi.query('*IDN?'))

    dc = multi.query_ascii_values('MEASURE:VOLTAGE:DC?')[0]

    print(f'{dc} V')


except:
    pass
multi.close()
