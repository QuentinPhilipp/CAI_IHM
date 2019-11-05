# https://fr.wikipedia.org/wiki/Note_de_musique

import sqlite3
connect = sqlite3.connect("frequencies.db")
cursor = connect.cursor()
cursor.execute("DROP TABLE IF EXISTS frequencies")
cursor.execute("CREATE TABLE frequencies ( \
                    octave INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,\
                    C float,\
                    CSharp float,\
                    D  float,\
                    DSharp float,\
                    E float,\
                    F float,\
                    FSharp float,\
                    G float,\
                    GSharp float,\
                    A      float,\
                    ASharp float,\
                    B float\
);")


f0=110.0
frequencies=[]
octaveList = [0,1,2,3,4]
octave=[]

for i in range(len(octaveList)):
    octave.append(i+1)
    for j in range (-9,3) :
        frequency=f0*2**(j/12.0)*(2**octaveList[i])
        octave.append(frequency)
    frequencies.append(octave)
    octave = []


print(frequencies)

cursor.executemany("INSERT INTO frequencies VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);", frequencies)
connect.commit()
