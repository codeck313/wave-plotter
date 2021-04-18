import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import wave
import os
from scipy.io import wavfile
import scipy.signal as sps

# Configuring the matplotlib and numpy param
mpl.rcParams['agg.path.chunksize'] = 10000
numpy.seterr(divide='ignore')

# Fetching the file list and making sure output folder is present
fileNames = os.listdir('./data')
if not os.path.exists('output'):
    os.makedirs('output')

# to be changed by user
nBitRate = 36

for _file in fileNames:
    print(_file)
    # extracting data from .wav file
    s_wave = wave.open('data/'+_file, 'r')
    _file = _file.split('.')[0]

    # Add the data to a numpy array
    bitRate = s_wave.getframerate()
    signalToPlot = np.frombuffer(s_wave.readframes(-1), dtype=np.int16)
    deinterleaved = [signalToPlot[idx::s_wave.getnchannels()]
                     for idx in range(s_wave.getnchannels())]
    time = np.linspace(0, len(signalToPlot)/s_wave.getnchannels() /
                       bitRate, num=int(len(signalToPlot)/s_wave.getnchannels()))

    # resampling for discrete time plot
    userDefinedSamples = round(
        len(signalToPlot) * (float(nBitRate) / bitRate))
    discreteSignalToPlot = sps.resample(signalToPlot, userDefinedSamples)
    deinterleavedDiscrete = [discreteSignalToPlot[idx::s_wave.getnchannels()]
                             for idx in range(s_wave.getnchannels())]
    timeDiscrete = np.linspace(0, len(discreteSignalToPlot)/s_wave.getnchannels() /
                               nBitRate, num=int(len(discreteSignalToPlot)/s_wave.getnchannels()))

    # plot config
    mpl.style.use('seaborn')
    plt.figure(figsize=(17.0, 15.0))

    plot_t = plt.subplot(311)
    plot_f = plt.subplot(312)
    plot_d = plt.subplot(313)

    plt.suptitle(_file+'\n')
    plot_t.set_ylabel('Amplitude')
    plot_t.set_xlabel('Time \n')
    plot_f.set_ylabel('Frequency')
    plot_f.set_xlabel('Time\n')
    plot_d.set_ylabel('Amplitude')
    plot_d.set_xlabel('Time(Discrete)\n')

    # plotting

    for channel in deinterleaved:
        plot_t.plot(time, channel, linewidth=.2)
        plot_f.specgram(channel, NFFT=1024, Fs=bitRate,
                        noverlap=900, cmap='plasma')
    for channel in deinterleavedDiscrete:
        plot_d.stem(timeDiscrete, channel)
    plt.tight_layout()
    # plt.show()
    plt.savefig('output/'+_file+'.png', dpi=512)
    plt.close()

print("---DONE---")
