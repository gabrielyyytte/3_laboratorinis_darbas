import matplotlib.pyplot as plt
import easygui
import soundfile as sf
import pandas as pd


def openFile():  
    # leidžia pasirinki wav faila
    filePath = easygui.fileopenbox()
    return filePath


def leng(data):
    # patikrina ar reiksmei galima rasti ilgi
    return hasattr(data[0], "__len__")


def getMaxValue(data):
    if (leng(data)):
        data = [item for sublist in data for item in sublist]
    return max(max(data), -min(data))


def normalizeValues(data):
    tmax = getMaxValue(data)

    if (leng(data)):
        return [[elem/tmax for elem in sublist] for sublist in data]
    return [elem/tmax for elem in data]


def visualization(elements, indexes):
    plt.figure()
    if (leng(elements)):
        df = pd.DataFrame({'Left': [sublist[0] for sublist in elements], 'Right': [
                          sublist[1] for sublist in elements]}, index=indexes)
        df.plot()
    else:
        df = pd.Series(elements, index=indexes)
        df.plot()

        # y ašis
    plt.ylabel('Values') 
        # x ašis
    plt.xlabel('Time') 

def addEcho(soundData, rate, echoVolume, delay):
    echoData = []
    # indeksas, nuo kurio pridedamas aidas
    index_delay = int((delay  * rate)

    for index, value in enumerate(soundData):
         # jei nepasiektas minetas indeksas, aidas nepridedamas
        if (index < index_delay):  
             # masyvas uzpildomas pradiniu garsu
            echoData.append(value) 
        else:
            # gaunama suvelinto garso reiksme
            delayedValue = soundData[index-index_delay]
            # masyvas uzpildomas echo pagal formule
            echoData.append(value + echoVolume *
                             delayedValue)  

    return echoData


filePath = openFile()
data, rate = sf.read(filePath)

echoData = addEcho(data, rate, 0.5, 0.2)

normalizedOriginal = normalizeValues(data)
normalizedEcho = normalizeValues(echoData)

indexes = [index/rate for index in range(len(data))]

sf.write('sound_with_echo.wav', echoData, rate)

visualization(normalizedOriginal, indexes)
visualization(normalizedEcho, indexes)
plt.show()
