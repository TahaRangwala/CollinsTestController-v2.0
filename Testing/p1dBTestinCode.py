#Test
import pyvisa
rm = pyvisa.ResourceManager('@py')
print(rm.list_resources())
theResource1 = 'TCPIP0::192.168.1.104::INSTR'
#theResource2 = 'TCPIP0::192.168.1.102::INSTR'

FG = rm.open_resource(theResource1)
#O = rm.open_resource(theResource2)
#O.read_termination = '\n'
#O.write_termination = '\n'
FG.read_termination = '\n'
FG.write_termination = '\n'

print(FG.query("*IDN?"))
#print(SA.query("*IDN?"))
#print(O.query("*IDN?"))

#print(FG.write(":SYST:POWS 6"))

print(FG.write(":OUTP1:STAT OFF"))

#print(SA.write(":SENS:FREQ:CENT 2MHZ"))
#(SA.query(":FETC:ACP?"))
#print(SA.query(":TRAC? TRACE1"))
#print(SA.query(":TRAC:MATH:PEAK?")) #gets frequency and amplitude(dbm)

#print(O.query("POWer:RIPPle:RESults:MEAN?"))
"""
print(O.write("Data INIT"))
print(O.write("DATA:SOU CH1"))
print(O.write("DATA:START 1"))
print(O.write("DATA:STOP 4000"))
print(O.write("DATA:WIDTH 1"))
print(O.write("DATA:ENC ASCII"))
print(O.query("CURVE?"))
#print(O.query("POW:QUAL:IRMS?"))"""