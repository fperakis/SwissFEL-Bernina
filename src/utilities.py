import numpy as np
import matplotlib.pyplot as plt
import h5py
import time
import sys

def discover_run_h5(run_num,path=None):
    '''
    discovers h5 file of a given run number
    '''
    run_file = []
    if path is None:
        run_path = '/sf/bernina/data/p17743/res/work/hdf5/'
    else:
        run_path = path
    h5_files = discover_files(run_path)
    n_file = len(h5_files)

    for h5 in h5_files:
        run_str = '%04d'%run_num
        if run_str in h5:
            run_file = h5
            
    return run_file

def do_histogram(a,bi,bf,db):
    '''
    finally a good histogram function
    '''
    bins = np.arange(bi-db/2.,bf+db/2.+db,db)
    y,x_tmp = np.histogram(a,bins=bins)
    x = np.array([(bins[j]+bins[j+1])/2. for j in range(len(bins)-1)])
    return x,y

def median_filter(arr, filter_length=5):
    '''
    median filter of 1D or 2D ndarray along fast-scan
    '''
    if arr.ndim == 1:
        median_filtered_arr = np.zeros((arr.shape[0]-filter_length,))
        for i in range(median_filtered_arr.shape[0]):
            median_filtered_arr[i] = np.median(arr[i:i+filter_length])
    else:
        median_filtered_arr = np.zeros((arr.shape[0], arr.shape[1]-filter_length))
        for i in range(median_filtered_arr.shape[0]):
            for j in range(median_filtered_arr.shape[1]):
                median_filtered_arr[i][j] = np.median(arr[i,j:j+filter_length])
    return median_filtered_arr

def normalize(array, low, high, subtract=False):
    if subtract:
        n = np.max(array[low:high])
        m = array.min()
        norm_array = (array-m) / (n-m) # normalized between 0 and 1
    else:
        n = np.sum(array[low:high])
        norm_array = array / n # normalized to area
    return norm_array


def save_h5(save_path,save_dict):
    '''
    Saves the processed data in h5.
    Takes as input a nested dictionary with {"detector_name":{"dataname": dataset}}
    '''

    h5f = h5py.File(save_path, 'w')

    for group in save_dict:
        h5g = h5f.create_group(group)
        for dataset in save_dict[group]:
            if (dataset.find("num") >= 0) or (dataset.find("event") >= 0):
                h5g.create_dataset(dataset, data=save_dict[group][dataset], dtype='u8') # unsigned 64-bit integer
            elif (dataset.find("laser_on") >= 0):
                h5g.create_dataset(dataset, data=save_dict[group][dataset], dtype='?') # boolean
            else:
                h5g.create_dataset(dataset, data=save_dict[group][dataset], dtype='f') # floating point (32-bit?)

    h5f.close()
    return

def get_date(filepath):
    '''
    Returns the when file was last modified
    '''
    stat = os.stat(filepath)
    return stat.st_mtime

def discover_files(path):
    '''
    Looks in the given directory and returns the filenames
    '''
    for (dirpath, dirnames, filenames) in os.walk(path):
        break
    return filenames
