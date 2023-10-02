import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pyvisa as visa
import time
from labo import save, v2k
import matplotlib.animation as animation
plt.style.use('./informes.mplstyle')

rm = visa.ResourceManager()

# multitermo = rm.open_resource('GPIB0::23::INSTR') #m1  Corregir, puede que esten al revez.
multires = rm.open_resource('GPIB0::22::INSTR')   #m2

fig, ax = plt.subplots()

def animate(i,t,T,t0):

    t = np.append(time.time()-t0)
    medicion_V = multires.query_ascii_values('MEASURE:RESistance? 100')[0]
    # medicion_V = medicion_V*1e3
    medicion_T = v2k(medicion_V) - 273.15
    T = np.append(T,[medicion_T])
    t = t[-200:]  #Para que el plot pueda correr por mucho tiempo
    T = T[-200:] 

    line.set_ydata(T)

    return line,

try:

    # MEDIR

    t = np.array([])  # s
    T = np.array([])  # K
    duracion = 10  # s
    T_amb = 20 + 273.15  # K
    T_range = 70  # C
    
    line, = ax.plot(t,T)

    t0 = time.time()
    ani = animation.FuncAnimation(fig,
                                  animate,
                                  fargs = (t,T,t0),
                                  interval = 16.6) #blit puede tirar problemas
    plt.show()
except:
    pass
# multitermo.close()
multires.close()