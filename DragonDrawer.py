# -*- coding: utf-8 -*-
"""
Created on Sun Aug 29 15:10:46 2021

This program draws dragon fractals

@author: Danny
"""
import numpy as np
from matplotlib import pyplot as plt


class DragonDrawer:
    def __init__(self,theta = np.pi/2, depth = 10):
        
        self.depth = depth
        self.phi = (1+np.sqrt(5))/2
        self.r = (1/self.phi)**(1/self.phi)
        theta = np.arccos((1+self.r**2 - self.r**4)/(2*self.r))
        self.R1 = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]]) 
        theta2 = np.pi - np.arccos((1+self.r**4 - self.r**2)/(2*self.r**2))
        self.R2 = np.array([[np.cos(theta2), -np.sin(theta2)],[np.sin(theta2),np.cos(theta2)]])

        self.maxPoints = 2**(self.depth+1)-1
        
    def createHandednessVector(self):
        # for a given detph there is 2^(depth+1)-1 points
        handVector = np.ones(2**(self.depth+1)-1,dtype = np.int8)
        #handVector = [1]*(2**(self.depth-1)-1)
        for i in range(self.depth):
            
            index = 2**(i+1) - 1
            nextIndex = 2**(i+2) - 1
            handVector[0:nextIndex] = np.concatenate((handVector[0:index],np.ones(1,dtype = np.int8),-np.flip(handVector[0:index])))
        return handVector
    
    
    def createPoints(self):
        handVector = self.createHandednessVector()
        coords = np.zeros((2,len(handVector)+2),dtype = np.double)
        direction = np.array([[1.0],[0.0]],dtype = np.double)
        
        for i in range(len(handVector)):
            
            if handVector[i] == 1:
                coords[:,np.newaxis,i+1] = coords[:,np.newaxis,i] + direction*self.r**2
                direction = np.matmul(self.R1 , direction)
            elif handVector[i] == -1:
                coords[:,np.newaxis,i+1] = coords[:,np.newaxis,i] + direction*(self.r)
                direction = np.matmul(self.R2 , direction)
            
        coords[:,np.newaxis,len(handVector)+1] = coords[:,np.newaxis,len(handVector)]+direction*self.r
        return coords
    
    def createPointsIFS(self):
        coords = np.zeros((2,self.maxPoints),dtype = np.double)
        colors = np.zeros(self.maxPoints)
        for i in range(self.maxPoints):
            for j in range(self.depth):
                if int(i/(2**j))%2 == 0:
                    coords[:,np.newaxis,i] = np.matmul(self.R1,coords[:,np.newaxis,i])*self.r
                    colors[i]+=1
                else:
                    coords[:,np.newaxis,i] = np.matmul(self.R2,coords[:,np.newaxis,i])*(self.r**2)+np.array([[1.0],[0.0]])
        return (coords,colors)
                
    
    def plotDragon(self):
        (coords,colors) = self.createPointsIFS()
       # colors = np.zeros((self.maxPoints,3),dtype = 'double')
       # for i in range(self.maxPoints):
        #    colors[i,:] = [.75,.5+.5*i/self.maxPoints,.75]
            
        fig = plt.figure()
        fig.patch.set_alpha(1)
        fig.set_size_inches(30,20)
        ax = fig.add_subplot(1,1,1)
        
        ax.scatter(coords[0,:],coords[1,:],s = .1, marker = ".",c =colors,cmap = 'cool',edgecolors = None)
        ax.set_aspect('equal')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

        plt.show()
        fig.savefig('GoldenDragonC1.png',transparent = True,dpi = 200)
        
if __name__ == '__main__':
    myDragon = DragonDrawer(depth = 22)
    myDragon.plotDragon()
        
        
        
            
        
    
        