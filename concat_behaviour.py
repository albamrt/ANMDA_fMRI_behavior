from glob import glob
import os
import numpy as np
import pandas as pd
import math 
import cmath

data_dir 	= '/archive/albamrt/MRI/behaviour/'
file_dir 	= '/storage/albamrt/NMDA/MRI/'
subjects 	= np.unique([subj[0:3] for subj in os.listdir(data_dir)])

def len2(x):
    if type(x) is not type([]):
        if type(x) is not type(np.array([])):
            return -1
    return len(x)

def phase2(x):
    if not np.isnan(x):
        return cmath.phase(x)
    return np.nan

def circdist(angles1, angles2):
    if len2(angles2) < 0:
        if len2(angles1) > 0:
            angles2 = [angles2]*len(angles1)
        else:
            angles2 = [angles2]
            angles1 = [angles1]     
    if len2(angles1) < 0:
        angles1 = [angles1]*len(angles2)
    return np.array(list(map(lambda a1, a2: phase2(np.exp(1j*a1) / np.exp(1j*a2)), 
        angles1, angles2)))

def angle_diff(theta1, theta2):
  theta = abs(theta1 - theta2) % 360 
  return(np.where(theta > 180, 360 - theta, theta))

def toRange(series):
    while any(series>90):
        series[series>90] = series[series>90] - 180
    while any(series<-90):
        series[series<-90] = series[series<-90] + 180
    return series

def wrap2halfpi(x):
    x[x > np.pi/2] = x[x > np.pi/2] - np.pi
    x[x < -np.pi/2] = x[x < -np.pi/2] + np.pi
    return x

data = pd.DataFrame()

for subj in subjects:
    print('subject', subj )
    sessions = np.unique([file for file in os.listdir(data_dir+subj)])
    for sess in sessions:
        print('session:', sess)
        sub_dir = data_dir + subj + '/' + sess
        # load LTM dataframes
        beh = []
        s = sess[1]
        dirs = glob(sub_dir + '/*.csv') 
        for i in range(len(dirs)):
            beh.append(pd.read_table(dirs[i], sep=';'))
            beh[i]['run'] = pd.Series(np.repeat(i, len(beh[i])))
            beh[i]['S_Angle_range'] = toRange(beh[i].S_Angle.copy())
            beh[i]['P_Angle_range'] = toRange(beh[i].P_Angle.copy())
            beh[i]['R_Angle_range'] = toRange(beh[i].R_Angle.copy())
            beh[i]['S_rad'] = beh[i].S_Angle_range.map(math.radians)
            beh[i]['P_rad'] = beh[i].P_Angle_range.map(math.radians)
            beh[i]['R_rad'] = beh[i].R_Angle_range.map(math.radians)

            beh[i]['prevstim_rad'] = np.roll(beh[i].S_rad, 1)
            beh[i]['prevstim_rad'][0] = np.nan
            beh[i]['prevresp_rad'] = np.roll(beh[i].R_rad, 1)
            beh[i]['prevresp_rad'][0] = np.nan
            beh[i]['prevmem'] = np.roll(beh[i].type, 1)
            beh[i]['prevmem'][0] = np.nan
            beh[i]['futurestim_rad'] = np.roll(beh[i].S_rad, -1)
            beh[i]['prevstim_rad'][len(beh[i]['futurestim_rad'])] = np.nan
            beh[i]['futureresp_rad'] = np.roll(beh[i].R_rad, -1)
            beh[i]['futureresp_rad'][len(beh[i]['futureresp_rad'])] = np.nan
            beh[i]['prevprob_rad'] = np.roll(beh[i].P_rad, 1)
            beh[i]['prevprob_rad'][0] = np.nan

        # attach to one single dataframe
        beh = pd.concat(beh)
        if beh.shape[0] != 0:
            beh['subject'] = pd.Series(np.repeat(subj, beh.shape[0]))
            beh['session'] = pd.Series(np.repeat(sess,len(beh)))
        # attach to all subjects dataframe
        data = pd.concat((data,beh)).reset_index(drop = True)

# add condition variable:
data['group'] = data['subject'].astype(str).str[0]
# add error (in degrees):
data['error0'] = circdist(data['R_rad'].values, data['S_rad'].values)
data['error'] = wrap2halfpi(data.error0.copy())
data['errorprevstim0'] = circdist(data['R_rad'].values, data['prevstim_rad'].values)
data['errorprevstim'] = wrap2halfpi(data.errorprevstim0.copy())
data['errorprevresp0'] = circdist(data['R_rad'].values, data['prevresp_rad'].values)
data['errorprevresp'] = wrap2halfpi(data.errorprevresp0.copy())
data['errorprevprobe0'] = circdist(data['R_rad'].values, data['prevprob_rad'].values)
data['errorprevprobe'] = wrap2halfpi(data.errorprevprobe0.copy())

# add distance from previous to current stimulus presentation:
data['diffstim0'] = circdist(data['prevstim_rad'].values, data['S_rad'].values)
data['diffstim'] = wrap2halfpi(data.diffstim0.copy())

data['diffresp0'] = circdist(data['prevresp_rad'].values, data['S_rad'].values)
data['diffresp'] = wrap2halfpi(data.diffresp0.copy())

data['difffuture0'] = circdist(data['futurestim_rad'].values, data['S_rad'].values)
data['difffuture'] = wrap2halfpi(data.difffuture0.copy())

data['difffutureresp0'] = circdist(data['prevprob_rad'].values, data['R_rad'].values)
data['difffutureresp'] = wrap2halfpi(data.difffutureresp0.copy())

data['diffprevprob0'] = circdist(data['futureresp_rad'].values, data['R_rad'].values)
data['diffprevprob'] = wrap2halfpi(data.diffprevprob0.copy())

data = data.drop(columns = ['S_Angle_range', 'P_Angle_range', 'R_Angle_range', 'error0', 'errorprevstim0', 
    'errorprevresp0', 'errorprevprobe0', 'diffstim0', 'diffresp0', 'difffuture0', 'difffutureresp0', 'diffprevprob0'])

data.to_csv(file_dir + 'behaviour.csv', sep=';', index=False)


