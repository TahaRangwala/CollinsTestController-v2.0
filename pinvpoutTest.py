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

class PinVPout_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel)
        self.outputTable = None
        self.peakFreq = []
        self.powerIn = []
        self.powerLoss = []
        self.powerMeasured = []
        self.peakAmplitude = []
        self.Pin_Pout = []
        self.iterationMax = 0
        
    def configurePowerInPowerLoss(self):
        self.iterationMax = 0
        with open("JSON/tests/PinvPoutSettings/PowerIn.txt") as testFileList:
            for line in testFileList:
                values = line.split(",")
                currentPeakFreq = int(values[0].strip())
                currentPowerIn = int(values[1].strip())
                self.peakFreq.append(currentPeakFreq)
                self.powerIn.append(currentPowerIn)
                self.iterationMax = self.iterationMax + 1
                
        with open("JSON/tests/PinvPoutSettings/PowerLoss.txt") as testFileList:
            for line in testFileList:
                currentPowerLoss = int(line.strip())
                self.powerLoss.append(currentPowerLoss)

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
        peakFreqOutput = []
        powerInOutput = []
        powerMeasuredOutput = []
        powerLossOutput = []
        peakAmplitudeOutput = []
        pinpoutOutput = []
        previousPowerLoss = 0
        iterationCount = 0
        commandString = 'cmd'
        firstTime = False
        
        while(abortTest == False and iterationCount <= self.iterationMax):
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
                                            currentPeakFreq = self.peakFreq[iterationCount]
                                            currentPowerIn = self.powerIn[iterationCount]
                                            centerPoint = int(len(frequency)/2)
                                            currentPowerMeasured = powerDB[centerPoint]
                                            currentPowerLoss = self.powerLoss[iterationCount]
                                            previousPowerLoss = currentPowerLoss
                                            currentPeakAmplitude = currentPowerMeasured + abs(currentPowerIn - currentPowerLoss)
                                            currentPinPout = abs(currentPowerMeasured) + abs(currentPowerIn - currentPowerLoss)
                                            
                                            #Adding stuff to table
                                            peakFreqOutput.append(currentPeakFreq)
                                            powerInOutput.append(currentPowerIn)
                                            powerMeasuredOutput.append(currentPowerMeasured)
                                            powerLossOutput.append(currentPowerLoss)
                                            peakAmplitudeOutput.append(currentPeakAmplitude)
                                            pinpoutOutput.append(currentPinPout)
                                            
                                        else:
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                            
                                            currentPeakFreq = self.peakFreq[iterationCount]
                                            currentPowerIn = self.powerIn[iterationCount]
                                            centerPoint = int(len(frequency)/2)
                                            currentPowerMeasured = powerDB[centerPoint]
                                            currentPowerLoss = self.powerLoss[iterationCount]
                                            previousPowerLoss = currentPowerLoss
                                            currentPeakAmplitude = currentPowerMeasured + abs(currentPowerLoss)
                                            currentPinPout = abs(currentPowerMeasured) + abs(currentPowerIn - currentPowerLoss)
                                            
                                            #Adding stuff to table
                                            peakFreqOutput.append(currentPeakFreq)
                                            powerInOutput.append(currentPowerIn)
                                            powerMeasuredOutput.append(currentPowerMeasured)
                                            powerLossOutput.append(currentPowerLoss)
                                            peakAmplitudeOutput.append(currentPeakAmplitude)
                                            pinpoutOutput.append(currentPinPout)
                                            
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

        if(abortTest == True):
            self.isConfigured = False
            return False, "Aborted", tableOutput
        
        tableOutput = go.Figure(data=[go.Table(
            header=dict(values=['Peak Frequency (MHz)', 'Power In (dBm)', 'Power Measured (dBm)', 'Power Loss', 'Peak Amplitude (dBm)' , 'Pin-Pout'],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='left'),
            cells=dict(values=[peakFreqOutput,
                               powerInOutput,
                               powerMeasuredOutput,
                               powerLossOutput,
                               peakAmplitudeOutput,
                               pinpoutOutput],
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='left'))
        ])
                
        return True, "Success", tableOutput
        
        