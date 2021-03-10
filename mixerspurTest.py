from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

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

class Mixer_Spur_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        self.matrixSize = 5
        self.inputFrequency = 0.0
        self.localOscillator = 0.0
        self.RF = 0.0
        
    def changeMixerParameters(self, matrixSize, inputFreq, localOscillate):
        self.matrixSize = int(matrixSize)
        self.inputFrequency = inputFreq
        self.localOscillator = localOscillate
        self.RF = self.inputFrequency + self.localOscillator

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False or numCommands <= 0):
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
        
        for i in range(self.matrixSize):
            scaleLocalOscillator.append((i+1) * float(self.localOscillator) * freqScaler)
            scaleRF.append((i+1) * float(self.RF) * freqScaler)
            cellString = "<b>" + str(i+1) + "x" + str(self.localOscillator) + freqUnits + "</b>"
            cellLabel.append(cellString)
            headerString = "<b>" + str(i+1) + "x" + str(self.RF) + freqUnits + "</b>"
            headerLabel.append(headerString)
        
        cellValues.append(cellLabel)

        iterationCount = 0
        iterationMax = self.matrixSize
        commandString = 'cmd'
        firstTime = False
        while(abortTest == False and iterationCount <= iterationMax):
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
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            ax.set_xlim(start, stop)
                                            line, = ax.plot(frequency, powerDB,'r-')
                                            plt.draw()
                                            plt.pause(0.02)
                                            firstTime = True
                                            
                                            #Spur Table 
                                            currentCell = []
                                            currentRF = scaleRF[iterationCount]
                                            for j in range(len(scaleOscillator)):
                                                currentString = ""
                                                currentFrequency = currentRF - scaleOscillator[j]
                                                if(currentFrequency >= frequency[0] and currentFrequency <= frequency[len(frequency)-1]):
                                                    centerPoint = int(frequency.index(frequency[min(range(len(frequency)), key = lambda i: abs(frequency[i]-currentFrequency))]))
                                                    currentPowerMeasured = powerDB[centerPoint]
                                                    currentString = str(currentPowerMeasured) + "dBm"
                                                else:
                                                    currentString = "Out of Range"
                                                
                                                currentCell.append(currentString)
                                            
                                            cellValues.append(currentCell)
                                                
                                        else:
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                            
                                            #Update Spur Table
                                            currentCell = []
                                            currentRF = scaleRF[iterationCount]
                                            for j in range(len(scaleOscillator)):
                                                currentString = ""
                                                currentFrequency = currentRF - scaleOscillator[j]
                                                if(currentFrequency >= frequency[0] and currentFrequency <= frequency[len(frequency)-1]):
                                                    centerPoint = int(frequency.index(frequency[min(range(len(frequency)), key = lambda i: abs(frequency[i]-currentFrequency))]))
                                                    currentPowerMeasured = powerDB[centerPoint]
                                                    currentString = str(currentPowerMeasured) + "dBm"
                                                else:
                                                    currentString = "Out of Range"
                                                
                                                currentCell.append(currentString)
                                            
                                            cellValues.append(currentCell)
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
            align=['left','center'], 
            font=dict(color='white', size=12) 
          ), 
          cells=dict( 
            values=cellValues, 
            line_color='darkslategray',
            fill_color='lightcyan', 
            align = ['left', 'center'], 
            font = dict(color = 'darkslategray', size = 11) 
            )) 
        ]) 
        
        if(abortTest == True):
            #self.isConfigured = False
            return False, "Aborted", tableOutput
        
        return True, "Success", tableOutput