import mdfreader
import numpy as np
# from os import listdir, mkdir, remove
from scipy.io import savemat, loadmat
from tqdm import tqdm
import inputRequest
from os.path import splitext as osSplitext
import sys
import winsound
def convert_dat2mat(folder = None, file_name = None, resample = None, tCut_input = None, name_file_out = None):
    def _convert_to_matlab_name(channel_name):
        allowed_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
        channel_name_mat = ''.join([i if i in allowed_str else '_' for i in channel_name])
        channel_name_mat = channel_name_mat[:62]
        return channel_name_mat
    if folder == None or file_name==None:
        folder, file_name = inputRequest.ricerca_file()
    print(f'{folder},{file_name}')

    # informazioni file MDF
    print('Caricamento informazioni..')
    info = mdfreader.MdfInfo()
    info.read_info(folder + '\\' + file_name)

    print('Apertura file...')
    file = mdfreader.Mdf(folder + '\\' + file_name, convert_after_read=True)
    print('File aperto!!')
    # "C:\DBnew\965_P2.548V\Analisi_FGTvsVGT_test\Dati\VGT_PCR5A\20220210 - VP394 2WD\01_Results\10-02-2022 16_00_18_965vgt_VP394 ldv.dat"
    # "C:\DBnew\965_P2.548V\Analisi_FGTvsVGT_test\Dati\FGT_PCR4D1\20220202\2022-02-02_965_fgt_00140_WLTP_HIGH_MASCHERA_CO2.dat"
    print(f'identificate {len(file.masterChannelList.keys())} base tempi, creazione di una base tempi comune...')
    t_ = [np.inf, -np.inf, 0]
    for j in tqdm(file.masterChannelList.keys()):
        __t__ = file.get_channel_data(j)
        if __t__ is not None:
            if t_[0] > min(__t__):
                t_[0] = min(__t__)
            if t_[1] < max(__t__):
                t_[1] = max(__t__)
            if t_[2] < len(__t__):
                t_[2] = len(__t__)

    print(f'tempo da {t_[0]:.1f} a {t_[1]:.1f} con {t_[2]:.0f} campioni')
    if resample == None:
        resample = inputRequest.resample_request()
    else:
        resample = float(resample)

    if tCut_input == None:
        tStart, tStop = inputRequest.time_space(t_[0], t_[1])
        if tStart is not None:
            t_[0] = tStart
        if tStop is not None:
            t_[1] = tStop
    elif len(tCut_input) == 1:
        pass
    else:
        ris = tCut_input.strip('][ ').split(',')
        t_[0] = float(ris[0])
        t_[1] = float(ris[1])

    time_space = np.linspace(t_[0], t_[1], int((t_[1] - t_[0]) / resample))

    print(f'base tempi creata!!! da {t_[0]} a {t_[1]:.1f} con {t_[2]:.1f} campioni')

    print('interpolazione su singola base tempi e salvataggio')

    grop_resampled = {'tTH':
                          {'time':
                               {'v': time_space,
                                'u': 's',
                                'd': 'Time Master'}}}
    # add bug in dat
    grop_resampled['tTH']['time']['v'] = np.asmatrix(grop_resampled['tTH']['time']['v'])
    shc = grop_resampled['tTH']['time']['v'].shape
    if shc[0] < shc[1]:
        grop_resampled['tTH']['time']['v'] = grop_resampled['tTH']['time']['v'].transpose()

    errori = {}
    file_, _ = osSplitext(file_name)
    # creazione file txt lista canali
    if name_file_out==None:
        name_file_outTXT = folder + f'\\{file_}_{round(t_[0], 1)}to{round(t_[1], 1)}.txt'
    else:
        name_file_outTXT = name_file_out+'_NameList.txt'
    file_listaCanali = open(name_file_outTXT, "w")
    file_listaCanali.write(f'name\tunit\t description\tmaster\tlen\tid\n')
    errori = dict()

    for group in tqdm(file.masterChannelList.keys()):
        # for channel in tqdm(info['allChannelList']):
        for channel in file.masterChannelList[group]:
            if not (channel == 'time'):
                time_master_name = file.get_channel_master(channel)
                time_master = file.get(channel, {}).get('master', {})
                if len(time_master):
                    time_master = file.get(time_master, {}).get('data', [])
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
                            name += str(cc)
                            while name in names:
                                name = name[:-(cc + 1)] + str(cc)
                                cc += 1
                        unit = unit if len(unit) else 'None'
                        dataInterpT = np.asmatrix(dataInterp).transpose()
                        grop_resampled['tTH'][name] = {'v': dataInterpT, 'u': str(unit), 'd': str(description)}
                    except:
                        errori[channel] = 'errore durante interpolazione'
                    try:
                        Stringa_salvataggio_info = f"{channel}\t{file[channel]['unit']}\t{file[channel]['description']}\t{file[channel]['master']}\t{len(file[channel]['data'])}\t"
                        for idCount in file[channel].get('id', ()):
                            for idCountCount in idCount:
                                Stringa_salvataggio_info += f'{idCountCount}\t'
                        Stringa_salvataggio_info += f'\n'
                        file_listaCanali.write(Stringa_salvataggio_info)
                    except:
                        errori[channel] = '\t errore esportazione txt segnale'

                else:
                    errori[channel] = 'dati non trovati'

    file_listaCanali.close()
    t_T = np.asmatrix(t_[0]).transpose()
    grop_resampled['tTH']['time']['v'] -= t_T[0]
    if name_file_out == None :
        name_file_out = folder + f'\\{file_}_{round(t_[0], 1)}to{round(t_[1], 1)}.mat'
    else:
        name_file_out = name_file_out+'.mat'
    # "C:\Users\matteo.demarco\Downloads\2022-04-05 13_20_30_M182_pVP85_constant1.2_.dat\2022-04-05 13_20_30_M182_pVP85_constant1.2_.dat"
    print('Salvataggio in corso non chiudere la finestra!!!')
    savemat(name_file_out, grop_resampled, do_compression=True,
            long_field_names=True)
    print('Salvataggio completato correttamente.')
    print(f'file salvato...')
    if len(errori.keys()):
        print(f'sono stati riscontrati {len(errori.keys())} errori:')
        for i in errori.keys():
            print(f'{i}: \t {errori[i]}')
    return name

if __name__ == "__main__":
    s = len(sys.argv)
    # folder = None, file_name = None, resample = None, tCut_input = None, name_file_out = None
    opt = [None, None, None, None, None]
    for i in range(1, s):
        inStr = sys.argv[i].replace("'", "")
        opt[i-1] = inStr
        if opt[i-1] =='None':
            opt[i - 1] = None

    convert_dat2mat(folder = opt[0], file_name = opt[1], resample = opt[2], tCut_input = opt[3], name_file_out = opt[4])
#example
# "C:\Users\matteo.demarco\Downloads\M189_PVP251_FDCAN11_FDCAN3_FDCAN5_OMOLOGAZIONE_COAST_DOWN_MDF\M189_PVP251_FDCAN11_FDCAN3_FDCAN5_OMOLOGAZIONE_COAST_DOWN.mdf"
# convert_dat2mat(folder = r"C:\Users\matteo.demarco\Downloads\M189_PVP251_FDCAN11_FDCAN3_FDCAN5_OMOLOGAZIONE_COAST_DOWN_MDF",
#              file_name = "M189_PVP251_FDCAN11_FDCAN3_FDCAN5_OMOLOGAZIONE_COAST_DOWN.mdf",
#               resample = 0.05, tCut_input = None, name_file_out = None)