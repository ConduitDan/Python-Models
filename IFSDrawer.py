"""
This class draws iterated function systems
"""
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt


class IFSGenerator:
    def __init__(self,IFS = None,depth = 10,overwrite = False):
        if IFS == None:
            raise "Please supply an IFS"
        self.IFS = IFS
        self.fileName ="fractals/"+IFS.name() + str(depth)

        self.overwrite = overwrite
        self.depth = depth
        self.File = None

    def canReadFromFile(self):
        readable = False
        if not self.overwrite:
            try:
                self.File = open(self.fileName+".out","r")
                readable = True
                self.File.close()
            except: FileNotFoundError
            
        return readable
    def readPointsFromFile(self):
        self.File = open(self.fileName+".out","r")
        xline = self.File.readline().split(',')
        yline = self.File.readline().split(',')
        x = list(float(element) for element in xline)
        y = list(float(element) for element in yline) 

        self.File.close()
        return (x,y)

                
                
    def generatePoints(self):
        if self.canReadFromFile():
            (self.x,self.y) = self.readPointsFromFile()
        else:
            fractionDone = .1
            functionList = self.IFS.getFunctionList()
            numOfFunctions = len(functionList)
            numPoints = (numOfFunctions**(self.depth+1))
            self.x = [0.0]*numPoints
            self.y = [0.0]*numPoints
            self.color = [0]*numPoints

            for i in range(numPoints):
                #for each possible combination 
                xi = 0.0
                yi = 0.0
                for j in range(self.depth):
                    # go through self.depth operations
                    funIndex = int(i/(numOfFunctions**j)) % numOfFunctions
                    (xi,yi) = functionList[funIndex](xi,yi)
                self.x[i] = xi
                self.y[i] = yi
                self.color[i] = i #color scheme  is here (paramterize?)
                if i/numPoints > fractionDone:
                    print("%"+str(int(fractionDone*100)) + " Done")
                    fractionDone = fractionDone+.1
            print('%100 Done')
    def plotFractal(self):
        fig = plt.figure()
        fig.patch.set_alpha(1)
        fig.set_size_inches(30,20)
        ax = fig.add_subplot(1,1,1)
        
        ax.scatter(self.x,self.y,s = .1, marker = ".",c = self.color,cmap = 'cool',edgecolors = None)
        ax.set_aspect('equal')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

        plt.show()
        fig.savefig(self.fileName +'.png',transparent = True,dpi = 200)
    def saveData(self):
        if self.overwrite or not self.canReadFromFile():
            self.File = open(self.fileName+".out",'w')
            for xi in self.x:
                self.File.write(str(xi)+',')
            self.File.write('\n')
            for yi in self.y:
                self.File.write(str(yi)+',') 
            self.File.write('\n')
            self.File.close()
    def draw(self):
        self.generatePoints()
        self.saveData()
        self.plotFractal()

class IFSGoldenDragon:
    def __init__(self):
        phi = (1+np.sqrt(5))/2
        self.r = (1/phi)**(1/phi)
        theta = np.arccos((1+self.r**2 - self.r**4)/(2*self.r))
        self.R1 = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]]) 
        theta2 = np.pi - np.arccos((1+self.r**4 - self.r**2)/(2*self.r**2))
        self.R2 = np.array([[np.cos(theta2), -np.sin(theta2)],[np.sin(theta2),np.cos(theta2)]])
    def fun1(self,x,y):
        v = np.array([[x],[y]])
        v = np.matmul(self.R1,v)*self.r
        return (v[0][0],v[1][0])
    def fun2(self,x,y):
        v = np.array([[x],[y]])
        v = np.matmul(self.R2,v)*self.r**2+np.array([[1.0],[0.0]])
        return (v[0][0],v[1][0])
    def getFunctionList(self):
        return [self.fun1,self.fun2]
    def name(self):
        return "GoldenDragon"

    
        



if __name__ == '__main__':
    anIFS = IFSGoldenDragon()
    myDrawBot = IFSGenerator(IFS = anIFS,depth = 21)
    myDrawBot.draw()
    

    



            
        
