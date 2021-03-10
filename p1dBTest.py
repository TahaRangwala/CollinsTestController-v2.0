from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np
import math

def parseGetTrace(plotPoints, centerFreq, freqSpan):
    str_data = str(plotPoints)
    str_data = str_data.split(" ", 1)[1]
    str_data = str_data.split(',')
    data_array = np.array(list(map(float, str_data[1:])))
    
    start = (int(centerFreq)-0.5*int(freqSpan)) * 10**6
    stop = (int(centerFreq)+0.5*int(freqSpan)) * 10**6
    step = (stop-start)/len(data_array)
    x = np.arange(start, stop, step)
    return x, data_array, start, stop

class P1dB_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        self.impedance = 0
        self.inputPower = 0
        self.smallVoltGain = 0
        self.setVoltCommand = None
        self.setFreqCommand = None
        self.traceDataCommand = None
        self.peakDataCommand = None
        
        self.freqStart = None
        self.freqStop = None
        self.voltStart = None
        self.voltStop = None
    
    def changeImpedance(self, impedance):
        self.impedance = impedance
    
    def setFrequencyRange(self, freqStart, freqStop):
        self.freqStart = freqStart
        self.freqStop = freqStop
    
    def setVoltSweepRange(self, voltStart, voltStop):
        self.voltStart = voltStart
        self.voltStop = voltStop
        
    def setUpP1dBRunCommands(self, numCommands):
        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            title = self.run[currentCommand]['title']
            if(title == 'Set Volts'):
                self.setVoltCommand = self.run[currentCommand]
            elif(title == 'Set Frequency'):
                self.setFreqCommand = self.run[currentCommand]
            elif(title == 'Get Trace'):
                self.traceDataCommand = self.run[currentCommand]
            elif(title == 'Get Peak'):
                self.peakDataCommand = self.run[currentCommand]
                
        if(self.setVoltCommand == None or self.setFreqCommand == None or self.traceDataCommand == None or self.peakDataCommand == None):
            return False
        else:
            return True

    def runTest(self):
        numCommands = int(self.run['num'])
        foundAllRunCommands = setUpP1dBRunCommands(numCommands)
        if(self.equipmentConnected == False or numCommands <= 0 or foundAllRunCommands == False):
            return False
        
        
        self.RMS = float(float(theNum) / (2 * math.sqrt(2)))
        self.inputPower = float(math.pow(self.RMS, 2) / float(self.impedance))
        self.inputPower = 10 * math.log10(1000 * self.inputPower)
        #self.smallVoltGain = self.inputPower - 
        
        print(self.RMS)
        print(self.inputPower)
        
        
