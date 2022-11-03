import matplotlib.pyplot as plt
import easygui
import soundfile as sf
import pandas as pd


def openFile():  # leidžia pasirinki wav faila
    file_path = easygui.fileopenbox()
    return file_path


def stereo(data):
    # patikrina ar reiksmei galima rasti ilgi
    return hasattr(data[0], "__len__")


def getTmax(data):
    if (stereo(data)):
        data = [item for sublist in data for item in sublist]
    return max(max(data), -min(data))


def normalizeValues(data):
    tmax = getTmax(data)

    if (stereo(data)):
        return [[elem/tmax for elem in sublist] for sublist in data]
    return [elem/tmax for elem in data]


def visualization(elements, indexes):
    plt.figure()
    if (stereo(elements)):
        df = pd.DataFrame({'Left': [sublist[0] for sublist in elements], 'Right': [
                          sublist[1] for sublist in elements]}, index=indexes)
        df.plot()
    else:
        df = pd.Series(elements, index=indexes)
        df.plot()

    plt.ylabel('Reikšmės')
    plt.xlabel('Laikas')


def addEcho(sound_data, rate, echo_volume, delay):
    echo_data = []
    # indeksas, nuo kurio pridedamas aidas
    index_delay = int((delay / 1000) * rate)

    for index, value in enumerate(sound_data):
        if (index < index_delay):  # jei nepasiektas minetas indeksas, aidas nepridedamas
            echo_data.append(value)  # masyvas uzpildomas pradiniu garsu
        else:
            # gaunama suvelinto garso reiksme
            delayed_value = sound_data[index-index_delay]
            echo_data.append(value + echo_volume *
                             delayed_value)  # masyvas uzpildomas echo pagal formule

    return echo_data


file_path = openFile()
data, rate = sf.read(file_path)

echo_data = addEcho(data, rate, 0.5, 200)

normalized_original = normalizeValues(data)
normalized_echo = normalizeValues(echo_data)

indexes = [index/rate for index in range(len(data))]

sf.write('sound_with_echo.wav', echo_data, rate)

visualization(normalized_original, indexes)
visualization(normalized_echo, indexes)
plt.show()
