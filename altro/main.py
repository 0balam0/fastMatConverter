import mdfreader
import numpy as np
from os import listdir, mkdir, remove
from scipy.io import savemat, loadmat
from tqdm import tqdm

def _convert_to_matlab_name(channel_name):
    allowed_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
    channel_name_mat = ''.join([i if i in allowed_str else '_' for i in channel_name])
    channel_name_mat = channel_name_mat[:62]
    return channel_name_mat


resample = 0.05
dir = r'C:\Users\matteo.demarco\Downloads\210409_2 Shift_250_2.2l_180HP_VPB717_Sheet250_VPB717_row168_km27923'
file = r'210409_2 Shift_250_2.2l_180HP_VPB717_Sheet250_VPB717_row168_km27923.mdf'
# tmpFolder = r'GruppiConvertiti'
# try:
#     mkdir(dir+'\\' + tmpFolder)
# except FileExistsError:
#     [remove(dir + '\\' + tmpFolder + '\\' + i) for i in listdir(dir +  '\\' + tmpFolder)]

info = mdfreader.MdfInfo()  # informazioni file MDF
info.read_info(dir+'\\'+file)

print('Apertura file...')
file = mdfreader.Mdf(dir + '\\' + file, convert_after_read=True)
print('File aperto')

print(f'identificate {len(file.masterChannelList.keys())} base tempi, creazione di una base tempi comune...')
t_ = [min([min(file[j]['data']) for j in file.masterChannelList.keys()]),
      max([max(file[j]['data']) for j in file.masterChannelList.keys()]),
      max([len(file[j]['data']) for j in file.masterChannelList.keys()])]
tStart, tStop = None, None # set to None
if tStart is not None:
    t_[0] = tStart
if tStop is not None:
    t_[1] = tStop
time_space = np.linspace(t_[0], t_[1], int((t_[1] - t_[0]) / resample))
print(f'base tempi creata!!! da {int(t_[0])} a {t_[1]} con {t_[2]} campioni')

print('interpolazione su singola base tempi e salvataggio')
grop_resampled = {'tTH':
                      {'time':
                           {'v': time_space,
                            'u': 's',
                            'd': 'Time Master'}}}

errori = {}
for group in tqdm(file.masterChannelList.keys()):
    # for channel in tqdm(info['allChannelList']):
    for channel in file.masterChannelList[group]:
        time_master = file.get(channel, {}).get('master', {})
        if len(time_master):
            time_master = file.get(time_master, {}).get('data',[])
        else:
            errori[channel] = 'base tempi non trovata'
        data = file.get(channel, {}).get('data', [])
        unit = file.get(channel, {}).get('unit', [])
        description = file.get(channel, {}).get('description', [])

        # data_mean, data_std = mean(data), std(data)
        if len(data) and len(time_master):
            try:
                dataInterp = np.interp(time_space, time_master, data)
                name = _convert_to_matlab_name(channel)
                names = list(grop_resampled.keys())
                if name in names:
                    cc = 1
                    name+=str(cc)
                    while name in names:
                        name = name[:-(cc+1)]+str(cc)
                        cc += 1
                unit = unit if len(unit) else 'None'

                grop_resampled['tTH'][name] = {'v': dataInterp, 'u': unit, 'd': description}
            except:
                errori[channel] = 'errore durante interpolazione'
        else:
            errori[channel] = 'dati non trovati'

grop_resampled['tTH']['time']['v'] -= t_[0]
savemat(dir + '\\acc3.mat', grop_resampled, do_compression=True, long_field_names=True)









