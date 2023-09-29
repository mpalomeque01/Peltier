import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvisa as visa
import time
from labo import save, v2k
plt.style.use('./informes.mplstyle')


rm = visa.ResourceManager()

multitermo = rm.open_resource('GPIB0::23::INSTR')   #M1  CHEQUEAR, PUEDE QUE ESTEN AL REVEZ
multires = rm.open_resource('GPIB0::24::INSTR')     #M2

try:

    # MEDIR

    t = []  # s
    V = []  # V
    R = []
    duracion = 10  # s
    T_amb = 20 + 273.15  # K
    T_range = 70  # C

    t0 = time.time()
    while time.time() - t0 <= duracion:
        t.append(time.time() - t0)
        medicion_V = multitermo.query_ascii_values('MEASURE:VOLTAGE:DC?')[0]
        medicion_R = multires.query_ascii_values('MEASURE:RESistance? 100')[0]
        V.append(medicion_V)
        R.append(medicion_R)
    
    t = np.array(t)  # s
    V = np.array(V) * 1e3  # mV
    T = v2k(V)  # K
    R = np.array(R)
    

    # GUARDAR DATOS
    
    df = pd.DataFrame({'Tiempo [s]' : t,
                        'Tension [mV]' : V,
                        'Temperatura [K]' : T,
                        'Resistencia [Ohm]' : R})
    df['Temp ambiente [K]'] = pd.Series([T_amb], index=[0])
    df['Rango temp [C]']    = pd.Series([T_range], index=[0])
    
    save(df, f'cal_termocupla2_resistencia', './Mediciones/Clase 1')
    

    # GRAFICAR

    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].set_ylabel('Tensión [mV]')
    ax[1].set_ylabel('Temperatura [C]')
    ax[1].set_xlabel('Tiempo [s]')

    ax[0].plot(t, V)
    ax[1].plot(t, T - 273.15, 'C3')

    plt.show()


except:
    pass
multi.close()