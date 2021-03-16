#File Description: This .py file contains PinVPout_Test class. This class inherits from the Run_Tests class in the test.py file, and it
#has its own unique run function, which contains the algorithm that produces the spectrum analyzer trace, pinvpout plot, and table associated
#with this test

#Required imports
from tests import Run_Tests#Importing the Run_Tests class from tests.py
import matplotlib.pyplot as plt#used for plotting graphs
import numpy as np#array calculations
import plotly.graph_objects as go#used for making tables
import random#generating random numbers

#This function returns a list of x values, an array of y values, and an x axis start and stop position based off a
#set of points passed in, a center frequency, and a frequency span as well
def parseGetTrace(plotPoints, centerFreq, freqSpan):
    
    #Formatting the data array
    str_data = str(plotPoints)
    str_data = str_data.split(" ", 1)[1]
    str_data = str_data.split(',')
    data_array = np.array(list(map(float, str_data[1:])))
    
    #Calculating the start, stop, and x values that will be returned
    start = (int(centerFreq)-0.5*int(freqSpan))
    stop = (int(centerFreq)+0.5*int(freqSpan))
    step = (stop-start)/len(data_array)
    x = np.arange(start, stop, step)
    return x, data_array, start, stop

#This function finds the index that contains the closest value to the val variable in the list of values passed in
def findClosestIndex(values, val):
    minPosition = 0
    minDifference = float('inf')
    for i in range(len(values)):
        currentVal = values[i]
        currentDiff = abs(currentVal - val)
        if(currentDiff < minDifference):
            minDifference = currentDiff
            minPosition = i
        
    return minPosition

#PinVPout_Test class declaration
class PinVPout_Test(Run_Tests):
    
    #Constructor for this class
    def __init__(self, name, fileName, title, xlabel, ylabel, freqUnits):
        #Passing in variables to the super class or parent class
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, freqUnits)
        
        #Instance variables unique to the PinVPout_Test class
        self.outputTable = None#output table
        self.peakFreq = []#peak frequency array
        self.powerIn = []#power in array
        self.powerLoss = []#power loss array
        self.powerMeasured = []#power measured array
        self.peakAmplitude = []#peak amplitidue array
        self.Pin_Pout = []#array for pin-pout graph/plot
        self.iterationMax = 0#number of iterations for the graphs and tables
    
    #This function loads in the data from the PowerIn.txt and PowerLoss.txt files located in the JSON/tests/PinvPoutSettings folder.
    #This location can be modified below if the user wants to use other file directories
    def configurePowerInPowerLoss(self):
        
        #Resetting all the instance variables for when the files are being reloaded
        self.iterationMax = 0
        self.outputTable = None
        self.peakFreq = []
        self.powerIn = []
        self.powerLoss = []
        self.powerMeasured = []
        self.peakAmplitude = []
        self.Pin_Pout = []
        
        #This code loops through the PowerIn.txt file to get the peak frequency and power in values
        with open("JSON/tests/PinvPoutSettings/PowerIn.txt") as testFileList:
            for line in testFileList:
                values = line.split(",")
                currentPeakFreq = int(values[0].strip())
                currentPowerIn = int(values[1].strip())
                self.peakFreq.append(currentPeakFreq)
                self.powerIn.append(currentPowerIn)
                self.iterationMax = self.iterationMax + 1
        
        #This code loops through the PowerLoss.txt file to get the power loss values
        with open("JSON/tests/PinvPoutSettings/PowerLoss.txt") as testFileList:
            for line in testFileList:
                currentPowerLoss = int(line.strip())
                self.powerLoss.append(currentPowerLoss)
    
    #This function runs the commands associated with the run section in the test json file. This function has been customized specifically
    #for the PinVPout test. Pay close attention to how the commands are specifically used for this tests. This is also described in the
    #user manual
    def runTest(self):
        numCommands = int(self.run['num'])
        if(self.equipmentConnected == False or numCommands <= 0):
            return False
        
        #Plot settings for trace and pinpout plot
        abortTest = False
        frequency = []#frequency (x values) for the spectrum analyzer trace
        powerDB = []#power (y values) for the spectrum analyzer trace
        powerInPlot = []#power in (x values) for pinpout plot
        peakAmpPlot = []#peak amplitude (y values) for pinpout plot
        plt.ion()#setting up plot
        fig, ax = plt.subplots(2,1)#Figure and axis
        fig.subplots_adjust(hspace = .5)#Space between subplots
        figNum = fig.number#the number of the figure (used for aborting tests)
        plt.show()#showing the plot
        line, = ax[0].plot(frequency, powerDB,'r-')#plotting the spectrum analyzer trace line
        pinpoutLine, = ax[1].plot(powerInPlot, peakAmpPlot, 'r-')#plotting the pin pout line
        ax[0].set_xlabel(self.xLabel)#x label of spectrum analyzer trace plot
        ax[0].set_ylabel(self.yLabel)#y label of spectrum analyzer trace plot
        ax[0].set_title(self.graphTitle)#title of spectrum analyzer trace plot
        ax[1].set_xlabel("Power In (dBm)")#x label of pinpout plot
        ax[1].set_ylabel("Power Out (dBm)")#y label of pinpout plot
        ax[1].set_title('Plot of Power In vs Power Out Values')#title of pinpout plot
                
        #Table Settings
        tableOutput = None#variable for table
        peakFreqOutput = []#peak frequency table output
        powerInOutput = []#power in table output
        powerMeasuredOutput = []#power measured table output
        powerLossOutput = []#power loss table output
        peakAmplitudeOutput = []#peak amplitude table output
        pinpoutOutput = []#pinpout table output
        previousPowerLoss = 0#variable to hold previous power loss
        iterationCount = 0#current iteration
        commandString = 'cmd'#string for command template
        firstTime = False#boolean to see if first iteration
        previousPeakFreq = 0#previous peak frequency
        peakFreqCount = 0#the peak frequency count
        freqScaler = 0#used for scaling the frequency based off the units
        
        #Main loop that runs each command. Pay close attention to the command titles because certain things occur only for certain commands, otherwise
        #the run command is just executed and nothing is done with the data that may be returned
        while(abortTest == False and iterationCount < self.iterationMax):#loops while the test is not aborted or the iteration count has not exceeded the maximum count
            for i in range(numCommands):#looping through all the run commands
                currentCommand = commandString + str(i + 1)#current command
                commandType = self.run[currentCommand]['type']#type of command
                commandSyntax = self.run[currentCommand]['cmd']#SCPI command syntax
                commandArgs = self.run[currentCommand]['args']#command arguments/parameters
                equipmentName = self.run[currentCommand]['Equipment']#equipment associated with command
                title = self.run[currentCommand]['title']
                for device in self.devices:#looping through all devices for this test
                    if(device.name == equipmentName):#checking the device name
                        fullCommand = str(commandSyntax) + str(commandArgs)#full command syntax including the arguments/parameters
                        if(commandType == 'q'):
                            if(title == 'Get Trace'):#Get Trace command is required for plotting everything and gathering data
                                if(plt.fignum_exists(figNum) and abortTest == False):
                                    try:
                                        if(firstTime == False):#checks if first iteration
                                            #Plotting the points for the spectrum analyzer trace
                                            plotPoints = device.query(fullCommand)#getting the plot points from the test equipment
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)#formatting the plot points
                                            ax[0].set_xlim(start, stop)#setting up the limits
                                            line, = ax[0].plot(frequency, powerDB,'r-')#plotting the formatted points
                                            plt.draw()#drawing the line
                                            plt.pause(0.02)#pausing plot to update it
                                            firstTime = True#no longer the first iteration
                                            
                                            #getting the current peak frequency and assigning values
                                            currentPeakFreq = int(self.peakFreq[iterationCount])
                                            previousPeakFreq = currentPeakFreq
                                            
                                            #Scaling the current peak frequency based off the frequency units
                                            scaleCurrentPeakFreq = 0
                                            freqScaler = 0
                                            if(self.freqUnits == "GHz"):
                                                scaleCurrentPeakFreq = float(currentPeakFreq) * 1000000000
                                                freqScaler = 1000000000
                                            elif(self.freqUnits == "MHz"):
                                                scaleCurrentPeakFreq = float(currentPeakFreq) * 1000000
                                                freqScaler = 1000000
                                            elif(self.freqUnits == "KHz"):
                                                scaleCurrentPeakFreq = float(currentPeakFreq) * 1000
                                                freqScaler = 1000
                                            else:
                                                scaleCurrentPeakFreq = float(currentPeakFreq)
                                                freqScaler = 1
                                            
                                            #Checking if the current peak frequency is in range, otherwise assigning the current peak frequency to the
                                            #default center frequency the user has set
                                            if(scaleCurrentPeakFreq >= frequency[0] and scaleCurrentPeakFreq <= frequency[len(frequency) - 1]):
                                                scaleCurrentPeakFreq = self.centerFrequency * freqScaler
                                            
                                            #Calculating all of values of the current iteration for the table output
                                            currentPowerIn = self.powerIn[iterationCount]
                                            centerPoint = findClosestIndex(frequency, scaleCurrentPeakFreq)
                                            currentPowerMeasured = powerDB[centerPoint]
                                            currentPowerLoss = self.powerLoss[iterationCount]
                                            previousPowerLoss = currentPowerLoss
                                            currentPeakAmplitude = currentPowerMeasured + abs(currentPowerIn - currentPowerLoss)
                                            currentPinPout = abs(currentPowerMeasured) + abs(currentPowerIn - currentPowerLoss)
                                            
                                            #Updating each array for the table output
                                            peakFreqOutput.append(currentPeakFreq)
                                            powerInOutput.append(currentPowerIn)
                                            powerMeasuredOutput.append(currentPowerMeasured)
                                            powerLossOutput.append(currentPowerLoss)
                                            peakAmplitudeOutput.append(currentPeakAmplitude)
                                            pinpoutOutput.append(currentPinPout)
                                            
                                            #Power In vs Power Loss Graph Setup
                                            lineLabel = str(currentPeakFreq) + " " + self.freqUnits
                                            powerInPlot.append(currentPowerIn)
                                            peakAmpPlot.append(currentPeakAmplitude)
                                            pinpoutLine, = ax[1].plot(powerInPlot, peakAmpPlot,'r-')
                                            pinpoutLine.set_label(lineLabel)
                                            ax[1].legend(loc = "upper right")
                                            peakFreqCount = peakFreqCount + 1
                                            
                                        else:
                                            #Replotting the points for the spectrum analyzer trace
                                            plotPoints = device.query(fullCommand)
                                            frequency, powerDB, start, stop = parseGetTrace(plotPoints, self.centerFrequency, self.frequencySpan)
                                            ax[0].set_xlim(start, stop)
                                            line.set_data(frequency, powerDB)
                                            plt.draw()
                                            plt.pause(0.02)
                                            
                                            #Getting the current peak frequency and scaling it
                                            currentPeakFreq = self.peakFreq[iterationCount]
                                            scaleCurrentPeakFreq = float(currentPeakFreq) * freqScaler
                                            
                                            #Making sure the peak frequency is valid and in range
                                            if(scaleCurrentPeakFreq >= frequency[0] and scaleCurrentPeakFreq <= frequency[len(frequency) - 1]):
                                                scaleCurrentPeakFreq = self.centerFrequency * freqScaler
                                            
                                            #Calculating all of values of the current iteration for the table output
                                            currentPowerIn = self.powerIn[iterationCount]
                                            centerPoint = findClosestIndex(frequency, scaleCurrentPeakFreq)
                                            currentPowerMeasured = powerDB[centerPoint]
                                            currentPowerLoss = self.powerLoss[iterationCount]
                                            previousPowerLoss = currentPowerLoss
                                            currentPeakAmplitude = currentPowerMeasured + abs(currentPowerLoss)
                                            currentPinPout = abs(currentPowerMeasured) + abs(currentPowerIn - currentPowerLoss)
                                            
                                            #Updating each array for the table output
                                            peakFreqOutput.append(currentPeakFreq)
                                            powerInOutput.append(currentPowerIn)
                                            powerMeasuredOutput.append(currentPowerMeasured)
                                            powerLossOutput.append(currentPowerLoss)
                                            peakAmplitudeOutput.append(currentPeakAmplitude)
                                            pinpoutOutput.append(currentPinPout)
                                            
                                            #Updating Power In vs Power Out Plot
                                            if(currentPeakFreq != previousPeakFreq):#if a new peak frequency has been read
                                                lineLabel = str(currentPeakFreq) + " " + self.freqUnits
                                                powerInPlot = []
                                                peakAmpPlot = []
                                                powerInPlot.append(currentPowerIn)
                                                peakAmpPlot.append(currentPeakAmplitude)
                                                pinpoutLine, = ax[1].plot(powerInPlot, peakAmpPlot,'r-')
                                                pinpoutLine.set_label(lineLabel)
                                                ax[1].legend(loc = "upper right")
                                                peakFreqCount = peakFreqCount + 1
                                                previousPeakFreq = currentPeakFreq
                                            else:#updating the pinpout line
                                                powerInPlot.append(currentPowerIn)
                                                peakAmpPlot.append(currentPeakAmplitude)
                                                pinpoutLine.set_data(powerInPlot, peakAmpPlot)
                                            
                                    except:#if the user closes the plot window, an exception is thrown, and the test is aborted
                                        abortTest = True
                                        break
                                else:
                                    print('NOT DOING ANYTHING')
                            else:#runs other query commands and does nothing with the data
                                device.query(fullCommand)
                        else:#runs the write commands
                            if(device.write(fullCommand) == True):
                                return False, "Failed", tableOutput
            
            #Updating the iteration count
            iterationCount = iterationCount + 1
            if(not plt.fignum_exists(figNum)):#if the plot is closed, the test is aborted
                abortTest = True
                plt.ioff()
                plt.show()
                break
        
        #Formatting the Pin V Pout plot
        tableOutput = go.Figure(data=[go.Table(
            header=dict(values=['Peak Frequency (' + str(self.freqUnits) + ')', 'Power In (dBm)', 'Power Measured (dBm)', 'Power Loss', 'Peak Amplitude (dBm)' , 'Pin-Pout'],
                        line_color='darkslategray',
                        fill_color='lightskyblue',
                        align='center'),
            cells=dict(values=[peakFreqOutput,
                               powerInOutput,
                               powerMeasuredOutput,
                               powerLossOutput,
                               peakAmplitudeOutput,
                               pinpoutOutput],
                       line_color='darkslategray',
                       fill_color='lightcyan',
                       align='center'))
        ])
        
        #if a test is aborted
        if(abortTest == True):
            #self.isConfigured = False
            if(plotPoints == None):
                return False, "Command Fail", tableOutput
            return False, "Aborted", tableOutput
        
        #A test was completed successfully
        return True, "Success", tableOutput
        
        