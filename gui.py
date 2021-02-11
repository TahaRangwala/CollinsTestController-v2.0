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
    tempLayout2 = [[sg.Text('Test:'), sg.Radio('Mix Spur Test', 'RADIO1', default=True, key = '-R1-'), sg.Radio('P1dB Test', 'RADIO1', key = '-R2-'), sg.Radio('PinvPout Test', 'RADIO1', key = '-R3-')],
                    [sg.Text('Name:'), sg.InputText(key='-IN3-')],
                    [sg.Text('JSON File:'), sg.InputText(key='-IN4-')],
                    [sg.Button('Add Test')],
                    [sg.Output(size=(60,10), key='-OUTPUT2-')], 
                    [sg.Button('Refresh Configurations')]]

    #Running Tests
    tempLayout3 = [[sg.Button('Mixer Spur Test'), sg.Button('P1dB Test'), sg.Button('PinvPout Test')]]

    #Plot Settings
    tempLayout4 = [[sg.Text('Title'), sg.InputText(key='-IN5-')],
                [sg.Text('X-Label'), sg.InputText(key='-IN6-')],
                [sg.Text('Y-Label'), sg.InputText(key='-IN7-')],
                [sg.Button('Apply Changes')]]

    #Entire GUI Layout
    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c'), sg.Text('   '), sg.Text('   '), sg.Text('   '), sg.Button('Reset Tests', size =(10, 2))],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot Settings', element_justification='c')],
            [sg.Button('Reset', size =(10, 2)), sg.Button('Close', size =(10, 2))]]

    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(950, 680))

    
    #Setting required data structures and variables
    equipmentList = []#all devices connected to PI

    #Tests the Program Offers
    MixerSpurTest = None
    P1dBTest = None
    PinVPoutTest = None

    #Loop running while GUI is open
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break

        elif event == 'Add Equipment':
            equipmentName = values['-IN1-']
            fileName = values['-IN2-']

            jsonError = False
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

            if(jsonError):
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
            configuredTests = False
            testName = values['-IN3-']
            fileName = values['-IN4-']

            outputString = ""
            if(values['-R1-'] == True):
                pass
            elif(values['-R2-'] == True):
                pass
            else:
                try:
                    PinVPoutTest = PinVPout_Test(testName, fileName)
                    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
                    configuredTests = PinVPoutTest.configureTest()
                    
                    if(equipmentFound and configuredTests):
                        outputString = outputString + testName + ": TEST CONFIGURED\n"
                    else:
                        outputString = outputString + testName + ": ERROR, TEST NOT CONFIGURED\n"
                except:
                    outputString = outputString + testName + ": ERROR, TEST NOT CONFIGURED\n"
                    isError = True
            window['-OUTPUT2-'].update(outputString)

            if(isError):
                sg.PopupError('Some test configurations have not been established. Please check the user manual to make sure your settings are correct.')   

        elif event == 'Refresh Configurations':
            pass

        elif event == 'Mixer Spur Test':
            pass

        elif event == 'P1dB Test':
            pass

        elif event == 'PinvPout Test':
            pass

        elif event == 'Reset':
            #Resetting Everything
            equipmentList = []

            MixerSpurTest = None
            P1dBTest = None
            PinVPoutTest = None

            window['-OUTPUT-'].update('')
            window['-OUTPUT2-'].update('')

        elif event == 'Reset Tests':
            passclear

    #Closes GUI
    window.close()