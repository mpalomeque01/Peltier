import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvisa as visa
import time
import metodos as met
plt.style.use('./informes.mplstyle')


rm = visa.ResourceManager()

multi_up = rm.open_resource('GPIB0::22::INSTR')
multi_down = rm.open_resource('GPIB0::23::INSTR')
gen = rm.open_resource('GPIB0::25::INSTR')


try:
    
    # MEDIR
    
    t = []  # s
    V = []  # V
    R = []  # Ohm
    duracion = 10  # s
    T_amb = 20  # °C
    
    t0 = time.time()
    while time.time() - t0 <= duracion:
        t.append(time.time() - t0)
        medicion_V = multi_down.query_ascii_values('MEASURE:VOLT:DC?')[0]
        medicion_R = multi_up.query_ascii_values('MEASURE:RESistance? 100')[0]
        V.append(medicion_V)
        R.append(medicion_R)
    
    t = np.array(t)  # s
    V = np.array(V) * 1e3  # mV
    R = np.array(R)  # Ohm
    
    
    # GUARDAR DATOS
    
    df = pd.DataFrame({'Tiempo [s]' : t,
                        'Tension [mV]' : V,
                        'Resistencia [Ohm]' : R})
    df['Temp ambiente [K]'] = pd.Series([T_amb], index=[0])
    
    met.save(df, f'cal_termocupla2_t{duracion}', './Mediciones/Clase 2')
    
    
    # GRAFICAR
    
    fig, ax = plt.subplots(2, 1, sharex=True)
    ax[0].set_ylabel('Tensión [mV]')
    ax[1].set_ylabel('Temperatura [°C]')
    ax[1].set_xlabel('Tiempo [s]')
    
    ax[0].plot(t, V)
    ax[1].plot(t, R*met.cal_pt100, 'C3')
    
    plt.show()
    
    
except:
    pass
multi_up.close()
multi_down.close()
gen.close()