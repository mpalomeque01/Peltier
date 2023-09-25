import pandas as pd
import matplotlib.pyplot as plt
from labo import v2k
plt.style.use('./informes.mplstyle')

df = pd.read_csv('./Mediciones/Clase 1/cal_termocupla-t=60.csv')
t = df['Tiempo [s]'].values
V = df['Tension [mV]'].values
# T = df['Temperatura [K]'].values - 273.15
T = v2k(V) - 273.15

fig, ax = plt.subplots(2, 1, sharex=True)
ax[0].set_ylabel('Tensión [mV]')
ax[1].set_ylabel('Temperatura [C]')
ax[1].set_xlabel('Tiempo [s]')

ax[0].plot(t, V)
ax[1].plot(t, T, 'C3')

plt.show()