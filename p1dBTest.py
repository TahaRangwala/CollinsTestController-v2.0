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

    def __init__(self, name, fileName, title, xlabel, ylabel):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel)
        self.impedance = 0
        self.inputPower = 0
        self.smallVoltGain = 0
        self.setVoltCommand = None
        self.setFreqCommand = None
        self.traceDataCommand = None
        self.peakDataCommand = None
        
        self.freqStart = 0
        self.freqStop = 0
        self.voltStart = 0
        self.voltStop = 0
    
    def changeImpedance(self, impedance):
        self.impedance = impedance
    
    def setFrequencyRange(self, freqStart, freqStop):
        self.freqStart = freqStart
        self.freqStop = freqStop
    
    def setVoltSweepRange(self, voltStart, voltStop):
        self.voltStart = voltStart
        self.voltStop = voltStop

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False and numCommands <= 0):
            return False
        
        