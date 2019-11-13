from observer import *
from soundModel import *

import sys
import os

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


class SoundGeneratorView(Observer):
    def __init__(self,parent,model,bg="white",width=600,height=300):
        Observer.__init__(self)
        self.parent = parent
        self.model = model
        self.width,self.height=width,height

        self.ready = False
        
        self.createListBox()
        self.createSoundDurationSlider()
        self.createButton()
        self.createFolderAsking()
        

    def resize(self,event):
        if event:
            print("resize | Height = ",event.height,"Width = ",event.width)
            self.width,self.height=event.width,event.height
            
    def packing(self) :
        self.octaveLabel.grid(row=0,column=0,columnspan=2)
        self.octaveListBox.grid(row=1,column=0,columnspan=2)
        self.noteLabel.grid(row=0,column=2,columnspan=2)
        self.noteListBox.grid(row=1,column=2,columnspan=2)
        self.durationSlider.grid(row=2,columnspan=4)
        self.confirmButton.grid(row=4,columnspan=4)
        self.pathLabel.grid(row=3,columnspan=3)
        self.directoryButton.grid(row=3,column=3)

    def createListBox(self):

        self.octaveLabel = tk.Label(self.parent,text="Octave")
        self.octaveListBox = tk.Listbox(self.parent,exportselection=0)
        self.octaveListBox.bind("<ButtonRelease-1>",self.checkButton)

        self.noteLabel = tk.Label(self.parent,text="Note")
        self.noteListBox = tk.Listbox(self.parent,exportselection=0)
        self.noteListBox.bind("<ButtonRelease-1>",self.checkButton)

        for item in self.model.getOctave():
            self.octaveListBox.insert(tk.END,item)

        for item in self.model.getNotes():
            self.noteListBox.insert(tk.END,item)

    def createSoundDurationSlider(self):
        self.duration = tk.DoubleVar()
        self.duration.set(0.5)
        self.durationSlider=tk.Scale(self.parent,variable=self.duration,label="Duration",orient="horizontal",resolution=0.1,length=250,from_=0.1,to=3.1,tickinterval=0.5)

    def createButton(self):
        self.buttonTxt = tk.StringVar()
        self.buttonTxt.set("Selectionnez une note et une octave")
        self.confirmButton = tk.Button(self.parent,textvariable=self.buttonTxt,state='disable')
        self.confirmButton.bind("<ButtonRelease-1>",self.generateSound)


    def generateSound(self,event):
        # destinationFolder = "GeneratedSounds/"
        destinationFolder = self.completePath
        degree = self.octaveListBox.get(self.octaveListBox.curselection())
        name = self.noteListBox.get(self.noteListBox.curselection())
        duration = self.duration.get()
        self.model.generate(degree,name,duration*1000,folder=destinationFolder)

    def updateButton(self):
        if(self.ready==True):
            self.confirmButton["state"]='normal'
            self.buttonTxt.set("Generer le son")
        else :
            self.confirmButton["state"]='disabled'
            self.buttonTxt.set("Selectionnez une note et une octave")

    def checkButton(self,event):
        noteSelectedIndex = self.noteListBox.curselection()
        octaveSelectedIndex = self.octaveListBox.curselection()
        okOctave = False
        okNote = False

        try :
            indexNote = int(noteSelectedIndex[0])
            okNote = True
        except:
            print('No note selected')

        try :
            indexOctave = int(octaveSelectedIndex[0])
            okOctave = True
        except:
            print('No octave selected')

        if(okOctave==True and okNote==True):
            self.ready = True
            print("Ready for generation")
            self.updateButton()

    def createFolderAsking(self):
        self.displayedPath = tk.StringVar()
        path = os.path.dirname(os.path.abspath(__file__))
        path += "/GeneratedSounds"
        self.completePath = path
        self.displayedPath.set(path[-26:])  #set the 26 last char
        self.pathLabel = tk.Label(self.parent,textvariable=self.displayedPath,bg="white",width=26)

        self.directoryButton = tk.Button(self.parent,text="Directory")
        self.directoryButton.bind("<ButtonRelease-1>",self.askDir)


    def askDir(self,event):
        path = filedialog.askdirectory()
        print(path)
        if not path:                    #if empty keep the last one
            path = self.completePath
            print("No path selected, keep the old one")
        self.completePath=path
        self.displayedPath.set(path[-26:])


if  __name__ == "__main__" :
    root=tk.Tk()
    root.title("Vue Creation Note")
    model=SoundGeneratorModel()
    view=SoundGeneratorView(root,model)
    view.packing()



    # model.attach(view)

    # view.update(model)
    root.mainloop()
