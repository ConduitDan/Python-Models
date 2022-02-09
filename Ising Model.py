
import numpy as np
from matplotlib import pyplot as plt

#TODO update to run with the animator
class Ising:
    '''This is a 2d lattice ising model, it will probably inherent from
 a generic lattice model. It's a model for magnetism'''


    def __init__(self, nx = 10, ny = 10, H = 0, T = 0, J = 1, IC=1):
    
        self.nx = nx # Size in the X-direction
        self.ny = ny # Size in the Y-direction
        self.H = H   # External Magnetic Field
        self.T = T   # Temperature
        self.J = J   # Interaction strength


        # IC = 0 all -1s
        # IC = 1 all ones
        # IC in (0,1) weighted random
        if IC == 1:
            self.lattice = np.ones((self.ny,self.nx))
        elif IC == 0:
            self.lattice = -np.ones((self.ny,self.nx))
        else:
            self.lattice = (np.random.rand(self.ny,self.nx)>IC)*2-1

    def step(self,i,j):
        '''Given a latice site use the Metropolis–Hastings algorithm to update'''
        
        
        E = self.lattice[i,j]*self.H # Energy
        ilook = [0,0,-1,1]
        jlook = [-1,1,0,0]
        for ii in range(4): # look left and right
            neighbori = (i +ilook[ii]) % self.ny
            neighborj = (j + jlook[ii]) % self.nx
            E -= self.J*self.lattice[i,j]*self.lattice[neighbori,neighborj]

        if E>0 or np.random.rand()<np.exp(E/(self.T+1e-16)): # accept or reject the move
            self.lattice[i,j] = -1*self.lattice[i,j]

    def update(self): 
        ''' Pick a random site and update'''
        j = np.random.randint(self.nx)
        i = np.random.randint(self.ny)
        self.step(i,j)
    
    def MCstep(self,numMCSteps = None):
        ''' For the number of MonteCarlo steps update a number of random 
        sites equal to the number of total latice sites'''
        
        if numMCSteps is None: # we haven't been told howmany to do, figure it out
            Tc = 2/np.log(1+np.sqrt(2))
            numMCSteps = np.log(1-abs(self.T/Tc)+1e-16)
            numMCSteps = min([numMCSteps,1e6]) #max out at 10000 steps
        Nstep = self.nx*self.ny
        for nn in range(numMCSteps):
            for n in range(Nstep):
                self.update()
                
        return self.lattice

    def annel(self):
        '''Create an anneling scheme still in progress'''
        Tc = 2*self.J/np.log(1+np.sqrt(2))
        for T in range(5,0):
            NMCsteps = np.log(T-Tc)
            
    def m(self):
        aveM = 0
        
        nsamples = 20
        for k in range(nsamples):
            m = 0
            for i in range(self.nx):
                for j in range(self.ny):
                    m += self.lattice[i,j]/(self.nx*self.ny)
            aveM+=abs(m)/nsamples
            self.MCstep(5)
        return aveM
    def msusceptibility(self):
        aveSus = 0 
        nsamples = 20
        startLattice = self.lattice
        for k in range(nsamples):
            self.lattice = startLattice
            mstart = self.m()
            dh = 0.1
            oldH = self.H
            self.H+=dh
            self.MCstep(200)
            self.H= oldH
            mend = self.m()
            aveSus +=(mend-mstart)/dh/nsamples
        return aveSus
    
        
        
        






class IsingExperiment:
    def __init__(self):
        pass
    
    def tempGrad(self,Tgrad,measurment):
        Tc = 2/np.log(1+np.sqrt(2))
        quantity=[];
        i =0
        nsample = 5
        for myT in Tgrad:
            q =0 
            i +=1;
            for i in range(nsample):
                myModel = Ising(T=myT)  
                myModel.MCstep(200)
                q += measurment(myModel)/nsample
        quantity.append()
        print(str(i*2)+"% done")
        return quantity
            
        
        
    def magGrad(self,Hgrad,myT,measurement):
        Tc = 2/np.log(1+np.sqrt(2))
        quantity=[];
        i =0
        myModel = Ising(T=myT,H=0)

        for myH in Hgrad:
            myModel.H=myH
            i +=1;
            myModel.MCstep(200)
            quantity.append(measurement(myModel))
            print(str(i*2)+"% done")


        
    def phaseTransitionGraph(self):
        Tgrad = np.linspace(5,0)
        m = self.tempGrad(Tgrad,Ising.m)
        plt.plot(Tgrad,m)
    
    def susceptibility(self):
        Tgrad = np.linspace(5,0)
        chi = self.tempGrad(Tgrad,Ising.msusceptibility)
        plt.plot(Tgrad,chi)
    
    def hysterisis(self):
        Hgrad = np.linspace(-1,1)
        m = self.magGrad(Hgrad,2,Ising.m)
        plt.plot(Hgrad,m)

            

            
        
        
        


if __name__ == '__main__':
        #fig, ax = plt.subplots(1,1)
        #fig.tight_layout()
        myExp = IsingExperiment()
        #myExp.phaseTransitionGraph()
        myExp.susceptibility()

            
            
    
                
                
        
        
        
