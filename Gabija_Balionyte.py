import wave
import numpy as np
import matplotlib.pyplot as plt
import os
import soundfile as sf
from tkinter import filedialog
 
def openFile():  #Failų nuskaitymas kompiuteryje iš bet kurio aplanko filtruojant tik wav tipo failus. 
    fileSource = filedialog.askopenfilename(filetypes=[("any file","*.wav")])
    return fileSource

def normalizeDataValues(data):  #Visos reikšmės sunormuotos 
    data = data / data.max()
    return data

def getSignalInfoFromFile(filePath):
    file = wave.open(filePath, "rb") 
    numberOfFrames = file.getnframes()   #grąžina garso frame skaičių  
    frameRate = file.getframerate() #grąžina dažnį
    dataByteString = file.readframes(numberOfFrames) # nuskaito tiek frames kiek yra garso faile
    file.close() 
    data = np.frombuffer(dataByteString, np.int16)
    data = normalizeDataValues(data)
    duration = numberOfFrames / frameRate
    return [data, numberOfFrames, frameRate, duration]

def visualizeDiagram(title, duration, data, xlabel, ylabel, lineY = None):
    durationArray = np.linspace(0, duration, num=len(data))
    plt.plot(durationArray, data)
    plt.title(title) #Naudojamas failo pavadinimas
    plt.xlabel(xlabel) #Naudojamas laikas
    plt.ylabel(ylabel) #Naudojamos normalizuotos reikšmės
    if lineY:
        plt.axhline(y=lineY, linewidth=0.2, color="r")
    plt.show() 

def fadeIn(data, rate, duration, step = 0.05): #Garso sumazejimo funkcija
    dataToFade = int(rate * (duration / 1000)) #Garsas paverciamas milisekundemis
    iterationLength = int(dataToFade/(1 / step))
    currentIterationLength = 0
    isStereo = False
    volume = 0
    result = []
    
    for index in range(len(data)):
        if (currentIterationLength > iterationLength): 
            volume = volume + step
            currentIterationLength = 0
        if (volume <= 1):
            if (isStereo):
                result.append([data[index][0] * volume, data[index][1] * volume])
            else:
                result.append(data[index] * volume)
        else:
            result.append(data[index])
        currentIterationLength = currentIterationLength + 1;

    return result

def fadeOut(data, rate, duration, step = 0.05):
    return fadeIn(data[::-1], rate, duration, step)[::-1] 

def fadeInOut(data, rate, duration, step = 0.05):
    fadedIn = fadeIn(data, rate, duration, step)
    return fadeOut(fadedIn, rate, duration, step)

filePath = openFile()
[data, numberOfFrames, sampleRate, duration] = getSignalInfoFromFile(fileath)
time = 0
time=input("Iveskite laika milisekundemis: ")
time=int(time)
fadedInOutData = fadeInOut(data, sampleRate, time)
sf.write("fade_in_fade_out.wav", fadedInOutData, sampleRate)
filename = os.path.basename(filePath)
visualizeDiagram(filename, duration, data, "Laikas", "Normalizuotos reikšmės")
visualizeDiagram(filename, duration, fadedInOutData, "Laikas", "Normalizuotos reikšmės ")
