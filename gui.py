import PySimpleGUI as sg
import sys
from equipment import Equipment_Connection

#Runs the entire GUI
def runGUI():
    #Color Theme of GUI
    sg.theme('LightGreen2')

    #Setting up Layout of GUI

    #Adding Equipment
    tempLayout1 = [[sg.Text('Name:'), sg.InputText(key='-IN1-')],
                    [sg.Text('JSON File:'), sg.InputText(key='-IN2-')],
                    [sg.Button('Add')],
                    [sg.Output(size=(60,10), key='-OUTPUT-')], 
                    [sg.Button('Refresh Connections')]]

    #Test Configuration
    tempLayout2 = [[sg.Text('Test:'), sg.Radio('Mix Spur Test', "RADIO1", default=True), sg.Radio('P1dB Test', "RADIO1"), sg.Radio('PinvPout Test', "RADIO1")],
                    [sg.Text('JSON File:'), sg.InputText(key='-IN3-')],
                    [sg.Button('Add')],
                    [sg.Output(size=(60,10), key='-OUTPUT2-')], 
                    [sg.Button('Refresh Configurations')]]

    #Running Tests
    tempLayout3 = [[sg.Button('Mixer Spur Test'), sg.Button('P1dB Test'), sg.Button('PinvPout Test')]]

    #Plot Settings
    tempLayout4 = [[sg.Text('Title'), sg.InputText(key='-IN4-')],
                [sg.Text('X-Label'), sg.InputText(key='-IN5-')],
                [sg.Text('Y-Label'), sg.InputText(key='-IN6-')],
                [sg.Button('Apply Changes')]]

    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot Settings', element_justification='c')],
            [sg.Button('Close', size =(10, 2))]]

    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(950, 630))

    
    #Setting required data structures and variables
    equipmentList = []#all devices connected to PI

    #Loop running while GUI is open
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Add':
            equipmentName = values['-IN1-']
            fileName = values['-IN2-']
            equipmentList.append(Equipment_Connection(equipmentName, fileName))

            #Outputting connection status for all testing equipment
            outputString = ""
            isError = False
            for device in equipmentList:
                isError = device.connect()
                if(isError):
                    outputString = outputString + device.name + ": ERROR\n"
                else:
                    outputString = outputString + device.name + ": CONNECTED\n"  
            window['-OUTPUT-'].update(outputString)
            #if(isError):
            #    sg.PopupError('Some equipment connections have not been established. Please check the user manual to make sure your settings are correct.')
        elif event == 'Refresh Connections':
            window['-OUTPUT-'].update("")
            outputString = ""
            isError = False
            for device in equipmentList:
                isError = device.connect()
                if(isError):
                    outputString = outputString + device.name + ": ERROR\n"
                else:
                    outputString = outputString + device.name + ": CONNECTED\n"  
            window['-OUTPUT-'].update(outputString)
            #if(isError):
            #    sg.PopupError('Some equipment connections have not been established. Please check the user manual to make sure your settings are correct.')

    #Closes GUI
    window.close()