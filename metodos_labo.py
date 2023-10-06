import numpy as np
from scipy.stats import chi2
import sympy as sp
from os.path import exists
from inspect import getsource
from types import FunctionType

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

R2C = lambda R: (R - 100)*cal_pt100

# incerteza lectura-rango resistencia
reading_100Ohm  =   0.00008
range_100Ohm    =   0.00004
range_1kOhm     =   0.00001
# Incerteza lectura-rango tension
reading_1V      =   0.00003
range_1V        =   0.000007


# ESTADISTICA

def least_squares(f, x, y, sigma):
    
    n = len(x)  # Numero de mediciones
    k = f.__code__.co_argcount - 1  # Numero de parametros
    parametros = f.__code__.co_varnames[1:k+1]
    
    
    # Conversion a array y definicion matriz sigma
    x = np.array(x)
    y = np.array([np.array(y)]).T
    sigma = np.array(sigma)
    if len(sigma.shape) == 1:
        sigma = np.identity(n)*sigma
    
    
    # Correccion de la funcion a sympy
    if 'np.' in getsource(f):
        f_code = compile(getsource(f).replace('np.', 'sp.'), '', 'exec')
        f = FunctionType(f_code.co_consts[0], globals(), "gfg")
    
    f = f(sp.symbols('x'), *sp.symbols(parametros))
    
    
    # Definicion de la matriz A
    A = []
    for parametro in sp.symbols(parametros):
        fprima_i = sp.diff(f, parametro).simplify()
        if 'x' in str(fprima_i):
            fprima_i = sp.lambdify('x', fprima_i)
            A.append(fprima_i(x))
        else:
            fprima_i = n*[float(fprima_i)]
            A.append(np.array(fprima_i))
    
    A = np.array(A).T
    
    
    # Resultados
    pcov = np.linalg.inv(A.T @ np.linalg.inv(sigma) @ A)
    popt = pcov @ A.T @ np.linalg.inv(sigma) @ y
    
    chi_sq = (y - A @ popt).T @ np.linalg.inv(sigma) @ (y - A @ popt)
    P = 1 - chi2.cdf(chi_sq[0,0], n-k)
    
    return popt.T[0], pcov, P