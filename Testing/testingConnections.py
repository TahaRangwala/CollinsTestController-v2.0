#Testing
import pyvisa
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
theResource = 'TCPIP0::192.168.1.101::INSTR'
my_instrument = rm.open_resource(theResource)
print(my_instrument)
my_instrument.read_termination = '\n'
my_instrument.write_termination = '\n'
print(my_instrument.query("*IDN?"))