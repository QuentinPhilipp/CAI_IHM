from math import sin,pi
import time,observer

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




class FreqController():
    def __init__(self,parent,model,view):
        print("Initializing Controller")
        self.model = model
        self.view=view
        self.create_controls(parent)

    def create_controls(self,parent):
        print("Creating control")
        self.frame = tk.LabelFrame(parent,text="Signal")
        self.amp = tk.IntVar()
        self.harm = tk.IntVar()
        self.freq = tk.IntVar()
        self.dephas = tk.DoubleVar()
        self.amp.set=1
        self.harm.set=1
        self.freq.set=100
        self.dephas.set=0.0

        self.scaleA=tk.Scale(self.frame,variable=self.amp,label="Amplitude",orient="horizontal",length=250,from_=0,to=5,tickinterval=1)
        self.scaleA.bind("<ButtonRelease-1>",self.update_magnitude)
        self.scaleA.pack()
        
        self.scaleB=tk.Scale(self.frame,variable=self.freq,label="Frequency",orient="horizontal",resolution=10,length=250,from_=0,to=5000,tickinterval=1000)
        self.scaleB.bind("<ButtonRelease-1>",self.update_frequency)
        self.scaleB.pack()

        self.scaleC=tk.Scale(self.frame,variable=self.dephas,label="Dephasage",resolution=0.5,orient="horizontal",length=250,from_=0,to=5,tickinterval=1)
        self.scaleC.bind("<ButtonRelease-1>",self.update_dephasage)
        self.scaleC.pack()

        self.scaleD=tk.Scale(self.frame,variable=self.harm,label="Harmoniques",resolution=1,orient="horizontal",length=250,from_=0,to=6,tickinterval=1)
        self.scaleD.bind("<ButtonRelease-1>",self.update_harmonic)
        self.scaleD.pack()


    def update_magnitude(self,event):
        self.model.setMagnitude(self.amp.get())
        self.model.generate_signal()
        
    def update_frequency(self,event):
        self.model.setFrequency(self.freq.get())
        self.model.generate_signal()

    def update_dephasage(self,event):
        self.model.setDephasage(self.dephas.get())
        self.model.generate_signal()

    def update_harmonic(self,event):
        self.model.setHarmonic(self.harm.get())
        self.model.generate_signal()


    def packing(self):
        self.frame.pack()