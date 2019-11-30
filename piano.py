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
    from tkinter import messagebox
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
        self.octaves=5
        self.generatorTopLevel = None


        self.frameGenerator = tk.LabelFrame(self.parent,labelanchor='n',text="Generateur de notes",height=100,width=100)
        self.framePiano = tk.LabelFrame(self.parent,labelanchor='n',text="Piano",height=100,width=100)
        self.frameVisualizer = tk.Frame(self.parent,height=100,width=100)

        # self.frameParameter = tk.LabelFrame(self.frameGeneration,labelanchor='n',text="Parametres",padx=15,pady=10)




        # FrequenciesVisualizer
        self.visualizerModel = FreqModel()
        self.visualizerView = FreqView(self.frameVisualizer,width=1200)
        self.visualizerView.grid(8)
        self.visualizerView.packing()
        self.visualizerModel.attach(self.visualizerView)


        # Piano
        self.piano = PianoView(self.framePiano,self.octaves,self.visualizerModel)


        # SoundGenerator
        self.soundGeneratorModel = SoundGeneratorModel(self.piano)
        self.soundGeneratorView = SoundGeneratorView(self.frameGenerator,self.soundGeneratorModel)
        self.soundGeneratorController=SoundGeneratorController(self.soundGeneratorView.topFrame,self.soundGeneratorModel,self.soundGeneratorView)
        self.soundGeneratorView.packing(mainFrame=True)
        self.soundGeneratorController.packing()
        self.soundGeneratorModel.attach(self.soundGeneratorView)

        self.createMenuBar()


    def createMenuBar(self):
        self.menubar = tk.Menu(root)
        filemenu = tk.Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open SoundGenerator alone", command=self.startGenerator)
        filemenu.add_command(label="Open SoundVisualizer alone", command=self.startVisualizer)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.dispExitPrev)
        self.menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="Developer", command=self.dispCredential)
        helpmenu.add_command(label="Read Me", command=self.dispReadMe)
        self.menubar.add_cascade(label="About", menu=helpmenu)


    def dispCredential(self):
        messagebox.showinfo("Developer","Developed by Quentin  Philipp")

    def dispExitPrev(self):
        answer = messagebox.askyesno("Leave ?", "Voulez vous vraiment quitter ?", icon='warning')
        print("exit :",answer)
        if answer==True :
            root.quit()
    
    def dispReadMe(self):
        print("Test ReadMe")
        f= open("README.txt","r")
        content = f.read()
        messagebox.showinfo("ReadMe",content)
        f.close()


    def startGenerator(self):
        if self.generatorTopLevel==None:
            self.generatorTopLevel = tk.Toplevel()      #frame
            self.generatorTopLevel.minsize(1170, 420)
            
            self.soundGeneratorViewTopLevel = SoundGeneratorView(self.generatorTopLevel,self.soundGeneratorModel)
            self.soundGeneratorControllerTopLevel=SoundGeneratorController(self.soundGeneratorViewTopLevel.topFrame,self.soundGeneratorModel,self.soundGeneratorViewTopLevel)
            self.soundGeneratorViewTopLevel.packing(mainFrame=True)
            self.soundGeneratorControllerTopLevel.packing()
            self.soundGeneratorModel.attach(self.soundGeneratorViewTopLevel)
        else :
            messagebox.showinfo("Impossible","Le générateur de sons est déjà lancé")

    def startVisualizer(self):
        self.visualizerTopLevel = tk.Toplevel()     #frame
        self.visualizerTopLevel.minsize(280,650)

        self.visualizerModelTopLevel = FreqModel()
        self.visualizerViewTopLevel = FreqView(self.visualizerTopLevel)
        self.visualizerViewTopLevel.grid(8)
        self.visualizerViewTopLevel.packing()
        self.visualizerModelTopLevel.generate_signal()
        self.visualizerModelTopLevel.attach(self.visualizerViewTopLevel)
        self.visualizerControlerTopLevel = FreqController(self.visualizerTopLevel,self.visualizerModelTopLevel,self.visualizerViewTopLevel)
        self.visualizerControlerTopLevel.packing()
        self.visualizerViewTopLevel.update(self.visualizerModelTopLevel)

    def packing(self):
        #Frames
        root.config(menu=self.menubar)
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

