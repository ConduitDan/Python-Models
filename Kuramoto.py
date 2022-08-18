import random
import math
import numpy as np
import neighborgrid
from matplotlib import pyplot as plt
import matplotlib.patches as patches
from animator import ModelAnimator
class KuramotoModel:
    ''' This class is for making kurmodo modles, this class will set up
    the oscillators and manage time and plotting commands'''
    def __init__(self, N=2, D = 0, K=-.1, dt = .01, maxT = 20, dtOutput = .05):
        self.N = N # number of oscillators 
        self.K = K # Coupling constant
        self.dt = dt # time step
        self.dtOutput = dtOutput # how often to output 
        self.t = 0 # time 
        
        self.maxT = maxT # stop time
        self.D = D # noise strength
        
        self.oscList = [] # list of oscilators
        
        for i in range(self.N): #Create the list of Kuramoto Oscillators
            self.oscList.append(KuramotoOscillator(noiseStrength = self.D,couplingStrength = self.K))
        
        self.connectNN() # Couple them Nearest Neighbor
        
        
        
    def connectNN(self):
        # connect the oscilators to adjecent ones
        for i in range(self.N):
            self.oscList[i].addNeighbor(self.oscList[(i-1)%self.N])
            self.oscList[i].addNeighbor(self.oscList[(i+1)%self.N])
        
        
    def update(self):
        '''The update function updates the current state, this will
        increase the time by dt'''

        # add dt to t
        self.t += self.dt

        for osc in self.oscList:
            osc.calculateUpdate(self.dt)

        for osc in self.oscList:
            osc.acceptUpdate()

        return self.output()
            
            
    def run(self):
        outputTime = 0
        while self.t<self.maxT:
            self.update()
            outputTime += self.dt
            if outputTime >self.dtOutput:
                outputTime = 0
                yield self.output()

    def isDone(self):
        return not self.t<self.maxT
    
    def output(self):
        # output angle list and time
        return (list(osc.theta for osc in self.oscList), self.t)
        

    def plot(self,angleList = None,t=None):
        # to plot we draw a large cirlce and a smaller circle on it for each Oscillator
        # the Oscillator are in RGB order
            if angleList == None:
                angleList = list(osc.theta for osc in self.oscList)
            R= .45
            CoM = (.5,.5)
            xList = list(R*np.cos(ang)+CoM[0] for ang in angleList)
            yList = list(R*np.sin(ang)+CoM[1] for ang in angleList)
            
            
            # Plot a unit circle
            bigCirlce = patches.Circle(CoM,radius = R,fill = False,color = [0,0,0])
            
            # plot smaler cirlces on the unit cirlce for each oscilator
            oscCircles = []
            HSVcm = plt.cm.hsv
            colors = list(HSVcm(i/self.N) for i in range(self.N))

            for (x,y,theta,c) in zip(xList, yList, angleList,colors):
                oscCircles.append(patches.Circle((x,y),radius = .05,color = c)) 
                
            
            self.axis.add_patch(bigCirlce)
            for circ in oscCircles:
                self.axis.add_patch(circ)
            
            self.axis.set_xlim(left = 0, right = 1)
            self.axis.set_ylim(bottom = 0, top = 1)
            self.axis.set_aspect('equal')
            self.axis.xaxis.set_ticks([])
            self.axis.yaxis.set_ticks([])
            
            
            
    def assignAxis(self,axis):
        self.axis = axis
        
    def NTimeSteps(self):
        return int(self.maxT/self.dtOutput)
    
    def runAndPlot(self):
        '''runs the model and yeilds an artist to draw the plot'''
        for output in self.run():
            print(self.t)
            yield self.plot()







class KuramotoOscillator:
    '''This class has is a single KuramotoOscillator it has natural
    fequencey and a Strategy for coupling'''
    def __init__(self, omega = 1, noiseStrength = 0,
               couplingStrength = 1,
               couplingStat = None,
               IC = None):
        
        self.omega = omega # frequency
        self.D = noiseStrength
        self.K = couplingStrength
        
        if couplingStat == None:
            self.couplingStrat = KuramotoCouplingBasic() # the standard kuramoto coupling
        else:
            self.couplingStrat = couplingStat # or use something less standard

        if IC == None:
            self.theta = np.random.random()*2*np.pi
        else:
            self.theta = IC
        

        self.neighbors = []
        self.newTheta = 0

        

    def addNeighbor(self,newNeighbor):
        self.neighbors.append(newNeighbor)
        
    def calculateRHS(self):
        return self.omega + self.K*self.couplingStrat.calculateCoupling(self)

    def calculateUpdate(self,dt):
        #Forward Euler, can add more later though strat
        self.newTheta = self.theta + dt * self.calculateRHS()
        
    def acceptUpdate(self):
        self.theta = self.newTheta % (2*np.pi)
    


class Singleton(type): # we only need one copy of each coupling strat so make them singletons
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
    
    
class KuramotoCouplingBasic(metaclass=Singleton):
    def calculateCoupling(self,oscillator):
        couplingTerm = 0
        for otherOsc in oscillator.neighbors:
            couplingTerm += np.sin(otherOsc.theta - oscillator.theta)
        
        couplingTerm/=len(oscillator.neighbors)
        
        return couplingTerm

class KuramotoCouplingAngleDep(metaclass=Singleton):
    def calculateCoupling(self,oscillator):
        couplingTerm = 0
        for otherOsc in oscillator.neighbors:
            couplingTerm += np.sin(oscillator.theta)*np.sin(otherOsc.theta - oscillator.theta)
        
        couplingTerm/=len(oscillator.neighbors)
        
        return couplingTerm
            



if __name__ == '__main__':
    #myModel = KuramotoModel()
    
    myModel = [[KuramotoModel() for i in range(5)] for j in range(5)]
    myAnimator = ModelAnimator(modelArray = myModel,filename = 'testKura.gif')
    myAnimator.animateAndSave()
