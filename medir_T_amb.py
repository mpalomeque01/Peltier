import numpy as np
import pandas as pd
import pyvisa as visa
import time
import metodos as met

rm = visa.ResourceManager()
multi_up = rm.open_resource('GPIB0::22::INSTR')

try:
    
    duracion = 10  # s
    
    t = []
    R = []
    
    t0 = time.time()
    while time.time() - t0 <= duracion:
        t.append(time.time() - t0)
        R.append(multi_up.query_ascii_values('MEASURE:RESistance? 100')[0])
    
    t = np.array(t)  # s
    R = np.array(R)  # Ohm
    
    df = pd.DataFrame({'Tiempo [s]' : t,
                        'Resistencia [Ohm]' : R})
    
    met.save(df, 'temp_amb', './Mediciones/Clase 2')
    
    
except:
    pass
multi_up.close()