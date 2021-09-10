"""
This class draws iterated function systems
"""
import numpy as np
from matplotlib import pyplot as plt


class IFSGenerator:
    def __init__(self, IFS=None, depth=10, numPoints = None, overwrite=False):
        if IFS is None:
            raise "Please supply an IFS"
        self.IFS = IFS
        self.fileName = "fractals/" + IFS.name() + str(depth)

        self.overwrite = overwrite
        self.File = None
        self.functionList = self.IFS.getFunctionList()
        self.numOfFunctions = len(self.functionList)
        
        
        if numPoints is None:
            self.depth = depth    
            self.numPoints = (self.numOfFunctions**(self.depth))
            
        else:
            self.numPoints = int(numPoints)
            self.depth = int(np.ceil(np.log(self.numPoints)/np.log(self.numOfFunctions)))
        
            
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
                #currentMaxDepth = int(np.ceil(np.log(self.numPoints+1)/np.log(self.numOfFunctions)))-1
                for j in range(self.depth):
                    # go through self.depth operations
                    #funIndex = int(i/(self.numOfFunctions**(j))) % self.numOfFunctions
                    
                    #Create the function index by
                    cumulitveP = 0
                    funIndex = 0
                    r = np.random.random()
                    for p in self.IFS.getProbablities():
                            cumulitveP += p
                            if r > cumulitveP :
                                funIndex += 1 
                            else: 
                                break
                    
                    
                    
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
        
        ax.scatter(self.x,self.y,s = 1000/np.sqrt(self.numPoints), marker = ".",c = range(self.numPoints),cmap = 'hsv',edgecolors = None)
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
            print("%50 Done")
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

class IFSAbstract:
    def getColors(self):
        return self.colorArray
            
    def getFunctionList(self):
        return self.funArray
    def name(self):
        return self.myName
    def getProbablities(self):
        #by default use equal probablities
        return [1/len(self.funArray)]*len(self.funArray)

        

class IFSGoldenDragon(IFSAbstract):
    def __init__(self):
        
        self.myName = "GoldenDragon"
        
        phi = (1+np.sqrt(5))/2
        r = (1/phi)**(1/phi)
        theta = np.arccos((1+r**2 - r**4)/(2*r))
        theta2 = np.pi - np.arccos((1+r**4 - r**2)/(2*r**2))
        
        self.funArray = (afineTransfrom(theta, r),
                         afineTransfrom(theta2, r**2, np.array([[1.0],[0.0]])))
        self.colorArray = ((0,0,0),(162.0/255,101.0/255,223.0/255))

        
    
class IFSCustomDragon(IFSAbstract):
    def __init__(self,theta = np.pi/5):
        
        self.myName = "CustomDragon"
        
        theta1 = theta
        theta2 = np.pi - theta1

        scale1 = 0.5/np.cos(theta1)
        scale2 = 0.5/np.cos(theta1)
        self.funArray = (afineTransfrom(theta = theta1, scale = scale1),
                         afineTransfrom(theta = theta2, scale = scale2, translation=np.array([[1.0],[0.0]])))
        self.colorArray = ((0,0,0),(162.0/255,101.0/255,223.0/255))
        

class IFSFern(IFSAbstract):
    def __init__(self):
        self.myName = "Fern"
        f1 = afineTransfrom(R = np.array([[0,0],[0,0.16]]),translation = np.array([[0.0],[0.0]]))
        f2 = afineTransfrom(R = np.array([[.85,0.04],[-0.04,0.85]]),translation = np.array([[0.0],[1.60]]))
        f3 = afineTransfrom(R = np.array([[.2,-0.26],[0.23,0.22]]),translation = np.array([[0.0],[1.60]]))
        f4 = afineTransfrom(R = np.array([[-.15,.28],[.26,0.24]]),translation = np.array([[0.0],[0.44]]))
        self.funArray = (f1,f2,f3,f4)
        self.colorArray = ((0,128/255,0),(0,64/255,0),(0,128/255,0),(0,128/255,0))
        self.p = (.01,.85,.07,.07)
    def getProbablities(self):
        return self.p
    

class afineTransfrom:
    def __init__(self,theta = None, R = None,scale = 1,translation = np.array([[0.0],[0.0]])):
        if R is None:
            self.R = np.array([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]]) * scale
        else:
            self.R = R
            
        self.t = translation


    def __call__(self,x,y):
        v = np.array([[x],[y]])
        v = np.matmul(self.R,v) + self.t
        return (v[0][0],v[1][0])

    




if __name__ == '__main__':
    #anIFS = IFSGoldenDragon()
    anIFS = IFSCustomDragon(theta =2* np.pi/3-.2)
    #anIFS = IFSFern()
    myDrawBot = IFSGenerator(IFS = anIFS,depth = 21,overwrite = False)
    myDrawBot.draw()
    

    



            
        
