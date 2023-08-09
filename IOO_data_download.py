# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 16:45:24 2023

@author: Brian_Tsui
"""


# Data Download 

# https://ooipy.readthedocs.io/en/latest/index.html 



import warnings
warnings.filterwarnings('ignore')


import os
import sys
import ooipy
import datetime
import matplotlib.pyplot as plt


start_time = datetime.datetime(2022,7,1,3,16,0)
end_time = datetime.datetime(2022,7,1,3,17,0)
node1 = 'LJ01C'
node2 = 'Eastern_Caldera'


# Download Broadband data
print('Downloading Broadband Data:')
hdata_broadband = ooipy.get_acoustic_data(start_time,end_time,node1,verbose=True)

print(hdata_broadband.stats)
# filename (str) – filename to store .wav file as
hdata_broadband.wav_write(filename='raw_data202207010316.wav')

# ooipy.plot(hdata_broadband)
# plt.show()


# Compute spectrogram of acoustic signal. 
# For each time step of the spectrogram either a modified periodogram (avg_time=None) or a power spectral density estimate using Welch’s method with median or mean averaging is computed.

# win (str, optional) – Window function used to taper the data. 
# See scipy.signal.get_window for a list of possible window functions (Default is Hann-window.)
# L (int, optional) – Length of each data block for computing the FFT (Default is 4096).
# avg_time (float, optional) – Time in seconds that is covered in one time step of the spectrogram. 
# Default value is None and one time step covers L samples. 
# If the signal covers a long time period it is recommended to use a higher value for avg_time to avoid memory overflows and to facilitate visualization.
# overlap (float, optional) – Percentage of overlap between adjacent blocks if Welch’s method is used. 
# Parameter is ignored if avg_time is None. (Default is 50%)
# verbose (bool, optional) – If true (default), exception messages and some comments are printed.
# average_type (str) – type of averaging if Welch PSD estimate is used. options are ‘median’ (default) and ‘mean’.

# A Spectrogram object that contains time and frequency bins as well as corresponding values. 
# If no noise date is available, None is returned.
spec1 = hdata_broadband.compute_spectrogram()


# Compute power spectral density estimates of noise data using Welch’s method.

# win (str, optional) – Window function used to taper the data. 
# See scipy.signal.get_window for a list of possible window functions (Default is Hann-window.)
# L (int, optional) – Length of each data block for computing the FFT (Default is 4096).
# overlap (float, optional) – Percentage of overlap between adjacent blocks if Welch’s method is used. 
# Parameter is ignored if avg_time is None. (Default is 50%)
# avg_method (str, optional) – Method for averaging the periodograms when using Welch’s method. 
# Either ‘mean’ or ‘median’ (default) can be used
# interpolate (float, optional) – Resolution in frequency domain in Hz. 
# If None (default), the resolution will be sampling frequency fs divided by L. 
# If interpolate is smaller than fs/L, the PSD will be interpolated using zero-padding
# scale (str, optional) – If ‘log’ (default) PSD in logarithmic scale (dB re 1µPa^2/H) is returned. 
# If ‘lin’, PSD in linear scale (1µPa^2/H) is returned
# verbose (bool, optional) – If true (default), exception messages and some comments are printed.

# A Psd object that contains frequency bins and PSD values. If no noise date is available, None is returned.
psd1 = hdata_broadband.compute_psd_welch()
ooipy.plot(spec1,fmin=0,fmax=28000,res_reduction_time=100,xlabel_rot=30)
ooipy.plot(psd1,fmin=10,fmax=32000)
fig, ax = plt.subplots(figsize=(22,14),dpi=100)

# 1. using median averaging (default)
hdata_broadband.compute_psd_welch()

f = hdata_broadband.psd.freq/1000
plt.plot(f,hdata_broadband.psd.values,label='Welch median',color='r')

# 2. using mean averaging
hdata_broadband.compute_psd_welch(avg_method='mean')

plt.plot(f,hdata_broadband.psd.values,label='Welch mean',color='b')
plt.xlabel('frequency [kHz]')
plt.ylabel('SDF [dB re µPa**2/Hz]')
plt.xlim(1,25)
plt.ylim(25,70)
plt.legend()
plt.show()


