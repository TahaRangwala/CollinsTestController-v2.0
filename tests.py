#File Description: This .py file is the file that contains the Run_Tests class. This class is in charge of actually running the tests,
#and this includes configuration, running, and resetting as well. The running functions are what is unique to each test, and it is not
#defined in this class since the tests using inheritance. Visit the .py files for each test to learn more about the run function there

#Required imports
from equipment import Equipment_Connection#Getting the Equipment_Connection class from the equipment.py file
import json#used for managing the json files for test connections

#The Run_Tests class declaration
class Run_Tests:
    """
    Module Used for Running Tests and Gathering Data
    """
    
    #Constructor for this class
    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        
        #This code will load the test json file the user has setup in the allTests.txt file (described more in gui.py)
        #, which must be in the JSON/test folder. This file location can be changed here
        #if the user wants to change locations of the test json files
        fileName = 'JSON/tests/' + fileName
        with open(fileName) as f:
            jsonData = json.load(f)
        
        #Assigning values to the instance variables using the information from the loaded json file
        self.name = name#name of test
        self.fileName = fileName#name of the test json file location
        self.jsonData = jsonData#loaded json file
        self.equipmentList = self.jsonData[name]['Equipment List']#list of equipment required for the test
        self.configuration = self.jsonData[name]['config']#all configuration commands
        self.run = self.jsonData[name]['run']#all run commands
        self.reset = self.jsonData[name]['reset']#all reset commands
        self.equipmentConnected = False#equipment not connected initially
        self.isConfigured = False#equipment not configured initially
        self.devices = []#Equipment_Connection objects for all the devices needed for the test
        self.graphTitle = str(title)#graph title for spectrum analyzer trace
        self.xLabel = str(xlabel)#graph x label for spectrum analyzer trace
        self.yLabel = str(ylabel)#graph y label for spectrum analyzer trace
        self.centerFrequency = 150#initial center frequency
        self.frequencySpan = 100#initial frequency span
        self.freqUnits = freqUnits#frequency units
    
    #This function modifies command parameters based off the command number and location
    def changeCommandParameter(self, commandNum, location, newParam):
        
        try:
            #This code here uses the command number to find the command location, and then it modifies its args in the json variable. Then
            #the configuration, run, and reset commands are all assigned new values for the command parameter change. If an error occurs,
            #the function returns false
            self.jsonData[self.name][location]['cmd' + str(commandNum)]['args'] = newParam
            self.configuration = self.jsonData[self.name]['config']
            self.run = self.jsonData[self.name]['run']
            self.reset = self.jsonData[self.name]['reset']
        except:
            return False
        return True
    
    #This function gets the number of commands in the configuration, run, and reset sections of the test json file
    def getNumberOfCommands(self):
        return int(self.configuration['num']), int(self.run['num']), int(self.reset['num'])
    
    #This function gets the three lists of titles, and these titles are the titles of the commands in the configuration, run, and reset
    #section in the test json file
    def getTitlesList(self):
        
        #Set to empty initially
        configList = []
        runList = []
        resetList = []
        
        #This loops through all the commands in the configuration section, and then it adds its title to the configuration title list
        commandString = 'cmd'
        for i in range(int(self.configuration['num'])):
            configList.append(str(self.configuration[commandString + str(i+1)]['title']))
        
        #This loops through all the commands in the run section, and then it adds its title to the run title list
        for i in range(int(self.run['num'])):
            runList.append(str(self.run[commandString + str(i+1)]['title']))
            
        #This loops through all the commands in the reset section, and then it adds its title to the reset title list
        for i in range(int(self.reset['num'])):
            resetList.append(str(self.reset[commandString + str(i+1)]['title']))   
        
        return configList, runList, resetList
    
    #This function gets the three lists of arguments or parameters, and these parameters are the parameters of the commands
    #in the configuration, run, and reset section in the test json file
    def getArgsList(self):
        
        #Set to empty initially
        configList = []
        runList = []
        resetList = []
        
        #This loops through all the commands in the configuration section, and then it adds its argument to the configuration arg list
        commandString = 'cmd'
        for i in range(int(self.configuration['num'])):
            configList.append(str(self.configuration[commandString + str(i+1)]['args']))
        
        #This loops through all the commands in the run section, and then it adds its argument to the run arg list
        for i in range(int(self.run['num'])):
            runList.append(str(self.run[commandString + str(i+1)]['args']))
            
        #This loops through all the commands in the reset section, and then it adds its argument to the reset arg list            
        for i in range(int(self.reset['num'])):
            resetList.append(str(self.reset[commandString + str(i+1)]['args']))   
        
        return configList, runList, resetList
    
    #This function changes the graph title, xlabel, ylabel, and frequency units
    def changeGraphSettings(self, title, xlabel, ylabel, freqUnits):
        self.graphTitle = title
        self.xLabel = xlabel
        self.yLabel = ylabel
        self.freqUnits = freqUnits
    
    #This function adds the equipment to the devices array
    def addEquipment(self, listOfDevices):
        equipmentFound = True#assumes all equipment is found initially
        
        #Loops through all the equipment names in the equipment list, and then it verifies them with the listOfDevices that is passed in.
        #It checks if the device is connected before contuing, otherwise the function returns false. Additionally, the connected devices
        #are added to the self.devices instance variable
        for equipment in self.equipmentList:
            found = False
            for device in listOfDevices:
                if(device.name == equipment):
                    if(device.isConnected == True):
                        self.devices.append(device)
                        found = True
            
            if(found == False):
                return False
        
        #Returns true if all equipment is connected and then list of devices is greater than 0, otherwise returns false
        self.equipmentConnected = equipmentFound and len(listOfDevices) > 0
        return self.equipmentConnected

    #This function is what runs the configuration commands in the configuration section of the tests json file
    def configureTest(self):
        numCommands = int(self.configuration['num'])#Gets the number of commands
        #Verifies equipment is connected and that the number of commands is greater than 0, otherwise returns false
        if(numCommands == 0 or self.equipmentConnected == False):
            return False
        
        #This code loops through every command in the configuration section of the json file
        #and it runs the command on the equipment based off the command settings
        commandString = 'cmd'
        for i in range(numCommands):
            currentCommand = commandString + str(i + 1)#current command in loop
            commandType = self.configuration[currentCommand]['type']#type of command
            commandSyntax = self.configuration[currentCommand]['cmd']#SCPI command syntax
            commandArgs = self.configuration[currentCommand]['args']#command argument/parameter
            equipmentName = self.configuration[currentCommand]['Equipment']#name of equipment associated with command
            title = self.configuration[currentCommand]['title']#title of command
            fullCommand = ''#full command syntax set to nothing initially
            for device in self.devices:#loops through all devices in the list
                if(device.name == equipmentName):#if the device name matches the device associated with the command
                    
                    #Here, these two if statements before certain things on certain commands based on the title.
                    #IMPORTANT: This is noted in the user manual, but the titles of the commands do matter. A configuration command
                    #titled 'Set Center Frequency' will run specific code for example as shown below
                    
                    #This sets the center frequency instance variable based off of the Set Center Frequency command
                    if(title == 'Set Center Frequency'):#
                        theString = str(commandArgs)
                        theNum = ""
                        for i in range(len(theString)):
                            currentVal = theString[i]
                            if(str(currentVal).isdigit()):
                                theNum = theNum + str(currentVal)
                            else:
                                break
                        self.centerFrequency = float(theNum)
                    
                    #This sets the frequency span instance variables based off of the Set Frequency Span command
                    elif(title == 'Set Frequency Span'):
                        theString = str(commandArgs)
                        theNum = ""
                        for i in range(len(theString)):
                            currentVal = theString[i]
                            if(str(currentVal).isdigit()):
                                theNum = theNum + str(currentVal)
                            else:
                                break
                        self.frequencySpan = float(theNum)
                    
                    #full command syntax includes the SCPI command and its command arguments
                    fullCommand = str(commandSyntax) + str(commandArgs)
                    
                    #Checks the type of command and runs a query or write command. The function returns false if a write command fails to
                    #run correctly
                    if(commandType == 'q'):
                        device.query(fullCommand)
                    else:
                        if(device.write(fullCommand) == True):
                            return False
        
        #If no errors occur, isConfigured is set to true and the function returns true as well
        self.isConfigured = True
        return self.isConfigured

    #This function runs the commands in the reset section of the json file
    def resetTest(self):
        numCommands = int(self.reset['num'])#gets the number of commands
        #Verifies equipment is connected and that the number of commands is greater than 0, otherwise returns false
        if(self.equipmentConnected == False or numCommands == 0):
            return False
        
        #This code loops through every command in the configuration section of the json file
        #and it runs the command on the equipment based off the command settings
        try:
            commandString = 'cmd'
            for i in range(numCommands):
                currentCommand = commandString + str(i + 1)
                commandType = self.reset[currentCommand]['type']#command type
                commandSyntax = self.reset[currentCommand]['cmd']#SCPI command syntax
                equipmentName = self.reset[currentCommand]['Equipment']#equipment associated with command
                commandArgs = self.configuration[currentCommand]['args']#command argument/parameter
                equipmentName = self.configuration[currentCommand]['Equipment']#name of equipment associated with command
                title = self.configuration[currentCommand]['title']#title of command
                fullCommand = ''
                for device in self.devices:#loops through the device list
                    if(device.name == equipmentName):#checks if name on device is the same as the equipment name
                        fullCommand = str(commandSyntax) + str(commandArgs)#sets up the full command to run on the equipment
                        if(commandType == 'q'):#runs a query command
                            device.query(fullCommand)
                        else:#runs a write command
                            if(device.write(fullCommand)):
                                return False
                            
            self.isConfigured = False#Set to false since equipment has been reset
            return True
        except:
            return False
