from os.path import split as osSplit
import winsound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 30  # Set Duration To 1000 ms == 1 second

def ricerca_file():
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    file = input('Trascina in file che vuoi converitre: ')
    file = file.replace('"', '')
    return osSplit(file)[0], osSplit(file)[1]

def resample_request():
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    risp = input('inserisci il tempo di campionamento in secondi (enter to default 0.05): ')
    if not len(risp):
        risp = '0.05'
    return float(risp)

def time_space():
    winsound.Beep(frequency, duration)
    winsound.Beep(frequency, duration)
    risp = input('inserisci l\'intervallo di tempo, ex. 0 1589.2 (enter to default): ')
    if not len(risp):
        return None, None
    return [float(risp.split(' ')[0]), float(risp.split(' ')[1])]