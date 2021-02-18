import gui
#from equipment import Equipment_Connection
#from pinvpoutTest import PinVPout_Test
#import matplotlib.pyplot as plt
#import numpy as np

#Runs the main program
if __name__ == '__main__':
    gui.runGUI()
    
    """plt.axis([0, 10, 0, 1])

    for i in range(10):
        y = np.random.random()
        plt.plot(i, y)
        plt.pause(0.05)

    plt.show()"""
    
    #USED FOR DEBUGGING
    """equipmentList = [Equipment_Connection("Function Generator", "FunctionGenerator.json"), Equipment_Connection("Spectrum Analyzer", "SpectrumAnalyzer.json")]
    testName = 'PinVPout'
    fileName = 'PinVPout.json'
    PinVPoutTest = PinVPout_Test(testName, fileName)
    equipmentFound = PinVPoutTest.addEquipment(equipmentList)
    configuredTests = PinVPoutTest.configureTest()
                    
    runTest = PinVPoutTest.runTest()
    if(runTest):
        print("good")
    else:
        ("bad")
    
    """
    
    """
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
            print("closed")"""