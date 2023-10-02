import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from labo import v2k
from metodos import R2C
plt.style.use('./informes.mplstyle')

df = pd.read_csv('./Mediciones/Clase 2/celda_tvsV_I=1.csv')
t = df['Tiempo [s]'].values
V_gen = df['Tension generador [V]'].values
V_frio = df['Tensión termocupla fria [V]'].values
V_caliente = df['Tensión termocupla caliente [V]'].values


T_frio = 24.90389706*V_frio * 1e3 + 28.40587788
T_caliente = 23.59800922*V_caliente * 1e3 + 27.53553998
DeltaT = T_caliente - T_frio



fig, ax = plt.subplots()
ax.set_ylabel('Tensión [V]')
ax.set_xlabel('Diferencia de temperatura [°C]')

ax.plot(DeltaT, V_gen)

plt.show()