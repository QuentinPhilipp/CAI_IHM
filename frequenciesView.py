from math import sin,pi
import time

from frequenciesController import *
from frequenciesModel import *
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
        self.canvas=tk.Canvas(parent,bg=bg,width=width,height=height)
        self.units=1
        self.signals={}
        self.width,self.height=width,height
        self.canvas.bind("<Configure>",self.resize)
        

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
    


if  __name__ == "__main__" :
    root=tk.Tk()
    root.title("Vue Frequencies")
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
