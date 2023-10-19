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

calibracion_termo = lambda m, b, V: m*V + b


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


def weighted(X, sigma):
    
    X = np.array(X)
    sigma = np.array(sigma)
    
    X_bar = np.sum(X / sigma**2) / np.sum(1 / sigma**2)
    sigma_X_bar = 1 / np.sum(1 / sigma**2)
    
    return X_bar, np.sqrt(sigma_X_bar)


def quadsum(*args):
    
    args = np.array(args)
    sum_sq = np.sqrt(np.sum(args**2))
    
    return sum_sq


def corr_propagation(f, X, cov):  # correlated propagation
    
    n_vars = f.__code__.co_argcount
    vars = sp.symbols(f.__code__.co_varnames[:n_vars])  # Variables
    
    X = np.array(X)
    cov = np.array(cov)
    if len(cov.shape) == 1:
        cov = np.identity(len(X))*cov
    
    
    # Function correction if necessary
    if 'np.' in getsource(f):
        f_code = compile(getsource(f).replace('np.', 'sp.'), '', 'exec')
        f = FunctionType(f_code.co_consts[0], globals(), "gfg")
    f = f(*vars)
    
    
    uncertainty = 0
    
    for i in range(0, n_vars):
        for j in range(i, n_vars):
            if i != j:  # Correlated terms
                fprima_i_j = sp.lambdify(vars, sp.diff(f, vars[i])*sp.diff(f, vars[j]).simplify())
                uncertainty += 2 * fprima_i_j(*X) * cov[i,j]
            else:  # Non correlated terms
                fprima_i_j = sp.lambdify(vars, sp.diff(f, vars[i]).simplify())
                uncertainty += cov[i,i] * fprima_i_j(*X)**2
    
    return np.sqrt(uncertainty)