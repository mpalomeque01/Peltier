import numpy as np
from scipy.stats import chi2
import sympy as sp
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

cal_pt100 = 1 / 0.385  # K/Ohm

def R2C(R):
    return (R - 100)*cal_pt100


# ESTADISTICA

def lineal(x, a1, a2):
    return a1 + a2*x

def least_squares(f, x, y, sigma):
    
    n = len(x)  # Numero de mediciones
    k = f.__code__.co_argcount - 1  # Numero de parametros
    parametros = f.__code__.co_varnames[1:k+1]


    if len(np.array(sigma).shape) == 1:
        sigma = np.identity(len(x))*np.array(sigma)

    f = f(sp.symbols('x'), *sp.symbols(parametros))

    A = []
    for parametro in sp.symbols(parametros):
        fprima_i = sp.lambdify('x', sp.diff(f, parametro).simplify())
        A.append(fprima_i(x))
    A = np.array(A).T

    y = np.array([y]).T
    pcov = np.linalg.inv(A.T @ np.linalg.inv(sigma) @ A)
    popt = pcov @ A.T @ np.linalg.inv(sigma) @ y

    chi_sq = (y - A @ popt).T @ np.linalg.inv(sigma) @ (y - A @ popt)
    P = 1 - chi2.cdf(chi_sq[0,0], n-k)

    return popt.T[0], pcov, P