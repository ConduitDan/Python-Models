import random
import math
import numpy as np
import neighborgrid
from matplotlib import pyplot as plt

class Vicsek:

    '''This is the Vicsek Model a flocking model, in this model there
    are arrows or 2d spins that move forward in their direction and
    align their direcation to thier neighbors within a radius R. The
    bounding box for this simulation is of size 1 so the density is
    equal to the number  of partilces. The velocity here has also been
    normalized to 1. The spins will align or 'flock' if depending on the
    density, the rotational diffusion Dr and the amount traveld in a
    single time step, here controlled by dt'''


    def __init__(self, rho = 10, Dr = .2, R = 0.1, dt = .01,
                 maxT = 5,spins = None):
        self.rho = rho # density
        self.Dr = Dr
        self.sigma = math.sqrt(2*Dr*dt)
        self.R = R
        self.dt = dt
        self.maxT = maxT
        self.nSteps = math.floor(maxT/dt)-1
        self.t = 0
        self.axis = None
        
        if spins == None:
            self.spins = list(VicsekSpins() for i in range(self.rho))
        else:
            self.spins = spins
            
        self.grid = neighborgrid.neigborgrid(R = self.R)
        self.grid.update(self.spins)

    def update(self):
        '''The update function updates the current state, this will
        increase the time by dt'''
        self.t += self.dt

        for spin_i in self.spins:
            aveVector = [0, 0]
            for spin_j in self.grid.getNeighborhood(spin_i):
                UV = spin_j.UnitVector()
                aveVector[0] += UV[0]
                aveVector[1] += UV[1]
            spin_i.nextAngle = math.atan2(aveVector[1],aveVector[0])+random.gauss(0,self.sigma)

        for spin_i in self.spins:
            spin_i.Update(self.dt)

        self.grid.update(self.spins)
        return self.output()
            
            
    def run(self):
        while self.t<self.maxT:
            
            yield self.update()

    def isDone(self):
        return not self.t<self.maxT
    
    def output(self):
        
        return (list(spin_i.x for spin_i in self.spins),
                list(spin_i.y for spin_i in self.spins),
                list(spin_i.angle for spin_i in self.spins),
                self.t)
        

    def plot(self,x = None ,y = None,angle = None,t=None):
            if x == None:
                x = list(spin.x for spin in self.spins)
            if y == None:
                y = list(spin.y for spin in self.spins)
            if angle == None:
                angle = list(spin.angle for spin in self.spins)
            
            HSVcm = plt.cm.hsv
            
            ArrowColor = list(HSVcm(theta/(2*np.pi)) for theta in angle)
            self.axis.quiver(x,y,np.cos(angle),np.sin(angle),color = ArrowColor)
            self.axis.set_xlim(left = 0, right = 1)
            self.axis.set_ylim(bottom = 0, top = 1)
            self.axis.set_aspect('equal')
            self.axis.xaxis.set_ticks([])
            self.axis.yaxis.set_ticks([])


    def NTimeSteps(self):
        return int(self.maxT/self.dt)
    
    def runAndPlot(self):
        '''runs the model and yeilds an artist to draw the quiver'''
        for output in self.run():
            print(self.t)
            yield self.plot()
    def assignAxis(self,axis):
        self.axis = axis
    
        
        
    
class VicsekSpins:

    '''This class implements the spins for the viscek model this spins
    have a position and orientation'''

    def __init__(self, x = None, y = None, angle = None):
        if x == None: x = random.random() 
        if y == None: y = random.random() 
        if angle == None: angle = random.random()*2*math.pi

        self.x = x
        self.y = y
        self.angle = angle
        self.nextAngle = 0.0

    def __sub__(self, other):
        '''returns the spacial distance between two spins'''
        xdiff = self.periodicDist(self.x,other.x)
        ydiff = self.periodicDist(self.y,other.y)

        return math.sqrt(xdiff**2+ydiff**2)

    def UnitVector(self):
        return (math.cos(self.angle), math.sin(self.angle))

    def Update(self,dt):
        self.x = (self.x + dt*math.cos(self.angle)) % 1
        self.y = (self.y + dt*math.sin(self.angle)) % 1
        self.angle = self.nextAngle % (np.pi*2)

    def periodicDist(self,x1,x2):
        diff1 = abs(x1 - x2)
        diff2 = abs(x1 - x2 + 1)
        diff3 = abs(x1 - x2 - 1)
        return min(diff1,diff2,diff3)





if __name__ == '__main__':
    basicModel = Vicsek(rho = 1000,maxT = 2)
    for (x,y,angle,t) in basicModel.run():
        pass
        #print(format(t,'1.2f'))
    





