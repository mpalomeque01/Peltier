import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import metodos as met
from scipy.optimize import curve_fit
plt.style.use('./informes.mplstyle')


n_termo = 2

R = []
V = []
R_sd = []
V_sd = []

for i in range(9):
    if i != 0:
        df = pd.read_csv(f'./Mediciones/Clase 2/cal_termocupla{n_termo}_t20({i}).csv')
    else:
        df = pd.read_csv(f'./Mediciones/Clase 2/cal_termocupla{n_termo}_t20.csv')
    
    # Tension
    V_temp = df['Tension [mV]'].values
    V_bar = np.mean(V_temp)
    V_est_err = np.sum((V_temp - V_bar)**2) / (len(V_temp) - 1)
    # V_lec_err = 0.00003*V_temp
    # V_range_err = 0.000007*V_temp
    
    V.append(V_bar)
    V_sd.append(np.sqrt(V_est_err**2))
    
    # Resistencia
    R_temp = df['Resistencia [Ohm]'].values
    R_bar = np.mean(R_temp)
    R_est_err = np.sum((R_temp - R_bar)**2) / (len(R_temp) - 1)
    # R_lec_err = 0.00008*R_temp
    # R_range_err = ((i < 5) * 0.00004 + (i >= 5) * 0.00001) * R_temp
    
    R.append(R_bar)
    R_sd.append(np.sqrt(R_est_err**2))

V = np.array(V)
T = met.R2C(np.array(R))
V_sd = np.array(V_sd)
T_sd = np.array(R_sd) * met.cal_pt100


# Cuadrados minimos

def lin(V, m, b):
    return m*V + b


popt, pcov = curve_fit(lin, V, T, sigma=T_sd, absolute_sigma=True)

print(popt, np.sqrt(np.diag(pcov)))


# Figuras y plots

fig, ax = plt.subplots()
ax.set_xlabel('Tensión [mV]')
ax.set_ylabel('Temperatura [°C]')

ax.errorbar(V, T, yerr=T_sd, fmt='ok', label='nose',
             capsize=2, capthick=1)
ax.plot(V, lin(V, *popt))


ax.legend()
plt.show()