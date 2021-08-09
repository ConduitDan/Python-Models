
import numpy as np
from matplotlib import pyplot as plt


class Ising:
    '''This is a 2d lattice ising model, it will probably inhairet from
    a generic lattice model. It's a model for magetisim'''


    def __init__(self, nx = 100, ny = 100, H = 0, T = 0, J = 1, IC=.5):
        self.nx = nx
        self.ny = ny
        self.H = H
        self.T = T
        self.J = 1


        # IC = 0 all -1s
        # IC = 1 all ones
        # IC in (0,1) weighted random intiation
        if IC == 1:
            self.lattice = np.ones((self.ny,self.nx))
        elif IC == 0:
            self.lattice = -np.ones((self.ny,self.nx))
        else:
            self.lattice = (np.random.rand(self.ny,self.nx)>IC)*2-1

    def step(self,i,j):
        E = 0
        for ii in range(-1,2):
            for jj in range(-1,2):
                neighbori = (i + ii) % self.ny
                neighborj = (j + jj) % self.nx
                E -= self.J*self.lattice[i,j]*self.lattice[neighbori,neighborj]+self.lattice[i,j]*self.H
        if E>0 or np.random.rand()>np.exp(self.T*E):
            self.lattice[i,j] = -1*self.lattice[i,j]

            
    def MCstep(self,numMCSteps):
        Nstep = self.nx*self.ny
        for nn in range(numMCSteps):
            for n in range(Nstep):
                j = np.random.randint(self.nx)
                i = np.random.randint(self.ny)
                self.step(i,j)
        return self.lattice

    def annel(self):
        Tc = 2*self.J/np.log(1+np.sqrt(2))
        for T in range(5,0):
            NMCsteps = log(T-Tc)

if __name__ == '__main__':
        #fig, ax = plt.subplots(1,1)
        #fig.tight_layout()
        mag = Ising(T=0)
        plt.matshow(mag.MCstep(10))
        plt.colorbar()
        plt.show()


            
            
    
                
                
        
        
        
