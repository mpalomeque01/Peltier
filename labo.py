import numpy as np
from os.path import exists

def save(df, filename=None, path='.'):
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

def v2k(mV): # en mV
    '''
    The coefficients for Temperature range 0 deg C to 500 deg C
    for Cr-Al type thermocouple
    Voltage range 0 mV to 20.644 mV
    Error range .04 deg C to -.05 deg C are:
    '''
    C0 = 293.15
    C1 = 2.508355 * 10**1
    C2 = 7.860106 * 10**-2
    C3 = -2.503131 * 10**-1
    C4 = 8.315270 * 10**-2
    C5 = -1.228034 * 10**-2
    C6 = 9.804036 * 10**-4
    C7 = -4.413030 * 10**-5
    C8 = 1.057734 * 10**-6
    C9 = -1.052755 * 10**-8
    T = C0 + C1*mV + C2*mV**2 + C3*mV**3 + C4*mV**4 + C5*mV**5 + C6*mV**6 + C7*mV**7 +  C8*mV**8 + C9*mV**9        
    
    return T * (mV < 20.644)  # K


# ESTADISTICA

def lineal(x, a1, a2):
    return a1 + a2*x

def correlacion(x, y):
    x_med = np.mean(x)
    y_med = np.mean(y)

    cov = np.sum((x - x_med) * (y - y_med))
    stds = np.sum((x - x_med)**2) * np.sum((y - y_med)**2)
    return cov / np.sqrt(stds)

def cuadrados_minimos(x, y, sigma):
    n = len(x)
    Delta = n*np.sum(x**2) - np.sum(x)**2

    a1 = (np.sum(x**2)*np.sum(y) - np.sum(x)*np.sum(x*y)) / Delta
    a2 = (n*np.sum(x*y) - np.sum(x)*np.sum(y)) / Delta
    cov = ((sigma**2)/Delta)*np.array([[np.sum(x**2), -np.sum(x)], [-np.sum(x), n]])

    return np.array([a1, a2]), cov