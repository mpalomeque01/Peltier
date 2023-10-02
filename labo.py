import numpy as np
from os.path import exists
from metodos import save

#Error de medicion para resistencia Multimetro 34401A
#Usando 90 Day +- 5 deg(C)
#Error de lectura_rango de Ohm
reading_100Ohm  =   0.00008
reading_1kOmh   =   0.00008
reading_10kOhm  =   0.00008
reading_100kOhm =   0.00008
#Error de rango utilizado
range_100Ohm    =   0.00004
range_1kOhm     =   0.00001
range_10kOhm    =   0.00001
range_100kOhm   =   0.00001
#Error de medición = error de lectura_rango + error de rango

#Error de medicion para Voltaje DC Multimetro 34401A
#Usando 90 Day +- 5 deg(C)
#Error de lectura_rango de Volt
reading_100mV   =   0.00004
reading_1V      =   0.00003
reading_10V     =   0.00002
#Error de rango utilizado
range_100mV     =   0.000035
range_1V        =   0.000007
range_10V       =   0.000005
#Error de medición = error de lectura_rango + error de rango

#Error de medicion para Corriente DC Multimetro 34401A
#Error de lectura_rango de Ampere
reading_10mA    =   0.0003
reading_100mA   =   0.0003
reading_1A      =   0.0008
reading_3A      =   0.0012
#Error de rango utilizado
range_10mA      =   0.0002
range_100mA     =   0.00005
range_1A        =   0.0001
range_3A        =   0.0002


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