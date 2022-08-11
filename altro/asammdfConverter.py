import asammdf as asa
from tqdm import tqdm
import numpy as np
file = {} # dictiony of file location

file['name'] = r'356MHEV_VP250_Prestazioni.dat'
file['dir']  = r'C:\DBnew\356_P2.548V\03_perfo\test\19-04-2021\tracce'


# ricerca time space
def TimeSpace(mdf, resample=0.05):
    __t__ = {'tmin': [], 'tmax': [], 'len': []}
    for i in tqdm(mdf.masters_db):
        master = mdf.get_master(i)
        if len(master):
            __t__['tmin'].append(min(master))
            __t__['tmax'].append(max(master))
            __t__['len'].append(len(master))

    t_ = [min(__t__['tmin']), max(__t__['tmax']), max(__t__['len'])]
    time_space = np.linspace(t_[0], t_[1], int((t_[1] - t_[0]) / resample))
    return time_space

if __name__ is '__main__':
    mdf = asa.MDF(file['dir'] + '\\' + file['name'])
    print('file Aperto.')
    for i in tqdm(mdf.iter_groups()):
        pass
    for n_group in mdf.masters_db:
        group_name = mdf.groups[n_group].channel_group.acq_name
        n_channel  = len(mdf.groups[n_group].channels)
        master = mdf.get_master(n_group)
        print(f'#gruppo {n_group} di {len(mdf.masters_db)}: name {group_name}')
        for n in tqdm(range(n_channel)):
            channel_name = mdf.get_channel_name(n_group, n)
            data = mdf.get(channel_name, n_group)
            if data.conversion is not None :
                storage = data
            # comment = mdf.get_channel_comment(channel_name, n_group)
            # unit = mdf.get_channel_unit(channel_name, n_group)



    # info = mdf.info()
    # print(info['comment'])
    # print('time space', TimeSpace(mdf, resample=0.05))
a = mdf.get_channel_metadata('EVO_REQ_02')
print(a.conversion.conversion_type)
# a.conversion.referenced_blocks == None
a = mdf.get_channel_metadata('Clutch1_Sts')
print(a.conversion.conversion_type)
a.address

with open(file['dir'] + '\\' + file['name'], 'rb') as mdfFile:
    ch1 = asa.blocks.v2_v3_blocks.ChannelConversion(stream = mdfFile, address=mdf.groups[0].channel_group.address)


# import mdfreader
# mdfRD = mdfreader.Mdf(file['dir'] + '\\' + file['name'], convert_after_read=True)