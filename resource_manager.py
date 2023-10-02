import pyvisa as visa
from metodos import R2C


rm = visa.ResourceManager()
print(rm.list_resources())


# # Multi arriba 'GPIB0::22::INSTR'

# multi_up = rm.open_resource('GPIB0::22::INSTR')
# print(multi_up.query_ascii_values('MEASURE:VOLT:DC?')[0] * 1e3)
# multi_up.close()


# # Multi abajo 'GPIB0::23::INSTR'

# multi_down = rm.open_resource('GPIB0::23::INSTR')
# R = multi_down.query_ascii_values('MEASURE:RESistance? 1000')[0]
# print(R, R2C(R))
# multi_down.close()


# # Gen 'GPIB0::25::INSTR'

# gen = rm.open_resource('GPIB0::25::INSTR')
# print(gen.query_ascii_values('MEASURE:VOLT:DC?')[0])
# gen.close()