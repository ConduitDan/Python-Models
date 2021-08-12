
import numpy as np
from matplotlib import pyplot as plt

#TODO update to run with the animator
class Ising:
    '''This is a 2d lattice ising model, it will probably inherent from
 a generic lattice model. It's a model for magnetism'''


    def __init__(self, nx = 100, ny = 100, H = 0, T = 0, J = 1, IC=.5):
    
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
        for ii in range(-1,2): # look left and right
            for jj in range(-1,2): #look up and down
                neighbori = (i + ii) % self.ny
                neighborj = (j + jj) % self.nx
                E -= self.J*self.lattice[i,j]*self.lattice[neighbori,neighborj]
        E += self.J # take off the self energy (i=0,j=0)

        if E>0 or np.random.rand()>np.exp(self.T*E): # accept or reject the move
            self.lattice[i,j] = -1*self.lattice[i,j]

    def update(self): 
        ''' Pick a random site and update'''
        j = np.random.randint(self.nx)
        i = np.random.randint(self.ny)
        self.step(i,j)
    
    def MCstep(self,numMCSteps):
        ''' For the number of MonteCarlo steps update a number of random 
        sites equal to the number of total latice sites'''
        
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

if __name__ == '__main__':
        #fig, ax = plt.subplots(1,1)
        #fig.tight_layout()
        mag = Ising(T=0)
        plt.matshow(mag.MCstep(10))
        plt.colorbar()
        plt.show()


            
            
    
                
                
        
        
        
