from observer import *
from soundModel import *
from soundController import *
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
    def __init__(self,parent,model,bg="white",width=715,height=390):
        Observer.__init__(self)
        self.parent = parent
        self.parent.minsize(715, 500)
        self.model = model
        self.path="./GeneratedSounds"
        self.topFrame=tk.Frame(self.parent)
        self.bottomFrame=tk.Frame(self.parent)
        self.createFileList(self.bottomFrame)
    

    def createFileList(self,frame):
        self.filesListBox = tk.Listbox(frame,bg='white')

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                self.filesListBox.insert(tk.END,filename)
            

        self.scrollbar = tk.Scrollbar(frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # attach listbox to scrollbar
        self.filesListBox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.filesListBox.yview)

    def packing(self):
        self.topFrame.pack()
        self.bottomFrame.pack(side=tk.TOP)
        self.filesListBox.pack()

    def update(self):
        self.filesListBox.delete(0,tk.END)

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                self.filesListBox.insert(tk.END,filename)

        self.packing()

if  __name__ == "__main__" :
    root=tk.Tk()
    root.title("Vue Creation Note")
    model=SoundGeneratorModel()
    view=SoundGeneratorView(root,model)
    view.packing()
    model.attach(view)
    ctrl=SoundGeneratorController(view.topFrame,model,view)
    ctrl.packing()

    # model.attach(view)

    # view.update(model)
    root.mainloop()
