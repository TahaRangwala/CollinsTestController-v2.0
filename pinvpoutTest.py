from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable

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
        self.outputTable = PrettyTable(["Peak Frequency (MHz)", "Power In (dBm)", "Power Measured (dBm)", "Peak Amplitude (dBm)", "Pin-Pout"])

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False and numCommands <= 0):
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

        iterationCount = 0
        commandString = 'cmd'
        firstTime = False
        while(abortTest == False and iterationCount <= 7):
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
                                        else:
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                    except:
                                        abortTest = True
                                        break
                                else:
                                    print('NOT DOING ANYTHING')
                            else:
                                device.query(fullCommand)
                        else:
                            if(device.write(fullCommand) == True):
                                return False, "Failed"
            iterationCount = iterationCount + 1
            if(not plt.fignum_exists(figNum)):
                abortTest = True
                plt.ioff()
                plt.show()
                break

        if(abortTest == True):
            self.isConfigured = False
            return False, "Aborted"
        
        return True, "Success"
        
        