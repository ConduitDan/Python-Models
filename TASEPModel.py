import random
import statistics
import numpy as np

from matplotlib import pyplot as plt

class TASEPModel:
    def __init__(self,N=100,alpha = 0.5,beta = 0.5,obs = None):
        self.lattice = [False]*N
        self.N = N
        self.alpha = alpha
        self.beta = beta
        self.count = 0
        self.obs = obs
    def setObs(self,obs):
        self.obs = obs
    def update(self):
        siteNo = random.randrange(0,self.N)
        self.updateSite(siteNo)
    def MCstep(self,numSteps):
        for i in range(numSteps):
            for j in range(self.N):
                self.update()
            if self.obs is not None:
                self.obs.takeMeasurement(self)            


    def updateSite(self,siteNo):
        # take care of inital and final first 
        if siteNo == 0:
            # first lattice site
            if not self.lattice[siteNo]:
                #if its empty fill it with probability alpha
                if random.random()<self.alpha:
                    self.lattice[siteNo] = True
                    self.count+=1
                return #if it was empty don't try and move it forward 
        if siteNo == self.N-1:
            #last lattice site
            if self.lattice[siteNo]:
                # if its occupied empty it with probablity beta
                if random.random()<self.beta:
                    self.lattice[siteNo] = False
                    self.count-=1
            return #never try and move the final site forward

        self.attemptMove(siteNo)

    def attemptMove(self,siteNo):
        # if the current site is full and the next site is empty, move it
        if self.lattice[siteNo] and not self.lattice[siteNo+1]:
            self.lattice[siteNo] = False
            self.lattice[siteNo+1] = True
    def density(self):
        return self.count/self.N
    def print(self):
        for site in self.lattice:
            if site:
                print("x",end='')
            else:
                print("_",end='')
        print("\n")

class TASEPModelObs:
    def __init__(self,fileName= None,SScheck = 100):
        self.file = None
        if fileName is not None:
            self.file = open(fileName)
        # keep track of 100 densites
        self.SScheck = SScheck
        self.den = [0.0]*SScheck
        self.place = 0
    def __del__(self):
        if self.file is not None:
            self.file.write(self.density())
            self.file.close()
    def takeMeasurement(self,TASEP):
        self.den[self.place%self.SScheck] = TASEP.density()
        self.place+=1
    def checkSS(self,tol):
        # calculate if the mean of the direive of the density is below the tol
        meanDir = 0
        for i in range(self.SScheck-1):
            meanDir += (self.den[i+1] - self.den[i])/(self.SScheck-1)
        return meanDir<tol
    def density(self):
        return statistics.mean(self.den)


class TASEPExperiment:
    def phaseDiagram(self):
        alpharange = np.linspace(0,1,50)
        betarange = np.linspace(0,1,50)
        density = np.zeros((len(alpharange),len(betarange)))
        max = len(alpharange)*len(betarange)
        for i in range(len(alpharange)):
            for j in range(len(betarange)):
                myModel = TASEPModel(N=1000,alpha=alpharange[i],beta=betarange[j])
                density[i,j] = self.runModel(myModel)
                # print("at alpha = %f and beta = %f density was %f"%(alpharange[i],betarange[j],density[i,j]))
            print("%d of %d done"%(i,len(alpharange)))
        fig,ax = plt.subplots()
        im = plt.imshow(density, extent=[0,1,0,1])
        fig.colorbar(im,ax=ax)
        file = open("densityData.txt",'w')
        file.write(str(density))
        file.close
        plt.savefig("densityMap.png",)

    def runModel(self,myModel):
        #run some equilibration first
        myModel.MCstep(1000)
        myObs = TASEPModelObs()
        myModel.setObs(myObs)
        myModel.MCstep(100)
        counter = 0
        while not myObs.checkSS(1e-6):

            myModel.MCstep(100)
            counter+=1
            if counter > 100:
                raise Exception("Couldn't reach steady state")

        return myObs.density()
    def test(self):
        myModel = TASEPModel(alpha=1,beta=0)
        print(self.runModel(myModel))





# for steady state check if the mean of the diriviet is below sqrt(N)?
if __name__ == "__main__":
    myEXP = TASEPExperiment()
    myEXP.phaseDiagram()
    # myEXP.test()



    # print(myModel.density())
    # myModel.print()







        

        
                

