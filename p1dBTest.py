from tests import Run_Tests

class P1dB_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan, impedance):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan)
        self.impedance = 0
    
    def changeImpedance(impedance):
        self.impedance = impedance

    def runTest(self):
        pass