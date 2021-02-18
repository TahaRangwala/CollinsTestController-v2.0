import PySimpleGUI as sg
import sys
from equipment import Equipment_Connection
from tests import Run_Tests
from mixerspurTest import Mixer_Spur_Test
from p1dBTest import P1dB_Test
from pinvpoutTest import PinVPout_Test

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
                    [sg.Text('Name:'), sg.InputText(default_text = 'PinVPout', key='-IN3-')],
                    [sg.Text('JSON File:'), sg.InputText(default_text = 'PinVPout.json', key='-IN4-')],
                    [sg.Button('Add Test')],
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

    #Entire GUI Layout
    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c'), sg.Text('   '), sg.Text('   '), sg.Text('   ')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot Settings', element_justification='c')],
            [sg.Button('Reset', size =(10, 2)), sg.Button('Close', size =(10, 2))]]

    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(1000, 700))

    
    #Setting required data structures and variables
    equipmentList = []#all devices connected to PI
        
    try:
        with open("JSON/equipment/allEquipment.txt") as equipmentFileList:
            for line in equipmentFileList:
                values = line.split(",")
                equipmentList.append(Equipment_Connection(values[0].strip(), values[1].strip()))
    except:
        sg.PopupError('Error with allEquipment.txt File. Not all pieces of equipment were added!')

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
        
        elif event == 'Add Test':
            isError = False
            equipmentFound = False
            testName = values['-IN3-']
            fileName = values['-IN4-']

            outputString = ""
            if(values['-R1-'] == True):
                pass
            elif(values['-R2-'] == True):
                pass
            elif(values['-R3-'] == True):
                try:
                    PinVPoutTest = PinVPout_Test(testName, fileName, title, xLabel, yLabel, centerFreq, freqSpan)
                    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
                
                    if(equipmentFound):
                        outputString = outputString + testName + ": TEST ADDED\n"
                    else:
                        outputString = outputString + testName + ": ERROR, CHECK YOUR JSON FILE\n"
                except:
                    outputString = outputString + testName + ": ERROR, CHECK YOUR JSON FILE\n"
                    isError = True
            else:
                pass
            window['-OUTPUT2-'].update(outputString)

            if(isError):
                sg.PopupError('Some test configurations have not been established. Please check the user manual to make sure your settings are correct.')   

        elif event == 'Configure Selected Test':
            if(values['-R1-'] == True):
                pass
            elif(values['-R2-'] == True):
                pass
            elif(values['-R3-'] == True):
                if(PinVPoutTest != None):
                    configuredTests = PinVPoutTest.configureTest()
                    if(configuredTests == True):
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is ready to run")
                    else:
                        window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
                else:
                    window['-OUTPUT2-'].update("The Pin vs. Pout Test is NOT configured correctly")
            else:
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