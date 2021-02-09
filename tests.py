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

    def configureTest(self):
        x = 5
    
    def resetTest(self):
        x = 5