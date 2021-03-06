#File Description: This .py file manages the gui and it connects the user interface to all the test classes, equipments classes, and everything else associated with
#this program

#Required imports
import PySimpleGUI as sg#GUI library we used
from equipment import Equipment_Connection#gets the class from the equipment.py file
from tests import Run_Tests#Gets the class from the test.py file
from mixerspurTest import Mixer_Spur_Test#gets the class from the mixerspurTest.py file
from p1dBTest import P1dB_Test#gets the class from the p1dBTest.py file
from pinvpoutTest import PinVPout_Test#gets the class from the pinvpoutTest.py file
from otherTest import Other_Test#gets the class from the otherTest.py file
import plotly.graph_objects as go#used for outputting the tables

#Runs the entire GUI
def runGUI():
    #Color Theme of GUI
    sg.theme('LightGreen2')

    #Setting up Layout of GUI

    #Adding Equipment
    tempLayout1 = [[sg.Text('Name:'), sg.InputText(key='-IN1-')],
                    [sg.Text('JSON File:'), sg.InputText(key='-IN2-')],
                    [sg.Button('Add Equipment')],
                    [sg.Output(size=(60,10), key='-OUTPUT-')], 
                    [sg.Button('Refresh Connections')]]

    #Test Configuration
    tempLayout2 = [[sg.Text('Test:'), sg.Radio('Mix Spur Test', 'RADIO1', default=True, key = '-R1-'), sg.Radio('P1dB Test', 'RADIO1', key = '-R2-'), sg.Radio('PinvPout Test', 'RADIO1', key = '-R3-'), sg.Radio('Other Test', 'RADIO1', key = '-R4-')],
                    [sg.Output(size=(60,10), key='-OUTPUT2-')],
                    [sg.Text('Choose Side Band'), sg.Radio('Low Side', 'RADIO4', default=True, key = '-RL-'), sg.Radio('High Side', 'RADIO4', key = '-RH-')], 
                    [sg.Text('Number of Harmonics: '), sg.InputText(default_text = '3', key = '-INMSize-')],
                    [sg.Text('Input Frequency (IF): '), sg.InputText(default_text = '0.1', key = '-INMFreq-')],
                    [sg.Text('Local Oscillator Frequency (LO): '), sg.InputText(default_text = '5', key = '-INMLO-')],
                    [sg.Text('Radio Frequency (RF): '), sg.InputText(key = '-INMRF-')],
                    [sg.Text('Output Impedance (Ohm):'), sg.InputText(default_text = '50', key = '-INI-')],
                    [sg.Text('Frequency Range Start:'), sg.InputText(default_text = '1', key = '-INFstart-')],
                    [sg.Text('Frequency Range Stop:'), sg.InputText(default_text = '2', key = '-INFstop-')],
                    [sg.Text('Frequency Range Step:'), sg.InputText(default_text = '1', key = '-INFstep-')],
                    [sg.Text('Voltage Sweep Start:'), sg.InputText(default_text = '-20', key = '-INVstart-')],
                    [sg.Text('Voltage Sweep Stop:'), sg.InputText(default_text = '20', key = '-INVstop-')],
                    [sg.Text('Voltage Sweep Step:'), sg.InputText(default_text = '5', key = '-INVstep-')],
                    [sg.Button('Configure Selected Test')],
                    [sg.Button('Reset Selected Test')]]

    #Running Tests
    tempLayout3 = [[sg.Button('Mixer Spur'), sg.Button('P1dB'), sg.Button('PinvPout'), sg.Button('Other')]]

    #Plot Settings
    tempLayout4 = [[sg.Text('Plot Title'), sg.InputText(default_text = 'Spectrum Analyzer Trace', key='-IN5-')],
                [sg.Text('X-Label'), sg.InputText(default_text = 'Frequency (MHz)',key='-IN6-')],
                [sg.Text('Y-Label'), sg.InputText(default_text = 'Power (dBm)', key='-IN7-')],
                [sg.Text('Frequency Units:'), sg.Radio('Hz', 'RADIO2', default=True, key = '-R5-'), sg.Radio('KHz', 'RADIO2', key = '-R6-'), sg.Radio('MHz', 'RADIO2', key = '-R7-', default=True), sg.Radio('GHz', 'RADIO2', key = '-R8-')],
                [sg.Text('Power Units:'), sg.Radio('dBm', 'RADIO3', default=True, key = '-R9-'), sg.Radio('Vpp', 'RADIO3', key = '-R10-')],
                [sg.Button('Apply Plot and Table Changes')]]

    
    #Setting required data structures and variables
    
    #Automatically Connecting Equipment
    equipmentList = []#all devices connected to PI
    
    #This will loop throught the allEquipment.txt file (described in the user manual more). This location can be changed here if needed
    try:
        with open("JSON/equipment/allEquipment.txt") as equipmentFileList:
            for line in equipmentFileList:
                values = line.split(",")
                equipmentList.append(Equipment_Connection(values[0].strip(), values[1].strip()))
    except:
        sg.PopupError('Error with allEquipment.txt File. Not all pieces of equipment were added!')
        
    #Automatically Connecting Tests
        
    #Tests the Program Offers
    MixerSpurTest = None
    P1dBTest = None
    PinVPoutTest = None
    OtherTest = None
    
    #Default Command Names
    mixerSpurCommands = None
    p1DBCommands = None
    pinpoutCommands = None
    otherCommands = None
    
    #Default Plot Settings
    title = "Spectrum Analyzer Trace"
    xLabel = "Frequency (MHz)"
    yLabel = "Power (dBm)"
    
    #empty tabs and settings tabs (empty tabs if no test was added)
    settingsTab = []
    emptyTab =  [[sg.T('No test has been added here')]]
    emptyTab2 =  [[sg.T('No test has been added here')]]  
    emptyTab3 =  [[sg.T('No test has been added here')]]  
    emptyTab4 =  [[sg.T('No test has been added here')]]  
    
    #This adds the test automically based off of the allTests.txt file (described more in the manual). The location of this can be changed here
    #as well as anything else as well. Pay close attention to this part of the code
    try:
        testNum = 1
        with open("JSON/tests/allTests.txt") as testFileList:
            for line in testFileList:
                values = line.split(",")
                testName = str(values[0].strip())
                fileName = str(values[1].strip())
                testType = str(values[2].strip())
                if(testType == 'MixerSpurTest'):#adding the mixer spur test
                    if(MixerSpurTest == None):
                        commandNames = []
                        MixerSpurTest = Mixer_Spur_Test(testName, fileName, title, xLabel, yLabel, "MHz", "dBm")
                        configNum, runNum, resetNum = MixerSpurTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = MixerSpurTest.getTitlesList()
                        configArgs, runArgs, resetArgs = MixerSpurTest.getArgsList()
                        currentString = ""
                        defString = ""
                        
                        #all these for loops are for getting the list of commands ready so the user can modify them on the GUI
                        for i in range(configNum):
                            tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                            paramString = "Current Param: " + configArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                            paramString = "Current Param: " + runArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                            paramString = "Current Param: " + resetArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                        
                        mixerSpurCommands = commandNames

                        settingsTab.append(sg.Tab('Mixer Spur Test', [[sg.Listbox(commandNames, default_values = defString, size=(70,10), enable_events=True, key = '-LIST-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN10-')], [sg.Button('Change Mixer Spur Test Settings')]]))
                elif(testType == 'P1dBTest'):#adding the P1dB Test
                    if(P1dBTest == None):
                        commandNames = []
                        P1dBTest = P1dB_Test(testName, fileName, title, xLabel, yLabel, "MHz", "dBm")
                        configNum, runNum, resetNum = P1dBTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = P1dBTest.getTitlesList()
                        configArgs, runArgs, resetArgs = P1dBTest.getArgsList()
                        
                        currentString = ""
                        defString = ""
                        for i in range(configNum):
                            tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                            paramString = "Current Param: " + configArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                            paramString = "Current Param: " + runArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                            paramString = "Current Param: " + resetArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        p1DBCommands = commandNames
                        
                        settingsTab.append(sg.Tab('P1dB Test', [[sg.Listbox(commandNames, default_values = defString, size=(70,10), enable_events=True, key = '-LIST2-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN11-')], [sg.Button('Change P1dB Test Settings')]]))
                
                elif(testType == 'PinvPoutTest'):#adding the PinVPout test
                    if(PinVPoutTest == None):
                        commandNames = []
                        PinVPoutTest = PinVPout_Test(testName, fileName, title, xLabel, yLabel, "MHz", "dBm")
                        configNum, runNum, resetNum = PinVPoutTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = PinVPoutTest.getTitlesList()
                        configArgs, runArgs, resetArgs = PinVPoutTest.getArgsList()
                        PinVPoutTest.configurePowerInPowerLoss()
                
                        currentString = ""
                        defString = ""
                        for i in range(configNum):
                            tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                            paramString = "Current Param: " + configArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                            paramString = "Current Param: " + runArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                            paramString = "Current Param: " + resetArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                        
                        pinpoutCommands = commandNames
                        
                        settingsTab.append(sg.Tab('Pin vs. Pout Test', [[sg.Listbox(commandNames, default_values = defString, size=(70,10), enable_events=True, key = '-LIST3-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN12-')], [sg.Button('Change Pin vs. Pout Test Settings')]]))
                else:
                    if(OtherTest == None):#Adding the other test
                        commandNames = []
                        OtherTest = Other_Test(testName, fileName, title, xLabel, yLabel, "MHz", "dBm")
                        configNum, runNum, resetNum = OtherTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = OtherTest.getTitlesList()
                        configArgs, runArgs, resetArgs = OtherTest.getArgsList()
                        
                        currentString = ""
                        defString = ""
                        for i in range(configNum):
                            tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                            paramString = "Current Param: " + configArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                            paramString = "Current Param: " + runArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                            paramString = "Current Param: " + resetArgs[i]
                            currentString = ""
                            spacesAdded = ""
                            while(len(currentString) < 70):
                                currentString = tempString + spacesAdded + paramString
                                spacesAdded = spacesAdded + " "
                            if(i == 0):
                                defString = currentString
                            commandNames.append(currentString)

                        otherCommands = commandNames

                        settingsTab.append(sg.Tab('Other Test', [[sg.Listbox(commandNames, size=(70,10), default_values = defString, enable_events=True, key = '-LIST4-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN13-')], [sg.Button('Change Other Test Settings')]]))
                testNum = testNum + 1
                if(testNum > 4):
                    break
    except:#if an error occurred while adding the tests
        sg.PopupError('Error with allTests.txt File. Not all tests were added!')
    
    #if a test was not added, an empty tab will be associated with it on the GUI
    if(MixerSpurTest == None):
        settingsTab.append(sg.Tab('Mixer Spur Test', emptyTab, tooltip = 'Mixer Spur'))
    if(P1dBTest == None):
        settingsTab.append(sg.Tab('P1dB Test', emptyTab2, tooltip = 'P1dB'))
    if(PinVPoutTest == None):
        settingsTab.append(sg.Tab('Pin vs. Pout Test', emptyTab3, tooltip = 'PinvPout'))
    if(OtherTest == None):
        settingsTab.append(sg.Tab('Other Test', emptyTab4, tooltip = 'Other'))
    
    settingsLayout = [[sg.TabGroup([settingsTab], tooltip='Select a command')]]
    
    #Connecting everything and finalizing the GUI layout
    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c'), sg.Frame(layout=settingsLayout, title='Test Settings', element_justification='c', size=(300, 300))],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c'), sg.Text('   '), sg.Text('   '), sg.Text('   ')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot and Table Settings', element_justification='c')],
            [sg.Button('Reset', size =(10, 2)), sg.Button('Close', size =(10, 2))]]
    
    #Setting up the size of the window, its title, layout, and element justification
    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(1535, 975))
        
    #Loop running while GUI is open
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Close':#when the window is closed
            break

        elif event == 'Add Equipment':#adding equipment
            equipmentName = values['-IN1-']
            fileName = values['-IN2-']
            
            sameName = False
            for device in equipmentList:
                if(device.name == equipmentName):
                    sameName = True
                    
            jsonError = False
            if(sameName == False):
                try:
                    equipmentList.append(Equipment_Connection(equipmentName, fileName))
                except:
                    jsonError = True

                #Outputting connection status for all testing equipment
                outputString = ""
                isError = False
                for device in equipmentList:
                    isError = device.connect()
                    if(isError):
                        outputString = outputString + device.name + ": ERROR, NOT CONNECTED\n"
                    else:
                        outputString = outputString + device.name + ": CONNECTED\n"  
                window['-OUTPUT-'].update(outputString)

            
            if(sameName):
                sg.PopupError('Please make sure each piece of equipment has a unique name!')
            elif(jsonError):
                sg.PopupError('Your JSON File Is Configured Incorrectly!')
            elif(isError):
                sg.PopupError('Some equipment connections have not been established. Please check the user manual to make sure your settings are correct.')
                
        elif event == 'Refresh Connections':#Refresh equipment connections
            window['-OUTPUT-'].update("")
            outputString = ""
            jsonError = False
            isError = False

            try:
                for device in equipmentList:
                    device.reloadFile()
                    isError = device.connect()
                    if(isError):
                        outputString = outputString + device.name + ": ERROR, NOT CONNECTED\n"
                    else:
                        outputString = outputString + device.name + ": CONNECTED\n"  
                window['-OUTPUT-'].update(outputString)
            except:
                jsonError = True

            if(jsonError):
                sg.PopupError('Your JSON File Is Configured Incorrectly!')
            elif(isError):
                sg.PopupError('Some equipment connections have not been established. Please check the user manual to make sure your settings are correct.')

        elif event == 'Configure Selected Test':#Configure the selected test based on the radio button
            if(values['-R1-'] == True):
                if(MixerSpurTest != None):
                    allInputs = True
                    matrixSize = values['-INMSize-']
                    inputFreq = values['-INMFreq-']
                    LO = values['-INMLO-']
                    RF = values['-INMRF-']
                    freqStart = values['-INFstart-']
                    freqStop = values['-INFstop-']
                    
                    isHighSide = True
                    if(values['-RL-'] == True):
                        isHighSide = False
                        
                    if(str(matrixSize) != "" and str(inputFreq) != "" and str(LO) != "" and str(RF) == ""):
                        try:
                            int(matrixSize)
                            float(inputFreq)
                            float(LO)
                            float(freqStart)
                            float(freqStop)
                            MixerSpurTest.changeMixerParameters(matrixSize, inputFreq, LO, 0, freqStart, freqStop, isHighSide)
                        except:
                            allInputs = False
                    elif(str(matrixSize) != "" and str(inputFreq) != "" and str(RF) != "" and str(LO) == ""):
                        try:
                            int(matrixSize)
                            float(inputFreq)
                            float(RF)
                            float(freqStart)
                            float(freqStop)
                            MixerSpurTest.changeMixerParameters(matrixSize, inputFreq, 0, RF, freqStart, freqStop)
                        except:
                            allInputs = False
                    elif(str(matrixSize) != "" and str(LO) != "" and str(RF) != "" and str(inputFreq) == ""):
                         try:
                            int(matrixSize)
                            float(RF)
                            float(LO)
                            float(freqStart)
                            float(freqStop)
                            MixerSpurTest.changeMixerParameters(matrixSize, 0, LO, RF, freqStart, freqStop)
                         except:
                            allInputs = False
                    else:
                         allInputs = False
                    
                    if(allInputs == True):
                        window['-OUTPUT2-'].update("Currently configuring the mixer spur test")
                        equipmentFound = MixerSpurTest.addEquipment(equipmentList)
                        configuredTests = MixerSpurTest.configureTest()
                        if(configuredTests == True and equipmentFound == True):
                            window['-OUTPUT2-'].update("The Mixer Spur Test is ready to run")
                        elif(equipmentFound == False):
                            window['-OUTPUT2-'].update("The Mixer Spur Test does not have all required test equipment")
                        else:
                            window['-OUTPUT2-'].update("The Mixer Spur Test is NOT configured correctly")
                    else:
                        sg.Popup('Make sure mixer spur test inputs are correct!')    
                        
                else:
                    window['-OUTPUT2-'].update("The Mixer Spur Test is NOT configured correctly")
            elif(values['-R2-'] == True):                
                if(P1dBTest != None):
                    isValidImpedance = True
                    equipmentFound = False
                    configuredTests = False
                    impedance = values['-INI-']
                    freqStart = values['-INFstart-']
                    freqStop = values['-INFstop-']
                    freqStep = values['-INFstep-']
                    voltStart = values['-INVstart-']
                    voltStop = values['-INVstop-']
                    voltStep = values['-INVstep-']
                    
                    try:
                        float(impedance)
                        float(freqStart)
                        float(freqStop)
                        float(freqStep)
                        float(voltStart)
                        float(voltStop)
                        float(voltStep)
                        P1dBTest.changeImpedance(impedance)
                        P1dBTest.setFrequencyRange(freqStart, freqStop, freqStep)
                        P1dBTest.setVoltSweepRange(voltStart, voltStop, voltStep)
                    except:
                        isValidImpedance = False                           

                    if(isValidImpedance == True):
                        window['-OUTPUT2-'].update("Currently configuring the P1dB test")
                        equipmentFound = P1dBTest.addEquipment(equipmentList)
                        configuredTests = P1dBTest.configureTest()  
                        if(configuredTests == True and equipmentFound == True):
                            window['-OUTPUT2-'].update("The P1dB Test is ready to run")
                        elif(equipmentFound == False):
                            window['-OUTPUT2-'].update("The P1dB Test does not have all required test equipment")
                        else:
                            window['-OUTPUT2-'].update("The P1dB Test is NOT configured correctly")
                    else:
                        sg.Popup('Please input the output impedance, frequency range and steps, and voltage sweep range and steps for the P1dB test!')    

                else:
                    window['-OUTPUT2-'].update("The P1dB Test is NOT configured correctly")
            elif(values['-R3-'] == True):
                if(PinVPoutTest != None):
                    window['-OUTPUT2-'].update("Currently configuring the PinVPout test")
                    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
                    configuredTests = PinVPoutTest.configureTest()
                    failPower = False
                    
                    try:
                        PinVPoutTest.configurePowerInPowerLoss()
                    except:
                        failPower = True
                    
                    if(failPower == True):
                        window['-OUTPUT2-'].update("Check The Pin vs. Pout Test Settings Folder's txt files")
                    elif(configuredTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is ready to run")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
            else:
                if(OtherTest != None):
                    window['-OUTPUT2-'].update("Currently configuring the Other test")
                    equipmentFound = OtherTest.addEquipment(equipmentList)
                    configuredTests = OtherTest.configureTest()
                    if(configuredTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Other Test is ready to run")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Other Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Other Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The Other Test is NOT configured correctly")
        
        elif event == 'Reset Selected Test':
            if(values['-R1-'] == True):
                if(MixerSpurTest != None):
                    equipmentFound = MixerSpurTest.addEquipment(equipmentList)
                    resetTests = MixerSpurTest.resetTest()
                    if(resetTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Mixer Spur Test was reset")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Mixer Spur Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Mixer Spur Test was NOT reset correctly")
                else:
                    window['-OUTPUT2-'].update("The Mixer Spur Test was NOT reset correctly")
            elif(values['-R2-'] == True):
                if(P1dBTest != None):
                    equipmentFound = P1dBTest.addEquipment(equipmentList)
                    resetTests = P1dBTest.resetTest()
                    if(resetTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The P1dB Test was reset")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The P1dB Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The P1dB Test was NOT reset correctly")
                else:
                    window['-OUTPUT2-'].update("The P1dB Test was NOT reset correctly")
            elif(values['-R3-'] == True):
                if(PinVPoutTest != None):
                    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
                    resetTests = PinVPoutTest.resetTest()
                    if(resetTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test was reset")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test was NOT reset correctly")
                else:
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test was NOT reset correctly")
            else:
                if(OtherTest != None):
                    equipmentFound = OtherTest.addEquipment(equipmentList)
                    resetTests = OtherTest.resetTest()
                    if(resetTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Other Test was reset")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Other Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Other Test was NOT reset correctly")
                else:
                    window['-OUTPUT2-'].update("The Other Test was NOT reset correctly")
        
        elif event == 'Change Mixer Spur Test Settings':#changes the mixer spur test command parameters
            try:
                testParam = values['-IN10-']
                listValue = str(values['-LIST-'])
                selectedValue = True
                if(listValue == '[]'):
                    selectedValue = False
                
                if(selectedValue == True):
                    minusCount = 1
                    commandNumString = ""
                    digitFound = False
                    while(digitFound == False):
                        currentVal = listValue[listValue.find(':') - minusCount]
                        if(str(currentVal).isdigit()):
                            commandNumString = str(currentVal) + commandNumString
                        else:
                            digitFound = True
                        minusCount = minusCount + 1
                    commandNum = int(commandNumString)
  
                    if 'Config' in listValue:
                        MixerSpurTest.changeCommandParameter(commandNum,'config', str(testParam))
                    elif 'Run' in listValue:
                        MixerSpurTest.changeCommandParameter(commandNum,'run', str(testParam))
                    elif 'Reset Command' in listValue:
                        MixerSpurTest.changeCommandParameter(commandNum,'reset', str(testParam))
                    else:
                        sg.PopupError('Your JSON file format is incorrect')
                    
                    configTitles, runTitles, resetTitles = MixerSpurTest.getTitlesList()
                    configArgs, runArgs, resetArgs = MixerSpurTest.getArgsList()
                    configNum, runNum, resetNum = MixerSpurTest.getNumberOfCommands()
                    
                    commandNames = []
                    currentString = ""
                    defString = ""
                    for i in range(configNum):
                        tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                        paramString = "Current Param: " + configArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)
                            
                    for i in range(runNum):
                        tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                        paramString = "Current Param: " + runArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    for i in range(resetNum):
                        tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                        paramString = "Current Param: " + resetArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    window['-LIST-'].update(commandNames)
                else:
                    sg.Popup('Please select a command')
            except:
                sg.PopupError('An error occurred. Please try again.')
            
        elif event == 'Change P1dB Test Settings':#changes the P1dB test command parameters
            try:
                testParam = values['-IN11-']
                listValue = str(values['-LIST2-'])
                selectedValue = True
                if(listValue == '[]'):
                    selectedValue = False
                
                if(selectedValue == True):
                    minusCount = 1
                    commandNumString = ""
                    digitFound = False
                    while(digitFound == False):
                        currentVal = listValue[listValue.find(':') - minusCount]
                        if(str(currentVal).isdigit()):
                            commandNumString = str(currentVal) + commandNumString
                        else:
                            digitFound = True
                        minusCount = minusCount + 1
                    commandNum = int(commandNumString)
                    
                    if 'Config' in listValue:
                        P1dBTest.changeCommandParameter(commandNum,'config', str(testParam))
                    elif 'Run' in listValue:
                        P1dBTest.changeCommandParameter(commandNum,'run', str(testParam))
                    elif 'Reset Command' in listValue:
                        P1dBTest.changeCommandParameter(commandNum,'reset', str(testParam))
                    else:
                        sg.PopupError('Your JSON file format is incorrect')
                    
                    configTitles, runTitles, resetTitles = P1dBTest.getTitlesList()
                    configArgs, runArgs, resetArgs = P1dBTest.getArgsList()
                    configNum, runNum, resetNum = P1dBTest.getNumberOfCommands()
                    
                    commandNames = []
                    currentString = ""
                    defString = ""
                    for i in range(configNum):
                        tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                        paramString = "Current Param: " + configArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)
                            
                    for i in range(runNum):
                        tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                        paramString = "Current Param: " + runArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    for i in range(resetNum):
                        tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                        paramString = "Current Param: " + resetArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    window['-LIST2-'].update(commandNames)
                else:
                    sg.Popup('Please select a command')
            except:
                sg.PopupError('An error occurred. Please try again.')
        
        elif event == 'Change Pin vs. Pout Test Settings':#changes the PinVPout test command parameters
            try:
                testParam = values['-IN12-']
                listValue = str(values['-LIST3-'])
                selectedValue = True
                if(listValue == '[]'):
                    selectedValue = False
                
                if(selectedValue == True):
                    minusCount = 1
                    commandNumString = ""
                    digitFound = False
                    while(digitFound == False):
                        currentVal = listValue[listValue.find(':') - minusCount]
                        if(str(currentVal).isdigit()):
                            commandNumString = str(currentVal) + commandNumString
                        else:
                            digitFound = True
                        minusCount = minusCount + 1
                    commandNum = int(commandNumString)
                    
                    if 'Config' in listValue:
                        PinVPoutTest.changeCommandParameter(commandNum,'config', str(testParam))
                    elif 'Run' in listValue:
                        PinVPoutTest.changeCommandParameter(commandNum,'run', str(testParam))
                    elif 'Reset Command' in listValue:
                        PinVPoutTest.changeCommandParameter(commandNum,'reset', str(testParam))
                    else:
                        sg.PopupError('Your JSON file format is incorrect')
                    
                    configTitles, runTitles, resetTitles = PinVPoutTest.getTitlesList()
                    configArgs, runArgs, resetArgs = PinVPoutTest.getArgsList()
                    configNum, runNum, resetNum = PinVPoutTest.getNumberOfCommands()
                    
                    commandNames = []
                    currentString = ""
                    defString = ""
                    for i in range(configNum):
                        tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                        paramString = "Current Param: " + configArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)
                            
                    for i in range(runNum):
                        tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                        paramString = "Current Param: " + runArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    for i in range(resetNum):
                        tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                        paramString = "Current Param: " + resetArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    window['-LIST3-'].update(commandNames)
                else:
                    sg.Popup('Please select a command')
            except:
                sg.PopupError('An error occurred. Please try again.')
                
        elif event == 'Change Other Test Settings':#changes the other test command parameters
            try:
                testParam = values['-IN13-']
                listValue = str(values['-LIST4-'])
                selectedValue = True
                if(listValue == '[]'):
                    selectedValue = False
                
                
                if(selectedValue == True):
                    minusCount = 1
                    commandNumString = ""
                    digitFound = False
                    while(digitFound == False):
                        currentVal = listValue[listValue.find(':') - minusCount]
                        if(str(currentVal).isdigit()):
                            commandNumString = str(currentVal) + commandNumString
                        else:
                            digitFound = True
                        minusCount = minusCount + 1
                        
                    commandNum = int(commandNumString)                        
                    if 'Config' in listValue:
                        OtherTest.changeCommandParameter(commandNum,'config', str(testParam))
                    elif 'Run' in listValue:
                        OtherTest.changeCommandParameter(commandNum,'run', str(testParam))
                    elif 'Reset Command' in listValue:
                        OtherTest.changeCommandParameter(commandNum,'reset', str(testParam))
                    else:
                        sg.PopupError('Your JSON file format is incorrect')
                    
                    configTitles, runTitles, resetTitles = OtherTest.getTitlesList()
                    configArgs, runArgs, resetArgs = OtherTest.getArgsList()
                    configNum, runNum, resetNum = OtherTest.getNumberOfCommands()
                    
                    commandNames = []
                    currentString = ""
                    defString = ""
                    for i in range(configNum):
                        tempString = 'Config CMD ' + str(i + 1) + ': ' + str(configTitles[i])
                        paramString = "Current Param: " + configArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)
                            
                    for i in range(runNum):
                        tempString = 'Run CMD ' + str(i + 1) + ': ' + str(runTitles[i])
                        paramString = "Current Param: " + runArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    for i in range(resetNum):
                        tempString = 'Reset CMD ' + str(i + 1) + ': ' + str(resetTitles[i])
                        paramString = "Current Param: " + resetArgs[i]
                        currentString = ""
                        spacesAdded = ""
                        while(len(currentString) < 70):
                            currentString = tempString + spacesAdded + paramString
                            spacesAdded = spacesAdded + " "
                        if(i == 0):
                            defString = currentString
                        commandNames.append(currentString)

                    window['-LIST4-'].update(commandNames)
                else:
                    sg.Popup('Please select a command')
            except:
                sg.PopupError('An error occurred. Please try again.')
        
        elif event == 'Mixer Spur':#Runs the mixer spur test
            testStatus = False
            theReason = ""
            tableOutput = None
            if(MixerSpurTest != None):
                if(MixerSpurTest.isConfigured == True):
                    window['-OUTPUT2-'].update("The Mixer Spur Test is Starting\nNOTE: Close the plot window to abort the test")
                    
                    try:
                        testStatus, theReason, tableOutput = MixerSpurTest.runTest()
                    except Exception as e:
                        testStatus = False
                        theReason = "Failed"
                    
                    if(testStatus == False and theReason == "Failed"):
                        window['-OUTPUT2-'].update("Check your JSON File. The Mixer Spur Test Failed")
                    elif(testStatus == False and theReason == "Aborted"):
                        window['-OUTPUT2-'].update("Mixer Spur Test ABORTED")
                        #tableOutput.show()#outputs the table
                    else:
                        window['-OUTPUT2-'].update("Mixer Spur Test Completed!")
                        tableOutput.show()#outputs the table
                else:
                    window['-OUTPUT2-'].update("Configure the Mixer Spur Test Before Running It")
            else:
                window['-OUTPUT2-'].update("Configure the Mixer Spur Test Before Running It")

        elif event == 'P1dB':#Runs the P1dB Test
            testStatus = False
            theReason = ""
            tableOutput = None
            if(P1dBTest != None):
                if(P1dBTest.isConfigured == True):
                    window['-OUTPUT2-'].update("The P1dB Test is Starting\nNOTE: Close the plot window to abort the test")
                    print("testing")
                    
                    try:
                        testStatus, theReason, tableOutput = P1dBTest.runTest()
                    except Exception as e:
                        testStatus = False
                        theReason = "Failed"
                    
                    if(testStatus == False and theReason == "Failed"):
                        window['-OUTPUT2-'].update("Check your JSON File. The P1dB Test Failed")
                    elif(testStatus == False and theReason == "Aborted"):
                        window['-OUTPUT2-'].update("P1dB Test ABORTED")
                        tableOutput.show()#outputs the table
                    else:
                        window['-OUTPUT2-'].update("P1dB Test Completed!")
                        tableOutput.show()#outputs the table
                else:
                    window['-OUTPUT2-'].update("Configure the P1dB Test Before Running It")
            else:
                window['-OUTPUT2-'].update("Configure the P1dB Test Before Running It")

        elif event == 'PinvPout':#Runs the PinVPout test
            testStatus = False
            theReason = ""
            tableOutput = None
            if(PinVPoutTest != None):
                if(PinVPoutTest.isConfigured == True):
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test is Starting\nNOTE: Close the plot window to abort the test")
                    
                    try:
                        testStatus, theReason, tableOutput = PinVPoutTest.runTest()
                    except Exception as e:
                        testStatus = False
                        theReason = "Failed"
                    
                    if(testStatus == False and theReason == "Failed"):
                        window['-OUTPUT2-'].update("Check your JSON File. The Pin Vs. Pout Test Failed")
                    elif(testStatus == False and theReason == "Aborted"):
                        window['-OUTPUT2-'].update("Pin vs. Pout Test ABORTED")
                        #tableOutput.show()#outputs the table
                    elif(testStatus == False and theReason == "Command Fail"):
                        window['-OUTPUT2-'].update("Pin vs. Pout Test ABORTED Due to SCPI Commands Failing")
                    else:
                        window['-OUTPUT2-'].update("Pin vs. Pout Test Completed!")
                        tableOutput.show()#outputs the table
                else:
                    window['-OUTPUT2-'].update("Configure the Pin vs. Pout Test Before Running It")
            else:
                window['-OUTPUT2-'].update("Configure the Pin vs. Pout Test Before Running It")
        
        elif event == 'Other':#runs the other test
            testStatus = False
            theReason = ""
            if(OtherTest != None):
                if(OtherTest.isConfigured == True):
                    window['-OUTPUT2-'].update("The Other Test is Starting\nNOTE: Close the plot window to abort the test")
                    
                    try:
                        testStatus, theReason = OtherTest.runTest()
                    except Exception as e:
                        testStatus = False
                        theReason = "Failed"
                    
                    if(testStatus == False and theReason == "Failed"):
                        window['-OUTPUT2-'].update("Check your JSON File. The Other Test Failed")
                    elif(testStatus == False and theReason == "Aborted"):
                        window['-OUTPUT2-'].update("Other Test ABORTED")
                    else:
                        window['-OUTPUT2-'].update("Other Test Completed!")
                else:
                    window['-OUTPUT2-'].update("Configure the Other Test Before Running It")
            else:
                window['-OUTPUT2-'].update("Configure the Other Test Before Running It")
        
        elif event == 'Reset':#resets everything
            #Resetting Everything
            window['-OUTPUT-'].update('')
            window['-OUTPUT2-'].update('')
            
            #Reset list to default commands
            window['-LIST-'].update(mixerSpurCommands)
            window['-LIST2-'].update(p1DBCommands)
            window['-LIST3-'].update(pinpoutCommands)
            window['-LIST4-'].update(otherCommands)
            
            sg.Popup("Everything has been reset!")

        elif event == 'Apply Plot and Table Changes':#changes the plot and table settings
            readyToChange = False
            title = values['-IN5-']
            xLabel = values['-IN6-']
            yLabel = values['-IN7-']
            
            freqUnits = "MHz"
            if(values['-R5-'] == True):
                freqUnits = "Hz"
            if(values['-R6-'] == True):
                freqUnits = "KHz"
            if(values['-R8-'] == True):
                freqUnits = "GHz"

            powUnits = "dBm"
            if(values['-R10-'] == True):
                powUnits = "Vpp"
                    
            if(title != "" and xLabel != "" and yLabel != ""):
                readyToChange = True
            
            if(readyToChange == True):
                if(MixerSpurTest != None):
                    MixerSpurTest.changeGraphSettings(title, xLabel, yLabel, freqUnits, powUnits)
                if(P1dBTest != None):
                    P1dBTest.changeGraphSettings(title, xLabel, yLabel, freqUnits, powUnits)
                if(PinVPoutTest != None):
                    PinVPoutTest.changeGraphSettings(title, xLabel, yLabel, freqUnits, powUnits)
                if(OtherTest != None):
                    OtherTest.changeGraphSettings(title, xLabel, yLabel, freqUnits, powUnits)
                sg.Popup("Plot and table settings have been changed for added tests!")
            else:
                sg.PopupError('Your plot and table settings are incorrect!')   

    #Closes GUI
    window.close()