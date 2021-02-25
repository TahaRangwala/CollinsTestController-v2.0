from equipment import Equipment_Connection
import json

class Run_Tests:
    """
    Module Used for Running Tests and Gathering Data
    """

    def __init__(self, name, fileName, title, xlabel, ylabel):
        fileName = 'JSON/tests/' + fileName
        with open(fileName) as f:
            jsonData = json.load(f)
        
        self.name = name
        self.fileName = fileName
        self.jsonData = jsonData
        self.equipmentList = self.jsonData[name]['Equipment List']
        self.configuration = self.jsonData[name]['config']
        self.run = self.jsonData[name]['run']
        self.reset = self.jsonData[name]['reset']
        self.equipmentConnected = False
        self.isConfigured = False
        self.devices = []
        self.graphTitle = str(title)
        self.xLabel = str(xlabel)
        self.yLabel = str(ylabel)
        self.centerFrequency = 150
        self.frequencySpan = 100
    
    def changeCommandParameter(self, commandNum, location, newParam):
        
        try:
            self.jsonData[self.name][location]['cmd' + str(commandNum)]['args'] = newParam
                
            self.configuration = self.jsonData[self.name]['config']
            self.run = self.jsonData[self.name]['run']
            self.reset = self.jsonData[self.name]['reset']
        except:
            return False
        return True
        
    def getNumberOfCommands(self):
        return int(self.configuration['num']), int(self.run['num']), int(self.reset['num'])
    
    def getTitlesList(self):
        configList = []
        runList = []
        resetList = []
        
        commandString = 'cmd'
        for i in range(int(self.configuration['num'])):
            configList.append(str(self.configuration[commandString + str(i+1)]['title']))
        
        for i in range(int(self.run['num'])):
            runList.append(str(self.run[commandString + str(i+1)]['title']))
            
        for i in range(int(self.reset['num'])):
            resetList.append(str(self.reset[commandString + str(i+1)]['title']))   
        
        return configList, runList, resetList
    
    def getArgsList(self):
        configList = []
        runList = []
        resetList = []
        
        commandString = 'cmd'
        for i in range(int(self.configuration['num'])):
            configList.append(str(self.configuration[commandString + str(i+1)]['args']))
        
        for i in range(int(self.run['num'])):
            runList.append(str(self.run[commandString + str(i+1)]['args']))
            
        for i in range(int(self.reset['num'])):
            resetList.append(str(self.reset[commandString + str(i+1)]['args']))   
        
        return configList, runList, resetList
        
    def changeGraphSettings(self, title, xlabel, ylabel):
        self.graphTitle = title
        self.xLabel = xlabel
        self.yLabel = ylabel

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
            for device in self.devices:
                if(device.name == equipmentName):
                    if(title == 'Set Center Frequency'):
                        theString = str(commandArgs)
                        theNum = ""
                        for i in range(len(theString)):
                            currentVal = theString[i]
                            if(str(currentVal).isdigit()):
                                theNum = theNum + str(currentVal)
                            else:
                                break
                        self.centerFrequency = int(theNum)
                    elif(title == 'Set Frequency Span'):
                        theString = str(commandArgs)
                        theNum = ""
                        for i in range(len(theString)):
                            currentVal = theString[i]
                            if(str(currentVal).isdigit()):
                                theNum = theNum + str(currentVal)
                            else:
                                break
                        self.frequencySpan = int(theNum)
                        
                    fullCommand = str(commandSyntax) + str(commandArgs)
                    
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
        try:
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
            self.isConfigured = False
            return True
        except:
            return False
