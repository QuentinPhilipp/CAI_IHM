# -*- coding: utf-8 -*-
# https://stackoverflow.com/questions/34522095/gui-button-hold-down-tkinter

import sys
from frequenciesView import *
from frequenciesModel import *
import sqlite3
conn = sqlite3.connect('frequencies.db')
c = conn.cursor()

print(sys.version)

from tkinter import Tk,Frame,Button,Label

import collections

from observer  import *

import subprocess
#import sys
#sys.path.append("./Sounds")

class Octave(Subject) :
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

class Screen(Observer):
    def __init__(self,parent,degree) :
        self.parent=parent
        self.create_screen(degree)

    def create_screen(self,degree) :
        self.screen=Frame(self.parent,borderwidth=5,width=300,height=160,bg="grey")
        txtToDisplay = "Octave n°" + str(degree)
        self.info=Label(self.screen,text=txtToDisplay, bg="grey",fg="white",font=('Arial',10))
        self.info.pack()

    def get_screen(self) :
        return self.screen

    def update(self,model,key="C") :
        if __debug__:
            if key not in model.gamme.keys()  :
                raise AssertionError



        print("Degree : ",model.get_degree())
        octave = model.get_degree()

        print("Note : ",key)



        dbOrder = ["octave","C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
        index = dbOrder.index(key)

        print("Get frequency from database to display in the graph")
        c.execute('SELECT * FROM frequencies WHERE octave=?', (octave,))
        row = c.fetchone()
        
        print(row)
        print("At index : ",index)
        goodFrequency = row[index]
        print("frequency : ",goodFrequency)


        modelFreq.setFrequency(goodFrequency)
        modelFreq.generate_signal()
        
        if self.info :
            self.info.config(text = "Vous avez joue la note : " + key + str(model.get_degree()))

        subprocess.call(["aplay", model.get_gamme()[key]])




class Keyboard :
    def __init__(self,parent,model) :
        self.parent=parent
        self.model=model
        self.create_keyboard()
    def create_keyboard(self) :
        key_w,key_h=40,150
        dx_white,dx_black=0,0
        self.keyboard=Frame(self.parent,borderwidth=3,width=7*key_w,height=key_h,bg="grey")
        for key in self.model.gamme.keys() :
            if  key.startswith( '#', 1, len(key) ) :
                delta_w,delta_h=3/4.,2/3.
                delta_x=3/5.
                button=Button(self.keyboard,name=key.lower(),width=3,height=6, bg = "black")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w*delta_w,height=key_h*delta_h,x=key_w*delta_x+key_w*dx_black,y=0)
                if key.startswith('D#', 0, len(key) ) :
                    dx_black=dx_black+2
                else :
                    dx_black=dx_black+1
            else :
                button=Button(self.keyboard,name=key.lower(),bg = "white")
                button.bind("<Button-1>",lambda event,x = key : self.play_note(x))
                button.place(width=key_w,height=key_h,x=key_w*dx_white,y=0)
                dx_white=dx_white+1
    def play_note(self,key) :
        self.model.notify(key)
    def get_keyboard(self) :
        return self.keyboard


class Piano :
    def __init__(self,parent,octaves) :
        self.parent=parent
        self.octaves=[]
        self.frame=Frame(self.parent,bg="yellow")
        for octave in range(octaves) :
            self.create_octave(self.frame,octave+1)
    def create_octave(self,parent,degree=3) :
        frame=Frame(parent,bg="gray38")
        model=Octave(degree)
        self.octaves.append(model)
        control=Keyboard(frame,model)
        view=Screen(frame,degree)
        model.attach(view)
        view.get_screen().pack()
        control.get_keyboard().pack()
        frame.pack(side="left",fill="x",expand=True)
    def packing(self) :
        self.frame.pack()


if __name__ == "__main__" :
    root = Tk()
    root.geometry("1400x300")
    octaves=5
    modelFreq=FreqModel()
    print(modelFreq.name)
    modelFreq.generate_signal()
    root.title("La leçon de piano à "+ str(octaves) + " octaves")
    graph=FreqView(root)
    graph.grid(4)
    modelFreq.attach(graph)

    graph.update(modelFreq)

    piano=Piano(root,octaves)
    # mainWindow = MainWindow(root,octaves)
    piano.packing()
    # mainWindow.packing()
    graph.packing()
    root.mainloop()
