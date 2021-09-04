"""
This class draws iterated function systems
"""
from pathlib import Path
import numpy as np

class IFSGenerator:
    def __init__(self,IFS = None,depth = 10,overwrite = False):
        if IFS == None:
            raise "Please supplie an IFS"
        self.IFS = IFS
        self.fileName = IFS.name() + str(depth) + ".out"

        self.overwrite = overwrite
        self.depth = depth
        self.File = None

    def canReadFromFile(self):
        readable = False
        if not self.overwrite:
            try:
                self.File = open(self.fileName,"r")
                readable = True
                close(self.File)
            except: FileNotFoundError
            
        return readable
    def readPointsFromFile(self):
        self.File = open(self.fileName,"r")
        xline = self.File.readline().split(',')
        yline = self.File.readline().split(',')
        x = list(float(element) for element in xline)
        y = list(float(element) for element in yline) 

        self.File.close()
        return (x,y)

                
                
    def generatePoints(self):
        if self.canReadFromFile():
            (self.x,self.y) = readPointsFromFile()
        else:
            functionList = self.IFS.getFunctionList()
            numOfFunctions = len(functionList)
            numPoints = (numOfFunctions**(self.depth+1)-1)
            self.x = [0.0]*numPoints
            self.y = [0.0]*numPoints
            self.color = [0]*numPoints

            for i in range(numPoints):
                #for each possible combination 
                xi = 0.0
                yi = 0.0
                for j in range(self.depth):
                    # go through self.depth operations
                    funIndex = int(i/(numOfFunctions**self.depth)) % numOfFunctions
                    (xi,yi) = functionList[i](xi,yi)
                self.x[i] = xi
                self.y[i] = yi
                self.color[i] = i #color scheme  is here (paramterize?)
                
    def plotFractal(self):
        fig = plt.figure()
        fig.patch.set_alpha(1)
        fig.set_size_inches(30,20)
        ax = fig.add_subplot(1,1,1)
        
        ax.scatter(self.x,self.y,s = .1, marker = ".",c = self.colors,cmap = 'cool',edgecolors = None)
        ax.set_aspect('equal')
        ax.xaxis.set_ticks([])
        ax.yaxis.set_ticks([])

        plt.show()
        fig.savefig('GoldenDragonC1.png',transparent = True,dpi = 200)
    def saveData(self):
        if self.override or not self.canReadFromFile():
            self.File = open(self.fileName,'w')
            for xi in self.x:
                self.File.write(str(xi),',')
            self.File.write('\n')
            for yi in self.y:
                self.File.write(str(yi),',') 
            self.File.write('\n')
            
    def draw(self):
        self.generatePoints()
        self.plotFractal()
        self.saveData()

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
        return (v[0],v[1])
    def fun2(self,x,y):
        v = np.array([[x],[y]])
        v = np.matmul(self.R2,v)*self.r**2+np.array([[1.0],[0.0]])
        return (v[0],v[1])
    def getFunctionList(self):
        return [self.fun1,self.fun2]
    def name(self):
        return "GoldenDragon"
    
        



if __name__ == '__main__':
    anIFS = IFSGoldenDragon()
    myDrawBot = IFSGenerator(IFS = anIFS,depth = 10)
    myDrawBot.draw()
    

    



            
        
