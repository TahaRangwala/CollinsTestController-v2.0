"""import numpy as np
import matplotlib.pyplot as plt

plt.ion()
a = np.arange(10)

fig,ax = plt.subplots(2,1)
plt.show()

b = 10 * np.random.randint(0,10,size=10)
rects, = ax[0].plot(a,b,'r-')
line, = ax[1].plot(a,b,'r-')
ax[0].set_ylim(0,100)
ax[1].set_ylim(0,100)

for i in range(100):
    b = 10 * np.random.randint(0,10,size=10)
    rects.set_data(a,b)
    line.set_data(a,b)
    plt.draw()
    plt.pause(0.02)"""
import matplotlib.pyplot as plt
import numpy as np

data = [(0,1),(1,3),(1,3)]
N = len(data)
cmap = plt.cm.get_cmap("hsv", N+1)
for i in range(N):
    X,Y = data[i]
    plt.scatter(X, Y, c=cmap(i))