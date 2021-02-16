from tests import Run_Tests
import matplotlib.pyplot as plt

def parseGetTrace(plotPoints):
    str_data = str(plotPoints)
    str_data = str_data.split("  ", 1)[1]
    str_data = str_data.split(',')
    data_array = np.array(list(map(float, str_data[1:])))
    
    start = (int(1)-0.5*int(1)) * 10**6
    stop = (int(1)+0.5*int(1)) * 10**6
    step = (stop-start)/len(data_array)
    x = np.arange(start, stop, step)
    
    return x, data_array, start, stop

class PinVPout_Test(Run_Tests):

    def __init__(self, name, fileName):
        Run_Tests.__init__(self, name, fileName)
        self.figure = plt.gcf()
        self.number = self.figure.number

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False and numCommands <= 0):
            return False
        #currentSubplot = self.figure.add_subplot(311)
        #currentSubplot.cla()
        #currentSubplot.set_xlabel = self.xLabel
        #currentSubplot.set_ylabel = self.yLabel
        #currentSubplot.set_title = self.graphTitle
        iterationCount = 0
        abortTest = False
        commandString = 'cmd'
        while(abortTest == False and iterationCount <= 7):
            if(not plt.fignum_exists(self.number)):
               abortTest = True
            for i in range(numCommands):
                currentCommand = commandString + str(i + 1)
                commandType = self.run[currentCommand]['type']
                commandSyntax = self.run[currentCommand]['cmd']
                commandArgs = self.run[currentCommand]['args']
                equipmentName = self.run[currentCommand]['Equipment']
                for device in self.devices:
                    if(device.name == equipmentName):
                        fullCommand = str(commandSyntax) + str(commandArgs)
                        print(fullCommand)
                        if(commandType == 'q'):
                            if(self.run[currentCommand]['title'] == 'Get Trace'):
                                plotPoints = device.query(fullCommand)
                                frequency, powerDB, start, stop = parseGetTrace(plotPoints)
                                #print(powerDB)
                                #currentSubplot.plot(frequency, powerDB)
                                #currentSubplot.set_xlim(start, stop)
                                #plt.show()
                            else:
                                device.query(fullCommand)
                        else:
                            if(device.write(fullCommand) == True):
                                return False, "Failed"
            iterationCount = iterationCount + 1
            #print(iterationCount)
        if(abortTest == True):
            return False, "Aborted"
        return True, "Success"
        
        