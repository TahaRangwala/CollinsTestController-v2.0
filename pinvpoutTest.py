from tests import Run_Tests
import matplotlib.pyplot as plt
import numpy as np

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

    def __init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan)
        self.figure = None

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False and numCommands <= 0):
            return False
        
        #Plot settings for trace
        frequency = []
        powerDB = []
        plt.title(self.graphTitle)
        plt.xlabel(self.xLabel)
        plt.ylabel(self.yLabel)
        plt.show()

        iterationCount = 0
        abortTest = False
        commandString = 'cmd'
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
                                plotPoints = device.query(fullCommand)
                                frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                plt.xlim(start, stop)
                                plt.plot(frequency, powerDB)
                            else:
                                device.query(fullCommand)
                        else:
                            if(device.write(fullCommand) == True):
                                return False, "Failed"
            iterationCount = iterationCount + 1
            if(abortTest == False and not plt.fignum_exists(figNum)):
                abortTest = True

        if(abortTest == True):
            return False, "Aborted"
        
        self.isConfigured = False
        return True, "Success"
        
        