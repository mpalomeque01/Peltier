import numpy as np
from os.path import exists

def save(df, filename, path='.'):
    if exists(f'{path}/{filename}.csv'):
        i = 1
        while True:
            if exists(f'{path}/{filename}({i}).csv'):
                i += 1
                continue
            else:
                df.to_csv(f'{path}/{filename}({i}).csv')
                break
    else:
        df.to_csv(f'{path}/{filename}.csv')


# PELTIER

cal_pt100 = 1 / 0.385  # °C/Ohm


# ESTADISTICA

def lineal(x, a1, a2):
    return a1 + a2*x

def cuadrados_minimos(x, y, sigma):
    n = len(x)
    Delta = n*np.sum(x**2) - np.sum(x)**2

    a1 = (np.sum(x**2)*np.sum(y) - np.sum(x)*np.sum(x*y)) / Delta
    a2 = (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / Delta
    cov = ((sigma**2)/Delta)*np.array([[np.sum(x**2), -np.sum(x)], [-np.sum(x), n]])

    return np.array([a1, a2]), cov