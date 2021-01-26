import PySimpleGUI as sg
import sys

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
                    [sg.Text('JSON File:'), sg.InputText(key='-IN2-')],
                    [sg.Button('Add')],
                    [sg.Output(size=(60,10), key='-OUTPUT-')], 
                    [sg.Button('Refresh Configurations')]]

    #Running Tests
    tempLayout3 = [[sg.Button('Mixer Spur Test'), sg.Button('P1dB Test'), sg.Button('PinvPout Test')]]

    #Plot Settings
    tempLayout4 = [[sg.Text('Title'), sg.InputText(key='-IN3-')],
                [sg.Text('X-Label'), sg.InputText(key='-IN4-')],
                [sg.Text('Y-Label'), sg.InputText(key='-IN5-')],
                [sg.Button('Apply Changes')]]

    layout = [[sg.Frame(layout=tempLayout1, title='Equipment Connections', element_justification='c'), sg.Frame(layout=tempLayout2, title='Test Configuration', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout3, title='Runnable Tests', element_justification='c')],
            [sg.Text('')],
            [sg.Frame(layout=tempLayout4, title='Plot Settings', element_justification='c')],
            [sg.Button('Close', size =(10, 2))]]

    window = sg.Window('Universal PA Test Controller v2.0', layout, element_justification='c', size=(950, 630))

    #Loop running while GUI is open
    i = -1
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Close':
            break
        elif event == 'Add':
            i += 1
            

    #Closes GUI
    window.close()