from observer import *
import collections
import subprocess
import sqlite3
conn = sqlite3.connect('frequencies.db')
c = conn.cursor()
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


class KeyboardView(Observer):
    def __init__(self,parent,degree,visualizer) :
        Observer.__init__(self)
        self.parent=parent
        # self.create_screen(degree)
        self.visualizer=visualizer

    def create_screen(self,degree) :
        self.screen=tk.Frame(self.parent,borderwidth=5,width=300,height=160,bg="grey")
        txtToDisplay = "Octave n°" + str(degree)
        self.info=tk.Label(self.screen,text=txtToDisplay, bg="grey",fg="white",font=('Arial',10))
        self.info.pack()

    # def get_screen(self) :
    #     return self.screen
    
    def getFrequencyFromNote(self,octave,note):    
        translateList = ["C","CSharp","D","DSharp","E","F","FSharp","G","GSharp","A","ASharp","B"]
        originalList = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        
        #On traduit de la notation C# à CSharp
        noteIndex = originalList.index(note)
        translateNote = translateList[noteIndex]
        print(translateNote)
        print(octave)

        #on cherche cette note dans la base de donnée a la bonne octave
        query = 'SELECT '+translateNote+' FROM frequencies WHERE octave=?'

        c.execute(query,(octave,))
        frequency = c.fetchone()

        # print("Frequency = ",frequency)
        return frequency[0]     #tuple

    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys()  :
                raise AssertionError

        subprocess.call(["aplay", model.get_gamme()[key]])
        if(self.visualizer!=None):   #Si on a ajouté un visualiseur de signal, le notifier
            freq = self.getFrequencyFromNote(model.get_degree(),key)
            self.visualizer.setFrequency(freq)
            self.visualizer.setMagnitude(3)
            self.visualizer.generate_signal()


class KeyboardModel(Subject) :
    def __init__(self,degree=3) :
        Subject.__init__(self)
        self.degree=degree
        self.set_gamme(degree)
    def set_gamme(self,degree=3) :
        self.degree=degree
        folder="Sounds"
        notes=["C","D","E","F","G","A","B","C#","D#","F#","G#","A#"]
        self.gamme=collections.OrderedDict()
        for key in notes :
            self.gamme[key]=folder+"/"+key+str(degree)+".wav"
        return self.gamme
    def get_gamme(self) :
        return self.gamme
    def get_degree(self) :
        return self.degree

    def notify(self,key) :
        for obs in self.observers:
            obs.update(self,key)


class Keyboard :
    def __init__(self,parent,model,noteVisibility) :
        self.parent=parent
        self.model=model
        self.noteVisibility = noteVisibility
        if self.noteVisibility :
            self.showNoteName()
            print("show")
        else :
            self.hideNoteName()
            print("hide")

        self.create_keyboard()


    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=tk.Frame(self.parent,width=7*key_w,height=key_h)
        for key in self.model.gamme.keys() :
            if  key.startswith( '#', 1, len(key) ) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=tk.Button(self.keyboard,name=key.lower(),width=3,height=6, bg = "black",text=key,anchor="s",fg=self.blackButtonFg,activeforeground=self.activeforeground,activebackground="grey90")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                button=tk.Button(self.keyboard,name=key.lower(),bg = "white",text=key,anchor="s",fg=self.whiteButtonFg,activeforeground=self.activeforeground,activebackground="grey90")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1

    def play_note(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard

    def showNoteName(self):
        self.blackButtonFg="white"
        self.whiteButtonFg="black"
        self.activeforeground="black"

    def hideNoteName(self):
        self.blackButtonFg="black"
        self.whiteButtonFg="white"
        self.activeforeground="grey90"

class PianoView(Observer) :
    def __init__(self,parent,octaveNumber,visualizer=None) :
        Observer.__init__(self)
        self.parent=parent
        self.octaves=[]
        self.octaveNumber = octaveNumber
        self.frame=tk.Frame(self.parent,bg="yellow")
        self.noteVisibility = True
        self.visualizer=visualizer
       
        for octave in range(octaveNumber) :
            self.create_octave(self.frame,self.visualizer,octave+1)

        self.createHideButton()

    def create_octave(self,parent,visualizer,degree=3) :
        frame=tk.Frame(parent,bg="gray38")
        model=KeyboardModel(degree)
        self.octaves.append(model)
        control=Keyboard(frame,model,self.noteVisibility)
        view=KeyboardView(frame,degree,visualizer)
        model.attach(view)
        # view.get_screen().pack()
        control.get_keyboard().pack()
        frame.pack(side=tk.LEFT,expand=True)
    def packing(self) :
        self.frame.pack(side=tk.TOP)
        self.hideButton.pack(side=tk.TOP)

    def createHideButton(self):
        self.hideButton=tk.Button(self.parent,bg = "white",width=12,text="Hide Note")
        self.hideButton.bind("<ButtonRelease-1>",self.changeNoteNameVisibility)
    
    def changeNoteNameVisibility(self,event=None):
        self.noteVisibility = not self.noteVisibility
        if(self.noteVisibility):
            self.noteVisibility=True
            self.hideButton["text"]="Hide Note"
        else : 
            self.noteVisibility=False
            self.hideButton["text"]="Display Note"

        self.octaves = []
        self.frame.destroy()
        self.hideButton.pack_forget()
        self.frame=tk.Frame(self.parent,bg="yellow")

        for octave in range(self.octaveNumber) :
            self.create_octave(self.frame,self.visualizer,octave+1)

        self.packing()


if __name__ == "__main__" :
    root = tk.Tk()
    root.minsize(1400, 250)
    octaves=5
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    view = PianoView(root,octaves)
    view.packing()

    root.mainloop()