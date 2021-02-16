from equipment import Equipment_Connection
import json

class Run_Tests:
    """
    Module Used for Running Tests and Gathering Data
    """

    def __init__(self, name, fileName):
        fileName = 'JSON/tests/' + fileName
        with open(fileName) as f:
            jsonData = json.load(f)
        
        self.name = name
        self.equipmentList = jsonData[name]['Equipment List']
        self.configuration = jsonData[name]['config']
        self.run = jsonData[name]['run']
        self.reset = jsonData[name]['reset']
        self.equipmentConnected = False
        self.isConfigured = False
        self.devices = []
        self.graphTitle = "Spectrum Analyzer Trace"
        self.xLabel = "Frequency (MHZ)"
        self.yLabel = "Power (dBm)"
        self.centerFrequency = "2"
        self.frequencySpan = "2"
    
    def changeGraphSettings(self, title, xlabel, ylabel, centerFreq, freqSpan):
        self.graphTitle = title
        self.xLabel = xlabel
        self.yLabel = ylabel
        self.centerFrequency = centerFreq
        self.frequencySpan = freqSpan

    def addEquipment(self, listOfDevices):
        equipmentFound = True
        for equipment in self.equipmentList:
            found = False
            for device in listOfDevices:
                if(device.name == equipment):
                    if(device.isConnected == True):
                        self.devices.append(device)
                        found = True
            
            if(found == False):
                return False
        
        self.equipmentConnected = equipmentFound and len(listOfDevices) > 0
        print(self.devices)
        return self.equipmentConnected

    def configureTest(self):
        numCommands = int(self.configuration['num'])
        if(numCommands == 0 or self.equipmentConnected == False):
            return False

        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            commandType = self.configuration[currentCommand]['type']
            commandSyntax = self.configuration[currentCommand]['cmd']
            commandArgs = self.configuration[currentCommand]['args']
            equipmentName = self.configuration[currentCommand]['Equipment']
            title = self.configuration[currentCommand]['title']
            fullCommand = ''
            print(self.devices)
            for device in self.devices:
                if(device.name == equipmentName):
                    if(title == 'Set Center Frequency'):
                        fullCommand = str(commandSyntax) + str(self.centerFrequency) + "MHZ"
                    elif(title == 'Set Frequency Span'):
                        fullCommand = str(commandSyntax) + str(self.frequencySpan) + "MHZ"
                    else:
                        fullCommand = str(commandSyntax) + str(commandArgs)
                    
                    #print(fullCommand)
                    
                    if(commandType == 'q'):
                        device.query(fullCommand)
                    else:
                        if(device.write(fullCommand) == True):
                            return False
        self.isConfigured = True
        return self.isConfigured

    
    def resetTest(self):
        numCommands = int(self.reset['num'])
        if(numCommands == 0):
            return False

        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            commandType = self.reset[currentCommand]['type']
            commandSyntax = self.reset[currentCommand]['cmd']
            equipmentName = self.reset[currentCommand]['Equipment']
            for device in self.devices:
                if(device.name == equipmentName):
                    if(commandType == 'q'):
                        device.query(commandSyntax)
                    else:
                        if(device.write(commandSyntax)):
                            return False
        
        return True