from asammdf import MDF
from tqdm import tqdm
from numpy import inf, linspace

frequency = 2500  # Set Frequency To 2500 Hertz
duration = 30  # Set Duration To 1000 ms == 1 second

def _convert_to_matlab_name(channel_name):
    allowed_str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'
    channel_name_mat = ''.join([i if i in allowed_str else '_' for i in channel_name])
    channel_name_mat = channel_name_mat[:62]
    return channel_name_mat



# folder , file_name = inputRequest.ricerca_file()
folder = r'C:\Users\matteo.demarco\Downloads\2021-04-20 15_58_12_520_M215_LDV 520_'
file_name = r'2021-04-20 15_58_12_520_M215_LDV 520 .mf4'

print('Apertura file...')
mdf = MDF(folder + '\\' + file_name)
group = mdf.masters_db
print('\t file aperto.')

print(f'Sono stati identificati {len(group)} gruppi\n\t identificazione base tempi comune!')
t_ = [inf, -inf, 0]
__t__={}

for j in tqdm(group.keys()):
    __t__[j] = mdf.get_master(group[j])
    if __t__[j] is not None:
        if t_[0] > min(__t__[j]):
            t_[0] = min(__t__[j])
        if t_[1] < max(__t__[j]):
            t_[1] = max(__t__[j])
        if t_[2] < len(__t__[j]):
            t_[2] = len(__t__[j])
print(f'\t tempo minimo {round(t_[0],2)}; tempo massimo {round(t_[1],2)}; massimo numero di campioni {round(t_[2],2)}')

resample = 0.05 #inputRequest.resample_request()
tStart, tStop = None, None #inputRequest.time_space()
if tStart is not None:
    t_[0] = tStart
if tStop is not None:
    t_[1] = tStop
time_space = linspace(t_[0], t_[1], int((t_[1] - t_[0]) / resample))
print(f'base tempi creata!!! da {round(t_[0],2)} a {round(t_[1],2)} con {round(len(time_space))} campioni')

acq_name = mdf.groups[0].channel_group.acq_name
channels = mdf.groups[0].channels
channel = mdf.groups[0].channels[0]
channel_name = channel.name