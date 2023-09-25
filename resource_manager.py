import pyvisa as visa

rm = visa.ResourceManager()
print(rm.list_resources())

multitermo = rm.open_resource('GPIB0::23::INSTR')
multires = rm.open_resource('GPIB0::24::INSTR')


multitermo.close()
multires.close()