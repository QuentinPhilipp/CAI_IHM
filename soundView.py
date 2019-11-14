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
        

        self.createStruct()
        self.createListBox()
        self.createSoundDurationSlider()
        self.createButton()
        self.createFolderAsking()
        self.createAccordList()
        self.createAccordButton()

    def resize(self,event):
        if event:
            print("resize | Height = ",event.height,"Width = ",event.width)
            self.width,self.height=event.width,event.height
            
    def packing(self) :
        self.titleLabelNote.grid(row=0,column=0,columnspan=4)
        self.titleLabelAccord.grid(row=0,column=4,columnspan=4)
        self.octaveLabel.grid(row=1,column=0,columnspan=2)
        self.octaveListBox.grid(row=2,column=0,columnspan=2)
        self.noteLabel.grid(row=1,column=2,columnspan=2)
        self.noteListBox.grid(row=2,column=2,columnspan=2)
        self.durationSlider.grid(row=3,columnspan=4)
        self.pathLabel.grid(row=4,columnspan=3)
        self.directoryButton.grid(row=4,column=3)
        self.confirmButton.grid(row=5,columnspan=4)
        self.accordLabel.grid(row=1,column=4,columnspan=2)
        self.accordList.grid(row=2,column=4,columnspan=2)
        self.accordLabelOctave.grid(row=1,column=6,columnspan=2)
        self.accordListOctave.grid(row=2,column=6,columnspan=2)
        self.accordWarning.grid(row=3,column=4,columnspan=4)
        self.accordButton.grid(row=4,column=5,columnspan=2)


    def createAccordList(self):
        self.accordLabelVar = tk.StringVar()
        self.accordLabelVar.set("Choisissez 3 notes")

        self.accordLabel= tk.Label(self.parent,text="Notes")
        self.accordList = tk.Listbox(self.parent,selectmode='multiple',exportselection=0)
        self.accordList.bind("<ButtonRelease-1>",self.checkAccordList)

        self.accordLabelOctave= tk.Label(self.parent,text="Octaves")
        self.accordListOctave = tk.Listbox(self.parent,exportselection=0)
        self.accordListOctave.bind("<ButtonRelease-1>",self.checkAccordList)

        for item in self.model.getNotes():
            self.accordList.insert(tk.END,item)

        for item in self.model.getOctave():
            self.accordListOctave.insert(tk.END,item)

        self.accordWarning=tk.Label(self.parent,textvariable=self.accordLabelVar)

    def checkAccordList(self,event):
        selectedNotes = self.accordList.curselection()
        if not selectedNotes :                  # if empty
            print("No notes selected")
            self.accordLabelVar.set("Choisissez 3 notes")
        else :
            print("Selected index : ",selectedNotes)
            if(len(selectedNotes)<3):
                txt="Choisissez "+str(3-len(selectedNotes))+" notes"
                self.accordButton["state"]="disable"
            elif(len(selectedNotes)==3):
                selectedOctave = self.accordListOctave.curselection()
                if not selectedOctave :
                    txt="Choisissez une octave"
                    self.accordButton["state"]="disable"
                else :
                    txt="Vous pouvez créer un accord"
                    self.accordButton["state"]="normal"
            elif(len(selectedNotes)>3):
                txt="Retirez "+str(len(selectedNotes)-3)+" notes" 
                self.accordButton["state"]="disable"           
            
            self.accordLabelVar.set(txt)

    
    def createAccordButton(self):
        self.accordButton = tk.Button(self.parent,text="Générer un accord",state='disable')
        self.accordButton.bind("<ButtonRelease-1>",self.generateSoundsChords)



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


    def createStruct(self):
        self.titleLabelNote = tk.Label(self.parent,text="Creation de note")
        self.titleLabelAccord = tk.Label(self.parent,text="Creation d'accord")


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
        self.model.generateNote(degree,name,duration*1000,folder=destinationFolder)

        self.noteListBox.select_clear(0,tk.END)
        self.octaveListBox.select_clear(0,tk.END)

    def generateSoundsChords(self,event):
        self.model.generateChords()
        self.accordList.select_clear(0,tk.END)
        self.accordListOctave.select_clear(0,tk.END)

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
