from asammdf import MDF, MDF2, MDF3, MDF4
path_info = r'.\readme.txt'
file = r'C:\Users\matteo.demarco\Downloads\20210726 - VP 16 2WD\01_Results\26-07-2021 11_02_31_520 vp 16 wltc\26-07-2021 11_02_31_520 vp 16 wltc.dat'
raster = 0.05
time_from_zero = True


with MDF(file) as mdf_file:
    mdf_info = mdf_file.info()
    # identificazione versione del File
    version = float(mdf_info['version'])

    if version>=3 and version<4:
        mdf_file = MDF3(file)

    # resample file
    # mdf_file.resample(raster, time_from_zero=time_from_zero)

    # # scrivo tutte le info in path_info
    # with open(path_info, 'w') as info_file:
    #     infoKeys = mdf_info.keys()
    #     for i in mdf_info.keys():
    #         if 'group ' not in i:
    #             info_file.write(f"{i}:\t{mdf_info[i]}\n")

