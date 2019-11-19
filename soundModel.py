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



class SoundGeneratorModel(Subject):
    def __init__(self):
        Subject.__init__(self)
        self.octaves = ["1","2","3","4","5"]
        self.notes = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        self.currentNotes = self.getAllNotes()
        self.major=True
        self.noteListChord=[]


    def getOctave(self):
        return self.octaves
    
    def getNoteListChord(self):
        return self.noteListChord
    
    def resetSelection(self):
        self.noteListChord = []
    
    def getNotes(self):
        return self.notes

    def getCurrentNotes(self):
        return self.currentNotes
    
    def getAllNotes(self):
        noteList = []
        for octave in self.octaves:
            for note in self.notes:
                s = note + octave
                noteList.append(s)
        return noteList


    def setMajor(self):
        self.currentNotes=[]
        self.major=True
        notes = ["C","D","E","F","G","A","B"]
        for octave in self.octaves:
            for note in notes:
                s = note + octave
                self.currentNotes.append(s)
        self.notify()
    
    def setMinor(self):
        self.major=False
        self.currentNotes=self.getAllNotes()
        self.notify()

    def forceNote(self,noteList):
        self.currentNotes=noteList

    def checkAccord(self,notes):
        print("Checking chord")

        previousLen=len(self.noteListChord)


        if(len(self.noteListChord)==0 and len(notes)>0): #Si la liste est vide
            self.noteListChord.append(notes[0])
            print("Ajout de la premiere note")

        elif(len(self.noteListChord)<len(notes)):       #l'utilisateur a ajouté un element
            self.noteListChord.append(notes[len(notes)-1])
            print("l'utilisateur a ajouté un element")

        elif(len(self.noteListChord)>len(notes)):       #l'utilisateur a retiré un element
            self.noteListChord.pop()
            print("l'utilisateur a retiré un element")
        
        if(self.noteListChord==[]):
            if(self.major):
                self.setMajor()
            else : 
                self.setMinor()

        
        print(self.noteListChord)

        if(len(self.noteListChord)==1 and previousLen==0):
            currentNoteList=self.getCurrentNotes()
            indexNote0 = currentNoteList.index(self.noteListChord[0])
            authNoteList = []
            authNoteList.append(currentNoteList[indexNote0])
            authNoteList.append(currentNoteList[indexNote0+2])
            authNoteList.append(currentNoteList[indexNote0+4])

            self.forceNote(authNoteList)





    def getFrequencyFromNote(self,octave,note):    
        translateList = ["C","CSharp","D","DSharp","E","F","FSharp","G","GSharp","A","ASharp","B"]
        originalList = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        
        #On traduit de la notation C# à CSharp
        noteIndex = originalList.index(note)
        translateNote = translateList[noteIndex]

        #on cherche cette note dans la base de donnée a la bonne octave
        query = 'SELECT '+translateNote+' FROM frequencies WHERE octave=?'

        c.execute(query,(octave,))
        frequency = c.fetchone()

        # print("Frequency = ",frequency)
        return frequency[0]     #tuple


    def generateNote(self,degree,name,duration=1000,sampling=44100,folder="GeneratedSounds") :
        if type(degree) != str :
            degree=str(degree)

        frequency = self.getFrequencyFromNote(degree,name)
        file=folder+"/"+name+degree+".wav"
        sound=wave.open(file,'w')
        nb_channels = 2    # stéreo
        nb_bytes = 1       # taille d'un échantillon : 1 octet = 8 bits
        left_level = 1     # niveau canal de gauche (0 à 1) ? '))
        right_level= 1    # niveau canal de droite (0 à 1) ? '))
        nb_samples = int((duration/1000)*sampling)
        params = (nb_channels,nb_bytes,sampling,nb_samples,'NONE','not compressed')
        sound.setparams(params)    # création de l'en-tête (44 octets)

        # niveau max dans l'onde positive : +1 -> 255 (0xFF)
        # niveau max dans l'onde négative : -1 ->   0 (0x00)
        # niveau sonore nul :                0 -> 127.5 (0x80 en valeur arrondi)

        left_magnitude = 127.5*left_level
        right_magnitude= 127.5*right_level

        for i in range(0,nb_samples):
            # canal gauche
            # 127.5 + 0.5 pour arrondir à l'entier le plus proche
            left_value = wave.struct.pack('B',int(128.0 + left_magnitude*math.sin(2.0*math.pi*frequency*i/sampling)))
            # canal droit
            right_value = wave.struct.pack('B',int(128.0 + right_magnitude*math.sin(2.0*math.pi*frequency*i/sampling)))
            sound.writeframes(left_value + right_value) # écriture frame

        sound.close()
        self.notify()


    def generateChords(self,note1,note2,note3):
        print("Generate Sounds")
        sound=wave.open('GeneratedSounds/CMajor2.wav','w')
        folder = "Sounds/"
        note1=folder+str(note1)+'.wav'
        note2=folder+str(note2)+'.wav'
        note3=folder+str(note3)+'.wav'
        data1,framerate1 = open_wav(note1)
        data2,framerate2 = open_wav(note2)
        data3,framerate3 = open_wav(note3)
        duration =1000
        sampling=44100

        nb_channels = 2    # stéreo
        nb_bytes = 1       # taille d'un échantillon : 1 octet = 8 bits
        left_level = 1     # niveau canal de gauche (0 à 1) ? '))
        right_level= 1    # niveau canal de droite (0 à 1) ? '))
        nb_samples = int((duration/1000)*sampling)
        params = (nb_channels,nb_bytes,sampling,nb_samples,'NONE','not compressed')
        sound.setparams(params)    # création de l'en-tête (44 octets)

        data = [] # liste des échantillons de l'accord

        for i in range(len(data1)):
            data.append((data1[i]+data2[i]+data3[i])/3.0) # calcul de la moyenne de chacun des échantillons de même index issus des trois listes   
            sound.writeframes(wave.struct.pack('B',128+int((data1[i]+data2[i]+data3[i])/3.0)))
       
        save_wav('GeneratedSounds/CMajor.wav',data,framerate1)
        
        sound.close()
        self.notify()