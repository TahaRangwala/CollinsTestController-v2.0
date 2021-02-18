from tests import Run_Tests

class P1dB_Test(Run_Tests):

    def __init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan) 

    def runTest(self):
        pass