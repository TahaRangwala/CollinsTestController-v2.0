"""File Description: This .py file is the file the contains the Equipment_Connection class. This class is in charge of connecting and reconnecting to testing equipment,
   running write and query commands, and anything else that would involve directly communicating with testing equipment
"""

#Required imports
import pyvisa as visa#pyvisa library used to connect to testing equipment and run write and query commands using the SCPI command syntax
import json#used for managing the json files for equipment connections

#The Equipment_Connection class declaration
class Equipment_Connection:
    """
    Module Used for Connecting to Equipment and Running Commands
    """
    
    #Constructor for this class
    def __init__(self, name, fileName):
        
        #This code will load the equipment json file the user has entered, which must be in the JSON/equipment folder. This file location can be changed here
        #if the user wants to change locations of the equipment json files
        fileName = 'JSON/equipment/' + fileName
        with open(fileName) as f:
            jsonData = json.load(f)
        
        #Assigning values to the instance variables using the information from the loaded json file
        self.resourceManager = visa.ResourceManager('@py')#pyvisa manager
        self.name = name#name of the equipment in the json file
        self.fileName = fileName#name of the equipment json file location
        self.address = jsonData[name]['address']#VISA addressed used to connect to the testing equipment
        self.timeout = jsonData[name]['timeout']#command timeout for each SCPI command used
        self.idn_cmd = jsonData[name]['idn_cmd']#the equipment's IDN command to verify connections
        self.write_termination = jsonData[name]['write_termination']#equipment read termination for commands
        self.read_termination = jsonData[name]['read_termination']#equipment write termination for commands
        self.device = None#This is the actual instance of the testing equipment device, which will be assigned a value in the connect function
        self.isConnected = False#boolean for if the equipment is connected correctly is initially set to false
    
    #This function reloads data from the equipment json file associated with the current object in an attempt to try to reconnect with the testing equipment
    def reloadFile(self):
        
        #Reloading the data from the equipment json file the user entered previously
        with open(self.fileName) as f:
            jsonData = json.load(f)
            
        #Reassigning variables to the new values found in the file that was reloaded (each value is described in more detail in the constructor above)
        self.resourceManager = visa.ResourceManager('@py')
        self.address = jsonData[self.name]['address']
        self.timeout = jsonData[self.name]['timeout']
        self.idn_cmd = jsonData[self.name]['idn_cmd']
        self.write_termination = jsonData[self.name]['write_termination']
        self.read_termination = jsonData[self.name]['read_termination']
        self.isConnected = False
    
    #This function is what verifies that the user has succesfully connected to a piece of testing equipment using the pyvisa library
    def connect(self):
        error = False#No error initially
        
        #This code will first attempt to connect to the testing equipment using the resource manager, address, read and write termination, and the timeout the user
        #has inputted into the json file. Additionally, it then attempts to run the IDN command, and if no errors occurr, the connection is succesfully verified. If an error occurs,
        #the connection has not be succesfully verified
        try:
            self.device = self.resourceManager.open_resource(self.address, write_termination = self.write_termination,
            read_termination = self.read_termination, timeout = self.timeout)
            self.device.query(self.idn_cmd)
            self.isConnected = True
        except:
            error = True
        return error
    
    #This function closes the device once its connection is no longer necessary (note: this is actually never called in the test controller program, but it could be useful
    #if the user wants to modify the program
    def close(self):
        try:
            self.device.close()
        except:
            pass
    
    #This function runs a query command on the piece of testing equipment
    def query(self, cmd):
        response = None#no response initially
        
        #This code will run the query command, and if an error occurs, the error will be printed out so the user can see if the SCPI command has caused an error. If no error occurs,
        #the SCPI command was ran succesfully, and its response is returned
        try:
            response = self.device.query(cmd)
        except Exception as e:
            print(e)
        return response
    
    #This function runs a write command on the piece of testing equipment
    def write(self, cmd):
        error = False#No error initially
        
        #This code will run the write command, and if an error occurs, the function will return true. If there is no error, the write command was run succesfully, and it will return
        #false instead
        try:
            self.device.write(cmd)
        except:
            error = True
        return error