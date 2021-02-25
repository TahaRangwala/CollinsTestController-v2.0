import numpy as np
import matplotlib.pyplot as plt

plt.ion()
a = np.arange(10)

fig,ax = plt.subplots(1,1)
figNum = fig.number
print(fig.number)
plt.show()

b = 10 * np.random.randint(0,10,size=10)
line, = ax.plot(a,b,'r-')
ax.set_ylim(0,100)
ax.set_xlim(0, 10)
ax.set_xlabel("Frequency (MHz)")
ax.set_ylabel("Power (dBm)")
ax.set_title("Spectrum Analyzer Trace")

for i in range(100):
    if(not plt.fignum_exists(figNum)):
        print("aborted")
        break
    else:
        try:
            b = 10 * np.random.randint(0,10,size=10)
            line.set_data(a,b)
            plt.draw()
            plt.pause(0.02)
        except Exception as e:
            print('closed')
    
