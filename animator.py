#import ffmpeg
import matplotlib
from VicsekModel import Vicsek
from VicsekModel import VicsekSpins
from matplotlib import pyplot as plt
from matplotlib import patches as patches
from matplotlib.animation import FuncAnimation
from matplotlib.animation import FFMpegWriter
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib import gridspec
from itertools import chain
plt.style.use('seaborn-pastel')
matplotlib.rcParams['animation.ffmpeg_path'] = r'C:\ffmpeg\bin\ffmpeg.exe'

class ModelAnimator:
    '''This runs a physical model and animates it. You pass it an array
    of models it decieds how to format it. Creates subplots and passes
    the artist handles to the models and then creates its main animation
    fuction that calles next of each of the generators on of the run()
    function of the models'''


    def __init__(self, modelArray = [[Vicsek()]], filename = 'test'):
            
        self.modelArray = modelArray
        self.numPlotsY = len(modelArray)
        self.numPlotsX = max(len(elem) for elem in modelArray)


        nrow = self.numPlotsY
        ncol = self.numPlotsX

        self.fig = plt.figure(figsize=(ncol+1, nrow+1)) 
        self.fig.set_size_inches(15, 15)
        myGridSpec = gridspec.GridSpec(nrow, ncol,
                               wspace=0.0, hspace=0.0, 
                               top=1.-0.5/(nrow+1), bottom=0.5/(nrow+1),
                               left=0.5/(ncol+1), right=1-0.5/(ncol+1)) 
        
        self.ax = []
        for i in range(nrow):
            axrow = []
            for j in range(ncol):
                axrow.append(plt.subplot(myGridSpec[i,j]))
            self.ax.append(axrow)
        

        self.maxSteps = 0 
        for i in range(self.numPlotsY):
            for j in range(self.numPlotsX):
                modelArray[i][j].assignAxis(self.ax[i][j])
                self.maxSteps = max(self.maxSteps,modelArray[i][j].NTimeSteps())
            

        
        #self.fig.tight_layout()
        self.filename = filename

    def animationFunction(self):
        while not self.isDone(): #run every model untill its done
            #clear the axies
            for ax in list(chain.from_iterable(self.ax)):
                ax.cla() 
            for i in range(self.numPlotsY):
                for j in range(self.numPlotsX):
                    try:
                        next(self.modelArray[i][j].run())
                    except StopIteration:
                        pass
                    self.modelArray[i][j].plot()
            self.fig.suptitle('T = ' +'{:.2f}'.format(self.modelArray[0][0].t))
            yield
     
        
    def isDone(self):
        done = True
        for row in self.modelArray:
            for model in row:
                if not model.isDone():
                    done = False
                    return done

        return done
 

    def manageAxes(self,obj):
        
        axlist =list(chain.from_iterable(self.ax))
        return axlist
    
    def animateAndSave(self):
        anim = FuncAnimation(self.fig,self.manageAxes, frames = self.animationFunction,blit=False,
                             repeat = False, cache_frame_data = False,save_count = self.maxSteps)

       # anim = FuncAnimation(self.fig, self.createAnimation,
        #                     frames=self.model.run,blit=True,
         #                    save_count = self.model.nSteps-1,
          #                   repeat = False, cache_frame_data = False)
        #anim.save(self.filename, fps=30, extra_args=['-vcodec', 'libx264'])
        anim.save(self.filename,fps = 30)
        plt.show()

        
if __name__ == '__main__':
    modelToRun = [[]]
    den = [10,20,30,40]
    noise = [.01, .05, .1, .5]
    modelToRun = [[Vicsek(rho =denVal,maxT = 2, Dr =NVal, R=.1) for denVal in den] for NVal in noise]
            #modelToRun = [[Vicsek(rho =10,maxT = 1, Dr =0.01, R=.01)]]
    #print(type(modelToRun.plot()))
                    
    flyingSpins = ModelAnimator(modelArray = modelToRun,filename = 'testArray.gif' )
    flyingSpins.animateAndSave()


