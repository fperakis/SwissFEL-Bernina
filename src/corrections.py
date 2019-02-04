from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from escape.parse import swissfel
import h5py
from jungfrau_utils import apply_gain_pede, apply_geometry
import time,sys

sys.path.insert(0, '../src/')
from integrators import *
from pedestals import*
from masking import *


def load_corrections(run):
    '''
    Loads the corrections for the jungfrau07 detector (16Mpix)
    '''
    jf3_pede_file, jf7_pede_file = get_pedestals(run)
    gain_file = '/sf/bernina/config/jungfrau/gainMaps/JF07T32V01/gains.h5'
    pede_file = jf7_pede_file
    mask_file = '/sf/bernina/data/p17743/res/JF_pedestals/pedestal_20190115_1551.JF07T32V01.res.h5'
   with h5py.File(gain_file,'r') as f:
        gains = f['gains'].value
    with h5py.File(pede_file,'r') as f:
        pede = f['gains'].value
    with h5py.File(mask_file,'r') as f:
        noise = f['gainsRMS'].value
        mask = f['pixel_mask'].value
    print('using pedestal from: %s' % pede_file)
    return gains,pede,noise,mask


def load_corrections_i0(run):
    '''
    Loads the corrections for jungfrau03 detector (small one - i0 monitor)
    '''

    jf3_pede_file, jf7_pede_file = get_pedestals(run)
    with h5py.File('/sf/bernina/config/jungfrau/gainMaps/JF03T01V01/gains.h5','r') as f:
        gains = f['gains'].value
    with h5py.File(jf3_pede_file,'r') as f:
        pede = f['gains'].value
    with h5py.File('/sf/bernina/data/p17743/res/JF_pedestal/pedestal_20190115_1551.JF03T01V01.res.h5','r') as f:
        noise = f['gainsRMS'].value
        mask = f['pixel_mask'].value

    return gains,pede,noise,mask


def get_i0(jf3_image,gains,pede,mask):
    '''
    calculates the i0 from an ROI of the  small jungfrau detector (JF3)
    '''
    # parameters
    X1,X2 = 10,240 #260,500
    Y1,Y2 = 260,500

    icorr = apply_gain_pede(jf3_image,G=gains, P=pede, pixel_mask=mask)
    icorr_geom = apply_geometry(icorr,'JF03T01V01')
    i0 = np.average(icorr_geom[X1:X2,Y1:Y2])

    return i0

