from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np
import math
import plotly.graph_objects as go

def parseGetTrace(plotPoints, centerFreq, freqSpan, freqUnits):
    str_data = str(plotPoints)
    
    freqScaler = 0
    if(freqUnits == "GHz"):
        freqScaler = 1000000000
    elif(freqUnits == "MHz"):
        freqScaler = 1000000
    elif(freqUnits == "KHz"):
        freqScaler = 1000
    else:
        freqScaler = 1
        
    freqSpan = freqSpan * freqScaler
            
    if(str_data != None):
        str_data = str_data.split(" ", 1)[1]
        str_data = str_data.split(',')
        data_array = np.array(list(map(float, str_data[1:])))

        start = (int(centerFreq)-0.5*int(freqSpan))
        stop = (int(centerFreq)+0.5*int(freqSpan))
        step = (stop-start)/len(data_array)
        x = np.arange(start, stop, step)
        return x, data_array, start, stop
    else:
        return [], [], 0, 0

def findClosestIndex(values, val):
    minPosition = 0
    minDifference = float('inf')
    for i in range(len(values)):
        currentVal = values[i]
        currentDiff = abs(currentVal - val)
        if(currentDiff < minDifference):
            minDifference = currentDiff
            minPosition = i
        
    return minPosition

class P1dB_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        self.impedance = 0
        self.inputPower = 0
        self.smallVoltGain = 0
        self.setVoltCommand = None
        self.setFreqCommand = None
        self.setCenterFreqCommand = None
        self.voltDevice = None
        self.freqDevice = None
        
        self.freqStart = None
        self.freqStop = None
        self.freqStep = None
        self.voltStart = None
        self.voltStop = None
        self.voltStep = None
    
    def changeImpedance(self, impedance):
        self.impedance = float(impedance)
    
    def setFrequencyRange(self, freqStart, freqStop, freqStep):
        self.freqStart = float(freqStart)
        self.freqStop = float(freqStop)
        self.freqStep = float(freqStep)
    
    def setVoltSweepRange(self, voltStart, voltStop, voltStep):
        self.voltStart = float(voltStart)
        self.voltStop = float(voltStop)
        self.voltStep = float(voltStep)
        
    def setUpP1dBRunCommands(self, numCommands):
        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            title = self.run[currentCommand]['title']
            if(title == 'Set Volts'):
                self.setVoltCommand = self.run[currentCommand]
            elif(title == 'Set Frequency'):
                self.setFreqCommand = self.run[currentCommand]
            elif(title == 'Set Center Frequency'):
                self.setCenterFreqCommand = self.run[currentCommand]
                
        if(self.setVoltCommand == None or self.setFreqCommand == None):
            return False
        else:
            return True

    def runTest(self):
        numCommands = int(self.run['num'])
        foundAllRunCommands = self.setUpP1dBRunCommands(numCommands)
        if(self.equipmentConnected == False or numCommands <= 0 or foundAllRunCommands == False):
            return False
        
        #Plot settings for trace and p1dB graph as well
        abortTest = False
        frequency = []
        powerDB = []
        
        plt.ion()
        fig, ax = plt.subplots(1,1)
        figNum = fig.number
        plt.show()
        line, = ax.plot(frequency, powerDB,'r-')
        ax.set_xlabel(self.xLabel)
        ax.set_ylabel(self.yLabel)
        ax.set_title(self.graphTitle)
        
        #Getting frequency scaler
        freqScaler = 0
        if(self.freqUnits == "GHz"):
            freqScaler = 1000000000
        elif(self.freqUnits == "MHz"):
            freqScaler = 1000000
        elif(self.freqUnits == "KHz"):
            freqScaler = 1000
        else:
            freqScaler = 1
            
        #Table Setup
        frequencyOutput = []
        dBCompressionPoint = []
        headerLabel = []
        headerLabel.append("Frequency (" + self.freqUnits + ")")
        headerLabel.append('Input Power 1dB Compression Point')
        
        iterationCount = 0
        iterationMax = 1
        previousIterationCount = 0
        commandString = 'cmd'
        firstTime = False
        smallPowerDiff = 0
        
        while(abortTest == False and iterationCount < iterationMax):
            for i in range(numCommands):
                currentCommand = commandString + str(i + 1)
                commandType = self.run[currentCommand]['type']
                commandSyntax = self.run[currentCommand]['cmd']
                commandArgs = self.run[currentCommand]['args']
                equipmentName = self.run[currentCommand]['Equipment']
                title = self.run[currentCommand]['title']
                for device in self.devices:
                    if(device.name == equipmentName):
                        fullCommand = str(commandSyntax) + str(commandArgs)
                        if(title == 'Set Center Frequency'):
                            continue
                        if(title == 'Set Volts'):
                            self.voltDevice = device
                            continue
                        if(title == 'Set Frequency'):
                            self.freqDevice = device
                            continue
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency * freqScaler, self.frequencySpan, self.freqUnits)
                                            ax.set_xlim(start, stop)
                                            ax.set_ylim(-70, 30)
                                            line, = ax.plot(frequency, powerDB,'r-')
                                            plt.draw()
                                            plt.pause(0.02)
                                            firstTime = True
                                            
                                            #Gathering data for P1dB Graph
                                            freqCount = self.freqStart
                                            while(freqCount <= float(self.freqStop) + 0.05):
                                                currentFrequency = freqCount
                                                currentDBCompression = None
                                                currentFreqString = ""
                                                currentDBString = ""
                                                voltCount = self.voltStart
                                                smallPowerDiff = 0
                                                freqCommand = self.setFreqCommand['cmd'] + str(freqCount * freqScaler)
                                                self.freqDevice.write(freqCommand)
                                                centerFreqCommand = self.setCenterFreqCommand['cmd'] + str(freqCount) + self.freqUnits.upper()
                                                device.write(centerFreqCommand)
                                                print(freqCount)
                                                while(voltCount <= self.voltStop):
                                                    voltCommand = self.setVoltCommand['cmd'] + str(voltCount)
                                                    self.voltDevice.write(voltCommand)
                                                    plotPoints = device.query(fullCommand)
                                                    frequency, powerDB, start, stop = parseGetTrace(plotPoints, freqCount * freqScaler, self.frequencySpan, self.freqUnits)
                                                    ax.set_xlim(start, stop)
                                                    line.set_data(frequency, powerDB)
                                                    plt.draw()
                                                    plt.pause(0.02)
                                                    
                                                    RMS = float(float(voltCount) / (2 * math.sqrt(2)))
                                                    inputPower = float(math.pow(RMS, 2) / float(self.impedance))
                                                    inputPower = 10 * math.log10(1000 * inputPower)
                                                    closestIndex = findClosestIndex(frequency, freqCount * freqScaler)
                                                    outputPower = powerDB[closestIndex]
                                                    powerDiff = inputPower - outputPower
                                                    
                                                    if(voltCount == self.voltStart):
                                                        smallPowerDiff = powerDiff
                                                    else:
                                                        currentDiff = inputPower - outputPower
                                                        currCalc = abs(smallPowerDiff - currentDiff)
                                                        if(currCalc <= 1):
                                                            currentDBCompression = inputPower
                                                            currentFrequency = freqCount
                                                        else:
                                                            break
                                                        
                                                    voltCount = voltCount + self.voltStep
                                                
                                                currentFreqString = str(currentFrequency)
                                                if(currentDBCompression == None):
                                                    currentDBString = "Not Found"
                                                else:
                                                    currentDBString = str(currentDBCompression)
                                                    
                                                frequencyOutput.append(currentFreqString)
                                                dBCompressionPoint.append(currentDBString)
                                                    
                                                freqCount = freqCount + self.freqStep
                                            
                                    except:
                                        abortTest = True
                                        break
                                else:
                                    print('NOT DOING ANYTHING')
                            else:
                                device.query(fullCommand)
                        else:
                            if(device.write(fullCommand) == True):
                                return False, "Failed", tableOutput
            previousIterationCount = iterationCount
            iterationCount = iterationCount + 1
            if(not plt.fignum_exists(figNum)):
                abortTest = True
                plt.ioff()
                plt.show()
                break
        tableOutput = go.Figure(data=[go.Table( 
          header=dict( 
            values=headerLabel, 
            line_color='darkslategray',
            fill_color='lightcyan', 
            align=['center','center'], 
            font=dict(color='black', size=12) 
          ), 
          cells=dict( 
            values=[frequencyOutput, dBCompressionPoint], 
            line_color='darkslategray',
            fill_color='lightcyan', 
            align = ['left', 'center'], 
            font = dict(color = 'darkslategray', size = 11) 
            )) 
        ]) 
                 
        if(abortTest == True):
            self.isConfigured = False
            return False, "Aborted", tableOutput
        
        self.isConfigured = False
        return True, "Success", tableOutput
    
        """
        self.RMS = float(float(theNum) / (2 * math.sqrt(2)))
        self.inputPower = float(math.pow(self.RMS, 2) / float(self.impedance))
        self.inputPower = 10 * math.log10(1000 * self.inputPower)
        #self.smallVoltGain = self.inputPower - 
        
        print(self.RMS)
        print(self.inputPower)"""