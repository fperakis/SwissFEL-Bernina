import numpy as np
import h5py
import time
import sys
from scipy.signal import medfilt

sys.path.insert(0, '../src/')
from corrections import *
from integrators import *

def load_processed_data(run,path=None):
    '''
    loads data from processed h5
    '''
    
    if path is None:
        h5path = '/sf/bernina/data/p17743/res/work/hdf5/run%s.h5'%run
    else:
        h5path = path+'run%s.h5'%run
    h5file = h5py.File(h5path,'r')
    sum = h5file['JF7/2D_sum'][:]
    Iq = h5file['JF7/I_Q'][:]
    r = h5file['JF7/Q_bins'][:]
    
    try:
        i0 = h5file['JF3/i0'].value
    except KeyError:
        i0 = h5file['JF7/i0'].value
    
    nshots = h5file['JF7/num_shots'].value

    try:
        nhits = np.int(h5file['JF7/num_hits'].value)
        sum_hits = h5file['JF7/2D_sum_hits'].value
        Iq_thr = h5file['JF7/I_threshold'].value
    except KeyError:
        nhits = None
        sum_hits = None
        Iq_thr = None
    
    laser_i0 = h5file['SARES20/i0'].value
    try:
        laser_on = h5file['SARES20/laser_on'].value
    except KeyError:
        laser_on = h5file['BERNINA/laser_on'].value
    event_ID = h5file['pulse_id'].value
          
    print('run%s: %d shots' % (run, h5file['JF7/num_shots'].value))
    h5file.close()
        
    return sum,Iq,r,int(nshots),sum_hits,Iq_thr,nhits,i0,laser_i0,laser_on,event_ID #maybe use dictionary here



def find_hits(Iq, threshold=0.015, r_min=200, r_max=400):
    '''
    finds the shots that hit water droplets based on
    a simple threshold on the average over a q-range
    note: give Iq in photon/pix units/i0
    '''
    metric = np.average(Iq[:,r_min:r_max],axis=1)
    hits = metric>threshold
    return metric,hits

def find_ice(Iq, q, threshold=0.1, filter_length=5, q_min=1.0, q_max=4.5):
    '''
    finds the shots that hit ice droplets
    based on maximum gradient of median filtered intensities
    note: give Iq in photon/pix units/i0
    '''
    median_filtered_Iq = medfilt(Iq, (1, filter_length))

    ice_range_idx = (q > q_min) * (q < q_max)
    diff = np.abs(median_filtered_Iq[:,ice_range_idx] - median_filtered_Iq[:,np.roll(ice_range_idx, 1)])
    metric = np.max(diff, axis=1)
    hits = ( metric > threshold )

    #omedian_filtered_Iq = median_filter(Iq, filter_length=filter_length)
    #ice_range_indices = np.where((q > q_min) & (q < q_max))
    #ometric = np.array([np.max(np.abs(i[ice_range_indices]-i[(ice_range_indices[0]+1)])) for i in omedian_filtered_Iq])
    #oldhits = metric>threshold

    #print(np.sum(np.abs(ometric - metric)))
    #print(np.sum(hits - oldhits))

    return metric,hits

def subtract_background(Iq,hits,misses=None,i0,nshots):
    '''
    Calculates the average of missed shots and subtracts it as a background
    '''

    # calculate background based on normalised misses
    if misses is None:
        miss = np.logical_not(hits)
    else:
        miss = misses
    Iq_background = np.average(Iq[miss],axis=0,weights=i0[miss])
    
    # in case there are no hits 
    if hits.sum() == 0:
        return Iq 
    
    # subtract background
    Iq_corr = np.zeros_like(Iq[hits])
    
    for i in range(np.sum(hits)):
        norm = i0[hits][i]/np.average(i0[hits])
        Iq_corr[i] = Iq[hits][i]/norm - Iq_background/norm
    
    return Iq_corr


def pump_probe_signal(Iq,hits,laser_on,r_min=200,r_max=300):
    '''
    calculate the pump probe signal
    '''    
    # important: cast laser_on to boolean (otherwise it messes up the code -ask TJ)
    laser_on_hits = laser_on[hits].astype(bool)   
    laser_off_hits = np.logical_not(laser_on_hits)
 
    # laser on and off shots
    Iq_on_avg = np.average(Iq[laser_on_hits],axis=0)
    Iq_off_avg = np.average(Iq[laser_off_hits],axis=0)
    
    # pump-probe difference signal
    diff_signal = normalize(Iq_on_avg, r_min, r_max) - normalize(Iq_off_avg, r_min, r_max)
 
    # in case there are no hits return en empty array
    if hits.sum()>0:
    	return diff_signal
    else:
        return np.zeros_like(diff_signal)

