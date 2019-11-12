from math import sin,pi
import time
from observer import *

## from pylab import linspace,sin

import sys
if sys.version_info.major == 2:
    print(sys.version)
    from Tkinter import Tk,Canvas
    import tkFileDialog as filedialog
else:
    print(sys.version)
    from tkinter import Tk,Canvas
    from tkinter import filedialog



class FreqModel(Subject):
    def __init(self,name="signal"):
        Subject.__init__(self)
        self.name = name
        self.signal = []
        self.a,self.f,self.p=1.0,2.0,0.0

    def vibration(self,t,harmoniques=1,impair=True):
        a,f,p=self.a,self.f,self.p
        somme=0
        for h in range(1,harmoniques+1) :
            somme=somme + (a/h)*sin(2*pi*(f*h)*t-p)
        return somme
    
    def generate_signal(self,period=2.0,samples=100):
        print("Dict : ",self.__dict__)
        del self.signal[0:]
        echantillons=range(int(samples)+1)
        Tech = period/samples
        print("Tech",Tech,period,samples)
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        print("Longueur du signal : ",len(self.signal))
        return self.signal
