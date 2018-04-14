import pandas as pd
import numpy as np
import csv
from sklearn.preprocessing import StandardScaler
from scipy.io.wavfile import read,write
import matplotlib.pyplot as plt

from librosa.core import stft,istft
from librosa.display import specshow
import librosa

def get_data(name,limit=None):
    rate,signal=read(name)
    if len(signal.shape)>1:
        signal=signal[:,0]
    if limit!=None:
        signal=signal[:limit]
    return signal.astype('float64')

def write_data(signal,name='test.wav'):
    write(name,8000,signal)

def get_chunks(stft,chunk_size=100):
    list_chunks=[]
    for i in range(0,stft.shape[0]-chunk_size,int(chunk_size/4)):
        list_chunks.append(stft[i:i+chunk_size])
    list_chunks=np.array(list_chunks)
    return list_chunks

def get_stft(signal):
    D=stft(signal)#,n_fft=1024,hop_length=512,win_length=1024)
    return D

def inverse_stft(stft):
    signal=istft(stft)#,hop_length=512,win_length=1024)
    return signal

def display_stft(stft):
    specshow(librosa.amplitude_to_db(stft,ref=np.max),y_axis='log', x_axis='time')
    plt.show()

def normalize(input):
    scaler = StandardScaler()
    input=scaler.fit_transform(input)
    return input,scaler

def unormalize(input,scaler):
    return scaler.inverse_transform(input)


# if __name__=="main":
