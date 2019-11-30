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


class FreqView(Observer):
    def __init__(self,parent,bg="white",width=600,height=300):
        Observer.__init__(self)
        self.parent = parent
        self.canvas=tk.Canvas(self.parent,width=width,height=height)
        self.units=1
        self.signals={}
        self.width,self.height=width,height
        self.canvas.bind("<Configure>",self.resize)
        self.canvas.config(background="White")
        

    def resize(self,event):
        if event:
            print("resize | Height = ",event.height,"Width = ",event.width)
            self.width,self.height=event.width,event.height
            self.canvas.delete("grid")
            for name in self.signals.keys():
                self.canvas.delete(name)
                self.plot_signal(self.signals[name],name)
            self.grid(self.units)

    def packing(self) :
            self.canvas.pack(expand=1,fill="both",padx=6)


    def update(self,subject=None):
        print("View : update()")
        print(subject)
        if subject.get_name() not in self.signals.keys():
            self.signals[subject.get_name()]=subject.get_signal()
        else :
            self.canvas.delete(subject.get_name())
        

        self.plot_signal(subject.get_signal(),subject.get_name())



    def plot_signal(self, signal,name,color="blue"):
        w,h = self.width,self.height
        if signal and len(signal) >1:
            print("Plot signal")
            plot = [(x*w,h/2.0*(1-y/(self.units/2.0))) for (x, y) in signal]
            self.signal_id = self.canvas.create_line(plot,fill=color,smooth=1,width=2,tags=name)

        return self.signal_id


    def grid(self,steps=2):
        self.units=steps
        tile_x=self.width/steps
        for t in range(1,steps+1):
            x =t*tile_x
            self.canvas.create_line(x,0,x,self.height,tags="grid")
            self.canvas.create_line(x,self.height/2-10,x,self.height/2+10,width=3,tags="grid")
        tile_y=self.height/steps
        for t in range(1,steps+1):
            y =t*tile_y
            self.canvas.create_line(0,y,self.width,y,tags="grid")
            self.canvas.create_line(self.width/2-10,y,self.width/2+10,y,width=3,tags="grid")
    

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
        self.amp.set(1)
        self.harm.set(1)
        self.freq.set(100)
        self.dephas.set(0.0)

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


# class VisualizerView():
#     def __init__(self,parent,model):
#         self.model = model
#         self.parent = parent



if  __name__ == "__main__" :
    root=tk.Tk()
    root.title("Vue Frequencies")
    root.minsize(280,650)
    print('Create model')
    model=FreqModel("signalPiano")
    print("Model created")
    view=FreqView(root)
    view.grid(8)
    view.packing()
    model.generate_signal()
    model.attach(view)
    ctrl = FreqController(root,model,view)
    ctrl.packing()
    view.update(model)
    root.mainloop()
