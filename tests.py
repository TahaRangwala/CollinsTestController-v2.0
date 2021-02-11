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

        self.devices = []

    def addEquipment(self, listOfDevices):
        equipmentFound = True
        for equipment in self.equipmentList:
            found = False
            for device in listOfDevices:
                if(device.name == equipment):
                    self.devices.append(device)
                    found = True
            
            if(found == False):
                return False
        
        self.equipmentConnected = equipmentFound and len(listOfDevices) > 0

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