#File Description: This .py file contains the Other_Test class. This is a template class that can be modified for a custom test.
#Make note of what the other test child classes are doing to get an idea of what a new test could look like

#Required imports
from tests import Run_Tests#Importing the Run_Tests class from tests.py
import matplotlib.pyplot as plt#used for plotting graphs
import numpy as np#used for array operations

#This function returns a list of x values, an array of y values, and an x axis start and stop position based off a
#set of points passed in, a center frequency, and a frequency span as well
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

#Other_Test class declaration
class Other_Test(Run_Tests):
    
    #Constructor for Other_Test
    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits, powUnits):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits, powUnits) 
    
    #Modifiable run test function that is unique for this child class.
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
        
        #Iterating through all of the commands in the run section of the tests json file associated with this
        #class
        iterationCount = 0
        commandString = 'cmd'
        firstTime = False
        while(abortTest == False and iterationCount <= 7):
            for i in range(numCommands):
                #Getting information on the current command
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
                            if(title == 'Get Trace'):#Unique to the Get Trace Command
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):#initial graph if first iteration
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            ax.set_xlim(start, stop)
                                            line, = ax.plot(frequency, powerDB,'r-')
                                            plt.draw()
                                            plt.pause(0.02)
                                            firstTime = True
                                        else:#updating graph
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
        
        #If the test is aborted
        if(abortTest == True):
            #self.isConfigured = False
            return False, "Aborted"
        
        return True, "Success"
