import PySimpleGUI as sg
import sys
from equipment import Equipment_Connection
from tests import Run_Tests
from mixerspurTest import Mixer_Spur_Test
from p1dBTest import P1dB_Test
from pinvpoutTest import PinVPout_Test
from otherTest import Other_Test

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
                    [sg.Button('Configure Selected Test')]]

    #Running Tests
    tempLayout3 = [[sg.Button('Mixer Spur Test'), sg.Button('P1dB Test'), sg.Button('PinvPout Test')]]

    #Plot Settings
    tempLayout4 = [[sg.Text('Title'), sg.InputText(default_text = 'Spectrum Analyzer Trace', key='-IN5-')],
                [sg.Text('X-Label'), sg.InputText(default_text = 'Frequency (MHz)',key='-IN6-')],
                [sg.Text('Y-Label'), sg.InputText(default_text = 'Power (dBm)', key='-IN7-')],
                [sg.Text('Center Frequency (MHz)'), sg.InputText(default_text = '1', key='-IN8-')],
                [sg.Text('Frequency Span (MHz)'), sg.InputText(default_text = '1', key='-IN9-')],
                [sg.Button('Apply Plot Changes')]]

    
    #Setting required data structures and variables
    
    #Automatically Connecting Equipment
    equipmentList = []#all devices connected to PI
        
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
    
    #Default Plot Settings
    title = "Spectrum Analyzer Trace"
    xLabel = "Frequency (MHz)"
    yLabel = "Power (dBm)"
    centerFreq = 1
    freqSpan = 1
    
    settingsTab = []
    emptyTab =  [[sg.T('No test has been added here')]]
    emptyTab2 =  [[sg.T('No test has been added here')]]  
    emptyTab3 =  [[sg.T('No test has been added here')]]  
    emptyTab4 =  [[sg.T('No test has been added here')]]  

    try:
        testNum = 1
        with open("JSON/tests/allTests.txt") as testFileList:
            for line in testFileList:
                values = line.split(",")
                testName = str(values[0].strip())
                fileName = str(values[1].strip())
                testType = str(values[2].strip())
                if(testType == 'MixerSpurTest'):
                    if(MixerSpurTest == None):
                        commandNames = []
                        MixerSpurTest = MixerSpurTest(testName, fileName, title, xLabel, yLabel, centerFreq, freqSpan)
                        configNum, runNum, resetNum = MixerSpurTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = MixerSpurTest.getTitlesList()
                        configArgs, runArgs, resetArgs = MixerSpurTest.getArgsList()
                        
                        currentString = ""
                        for i in range(configNum):
                            currentString = 'Config Command ' + str(i + 1) + ': ' + str(configTitles[i]) + "     Current Parameter: " + configArgs[i]
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            currentString = 'Run Command ' + str(i + 1) + ': ' + str(runTitles[i]) + "     Current Parameter: " + runArgs[i]
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            currentString = 'Reset Command ' + str(i + 1) + ': ' + str(resetTitles[i]) + "     Current Parameter: " + resetArgs[i]
                            commandNames.append(currentString)

                        settingsTab.append(sg.Tab('Mixer Spur Test', [[sg.Listbox(commandNames, default_values = currentString, size=(70,10), enable_events=True, key = '-LIST-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN10-')], [sg.Button('Change Mixer Spur Test Settings')]], tooltip = 'tip'))
                elif(testType == 'p1DBTest'):
                    if(P1dBTest == None):
                        commandNames = []
                        P1dBTest = P1dB_Test(testName, fileName, title, xLabel, yLabel, centerFreq, freqSpan)
                        configNum, runNum, resetNum = P1dBTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = P1dBTest.getTitlesList()
                        configArgs, runArgs, resetArgs = P1dBTest.getArgsList()
                        
                        currentString = ""
                        for i in range(configNum):
                            currentString = 'Config Command ' + str(i + 1) + ': ' + str(configTitles[i]) + "     Current Parameter: " + configArgs[i]
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            currentString = 'Run Command ' + str(i + 1) + ': ' + str(runTitles[i]) + "     Current Parameter: " + runArgs[i]
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            currentString = 'Reset Command ' + str(i + 1) + ': ' + str(resetTitles[i]) + "     Current Parameter: " + resetArgs[i]
                            commandNames.append(currentString)

                        settingsTab.append(sg.Tab('P1dB Test', [[sg.Listbox(commandNames, default_values = currentString, size=(70,10), enable_events=True, key = '-LIST2-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN11-')], [sg.Button('Change P1dB Test Settings')]], tooltip = 'tip'))
                
                elif(testType == 'PinvPoutTest'):
                    if(PinVPoutTest == None):
                        commandNames = []
                        PinVPoutTest = PinVPout_Test(testName, fileName, title, xLabel, yLabel, centerFreq, freqSpan)
                        configNum, runNum, resetNum = PinVPoutTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = PinVPoutTest.getTitlesList()
                        configArgs, runArgs, resetArgs = PinVPoutTest.getArgsList()
                
                        currentString = ""        
                        for i in range(configNum):
                            currentString = 'Config Command ' + str(i + 1) + ': ' + str(configTitles[i]) + "     Current Parameter: " + configArgs[i]
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            currentString = 'Run Command ' + str(i + 1) + ': ' + str(runTitles[i]) + "     Current Parameter: " + runArgs[i]
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            currentString = 'Reset Command ' + str(i + 1) + ': ' + str(resetTitles[i]) + "     Current Parameter: " + resetArgs[i]
                            commandNames.append(currentString)

                        settingsTab.append(sg.Tab('Pin vs. Pout Test', [[sg.Listbox(commandNames, default_values = currentString, size=(70,10), enable_events=True, key = '-LIST3-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN12-')], [sg.Button('Change Pin vs. Pout Test Settings')]], tooltip = 'tip'))
                else:
                    if(OtherTest == None):
                        commandNames = []
                        OtherTest = Other_Test(testName, fileName, title, xLabel, yLabel, centerFreq, freqSpan)
                        configNum, runNum, resetNum = OtherTest.getNumberOfCommands()
                        configTitles, runTitles, resetTitles = OtherTest.getTitlesList()
                        configArgs, runArgs, resetArgs = OtherTest.getArgsList()
                        
                        currentString = ""
                        for i in range(configNum):
                            currentString = 'Config Command ' + str(i + 1) + ': ' + str(configTitles[i]) + "     Current Parameter: " + configArgs[i]
                            commandNames.append(currentString)
                            
                        for i in range(runNum):
                            currentString = 'Run Command ' + str(i + 1) + ': ' + str(runTitles[i]) + "     Current Parameter: " + runArgs[i]
                            commandNames.append(currentString)

                        for i in range(resetNum):
                            currentString = 'Reset Command ' + str(i + 1) + ': ' + str(resetTitles[i]) + "     Current Parameter: " + resetArgs[i]
                            commandNames.append(currentString)

                        settingsTab.append(sg.Tab('Other Test', [[sg.Listbox(commandNames, size=(70,10), default_values = currentString, enable_events=True, key = '-LIST4-')], [sg.Text('Change the selected command parameter: '), sg.InputText(key='-IN13-')], [sg.Button('Change Pin vs. Pout Test Settings')]], tooltip = 'tip'))
                testNum = testNum + 1
                if(testNum > 4):
                    break
    except:
        sg.PopupError('Error with allTests.txt File. Not all tests were added!')
        
    if(MixerSpurTest == None):
        settingsTab.append(sg.Tab('Mixer Spur Test', emptyTab, tooltip = 'tip'))
    if(P1dBTest == None):
        settingsTab.append(sg.Tab('P1dB Test', emptyTab2, tooltip = 'tip'))
    if(PinVPoutTest == None):
        settingsTab.append(sg.Tab('Pin vs. Pout Test', emptyTab3, tooltip = 'tip'))
    if(OtherTest == None):
        settingsTab.append(sg.Tab('Other Test', emptyTab4, tooltip = 'tip'))
    
    settingsLayout = [[sg.TabGroup([settingsTab], tooltip='Select a command')]]
    
    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c'), sg.Frame(layout=settingsLayout, title='Test Settings', element_justification='c', size=(300, 300))],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c'), sg.Text('   '), sg.Text('   '), sg.Text('   ')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot Settings', element_justification='c')],
            [sg.Button('Reset', size =(10, 2)), sg.Button('Close', size =(10, 2))]]

    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(1500, 720))
        
    #Loop running while GUI is open
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break

        elif event == 'Add Equipment':
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
                    print("POOP")
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
                
        elif event == 'Refresh Connections':
            window['-OUTPUT-'].update("")
            outputString = ""
            jsonError = False
            isError = False

            try:
                for device in equipmentList:
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

        elif event == 'Configure Selected Test':
            if(values['-R1-'] == True):
                if(MixerSpurTest != None):
                    equipmentFound = MixerSpurTest.addEquipment(equipmentList)
                    configuredTests = MixerSpurTest.configureTest()
                    if(configuredTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Mixer Spur Test is ready to run")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Mixer Spur Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Mixer Spur Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The Mixer Spur Test is NOT configured correctly")
            elif(values['-R2-'] == True):
                if(P1dBTest != None):
                    equipmentFound = P1dBTest.addEquipment(equipmentList)
                    configuredTests = P1dBTest.configureTest()
                    if(configuredTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The P1dB Test is ready to run")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The P1dB Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The P1dB Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The P1dB Test is NOT configured correctly")
            elif(values['-R3-'] == True):
                if(PinVPoutTest != None):
                    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
                    configuredTests = PinVPoutTest.configureTest()
                    if(configuredTests == True and equipmentFound == True):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is ready to run")
                    elif(equipmentFound == False):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test does not have all required test equipment")
                    else:
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
            else:
                if(OtherTest != None):
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
        
        elif event == 'Change Mixer Spur Test Settings':
            pass
            
        elif event == 'Change P1dB Test Settings':
            pass
        
        elif event == 'Change Pin vs. Pout Test Settings':
            try:
                testParam = values['-IN12-']
                listValue = str(values['-LIST3-'])
                if(testParam == "" and listValue == ""):
                    sg.PopupError('Please enter a parameter')
                    
                
            except:
                sg.PopupError('An error occurred. Please try again.')
            
        elif event == 'Change Other Test Settings':
            pass
    
        elif event == 'Mixer Spur Test':
            pass

        elif event == 'P1dB Test':
            pass

        elif event == 'PinvPout Test':
            testStatus = False
            theReason = ""
            if(PinVPoutTest != None):
                if(PinVPoutTest.isConfigured == True):
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test is Starting\nNOTE: Close the plot window to abort the test")
                    
                    try:
                        testStatus, theReason = PinVPoutTest.runTest()
                    except Exception as e:
                        testStatus = False
                        theReason = "Failed"
                    
                    if(testStatus == False and theReason == "Failed"):
                        window['-OUTPUT2-'].update("Check your JSON File. The Pin Vs. Pout Test Failed")
                    elif(testStatus == False and theReason == "Aborted"):
                        window['-OUTPUT2-'].update("Pin vs. Pout Test ABORTED")
                    else:
                        window['-OUTPUT2-'].update("Pin vs. Pout Test Completed!")
                else:
                    window['-OUTPUT2-'].update("Configure the Pin vs. Pout Test Before Running It")
            else:
                window['-OUTPUT2-'].update("Configure the Pin vs. Pout Test Before Running It")

        elif event == 'Reset':
            #Resetting Everything
            equipmentList = []

            MixerSpurTest = None
            P1dBTest = None
            PinVPoutTest = None
            OtherTest = None

            window['-OUTPUT-'].update('')
            window['-OUTPUT2-'].update('')
            
            sg.Popup("Everything has been reset!")

        elif event == 'Apply Plot Changes':
            readyToChange = False
            title = values['-IN5-']
            xLabel = values['-IN6-']
            yLabel = values['-IN7-']
            centerFreq = values['-IN8-']
            freqSpan = values['-IN9-']
            
            if(title != "" and xLabel != "" and yLabel != ""):
                readyToChange = True
            
            try:
                int(centerFreq)
                int(freqSpan)
            except:
                readyToChange = False
            
            if(readyToChange == True):
                if(MixerSpurTest != None):
                    MixerSpurTest.changeGraphSettings(title, xLabel, yLabel, centerFreq, freqSpan)
                if(P1dBTest != None):
                    P1dBTest.changeGraphSettings(title, xLabel, yLabel, centerFreq, freqSpan)
                if(PinVPoutTest != None):
                    PinVPoutTest.changeGraphSettings(title, xLabel, yLabel, centerFreq, freqSpan)
                if(OtherTest != None):
                    OtherTest.changeGraphSettings(title, xLabel, yLabel, centerFreq, freqSpan)
                sg.Popup("Plot settings have been changed for added tests!")
            else:
                sg.PopupError('Your plot settings are incorrect!')   

                

    #Closes GUI
    window.close()