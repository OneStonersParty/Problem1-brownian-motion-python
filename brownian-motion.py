import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import random

PlotSize = 5000
StepTime = 1
ColouringConstant = 10

px = 1 / 4 + 0.01
py = 1 / 4
p_x = 1 / 4

P = [px, px + py, px + py + p_x]
MinCoord = - PlotSize / 2
MaxCoord = PlotSize / 2
ImageExtent=[MinCoord, MaxCoord, MinCoord, MaxCoord]

class BrownianMotion(object):
    def __init__(self, PlotSize, ColouringConstant, P):
        self.ColouringConstant = ColouringConstant
        self.PlotSize = PlotSize
        self.historyData = np.zeros((PlotSize, PlotSize))
        self.xpos = int(PlotSize/2)
        self.ypos = int(PlotSize/2)
        self.historyAtPos = 0.0
    def update(self):
        self.historyData[self.ypos][self.xpos] = self.historyAtPos + (1. - self.historyAtPos) / self.ColouringConstant
        # calculate new pos
        direction = random.uniform(0,1)
        if direction < P[0]:
            self.xpos += 1
        elif direction < P[1]:
            self.ypos += 1
        elif direction < P[2]:
            self.xpos -= 1
        else:
            self.ypos -= 1
        self.xpos = np.clip(self.xpos, 0, self.PlotSize - 1)
        self.ypos = np.clip(self.ypos, 0, self.PlotSize - 1)
        # save old history data at pos
        self.historyAtPos = self.historyData[self.ypos][self.xpos]
        # make current pos max brightness
        self.historyData[self.ypos][self.xpos] = 1
        return self.historyData

fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False,
                     xlim=(MinCoord, MaxCoord), ylim=(MinCoord, MaxCoord))
ax.set_aspect('equal')
ax.grid(True)

brownianSim = BrownianMotion(PlotSize, ColouringConstant, P)

def initAnimation():
    global image
    history = brownianSim.update()
    image = ax.imshow(history, extent=ImageExtent, interpolation='nearest')
    return image,

def updateAnimation(i):
    history = brownianSim.update()
    image.set_data(history)
    return image,

ani = animation.FuncAnimation(fig, updateAnimation, None, interval=StepTime,
                              blit=True, init_func=initAnimation)

plt.show()
