#Testing
import pyvisa
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
theResource1 = 'TCPIP0::192.168.1.149::INSTR'
theResource2 = 'TCPIP0::192.168.1.103::INSTR'
theResource3 = 'TCPIP0::192.168.1.104::INSTR'

SA = rm.open_resource(theResource1)
NA = rm.open_resource(theResource2)
FG = rm.open_resource(theResource3)
SA.read_termination = '\n'
SA.write_termination = '\n'
NA.read_termination = '\n'
NA.write_termination = '\n'
FG.read_termination = '\n'
FG.write_termination = '\n'
print(SA.query("*IDN?"))
print(NA.query("*IDN?"))
print(FG.query("*IDN?"))


###Network Analyzer, page 360 in manual
print(NA.write("SENS1:FREQ:CENT 100MHz"))
print(NA.query("SENS:FREQ:CENT?"))

print("DIVIDER")
### for signal generator ###
# WORKS VERY WELL #
print(FG.write(":OUTPUT OFF"))
print(FG.write(":VOLT 5"))
print(FG.write(":VOLT:OFFS 1"))
print(FG.write(":FREQ 1000000"))
print(FG.write(":PHAS 90"))
print(FG.write(":OUTPUT ON"))


### for spectrum analyzer ###
#print(my_instrument.query(":READ:CHP:CHP?"))
    ### Returns the channels power (dB or dBm)

### SEEMS TO WORK except for trace:peak stuff (there may not
### be measurable peaks)

#print(my_instrument.write(":OUTP:STAT ON"))
print(SA.write(":UNIT:POW DBM"))
#print(my_instrument.query(":OUTPut:STATe?"))
print(SA.write(":SENS:FREQ:CENT 1000000"))
print(SA.query(":SENS:FREQ:CENT?"))
print(SA.write(":SENS:FREQ:SPAN 0"))
print(SA.write(":TRAC:MATH:PEAK:TABL:STAT 0N"))
print(SA.write(":TRAC:MATH:PEAK:SORT FREQ"))

print(SA.query(":TRAC? TRACE1"))
print(SA.query(":TRAC:MATH:PEAK?"))
#print(my_instrument.write(":OUTP:STAT OFF"))
#print(my_instrument.query(":OUTP:STAT?"))

### for oscilloscope (not needed) ###
"""
print(Osci.write("Data INIT"))
print(Osci.write("DATA:SOU CH1"))
print(Osci.write("DATA:STAR 1"))
print(Osci.write("DATA:STOP 4000"))
print(Osci.write("DATA:WIDTH 1"))
print(Osci.write("DATA:ENC ASCII"))
print(Osci.query("CURV?"))"""
