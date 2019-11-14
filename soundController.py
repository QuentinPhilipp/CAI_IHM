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


class SoundGeneratorController(Observer):
    def __init__(self,parent,model,view,bg="white",width=715,height=390):
        Observer.__init__(self)
        self.parent = parent
        self.view = view
        self.model = model
        self.width,self.height=width,height
        self.parent.bind("<Configure>",self.resize)

        self.ready = False

        self.frameNote = tk.LabelFrame(self.parent,labelanchor='n',text="Creation de note")
        self.frameAccord = tk.LabelFrame(self.parent,labelanchor='n',text="Creation d'accord")
        self.frameGeneration = tk.Frame(self.parent,bd =3)
        self.frameParameter = tk.LabelFrame(self.frameGeneration,labelanchor='n',text="Parametres",padx=15,pady=10)


        self.createNoteList(self.frameNote)
        self.createAccordList(self.frameAccord)
        
        self.createSoundDurationSlider(self.frameParameter)
        self.createFolderAsking(self.frameParameter)
        
        self.createNoteButton(self.frameGeneration)
        self.createAccordButton(self.frameGeneration)

    def resize(self,event):
        if event:
            self.width,self.height=event.width,event.height
            # self.octaveListBox["width"]=int(0.2*self.width)
            # self.noteListBox["width"]=int(0.2*self.width)
            # self.accordList["width"]=int(0.2*self.width)
            # self.accordListOctave["width"]=int(0.2*self.width)

            
    def packing(self) :
        self.frameGeneration.grid(row=1,column=0,columnspan=2)
        self.frameNote.grid(row=0,column=0)
        self.frameAccord.grid(row=0,column=1)

    
        # Notes
        self.noteLabel.grid(row=0,column=0)
        self.noteListBox.grid(row=1,column=0)
        self.octaveLabel.grid(row=0,column=1)
        self.octaveListBox.grid(row=1,column=1)

        # Accords
        self.accordLabel.grid(row=0,column=0)
        self.accordList.grid(row=1,column=0)
        self.accordLabelOctave.grid(row=0,column=1)
        self.accordListOctave.grid(row=1,column=1)


        # Generation
        self.noteWarning.grid(row=0,column=0)
        self.noteButton.grid(row=1,column=0)
        self.frameParameter.grid(row=0,column=1,rowspan=2)
        self.accordWarning.grid(row=0,column=2)
        self.accordButton.grid(row=1,column=2)
        

        # Parameters
        self.durationSlider.pack(side=tk.TOP)
        self.pathLabel.pack(side=tk.LEFT)
        self.directoryButton.pack(side=tk.LEFT)

    def createNoteList(self,frame):
        self.octaveLabel = tk.Label(frame,text="Octave")
        self.octaveListBox = tk.Listbox(frame,exportselection=0)
        self.octaveListBox.bind("<ButtonRelease-1>",self.checkNoteList)

        self.noteLabel = tk.Label(frame,text="Note")
        self.noteListBox = tk.Listbox(frame,exportselection=0)
        self.noteListBox.bind("<ButtonRelease-1>",self.checkNoteList)

        for item in self.model.getOctave():
            self.octaveListBox.insert(tk.END,item)

        for item in self.model.getNotes():
            self.noteListBox.insert(tk.END,item)

    def createAccordList(self,frame):

        self.accordLabel= tk.Label(frame,text="Notes")
        self.accordList = tk.Listbox(frame,selectmode='multiple',exportselection=0)
        self.accordList.bind("<ButtonRelease-1>",self.checkAccordList)

        self.accordLabelOctave= tk.Label(frame,text="Octaves")
        self.accordListOctave = tk.Listbox(frame,exportselection=0)
        self.accordListOctave.bind("<ButtonRelease-1>",self.checkAccordList)

        for item in self.model.getNotes():
            self.accordList.insert(tk.END,item)

        for item in self.model.getOctave():
            self.accordListOctave.insert(tk.END,item)

    def createAccordButton(self,frame):
        self.accordLabelVar = tk.StringVar()
        self.accordLabelVar.set("Choisissez 3 notes")

        self.accordWarning=tk.Label(frame,textvariable=self.accordLabelVar,width=20,height=2)

        self.accordButton = tk.Button(frame,text="Générer un accord",state='disable',width=20,command=self.generateSoundsChords)

    def createNoteButton(self,frame):
        self.noteLabelVar = tk.StringVar()
        self.noteLabelVar.set("Selectionnez une note\n et une octave")

        self.noteWarning=tk.Label(frame,textvariable=self.noteLabelVar,width=20,height=2)

        self.noteButton = tk.Button(frame,text="Générer une note",state='disable',width=20,command=self.generateSound)

    def checkAccordList(self,event=None):
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
                    txt="Vous pouvez créer\nun accord"
                    self.accordButton["state"]="normal"
            elif(len(selectedNotes)>3):
                txt="Retirez "+str(len(selectedNotes)-3)+" notes" 
                self.accordButton["state"]="disable"           
            
            self.accordLabelVar.set(txt)

    def checkNoteList(self,event=None):
        selectedNote = self.noteListBox.curselection()
        selectedOctave = self.octaveListBox.curselection()
        okOctave = False
        okNote = False

        if not selectedNote :           #empty ?
            print("No note selected")
        else :
            okNote=True

        if not selectedOctave :
            print("No note selected")
        else :
            okOctave=True

        if(okNote and not okOctave):
            self.noteLabelVar.set("Selectionnez une octave")
            self.noteButton["state"]='disabled'
        elif(okOctave and not okNote):
            self.noteLabelVar.set("Selectionnez une note")
            self.noteButton["state"]='disabled'
        elif(okNote and okOctave):
            self.noteLabelVar.set("Vous pouvez créer\nune note")
            self.noteButton["state"]='normal'
        else:
            self.noteLabelVar.set("Selectionnez une note\n et une octave")
            self.noteButton["state"]='disabled'

    def createSoundDurationSlider(self,frame):
        self.duration = tk.DoubleVar()
        self.duration.set(0.5)
        self.durationSlider=tk.Scale(frame,variable=self.duration,label="Duration",orient="horizontal",resolution=0.1,length=250,from_=0.1,to=3.1,tickinterval=0.5)

    def generateSound(self):
        # destinationFolder = "GeneratedSounds/"
        destinationFolder = self.completePath
        degree = self.octaveListBox.get(self.octaveListBox.curselection())
        name = self.noteListBox.get(self.noteListBox.curselection())
        duration = self.duration.get()
        self.model.generateNote(degree,name,duration*1000,folder=destinationFolder)

        self.noteListBox.select_clear(0,tk.END)
        self.octaveListBox.select_clear(0,tk.END)

        self.noteLabelVar.set("Generation terminée")

        self.noteWarning.after(1500, self.checkNoteList)


    def generateSoundsChords(self):
        # self.model.generateChords()
        print("Generation accord")
        self.accordList.select_clear(0,tk.END)
        self.accordListOctave.select_clear(0,tk.END)

        self.accordLabelVar.set("Generation terminée")

        self.accordWarning.after(1500, self.checkAccordList)


    def createFolderAsking(self,frame):
        self.displayedPath = tk.StringVar()
        path = os.path.dirname(os.path.abspath(__file__))
        path += "/GeneratedSounds"
        self.completePath = path
        self.displayedPath.set(path[-26:])  #set the 26 last char
        self.pathLabel = tk.Label(frame,textvariable=self.displayedPath,bg="white",width=26)

        self.directoryButton = tk.Button(frame,text="Directory")
        self.directoryButton.bind("<ButtonRelease-1>",self.askDir)


    def askDir(self,event):
        path = filedialog.askdirectory()
        print(path)
        if not path:                    #if empty keep the last one
            path = self.completePath
            print("No path selected, keep the old one")
        self.completePath=path
        self.displayedPath.set(path[-26:])
        self.view.path=path
        self.view.update()




if  __name__ == "__main__" :
    root=tk.Tk()
    root.title("Vue Creation Note")
    model=SoundGeneratorModel()
    view=SoundGeneratorView(root,model)
    view.packing()



    # model.attach(view)

    # view.update(model)
    root.mainloop()
