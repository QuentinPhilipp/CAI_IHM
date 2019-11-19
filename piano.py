# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
from frequenciesView import *
from soundView import *
from keyboard import *
import collections
from observer  import *
import subprocess

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

from tkinter import Tk,Frame,Button,Label

class MainView(Observer):
    def __init__(self,parent,width=1000,height=500):
        Observer.__init__(self)
        self.parent = parent
        self.parent.minsize(width, height)
        self.octaves=4


        self.frameGenerator = tk.LabelFrame(self.parent,labelanchor='n',text="Generateur de notes",height=100,width=100,bg="blue")
        self.framePiano = tk.LabelFrame(self.parent,labelanchor='n',text="Piano",height=100,width=100,bg="yellow")
        self.frameVisualizer = tk.Frame(self.parent,height=100,width=100,bg='red')

        # self.frameParameter = tk.LabelFrame(self.frameGeneration,labelanchor='n',text="Parametres",padx=15,pady=10)

        self.piano = PianoView(self.framePiano,self.octaves)



    def packing(self):
        #Frames
        self.frameGenerator.pack()
        self.framePiano.pack()
        self.frameVisualizer.pack()




        #Piano 
        self.piano.packing()

if __name__ == "__main__" :
    root = tk.Tk()
    root.title("Projet Piano")
    view = MainView(root,1400,700)
    view.packing()
    
    
    
    octaves=5
    # viewPiano = PianoView(root,octaves)
    # viewPiano.packing()

    # modelGenerator=SoundGeneratorModel()
    # viewGenerator=SoundGeneratorView(root,modelGenerator)
    # viewGenerator.packing()
    # modelGenerator.attach(viewGenerator)

    # ctrl=SoundGeneratorController(viewGenerator.topFrame,modelGenerator,viewGenerator)
    # ctrl.packing()


    root.mainloop()

