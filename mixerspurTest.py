#File Description: This .py file contains the Mixer_Spur_Test class. This class inherits from the Run_Tests class in the test.py file, and it
#has its own unique run function, which contains the algorithm that produces the spectrum analyzer trace and the harmonics table output

#Required imports
from tests import Run_Tests#Importing the Run_Tests class from tests.py
import matplotlib.pyplot as plt#used for plotting graphs
import numpy as np#array calculations
import plotly.graph_objects as go#used for making tables

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

#Mixer_Spur_Test class declaration
class Mixer_Spur_Test(Run_Tests):

    #Constructor
    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        
        #Default values for instance variables
        self.matrixSize = 5#matrix size
        self.inputFrequency = 0.0#input frequency
        self.localOscillator = 0.0#local oscillator frequency
        self.RF = 0.0#Radio frequency
        self.freqStart = 0.0#frequency start
        self.freqStop = 0.0#frequency stop
        self.setCenterFreqCommand = None#commmand associated with set center frequency
    
    #This function changes the values of the instance variables
    def changeMixerParameters(self, matrixSize, inputFreq, localOscillate, RF, freqStart, freqStop):
        self.matrixSize = int(matrixSize)
        self.inputFrequency = inputFreq
        self.localOscillator = localOscillate
        self.RF = RF
        self.freqStart = freqStart
        self.freqStop = freqStop
        if self.localOscillator == 0:
            self.localOscillator = self.RF
            
    #This function runs the commands associated with the run section in the test json file. This function has been customized specifically
    #for the Mixer Spur test. Pay close attention to how the commands are specifically used for this tests. This is also described in the
    #user manual
    def runTest(self):
        numCommands = int(self.run['num'])
        foundAllCommands = False
        
        #Getting the command associated with the set center frequency and assigning it to an instance variable
        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            title = self.run[currentCommand]['title']
            if(title == 'Set Center Frequency'):
                self.setCenterFreqCommand = self.run[currentCommand]
        
        #Making sure everything is set up
        if(self.equipmentConnected == False or numCommands <= 0 or self.setCenterFreqCommand == None):
            return False, "Failed", None
        
        #Plot settings for spectrum analyzer trace
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
        
        #Table Settings for harmonics table output
        tableOutput = None
        headerLabel = [" "]
        cellLabel = []
        scaleLocalOscillator = []
        scaleRF = []
        scaleFreq = []
        cellValues = []
        
        #Freqeuncy scaler based off frequency units
        freqScaler = 0
        if(self.freqUnits == "GHz"):
            freqScaler = 1000000000
        elif(self.freqUnits == "MHz"):
            freqScaler = 1000000
        elif(self.freqUnits == "KHz"):
            freqScaler = 1000
        else:
            freqScaler = 1
        
        #scaling the frequency start and stop
        self.freqStart = float(self.freqStart) * freqScaler
        self.freqStop = float(self.freqStop) * freqScaler
        
        #Setting up the table arrays used for the harmonics table output and the different frequencies the
        #user has inputted in the GUI
        for i in range(self.matrixSize + 1):
            scaleLocalOscillator.append(i * float(self.localOscillator) * freqScaler)
            scaleRF.append(i * float(self.RF) * freqScaler)
            scaleFreq.append(i * float(self.inputFrequency) * freqScaler)
            cellString = "<b>" + str(i) + "x" + str(self.localOscillator) + self.freqUnits + "</b>"
            cellLabel.append(cellString)
            headerString = "<b>" + str(i) + "x" + str(self.inputFrequency) + self.freqUnits + "</b>"
            headerLabel.append(headerString)
        
        #Adding a cell value for the table label on the first column for the harmonics table
        cellValues.append(cellLabel)

        #Variables used for iteration
        iterationCount = 0
        iterationMax = self.matrixSize + 1#based off the matrix size the user inputted
        previousIterationCount = 0
        commandString = 'cmd'
        firstTime = False
        
        #looping through all the commands based on the iteration count or if the test has been aborted
        while(abortTest == False and iterationCount < iterationMax):
            for i in range(numCommands):
                #Getting information from the current command
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
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):#unique for the get trace command
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):
                                            #Setting up the plot initially and gathering the initial data from the spectrum analyzer
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency * freqScaler, self.frequencySpan, self.freqUnits)
                                            ax.set_xlim(start, stop)
                                            line, = ax.plot(frequency, powerDB,'r-')
                                            plt.draw()
                                            plt.pause(0.02)
                                            firstTime = True
                                            
                                            #Spur Table 
                                            currentCell = []
                                            currentFreq = scaleFreq[iterationCount]
                                            length = len(scaleLocalOscillator)
                                            print(iterationCount)
                                            for j in range(len(scaleLocalOscillator)):#looping through the local oscillator frequencies
                                                currentString = ""
                                                currentFrequency = abs(currentFreq - scaleLocalOscillator[j])
                                                if(currentFrequency >= frequency[0] and currentFrequency <= frequency[len(frequency)-1]):#making sure the frequency is in range
                                                    closestIndex = findClosestIndex(frequency, currentFrequency)#returns the index of the closest value in the frequency array
                                                    currentPowerMeasured = powerDB[closestIndex]#gets the power associated with the frequency
                                                    currentString = str(currentPowerMeasured) + " dBm"
                                                elif(currentFrequency >= self.freqStart and currentFrequency <= self.freqStop):#checking if frequency is in entire range
                                                    freqCommand = str(self.setCenterFreqCommand['cmd']) + str(currentFrequency)
                                                    isFreqError = device.write(freqCommand)
                                                    
                                                    #Changes the center frequency so we can read the correct value
                                                    plotPoints = device.query(fullCommand)
                                                    self.centerFrequency = currentFrequency
                                                    
                                                    #Reads the data from the spectrum analyzer
                                                    frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan, self.freqUnits)
                                                    if(len(frequency) != 0 and isFreqError == False):#checking if there is an error
                                                        #Doing same stuff as above with getting the current power and then updating the plot and table arrays
                                                        closestIndex = findClosestIndex(frequency, currentFrequency)
                                                        currentPowerMeasured = powerDB[closestIndex]
                                                        currentString = str(currentPowerMeasured) + " dBm"
                                                        ax.set_xlim(start, stop)
                                                        line.set_data(frequency, powerDB)
                                                        plt.draw()
                                                        plt.pause(0.02)
                                                    else:#error occurred
                                                        currentString = "ERROR"
                                                else:#frequency is not in the range
                                                    currentString = "Out of Range"
                                                
                                                currentCell.append(currentString)
                                            
                                            cellValues.append(currentCell)
                                                
                                        else:
                                            #updating the spectrum analyzer trace
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan, self.freqUnits)
                                            ax.set_xlim(start, stop)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                            
                                            #Update Spur Table (same as previous loop)
                                            currentCell = []
                                            currentFreq = scaleFreq[iterationCount]
                                            if(iterationCount != previousIterationCount):
                                                for j in range(len(scaleLocalOscillator)):
                                                    currentFrequency = abs(currentFreq - scaleLocalOscillator[j])
                                                    if(currentFrequency >= frequency[0] and currentFrequency <= frequency[len(frequency)-1]):
                                                        closestIndex = findClosestIndex(frequency, currentFrequency)
                                                        currentPowerMeasured = powerDB[closestIndex]
                                                        currentString = str(currentPowerMeasured) + " dBm"
                                                    elif(currentFrequency >= self.freqStart and currentFrequency <= self.freqStop):
                                                        freqCommand = str(self.setCenterFreqCommand['cmd']) + str(currentFrequency)
                                                        isFreqError = device.write(freqCommand)
                                                        plotPoints = device.query(fullCommand)
                                                        self.centerFrequency = currentFrequency
                                                        frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan, self.freqUnits)
                                                        if(len(frequency) != 0 and isFreqError == False):
                                                            closestIndex = findClosestIndex(frequency, currentFrequency)
                                                            currentPowerMeasured = powerDB[closestIndex]
                                                            currentString = str(currentPowerMeasured) + " dBm"
                                                            ax.set_xlim(start, stop)
                                                            line.set_data(frequency, powerDB)
                                                            plt.draw()
                                                            plt.pause(0.02)
                                                        else:
                                                            currentString = "ERROR"
                                                    else:
                                                        currentString = "Out of Range"
                                                        
                                                    currentCell.append(currentString)
                                                                                            
                                                cellValues.append(currentCell)
                                            else:
                                                continue
                                    except:#if the test is aborted
                                        abortTest = True
                                        break
                                else:
                                    print('NOT DOING ANYTHING')
                            else:
                                device.query(fullCommand)
                        else:
                            if(device.write(fullCommand) == True):
                                return False, "Failed", tableOutput
                            
            #updating the iteration count and making sure the plot has not been closed
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
            fill_color='lightskyblue', 
            align=['center','center'], 
            font=dict(color='white', size=12) 
          ), 
          cells=dict( 
            values=cellValues, 
            line_color='darkslategray',
            fill_color='lightcyan', 
            align = ['center', 'center'], 
            font = dict(color = 'darkslategray', size = 11) 
            )) 
        ]) 
        
        #if the test was aborted
        if(abortTest == True):
            self.isConfigured = False
            return False, "Aborted", tableOutput
        
        #Makes sure table has no dummy data
        tempCellValues = []
        tempCellValues.append(cellValues[0])
        for i in range(iterationMax):
            tempCellValues.append(cellValues[i+1])
        cellValues = tempCellValues
        
        self.isConfigured = False
        return True, "Success", tableOutput