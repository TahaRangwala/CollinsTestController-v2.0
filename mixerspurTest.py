from tests import Run_Tests

class Mixer_Spur_Test(Run_Tests):

    # This function is just like the function used for the PinvPout test. It is simply to get data points for plotting
    def parseGetTrace(plotPoints, centerFreq, freqSpan):
        str_data = str(plotPoints)
        str_data = str_data.split(" ", 1)[1]
        str_data = str_data.split(',')
        data_array = np.array(list(map(float, str_data[1:])))

        start = (int(centerFreq)-0.5*int(freqSpan)) * 10**6
        stop = (int(centerFreq)+0.5*int(freqSpan)) * 10**6
        step = (stop-start)/len(data_array)
        x = np.arange(start, stop, step)
        return x, data_array, start, stop


    #2/23/2021 We need to have the user specify amount of integer multple harmonics (think "n" times the frequency of the carrier and/or message)
    #          Then, we can make a spur table out of the results we get for those frequencies. For example, if we want 10 integer multiples,
    #          then we have to look at the 1x1, 1x2, ..., 1x10, 2x1, 2x2, ..., 10x10 frequencies. This frequency is evaluated as the absolute value
    #          of one harmonic of one frquency minus the other harmonic of the other frequency
    def __init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan):
        Run_Tests.__init__(self, name, fileName, title, xlabel, ylabel, centerFreq, freqSpan) 

    def runTest(self):
        pass