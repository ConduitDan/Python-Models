"""
This class draws iterated function systems
"""
import numpy as np
from matplotlib import pyplot as plt


class IFSGenerator:
    def __init__(self, IFS=None, depth=10, overwrite=False):
        if IFS is None:
            raise "Please supply an IFS"
        self.IFS = IFS
        self.fileName = "fractals/" + IFS.name() + str(depth)

        self.overwrite = overwrite
        self.depth = depth
        self.File = None
        self.functionList = self.IFS.getFunctionList()
        self.numOfFunctions = len(self.functionList)
        self.numPoints = (self.numOfFunctions**(self.depth))
        self.x = [0.0]*self.numPoints
        self.y = [0.0]*self.numPoints
        self.color = [[0,0,0]]*self.numPoints

    def canReadFromFile(self):
        readable = False
        if not self.overwrite:
            try:
                self.File = open(self.fileName+".out", "r")
                readable = True
                self.File.close()
            except:
                FileNotFoundError
        return readable
    
    def readPointsFromFile(self):
        self.File = open(self.fileName+".out","r")
        xline = self.File.readline().split(',')
        yline = self.File.readline().split(',')
        xline.pop() #remove /n
        yline.pop() #remove /n
        x = list(float(element) for element in xline)
        y = list(float(element) for element in yline) 

        self.File.close()
        return (x,y)

                
                
    def generatePoints(self):
        if self.canReadFromFile():
            (self.x,self.y) = self.readPointsFromFile()
        else:
            fractionDone = .1
            numColors = 4
            for i in range(self.numPoints):
                #for each possible combination 
                xi = 0.0
                yi = 0.0
                colorsi = [0,0,0]
                for j in range(self.depth):
                    # go through self.depth operations
                    funIndex = int(i/(self.numOfFunctions**(j))) % self.numOfFunctions
                    (xi,yi) = self.functionList[funIndex](xi,yi)
#                    colorsi = [a + b/self.depth for a,b in zip(colorsi, self.IFS.getColors()[funIndex])]
                self.x[i] = xi
                self.y[i] = yi
                colorProportion = int(numColors*(i/self.numPoints))/numColors
                self.color[i] =  [a*colorProportion + b*(1.0-colorProportion) for a,b in zip(self.IFS.getColors()[0], self.IFS.getColors()[1])]
                    
                    
                if i/self.numPoints > fractionDone:
                    print("%"+str(int(fractionDone*100)) + " Done")
                    fractionDone = fractionDone+.1
            print('%100 Done')
            
    def plotFractal(self):
        fig = plt.figure()
        fig.patch.set_alpha(1)
        fig.set_size_inches(30,20)
        ax = fig.add_subplot(1,1,1)
        
        ax.scatter(self.x,self.y,s = 10000/np.sqrt(self.numPoints), marker = ".",c = self.color,edgecolors = None)
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
        print("Generatating Points ...")
        self.generatePoints()
        print("Points Generated")
        print("Saving ...")
        self.saveData()
        print("Plotting ...")
        self.plotFractal()

class IFSGoldenDragon:
    def __init__(self):
        phi = (1+np.sqrt(5))/2
        r = (1/phi)**(1/phi)
        theta = np.arccos((1+r**2 - r**4)/(2*r))
        theta2 = np.pi - np.arccos((1+r**4 - r**2)/(2*r**2))
        
        self.funArray = (afineTransfrom(theta, r),
                         afineTransfrom(theta2, r**2, np.array([[1.0],[0.0]])))
                         
    def getFunctionList(self):
        return self.funArray
    
    def name(self):
        return "GoldenDragon"
    
    
class IFSCustomDragon:
    def __init__(self):
        theta1 = 1*np.pi/5
        theta2 = np.pi - theta1

        scale1 = 0.5/np.cos(theta1)
        scale2 = 0.5/np.cos(theta1)
        self.funArray = (afineTransfrom(theta1, scale1),
                         afineTransfrom(theta2, scale2, np.array([[1.0],[0.0]])))
        self.colorArray = ((0,0,0),(162.0/255,101.0/255,223.0/255))

    def getFunctionList(self):
        return self.funArray
    def getColors(self):
        return self.colorArray
        
    def name(self):
        return "CustomDragon"





class afineTransfrom:
    def __init__(self,theta,scale,translation = np.array([[0.0],[0.0]])):
        self.R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]]) * scale
        self.t = translation
    def __call__(self,x,y):
        v = np.array([[x],[y]])
        v = np.matmul(self.R,v) + self.t
        return (v[0][0],v[1][0])

    
        



if __name__ == '__main__':
    #anIFS = IFSGoldenDragon()
    anIFS = IFSCustomDragon()
    myDrawBot = IFSGenerator(IFS = anIFS,depth = 15,overwrite = True)
    myDrawBot.draw()
    

    



            
        
