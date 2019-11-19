from observer import *
# from soundModel import *
# from soundController import *
import sys
import os
import wave, struct, math, random
from wav_audio import *
import sqlite3
conn = sqlite3.connect('frequencies.db')
c = conn.cursor()

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



class SoundGeneratorController():
    def __init__(self,parent,model,view,bg="white",width=715,height=390):
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
        self.radioButtonFrame = tk.Frame(self.frameGeneration,bg="red")


        self.createNoteList(self.frameNote)
        self.createAccordList(self.frameAccord)
        self.createMajorMinorButton(self.radioButtonFrame)
        
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
            # self.accordListChosen["width"]=int(0.2*self.width)

            
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
        # self.accordLabelChosen.grid(row=0,column=1)
        # self.accordListChosen.grid(row=1,column=1)


        # Generation
        self.noteWarning.grid(row=0,column=0)
        self.noteButton.grid(row=2,column=0)
        self.frameParameter.grid(row=0,column=1,rowspan=3)
        self.accordWarning.grid(row=0,column=2)
        self.radioButtonFrame.grid(row=1,column=2)
        self.accordButton.grid(row=2,column=2)
        

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

        # self.accordLabelChosen= tk.Label(frame,text="Notes Choisies")
        # self.accordListChosen = tk.Listbox(frame,exportselection=0)
        # self.accordListChosen.bind("<KeyPress-Delete>",self.deleteNoteAccordList)

        self.updateNotesList()


    def createAccordButton(self,frame):
        self.accordLabelVar = tk.StringVar()
        self.accordLabelVar.set("Choisissez la tonique")

        self.accordWarning=tk.Label(frame,textvariable=self.accordLabelVar,width=20,height=2)

        self.accordButton = tk.Button(frame,text="Générer un accord",state='disable',width=20,command=self.generateSoundsChords)

    def createMajorMinorButton(self,frame):
        valeurs = ['Major', 'Minor']
        etiquettes = ['Accord Majeur', 'Accord Mineur']
        self.majorMinorVar = tk.StringVar()
        self.majorMinorVar.set(valeurs[0])
        self.model.setMajor()
        self.updateNotesList()
        
        for i in range(2):
            b= tk.Radiobutton(self.radioButtonFrame, variable=self.majorMinorVar, text=etiquettes[i], value=valeurs[i])
            b.bind("<ButtonRelease-1>",self.adaptNoteAvailable)
            b.pack(side='left', expand=1)

    
    def adaptNoteAvailable(self,event=None):

        self.model.resetSelection()
        if (self.majorMinorVar.get()=="Major"):
            print("Major Chords selected")
            self.model.setMajor()
            self.updateNotesList()
        else:
            print("Minor Chords selected")
            self.model.setMinor()
            self.updateNotesList()



    def createNoteButton(self,frame):
        self.noteLabelVar = tk.StringVar()
        self.noteLabelVar.set("Selectionnez une note\n et une octave")

        self.noteWarning=tk.Label(frame,textvariable=self.noteLabelVar,width=20,height=2)

        self.noteButton = tk.Button(frame,text="Générer une note",state='disable',width=20,command=self.generateSound)


    # def deleteNoteAccordList(self,event=None):
    #     print('delete')
    #     sel = self.accordListChosen.curselection()
    #     for index in sel[::-1]:
    #         self.accordListChosen.delete(index)


    def updateNotesList(self):
        newNotes = self.model.getCurrentNotes()
        self.accordList.delete(0,tk.END)
        for item in newNotes:
            self.accordList.insert(tk.END,item)

        #check selectedItem in Model
        selectedNotes = self.model.getNoteListChord()
        for i in range(self.accordList.size()):
            for selectedNote in selectedNotes:
                if (self.accordList.get(i) == selectedNote):
                    self.accordList.selection_set(i)


    def checkAccordList(self,event=None):
        noteList = []
        sel = self.accordList.curselection()
        for i in sel:
            noteList.append(self.accordList.get(i))
        self.model.checkAccord(noteList)
        self.updateNotesList()

        #Update Label 
        listFromModel = self.model.getNoteListChord()
        if(len(listFromModel)==3):
            txt="Vous pouvez générez\nun accord"
            self.accordButton["state"]="normal"
        elif(len(listFromModel)==2):
            txt="Voici les deux notes\npour completer l'accord"
            self.accordButton["state"]="disable"
        elif(len(listFromModel)==1):
            txt="Voici les deux notes\npour completer l'accord"
            self.accordButton["state"]="disable"
        elif(len(listFromModel)==0):
            txt="Choisissez la tonique"
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
        self.model.resetSelection()
        # self.accordListChosen.select_clear(0,tk.END)

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