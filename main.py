import gui
#from equipment import Equipment_Connection
#from pinvpoutTest import PinVPout_Test
import matplotlib.pyplot as plt

#Runs the main program
if __name__ == '__main__':
    #gui.runGUI()
    
    """
    #USED FOR DEBUGGING
    equipmentList = [Equipment_Connection("Function Generator", "FunctionGenerator.json"), Equipment_Connection("Spectrum Analyzer", "SpectrumAnalyzer.json")]
    testName = 'PinVPout'
    fileName = 'PinVPout.json'
    PinVPoutTest = PinVPout_Test(testName, fileName)
    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
    configuredTests = PinVPoutTest.configureTest()
                    
    if(equipmentFound and configuredTests):
        print(testName + ": TEST CONFIGURED\n")
    else:
        print(testName + ": ERROR, TEST NOT CONFIGURED\n")"""

    isClosed = False
    fig = plt.figure()
    num = fig.number

    plt.text(0.35, 0.5, 'Close Me!', dict(size=30))
    plt.show()

    while(isClosed == False):
        if(plt.fignum_exists(num)):
            isClosed = False
        else:
            isClosed = True
            print("closed")