import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
rm = visa.ResourceManager('@py')
theResource1 = 'TCPIP0::192.168.1.104::INSTR'
theResource2 = 'TCPIP0::192.168.1.149::INSTR'

FG = rm.open_resource(theResource1)
FG.read_termination = '\n'
FG.write_termination = '\n'

SA = rm.open_resource(theResource2)
SA.read_termination = '\n'
SA.write_termination = '\n'


print(FG.query("*IDN?"))
print(FG.write(":OUTP2 OFF"))
print(FG.write(":SOUR2:VOLT 2"))
print(FG.write(":SOUR2:VOLT:OFFSET 2"))
print(FG.write(":SOUR2:FREQ 2000"))
print(FG.write(":SOUR2:PHASe 0"))
print(FG.write(":OUTP2 ON"))

print(SA.query("*IDN?"))
figure = plt.gcf()
subplot1 = figure.add_subplot(311)




print(SA.write(":SENS:FREQ:CENT 1MHZ"))
print(SA.write(":SENS:FREQ:SPAN 1MHZ"))
print(SA.write(":TRACe:MATH:PEAK:TABLe:STATe ON"))
print(SA.write(":TRACe:MATH:PEAK:SORT AMPL"))
print(SA.query(":TRACe:MATH:PEAK:SORT?"))
str_data = str(SA.query(":TRAC? TRACE1")).strip()
data = SA.query(":TRAC:MATH:PEAK?")

#print(str_data)
pointFound = str_data.find("  ")
str_data = str_data.split("  ", 1)[1]
str_data = str_data.split(',')
#print(str_data)
data_array = np.array(list(map(float, str_data[1:])))
#print(data_array)



start = (int(1)-0.5*int(1)) * 10**6
stop = (int(1)+0.5*int(1)) * 10**6
step = (stop-start)/len(data_array)
x = np.arange(start, stop, step)
print(start)
print(stop)
subplot1.cla()
subplot1.plot(x, data_array)
subplot1.set_xlim(start, stop)
plt.show()