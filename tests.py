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

        self.devices = []

    def addEquipment(self, listOfDevices):
        allFound = False
        for device in listOfDevices:
            found = False
            for equipment in self.equipmentList:
                if(device.name == equipment):
                    self.devices.append(device)
                    found = True
                else:
                    continue
        
        return equipmentFound

    def configureTest(self):
        numCommands = self.configuration['num']
        if(numCommands == 0):
            return False

        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)
            commandType = self.configuration[currentCommand]['type']
            commandSyntax = self.configuration[currentCommand]['cmd']
            equipmentName = self.configuration[currentCommand]['Equipment']
            for device in self.devices:
                if(device.name == equipmentName):
                    if(commandType == 'q'):
                        device.query(commandSyntax)
                    else:
                        if(device.write(commandSyntax) == True):
                            return False
        
        return True

    
    def resetTest(self):
        numCommands = self.reset['num']
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