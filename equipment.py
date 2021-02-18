import pyvisa as visa
import json
import time

class Equipment_Connection:
    """
    Module Used for Connecting to Equipment and Running Commands
    """

    def __init__(self, name, fileName):
        fileName = 'JSON/equipment/' + fileName
        with open(fileName) as f:
            jsonData = json.load(f)
        self.resourceManager = visa.ResourceManager('@py')
        self.name = name
        self.address = jsonData[name]['address']
        self.timeout = jsonData[name]['timeout']
        self.idn_cmd = jsonData[name]['idn_cmd']
        self.write_termination = jsonData[name]['write_termination']
        self.read_termination = jsonData[name]['read_termination']
        self.isConnected = False
    
    def connect(self):
        error = False
        try:
            self.device = self.resourceManager.open_resource(self.address, write_termination = self.write_termination,
            read_termination = self.read_termination)
            self.device.query(self.idn_cmd)
            self.isConnected = True
        except:
            error = True
        return error

    def close(self):
        try:
            self.device.close()
        except:
            pass
    
    def query(self, cmd):
        response = None
        try:
            response = self.device.query(cmd)
            time.sleep(1)
            #print(response + "the response")
        except Exception as e:
            #print("ERROR OCCURRED")
            print(e)
        return response
    
    def write(self, cmd):
        error = False
        try:
            self.device.write(cmd)
            time.sleep(1)
        except:
            error = True
        return error