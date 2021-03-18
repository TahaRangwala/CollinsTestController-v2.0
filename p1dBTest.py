#File Description: This .py file contains the P1dB_Test class. This class inherits from the Run_Tests class in the test.py file, and it
#has its own unique run function, which contains the algorithm that produces the spectrum analyzer trace and the 1dB Compression Point table

#Required imports
from tests import Run_Tests#Importing the Run_Tests class from tests.py
import matplotlib.pyplot as plt#used for plotting graphs
import numpy as np#array calculations
import plotly.graph_objects as go#used for making tables
import math#used for some calculations

#This function returns a list of x values, an array of y values, and an x axis start and stop position based off a
#set of points passed in, a center frequency, and a frequency span as well
def parseGetTrace(plotPoints, centerFreq, freqSpan):
    
    #Formatting the data array
    str_data = str(plotPoints)
    str_data = str_data.split(" ", 1)[1]
    str_data = str_data.split(',')
    data_array = np.array(list(map(float, str_data[1:])))
    
    #Calculating the start, stop, and x values that will be returned
    start = (int(centerFreq)-0.5*int(freqSpan))
    stop = (int(centerFreq)+0.5*int(freqSpan))
    step = (stop-start)/len(data_array)
    x = np.arange(start, stop, step)
    return x, data_array, start, stop

#This function finds the index that contains the closest value to the val variable in the list of values passed in
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

#P1dB_Test class declaration
class P1dB_Test(Run_Tests):

    #Constructor
    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        self.impedance = 0#impedance
        self.inputPower = 0#input power
        self.smallVoltGain = 0#small voltage gain
        self.setVoltCommand = None#set volt command from json file
        self.setFreqCommand = None#set frequency comand from json file
        self.setCenterFreqCommand = None#set center frequency command from json file
        self.voltDevice = None#device associated with set volt command
        self.freqDevice = None#device associated with set frequency command
        self.freqStart = None#frequency start when looping through frequencies
        self.freqStop = None#frequency stop when looping through frequencies
        self.freqStep = None#frequency step when looping through frequencies
        self.voltStart = None#volt start when looping through vpps
        self.voltStop = None#volt stop when looping through vpps
        self.voltStep = None#volt step when looping through vpps
    
    #This function changes the impedance
    def changeImpedance(self, impedance):
        self.impedance = float(impedance)
    
    #This function changes the frequency range and step
    def setFrequencyRange(self, freqStart, freqStop, freqStep):
        self.freqStart = float(freqStart)
        self.freqStop = float(freqStop)
        self.freqStep = float(freqStep)
    
    #This function changes the voltage range and step
    def setVoltSweepRange(self, voltStart, voltStop, voltStep):
        self.voltStart = float(voltStart)
        self.voltStop = float(voltStop)
        self.voltStep = float(voltStep)
    
    #This function finds the commands associated with the P1dB Test and assigns them to instance variables
    #commands needed include set volts, set frequency, and set center frequency as well
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
                
        if(self.setVoltCommand == None or self.setFreqCommand == None or self.setCenterFreqCommand == None):
            return False
        else:
            return True
    
    #This function runs the commands associated with the run section in the test json file. This function has been customized specifically
    #for the P1dB test. Pay close attention to how the commands are specifically used for this tests. This is also described in the
    #user manual
    def runTest(self):
        numCommands = int(self.run['num'])
        foundAllRunCommands = self.setUpP1dBRunCommands(numCommands)
        if(self.equipmentConnected == False or numCommands <= 0 or foundAllRunCommands == False):
            return False
        
        #Plot settings for trace and p1dB graph as well
        abortTest = False
        frequency = []
        powerDB = []
        
        #Setting up the Spectrum Analyzer Trace plot
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
            
        #Table Setup for the 1dB Compression Point table
        frequencyOutput = []
        dBCompressionPoint = []
        headerLabel = []
        headerLabel.append("Frequency (" + self.freqUnits + ")")
        headerLabel.append('Input Power 1dB Compression Point')
        
        #Variables used throughout the iteration
        iterationCount = 0
        iterationMax = 1
        previousIterationCount = 0
        commandString = 'cmd'
        firstTime = False
        smallPowerDiff = 0
        
        #Loop to run through commands. Stops only if the iteration max has been met or the test has been aborted
        while(abortTest == False and iterationCount < iterationMax):
            for i in range(numCommands):
                #Getting information on the current command being looped through
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
                        if(title == 'Set Volts'):#Gets the device associated with the set volts command
                            self.voltDevice = device
                            continue
                        if(title == 'Set Frequency'):#Gets the device associated with the set frequency command
                            self.freqDevice = device
                            continue
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):#Takes information when the Get Trace command gets data
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):
                                            #Setting up the plot initially and gathering the initial data from the spectrum analyzer
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
                                            while(freqCount <= float(self.freqStop) + 0.05):#looping through the frequencies
                                                
                                                #Setting up variables
                                                currentFrequency = freqCount
                                                currentDBCompression = None
                                                currentFreqString = ""
                                                currentDBString = ""
                                                voltCount = self.voltStart
                                                smallPowerDiff = 0
                                                
                                                #Setting the freqeuncy asscociated with the device
                                                freqCommand = self.setFreqCommand['cmd'] + str(freqCount * freqScaler)
                                                self.freqDevice.write(freqCommand)
                                                #Setting the center frequency (same device as the Get Trace command)
                                                centerFreqCommand = self.setCenterFreqCommand['cmd'] + str(freqCount) + self.freqUnits.upper()
                                                device.write(centerFreqCommand)
                                                
                                                while(voltCount <= self.voltStop):#looping through the voltages (vpp)
                                                    voltCommand = self.setVoltCommand['cmd'] + str(voltCount)
                                                    
                                                    #Seting the voltage (vpp) for the device associated with it
                                                    self.voltDevice.write(voltCommand)
                                                    
                                                    #Gathering data from the spectrum analyzer
                                                    plotPoints = device.query(fullCommand)
                                                    frequency, powerDB, start, stop = parseGetTrace(plotPoints, freqCount * freqScaler, self.frequencySpan, self.freqUnits)
                                                    ax.set_xlim(start, stop)
                                                    line.set_data(frequency, powerDB)
                                                    plt.draw()
                                                    plt.pause(0.02)
                                                    
                                                    #Calculating associated with the P1dB Test
                                                    RMS = float(float(voltCount) / (2 * math.sqrt(2)))
                                                    inputPower = float(math.pow(RMS, 2) / float(self.impedance))
                                                    inputPower = 10 * math.log10(1000 * inputPower)
                                                    closestIndex = findClosestIndex(frequency, freqCount * freqScaler)
                                                    outputPower = powerDB[closestIndex]
                                                    powerDiff = inputPower - outputPower
                                                    
                                                    #This checks to see if the 1dB Compresion point has been found or not
                                                    if(voltCount == self.voltStart):
                                                        smallPowerDiff = powerDiff
                                                    else:#makes sure the first iteration has been completed at least otherwise sets the current compression point to the
                                                        #input power and its frequency to the current frequency
                                                        currentDiff = inputPower - outputPower
                                                        currCalc = abs(smallPowerDiff - currentDiff)
                                                        if(currCalc <= 1):
                                                            currentDBCompression = inputPower
                                                            currentFrequency = freqCount
                                                        else:
                                                            break
                                                        
                                                    voltCount = voltCount + self.voltStep
                                                    
                                                #Updating the 1dB Compresion point table array
                                                #Makes sure a compression point was found otherwise adds Not Found to table
                                                currentFreqString = str(round(currentFrequency, 3))
                                                if(currentDBCompression == None):
                                                    currentDBString = "Not Found"
                                                else:
                                                    currentDBString = str(round(currentDBCompression, 3))
                                                
                                                #Updating output arrays
                                                frequencyOutput.append(currentFreqString)
                                                dBCompressionPoint.append(currentDBString)
                                                    
                                                freqCount = freqCount + self.freqStep
                                            
                                    except:
                                        abortTest = True
                                        break
                                else:
                                    print('NOT DOING ANYTHING')
                            else:#runs query command if nothing else has been caught by the if statement
                                device.query(fullCommand)
                        else:#runs write commands
                            if(device.write(fullCommand) == True):
                                return False, "Failed", tableOutput
            
            #updating the iteration count and checking if the plot window has been closed
            previousIterationCount = iterationCount
            iterationCount = iterationCount + 1
            if(not plt.fignum_exists(figNum)):
                abortTest = True
                plt.ioff()
                plt.show()
                break
        
        #Setting up the table output
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
            align = ['centers', 'center'], 
            font = dict(color = 'darkslategray', size = 11) 
            )) 
        ]) 
        
        #if the test is aborted
        if(abortTest == True):
            self.isConfigured = False
            return False, "Aborted", tableOutput
        
        self.isConfigured = False
        return True, "Success", tableOutput