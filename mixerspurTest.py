from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np
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

class Mixer_Spur_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        self.matrixSize = 5
        self.inputFrequency = 0.0
        self.localOscillator = 0.0
        self.RF = 0.0
        self.freqStart = 0.0
        self.freqStop = 0.0
        self.setCenterFreqCommand = None
        
    def changeMixerParameters(self, matrixSize, inputFreq, localOscillate, RF, freqStart, freqStop):
        self.matrixSize = int(matrixSize)
        self.inputFrequency = inputFreq
        self.localOscillator = localOscillate
        self.RF = RF
        self.freqStart = freqStart
        self.freqStop = freqStop
        if self.localOscillator == 0:
            self.localOscillator = self.RF
            
        
    def runTest(self):
        numCommands = int(self.run['num'])
        foundAllCommands = False
        
        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            title = self.run[currentCommand]['title']
            if(title == 'Set Center Frequency'):
                self.setCenterFreqCommand = self.run[currentCommand]
                   
        if(self.equipmentConnected == False or numCommands <= 0 or self.setCenterFreqCommand == None):
            return False
        
        #Plot settings for trace
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
        
        #Table Settings
        tableOutput = None
        headerLabel = [" "]
        cellLabel = []
        scaleLocalOscillator = []
        scaleRF = []
        scaleFreq = []
        cellValues = []
        
        freqScaler = 0
        if(self.freqUnits == "GHz"):
            freqScaler = 1000000000
        elif(self.freqUnits == "MHz"):
            freqScaler = 1000000
        elif(self.freqUnits == "KHz"):
            freqScaler = 1000
        else:
            freqScaler = 1
        
        self.freqStart = float(self.freqStart) * freqScaler
        self.freqStop = float(self.freqStop) * freqScaler
        
        for i in range(self.matrixSize + 1):
            scaleLocalOscillator.append(i * float(self.localOscillator) * freqScaler)
            scaleRF.append(i * float(self.RF) * freqScaler)
            scaleFreq.append(i * float(self.inputFrequency) * freqScaler)
            cellString = "<b>" + str(i) + "x" + str(self.localOscillator) + self.freqUnits + "</b>"
            cellLabel.append(cellString)
            headerString = "<b>" + str(i) + "x" + str(self.inputFrequency) + self.freqUnits + "</b>"
            headerLabel.append(headerString)
        
        cellValues.append(cellLabel)

        iterationCount = 0
        iterationMax = self.matrixSize + 1
        previousIterationCount = 0
        commandString = 'cmd'
        firstTime = False
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
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):
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
                                            for j in range(len(scaleLocalOscillator)):
                                                currentString = ""
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
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan, self.freqUnits)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                            
                                            #Update Spur Table
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