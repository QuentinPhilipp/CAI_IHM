from wav_audio import *

''' ouverture des fichiers des trois notes, et récupération de leur liste d'échantillons
Remarque : les trois sons doivent bien entendu avoir été créé avec la même fréquence d'échantillonnage... '''

data1,framerate1 = open_wav('Sounds/C3.wav')
data2,framerate2 = open_wav('Sounds/F3.wav')
data3,framerate3 = open_wav('Sounds/G3.wav')

data = [] # liste des échantillons de l'accord

for i in range(len(data1)):
    data.append((1/3)*(data1[i]+data2[i]+data3[i])) # calcul de la moyenne de chacun des échantillons de même index issus des trois listes   

save_wav('CMajor.wav',data,framerate1)

