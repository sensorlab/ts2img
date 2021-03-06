import numpy as np
import pandas as pd


def all_equal(sig: np.ndarray) -> bool:
    """
    Checks if elements in input array are all of equal value. 
    """
    return np.min(sig) - np.max(sig) == 0
    

def percent_full(sig:np.ndarray) -> int:  
    """
    Return percent of missing data. 
    """  
    return ( np.count_nonzero(~np.isnan(sig)) / sig.shape[0] )


def fill_missing(sig:np.ndarray) -> np.ndarray:
    """
    Fill missing data first with backfill,then with forwardfill, finally convert to list and return it.
    """
    return np.asarray(pd.Series(sig).ffill().bfill().tolist())


def filter_empty_slices_and_fill_missing_samples(signal_slices:np.ndarray, time_stamp_slices:np.ndarray, par: dict) -> np.ndarray:
    """
    Loop trough slices of signal data and remove data that has less that par["missing_data_allowed"], if more fill NaNs with ffill and bfill. 

    :param: signal_slices - np.array of singal slices
    :param: time_stamp_slices - np.array of slices of time stamps

    :return: signal_out, time_stamp_out - tuple of [np.ndarray np.ndarray] of processed slices
    """
    try:
        signal_out, time_stamp_out =  zip(*[(fill_missing(sig), stamp) for sig, stamp in zip(signal_slices, time_stamp_slices) if percent_full(sig) > par["percentage_of_missing_data_allowed"] ])

    except ValueError:
        # In case when nothing to return, list comprehension returns ValueError.
        signal_out, time_stamp_out = ([],[])


    return np.asarray(list(signal_out)), np.asarray(list(time_stamp_out))


def filter_low_entropy_slices(signal_slices: np.ndarray, time_stamp_slices: np.ndarray, par: dict) -> np.ndarray:
    """ 
    Removes slices with power less than 10W and slices that have all samples of the same value. 
    """
    try:
        signal_out, time_stamp_out =  zip(*[[sig,stamp] for sig, stamp in zip(signal_slices, time_stamp_slices) if not all_equal(sig) and np.any(sig > 10) ]) # 10 is value used by nilmtk, 10W is a turn on treshold for most appliances.
        
    except ValueError:
        # In case when nothing to return, list comprehension returns ValueError.
        signal_out, time_stamp_out = ([],[])


    return np.asarray(list(signal_out)), np.asarray(list(time_stamp_out))