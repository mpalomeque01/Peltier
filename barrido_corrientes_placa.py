import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time
import metodos as met
plt.style.use('./informes.mplstyle')

rm = visa.ResourceManager()
gen = rm.open_resource('GPIB0::25::INSTR')
multi_up = rm.open_resource('GPIB0::22::INSTR')
multi_down = rm.open_resource('GPIB0::23::INSTR')

try:
    
    gen.write(":SOUR:FUNC:MODE CURR")
    gen.write(":SENS:VOLT:PROT 21")
    
    # corrientes = [0.1, 0.3, 0.5, 0.75, 1, 1.25, 1.5]
    I = 0.75  # A
    duracion = 60  # s

    t = []
    V_gen = []
    V_termo_up = []
    V_termo_down = []
    
    gen.write(f":SOUR:CURR {I}") # Pone la corriente
    
    t0 = time.time()
    while time.time() - t0 <= duracion:
        t.append(time.time() - t0)
        V_gen.append(gen.query_ascii_values('MEASURE:VOLT:DC?')[0])
        V_termo_up.append(multi_up.query_ascii_values('MEASURE:VOLT:DC?')[0])
        V_termo_down.append(multi_down.query_ascii_values('MEASURE:VOLT:DC?')[0])
  
    # GUARDAR DATOS
    
    t = np.array(t)  # s
    V_gen = np.array(V_gen)  # V
    V_termo_up = np.array(V_termo_up)
    V_termo_down = np.array(V_termo_down)
    
    df = pd.DataFrame({'Tiempo [s]' : t,
                        'Tension generador [V]' : V_gen,
                        'Tensión termocupla fria [V]' : V_termo_up,
                        'Tensión termocupla caliente [V]' : V_termo_down})
    
    met.save(df, f'celda_tvsV_I={I}', './Mediciones/Clase 2')
    
    
    # GRAFICAR
    
    fig, ax = plt.subplots()
    ax.set_ylabel('Tensión [V]')
    ax.set_xlabel('Tiempo [s]')
    
    ax.plot(t, V_gen)
    

except:
    pass
gen.close()

plt.show()