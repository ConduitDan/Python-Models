
import numpy as np

class neigborgrid:
    '''This class implements a neighborlist to faciliate the fast
    finding of nearby partilces. This implementation is for a 2D
    neighbor grid'''

    def __init__(self, xLim = (0,1), yLim = (0,1), R = 0.1, periodic = (1,1)):
        #set the bounding box for the simulation
        self.xLim = xLim
        self.yLim = yLim

        #set which dimentions are periodic
        self.periodic = periodic

        #set the interaction range
        self.R = R
        
        #break up the space of the simulation into a grid were the size
        #of each box is at least R/2 then we will only need to check the
        #9 boxes around each particle

        self.numX = np.floor((self.xLim[1]-self.xLim[0]) / (R/2))
        self.numY = np.floor((self.yLim[1]-self.yLim[0]) / (R/2))

        self.xBoxSize = (self.xLim[1]-self.xLim[0])/self.numX
        self.yBoxSize = (self.yLim[1]-self.yLim[0])/self.numY

        self.map = {}

    def update(self,particles):
        '''The update function takes in a list of particles (objects with an x and y) and will
        create a map from box number and from particle'''
        self.map.clear()
        for atom in particles:
            self.addItemToMap(self.convertPosToIndex(atom),atom)
            


    def convertPosToIndex(self,atom):
		# to do add assertions for x and y being fields
        x = atom.x
        y = atom.y
        if x<self.xLim[0] or x>self.xLim[1]:
            raise ValueError()
        if y<self.yLim[0] or y>self.yLim[1]:
            raise ValueError()
        xind = int(np.floor(x/self.xBoxSize))
        yind = int(np.floor(y/self.yBoxSize))
        return (xind, yind)



    def addItemToMap(self,key,value):
        if key in self.map:
            self.map[key].append(value)
        else:
            self.map[key] = [value]

    def getNeighborhood(self,atom):
        '''find the box that the atom is in, look in the 5x5 area around
        it and retun all that are within the interaction radius'''
        centerBox = self.convertPosToIndex(atom)  
        for box in self.AdjacentBoxes(centerBox):
            if box in self.map:
                if isinstance(self.map[box], list):
                   for atom_j in self.map[box]:
                       if atom-atom_j < self.R:
                           yield atom_j
               
       

    def AdjacentBoxes(self,centerBox):
        for i in range(-2,3):
            for j in range(-2,3):
                nextX  = (centerBox[0]+i) % self.numX
                nextY  = (centerBox[1]+j) % self.numY
                yield (nextX,nextY)
                
        
        
    
        
            


            

    
        
    
    
