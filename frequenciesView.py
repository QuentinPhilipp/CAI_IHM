from math import sin,pi
import time

from frequenciesController import *
from frequenciesModel import *
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


class FreqView(Observer):
    def __init__(self,parent,bg="grey",width=600,height=300):
        Observer.__init__(self)
        self.canvas=Canvas(parent,bg=bg,width=width,height=height)
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
            self.grid()

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
            plot = [(x*w,h/2.0*(1-y)) for (x, y) in signal]
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
    root=Tk()
    root.title("Vue Frequencies")
    model=FreqModel()
    view=FreqView(root)
    view.grid(8)
    view.packing()
    model.attach(view)
    model.generate_signal()
    ctrl = FreqController(root,model,view)
    ctrl.packing()
    root.mainloop()
