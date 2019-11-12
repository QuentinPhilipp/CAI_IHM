from math import sin,pi
import time
from observer import *

## from pylab import linspace,sin

import sys
if sys.version_info.major == 2 and sys.version_info.minor == 7 :
    print(sys.version)
    import Tkinter as tk
    import tkFileDialog as filedialog
elif sys.version_info.major == 3 and sys.version_info.minor == 6 :
    print(sys.version)
    import tkinter as tk
    from tkinter import filedialog
else :
    print("Your python version is : ")
    print(sys.version_info.major,sys.version_info.minor)
    print("... I guess it will work !")




class FreqModel(Subject):
    def __init__(self,name="signal"):
        Subject.__init__(self)
        self.name = name
        self.signal = []
        self.a,self.f,self.p=1.0,2.0,0.0
        self.h=1

    def vibration(self,t,harmoniques=1,impair=True):
        a,f,p=self.a,self.f,self.p
        somme=0
        if(self.h!=1):
            print("Harmoniques")
            harmoniques=self.h
        for h in range(1,harmoniques+1) :
            somme=somme + (a/h)*sin(2*pi*(f*h)*t-p)
        return somme
    
    def generate_signal(self,period=2.0,samples=10000):
        print(self.name)
        del self.signal[0:]
        echantillons=range(int(samples)+1)
        Tech = period/samples
        print("Amplitude :",self.a)
        print("Frequency :",self.f)
        print("Dephasage :",self.p)
        print("Harmoniques :",self.h)
        for t in echantillons :
            self.signal.append([t*Tech,self.vibration(t*Tech)])
        self.notify()
        return self.signal

    def get_name(self):
        return self.name
    
    def get_signal(self):
        return self.signal

    def setMagnitude(self,magnitude):
        print("Change magnitude to ",magnitude)
        self.a = magnitude

    def setFrequency(self,frequency):
        print("Change frequency to ",frequency)
        self.f = frequency/100.0

    def setDephasage(self,dephasage):
        print("Change dephasage to ",dephasage)
        self.p = dephasage

    def setHarmonic(self,harmonic):
        print("Change harmonic to ",harmonic)
        self.h = harmonic