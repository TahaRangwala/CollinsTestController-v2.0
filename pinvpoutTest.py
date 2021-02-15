from tests import Run_Tests
import matplotlib.pyplot as plt

def parseGetPeak(plotPoints):
    pass

class PinVPout_Test(Run_Tests):

    def __init__(self, name, fileName):
        Run_Tests.__init__(self, name, fileName)
        self.figure = plt.figure()
        self.abortTest = False

    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False and numCommands <= 0):
            return False
        
        iterationCount = 0
        
        commandString = 'cmd'
        while(self.abortTest == False and iterationCount <= 7):
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
                            if(self.run[currentCommand]['title'] == 'Get Peak'):
                                plotPoints = device.query(fullCommand)
                                frequency, powerDB = parseGetPeak(plotPoints)
                            else:
                                device.query(fullCommand)
                    else:
                        if(device.write(fullCommand) == True):
                            return False