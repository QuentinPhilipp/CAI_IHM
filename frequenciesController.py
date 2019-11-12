from math import sin,pi
import time,observer

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



class FreqController():
    def __init__(self,parent,model,view):
        self.model = model
        self.view=view
        self.create_controls(parent)

    def create_controls(self,parent):
        self.frame = Tk.LabelFrame(parent,text="Signal")
        self.amp=Tk.IntVar()
        self.amp.set=1
        self.scaleA=Tk.Scale(self.frame,variable=self.amp,label="Amplitude",orient="horizontal",length=250,from_=0,to=5,tickinterval=1)

        self.scaleA.bind("<Button-1>",self.update_magnitude)

    def update_magnitude(self,event):
        self.model.set_magnitude(self.amp.get())
        self.model.generate_signal()


    def packing(self):
        self.frame.pack()