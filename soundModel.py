import sys
import wave, struct, math, random
from observer import *
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

    def getOctave(self):
        return self.octaves
    
    def getNotes(self):
        return self.notes


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


    def generate(self,degree,name,duration=1000,sampling=44100,folder="GeneratedSounds") :
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



if  __name__ == "__main__" :
    sound = SoundGeneratorModel()
    sound.generate("3","A",100)
    sound.generate("3","C",1000)


    print("Test FrequencyFromNote : Should return 932.33")
    sound.getFrequencyFromNote(4,"A#")
    print("Test FrequencyFromNote : Should return 146.83")
    sound.getFrequencyFromNote(2,"D")
