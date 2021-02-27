import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager('@py')
theResource1 = 'TCPIP0::192.168.1.149::INSTR'

SA = rm.open_resource(theResource1)
SA.read_termination = '\n'
SA.write_termination = '\n'

#Changes dBm reference level
print(SA.query(":TRACe? TRACE1"))
print(SA.query(":TRACe:MATH:PEAK?"))